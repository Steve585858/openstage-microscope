using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace WindowsEventObjectTest
{
    ///
    /// This code is written purely as an example of how to hook up to the 
    ///  IN and OUT trigger events in WiRE3 from C#. Error handling and other such 
    ///  niceties are given little consideration here. 
    ///
    /// The software triggers are also available in WiRE3.0 hf3703.
    ///
    /// Copyright Renishaw plc 2008
    ///
    ///
    /// To use, run WiRE and this app on the same PC.
    /// Set up a new measurement in WiRE and on the Timing tab, set 
    ///      number of acquisitions     = 10
    ///      wait on software trigger   = true
    ///      send software trigger      = true
    /// and then run the measurement.
    ///
    /// Then from this project's dialog, simply click on the RunScan button to trigger each scan.
    ///
    /// Note that this triggering app has no connection with WiRE other than the named events.
    /// Only one client app can monitor these events because they are auto-reset events.
    /// The Run Scan (ie the InTrigger) is sent to WiRE on this app's main thread.
    /// WiRE's Software Out triggers are monitored for using a backgroundworker thread. This 
    /// reduces the likelyhood of missing any. If both IN and OUT triggering is used AND 
    /// the client starts listening for the trigger BEFORE sending the IN trigger, then 
    /// it is not possible to miss the out trigger.
    /// The purpose of the OUT trigger is to indicate that the ccd shutter has 
    ///  closed and that the data has been read off the CCD (although it is not necessarily 
    ///  saved into WiRE yet).
    /// As a result of both the IN and OUT triggers being auto-reset events, it is 
    ///  impossible for the client app not to catch all OUT triggers as long as it 
    ///  is always listening (as demonstrated in this example).
    ///
    /// Note that there is no communication with WIREQueue in this example. There could 
    /// be to, for example, submit the measurement to wire, and monitor its data.
    ///
    public partial class Form1 : Form
    {
        int m_outTriggerCount;
        int m_autoRun;
        NamedEvent m_triggerIN;
        NamedEvent m_triggerOUT;
        public delegate void SetOutCount(int outCount);
        public delegate void EnableButtons(bool bTriggerEnabled);
        public SetOutCount SetOutCountDelegate;
        public EnableButtons EnableButtonsDelegate;

        public Form1()
        {
            InitializeComponent();
            m_triggerIN = new NamedEvent("Global\\WiREInTrigger");
            m_triggerOUT = new NamedEvent("Global\\WiREOutTrigger");
            SetOutCountDelegate = new SetOutCount(SetOutCountImpl);
            EnableButtonsDelegate = new EnableButtons(EnableButtonsImpl);
        }


        /// <summary>
        /// Loads the form and starts monitoring WiRE's OUT trigger
        /// using a background worker.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Form1_Load(object sender, EventArgs e)
        {
            OutStatusLabel.Text = "Monitoring Out triggers";
            OutCountLabel.Text = "0";
            this.backgroundWorker1.RunWorkerAsync();
        }

        /// <summary>
        /// Worker function for the OUT trigger monitoring thread.
        ///  This simply watches the OUT Trigger named event and 
        ///  keeps going until this dialog is closed.
        /// 
        /// If the user has set the Auto-run mode then it will trigger 
        ///  the next scan immediately.
        /// </summary>
        private void outthread_MonitorWIREOutTrigger(BackgroundWorker bw)
        {
            do
            {
                int rc = m_triggerOUT.Wait(0); // wait for 20s
                switch (rc)
                {
                    case 0:    // event singnaled.
                        outthread_TriggerRecieved();
                        m_triggerOUT.Reset();
                        outthread_HandleAutoRun(bw);
                        break;

                    case 0x00000080:    // ABANDONED - exit the monitoring of the event
                        bw.CancelAsync();
                        break;

                    case 0x00000102:    // TIMEOUT  (drp through to default)
                    default:
                        break;          // never mind
                }
            }
            while (bw.CancellationPending == false);
        }

        
        private void outthread_HandleAutoRun(BackgroundWorker bw)
        {
            if (m_autoRun > 0)
            {
                m_autoRun--;        // decrement the number of autoruns we need ot do.
                m_triggerIN.Set();  // tell the scan to run another.

                if (m_autoRun == 0)
                    RunScanButton.Invoke(EnableButtonsDelegate, m_autoRun > 0);
            }
        }

        private void outthread_TriggerRecieved()
        {
            m_outTriggerCount++;
            OutCountLabel.Invoke(SetOutCountDelegate, m_outTriggerCount);
        }

        /// implementation method to be called from the background worker 
        ///  thread. Displays the number of OUT triggers seen by this app.
        private void SetOutCountImpl(int outCnt)
        {
            OutCountLabel.Text = outCnt.ToString();
        }

        /// implementation method to be called from the background worker 
        ///  thread. Greys/enables the buttons according to the state of the 
        ///  auto trigger thread.
        private void EnableButtonsImpl(bool bAutoTriggering)
        {
            AbortButton.Enabled = bAutoTriggering;
            AutoRunButton.Enabled = !bAutoTriggering;
        }

        /// <summary>
        /// Starts the background thread.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            outthread_MonitorWIREOutTrigger(backgroundWorker1);
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            this.backgroundWorker1.CancelAsync();
        }

        /// <summary>
        ///  runs a single scan.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void RunScanButton_Click(object sender, EventArgs e)
        {
            m_triggerIN.Set();
        }

        /// <summary>
        /// Starts the auto run - in which each time a OUT trigger
        /// is received from WiRE we then fire an IN trigger.
        /// Each time this is done the autoRun counter is decremented. The
        /// process stops when t gets to 0.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void AutoRunButton_Click(object sender, EventArgs e)
        {
            m_autoRun = Convert.ToInt32(NumToRunTextBox.Text);
            m_triggerIN.Set();
            m_autoRun--;
            EnableButtonsImpl(m_autoRun>0);

        }

        /// <summary>
        /// Stops the auto run cycle.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void AbortButton_Click(object sender, EventArgs e)
        {
            m_autoRun = 0;
            EnableButtonsImpl(m_autoRun > 0);
        }

        /// <summary>
        ///  closes the app.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ExitButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
