/** 
 * @file MainDlg.cpp
 *  Holds the main code for the CMainDlg class. This app is a simple dialog 
 *  app.
 *
 * This code is written purely as an example of how to hook up to the 
 *  IN and OUT trigger events in WiRE3. Error handling and other such 
 *  niceties are given little consideration here. 
 *
 * The software triggers are also available in WiRE3.0 hf3703.
 *
 * Copyright Renishaw plc 2008
 *
 *
 *  To use, run WiRE and this app on the same PC.
 *  Set up a new measurement in WiRE and on the Timing tab, set 
 *       number of acquisitions     = 10
 *       wait on software trigger   = true
 *       send software trigger      = true
 *  and then run the measurement.
 *
 * Then from this project's dialog, simply click on the RunScan button to trigger each scan.
 *
 * Note that this triggering app has no connection with wire other than the named events.
 * Only one client app can monitor these events because they are auto-reset events.
 * The Run Scan (ie the InTrigger) is sent to WiREon this app's main thread.
 * WiRE's Software Out triggers are monitored for using a worker thread. This reduces the 
 *  likelyhood of missing any. If both IN and OUT triggering is used AND the client starts 
 *  listening for the trigger BEFORE sending the IN trigger, then it is not possible to miss the 
 *  out trigger.
 *  The purpose of the OUT trigger is to indicate that the ccd shutter has 
 *  closed and that the data has been read off the CCD (although it is not necessarily 
 *  saved into WiRE yet).
 * As a result of both the IN and OUT triggers being auto-reset events, it is impossible for the 
 *  client app not to catch all OUT triggers as long as it is always listening (as demonstrated 
 *  in this example).
 *
 * Note that there is no communication with WIREQueue in this example. There could be to, for example, 
 *  submit the measurement to wire, and monitor its data.
 * 
 */

#include "stdafx.h"
#include "resource.h"

#include "MainDlg.h"

/**
 * OnInitDialog does two extra things:
 *  1/ gets handles to the In and Out trigger Windows Event objects.
 *  2/ Starts a thread that monitors the Out trigger event.
 */
LRESULT CMainDlg::OnInitDialog(UINT /*uMsg*/, WPARAM /*wParam*/, LPARAM /*lParam*/, BOOL& /*bHandled*/)
{
	// center the dialog on the screen
    m_outTriggerCount=0;
    m_autoRun=0;
    SetDlgItemText(IDC_OUT_STATUS_STATIC, _T("Out monitor not created"));
    SetDlgItemText(IDC_OUT_COUNT_STATIC, _T("0"));

	CenterWindow();

	// set icons
	HICON hIcon = (HICON)::LoadImage(_Module.GetResourceInstance(), MAKEINTRESOURCE(IDR_MAINFRAME), 
		IMAGE_ICON, ::GetSystemMetrics(SM_CXICON), ::GetSystemMetrics(SM_CYICON), LR_DEFAULTCOLOR);
	SetIcon(hIcon, TRUE);
	HICON hIconSmall = (HICON)::LoadImage(_Module.GetResourceInstance(), MAKEINTRESOURCE(IDR_MAINFRAME), 
		IMAGE_ICON, ::GetSystemMetrics(SM_CXSMICON), ::GetSystemMetrics(SM_CYSMICON), LR_DEFAULTCOLOR);
	SetIcon(hIconSmall, FALSE);

    CreateTriggers();
    SetDlgItemInt(IDC_NUM_TO_RUN_BTN, 10);

    StartThreads();

	return TRUE;
}

CMainDlg::~CMainDlg(void)
{
    if (m_event_in != INVALID_HANDLE_VALUE && m_event_in != NULL)
        CloseHandle(m_event_in);
    if (m_event_out != INVALID_HANDLE_VALUE && m_event_out != NULL)
        CloseHandle(m_event_out);
}

/**
 * When the dialog ends we need to kill off the worker thread.
 *  Note that the worker thread must not output to the GUI
 *  during its shutdown else it never closes cleanly.
 */
void CMainDlg::myEndDialog(WORD wID)
{
    m_bMonitoring = false;  // tell the threads to close

    // wait 5s for the worker thread to close.
    if (m_hOutThread != INVALID_HANDLE_VALUE)
    {
        bool bEnd(false);
        HANDLE arr[1]={m_hOutThread};
        while(!bEnd)
        {
            DWORD dw = MsgWaitForMultipleObjects(1, arr, FALSE, 5000, QS_ALLEVENTS);
            switch(dw)
            {
            case WAIT_OBJECT_0:// m_hOutThread terminated (drop through)
            case WAIT_TIMEOUT: // timeout expired
                bEnd=true;  
                break;

            case WAIT_OBJECT_0+1:// message arrived
                {
                    // dispatch it.
                    MSG msg; 
                        
                    // Read all of the messages in this next loop, 
                    // removing each message as we read it.
                    while (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) 
                    { 
                        // If it is a quit message, exit.
                        if (msg.message == WM_QUIT) 
                            bEnd=true;
                        ::DispatchMessage(&msg); // Otherwise, dispatch the message.
                    } // End of PeekMessage while loop.
                }
                break;
            default: 
                break;
            }
        }
    }
    
	EndDialog(wID);

}

LRESULT CMainDlg::OnOK(WORD /*wNotifyCode*/, WORD wID, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
{
    myEndDialog(wID);
	return 0;
}

LRESULT CMainDlg::OnCancel(WORD /*wNotifyCode*/, WORD wID, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
{
	myEndDialog(wID);
	return 0;
}

/**
 * The triggers are named windows events. They can be connected to either before or after
 *  WiRE is running.
 * Note that the trigger IN is an auto-reset event (to ensure it cannot be missed)
 *  and that the trigger OUT is an auto-reset event (to ensure it cannot be missed).
 */
void CMainDlg::CreateTriggers()
{
    m_event_in  = CreateEvent(  NULL,  // no security attributes
                                FALSE, // automatically reset the event
                                FALSE, // initially not signalled
                                _T("Global\\WiREInTrigger"));

    if (m_event_in==NULL)   // failed to create trigger ?
        DisplayLastError(_T("CreateEvent(Global\\WiREInTrigger)"));

    m_event_out = CreateEvent(  NULL,  // no security attributes
                                FALSE, // automatically reset the event
                                FALSE, // initially not signalled
                                _T("Global\\WiREOutTrigger"));

    if (m_event_out==NULL)   // failed to create trigger ?
        DisplayLastError(_T("CreateEvent(Global\\WiREOutTrigger)"));
}

void CMainDlg::DisplayLastError(LPCTSTR sFnName)
{
    LPVOID lpMsgBuf;
    LPVOID lpDisplayBuf;
    DWORD dw = GetLastError(); 

    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | 
        FORMAT_MESSAGE_FROM_SYSTEM |
        FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,
        dw,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR) &lpMsgBuf,
        0, NULL );

    // Display the error message and exit the process

    lpDisplayBuf = (LPVOID)LocalAlloc(LMEM_ZEROINIT, 
        (lstrlen((LPCTSTR)lpMsgBuf)+lstrlen((LPCTSTR)sFnName)+40)*sizeof(TCHAR)); 
    StringCchPrintf((LPTSTR)lpDisplayBuf, 
                    LocalSize(lpDisplayBuf),
                    _T("%s failed with error %d: %s"), 
                    sFnName, dw, lpMsgBuf); 
    MessageBox((LPCTSTR)lpDisplayBuf, _T("CreateTriggers Error"), MB_OK|MB_ICONERROR); 

    LocalFree(lpMsgBuf);
    LocalFree(lpDisplayBuf);
}

/**
 * Handler for the RunScan button click event.
 */
LRESULT CMainDlg::OnBnClickedRunScanButton(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
{
    SetEvent(m_event_in);
    return 0;
}



static DWORD WINAPI
BeginOutMonitorThread(void* pvMainDlg)
{
    CMainDlg* pMainDlg = reinterpret_cast<CMainDlg*>(pvMainDlg);
    pMainDlg->OutMonitorThread();
    return 0;
}

/**
 * Starts the thread that monitors the OUT trigger
 */
void CMainDlg::StartThreads()
{
    m_bMonitoring = true;
    DWORD dwThreadID;
    m_hOutThread = reinterpret_cast<HANDLE>(_beginthreadex(NULL, 0,
                                               reinterpret_cast<LPTHREADEX_FUNC>(BeginOutMonitorThread),
                                               static_cast<void*>(this), 0,
                                               reinterpret_cast<unsigned int*>(&dwThreadID)));
    if(m_hOutThread!=INVALID_HANDLE_VALUE)
        SetDlgItemText(IDC_OUT_STATUS_STATIC, _T("Monitoring Out triggers"));
}


/**
 * Worker function for the OUT trigger monitoring thread.
 *  This simply watches the OUT Trigger named event and 
 *  keeps going until this dialog is closed.
 *
 * If the user has set the Auto-run mode then it will trigger the next 
 *  scan immediately.
 */
void CMainDlg::OutMonitorThread()
{
    int i(0);

    do
    {
        DWORD dwResult = ::WaitForSingleObject(m_event_out, 1000);
        if (dwResult == WAIT_OBJECT_0)
        {
            outthread_TriggerRecieved();
            ResetEvent(m_event_out);
            if (m_autoRun > 0)
            {
                m_autoRun--;
                SetEvent(m_event_in);

                // the auto-run allows the next scan to run immediately.
                if (m_autoRun == 0)
                    EnableButtons(m_autoRun>0);
            }

        }
        else if (dwResult == WAIT_ABANDONED)
        {
            m_bMonitoring = false;
            break;
        }
        ATLTRACE(_T("%d thread: montoring = %s\n"), i++, m_bMonitoring?_T("true"):_T("false"));
    } while (m_bMonitoring);

    if (m_hOutThread)
    {
        CloseHandle(m_hOutThread);
        m_hOutThread = INVALID_HANDLE_VALUE;
    }
}

/**
 * This code is called each time an OUT trigger is observed. 
 *  The code is calle don the worker thread and thus 
 *  would be better served by Posting a mesasge back to my
 *  main thread for the GUI display.
 */
void CMainDlg::outthread_TriggerRecieved()
{
    m_outTriggerCount++;
    TCHAR txt[32];
    txt[31]=0;
    _sntprintf_s(txt, 31, _T("%d"), m_outTriggerCount);
    SetDlgItemText(IDC_OUT_COUNT_STATIC, txt);
}

/**
 * Auto tiggering is added to demonstrate that IN triggers can be set as soon
 *  as the OUT trigger is recieved, and that 
 *  the auto-triggering works when run over multiple measurements. 
 *
 *  For example, configure a series measurement using trigger-in and trigger-out,
 *      with 5 acquistions.
 *  Then set the auto-trigger to 10 on this app.
 *  Run the measurement - it will complete using 5 of the triggers.
 *  Re-run the measurement and it will use the other 5 triggers.
 *
 *  It might be wise to ensure that the IN trigger is reset BEFORE running the very first
 *  measurement.
 *  If the client software needs to control when the first scan in a measurement is triggered, 
 *  then it must RESET the IN trigger before running the measurement and then SET the trigger
 *  when it is ready for the scan to collect data.
 */
LRESULT CMainDlg::OnBnClickedAutoRunBtn(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
{
    m_autoRun = GetDlgItemInt(IDC_NUM_TO_RUN_BTN);
    SetEvent(m_event_in);
    m_autoRun--;    // because we have just triggered one.
    EnableButtons(m_autoRun>0);
    return 0;
}

LRESULT CMainDlg::OnBnClickedAbortBtn(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
{
    m_autoRun = 0;
    EnableButtons(m_autoRun>0);
    return 0;
}

void CMainDlg::EnableButtons(BOOL autoRunOn)
{
    //::EnableWindow(GetDlgItem(IDC_RUN_SCAN_BUTTON), !autoRunOn);
    ::EnableWindow(GetDlgItem(IDC_ABORT_BTN), autoRunOn);
    ::EnableWindow(GetDlgItem(IDC_AUTO_RUN_BTN), !autoRunOn);
}
