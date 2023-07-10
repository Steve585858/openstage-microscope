namespace WindowsEventObjectTest
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label3 = new System.Windows.Forms.Label();
            this.OutCountLabel = new System.Windows.Forms.Label();
            this.OutStatusLabel = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.RunScanButton = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.AbortButton = new System.Windows.Forms.Button();
            this.NumToRunTextBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.AutoRunButton = new System.Windows.Forms.Button();
            this.ExitButton = new System.Windows.Forms.Button();
            this.backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.OutCountLabel);
            this.groupBox1.Controls.Add(this.OutStatusLabel);
            this.groupBox1.Location = new System.Drawing.Point(12, 13);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(250, 67);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "WiRE OUT Triggering";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(10, 40);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(137, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Number of triggers received";
            // 
            // OutCountLabel
            // 
            this.OutCountLabel.AutoSize = true;
            this.OutCountLabel.Location = new System.Drawing.Point(151, 40);
            this.OutCountLabel.Name = "OutCountLabel";
            this.OutCountLabel.Size = new System.Drawing.Size(78, 13);
            this.OutCountLabel.TabIndex = 1;
            this.OutCountLabel.Text = "OutCountLabel";
            // 
            // OutStatusLabel
            // 
            this.OutStatusLabel.AutoSize = true;
            this.OutStatusLabel.Location = new System.Drawing.Point(10, 20);
            this.OutStatusLabel.Name = "OutStatusLabel";
            this.OutStatusLabel.Size = new System.Drawing.Size(80, 13);
            this.OutStatusLabel.TabIndex = 0;
            this.OutStatusLabel.Text = "OutStatusLabel";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.RunScanButton);
            this.groupBox2.Location = new System.Drawing.Point(12, 86);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(250, 67);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "WiRE IN Triggering";
            // 
            // RunScanButton
            // 
            this.RunScanButton.Location = new System.Drawing.Point(7, 20);
            this.RunScanButton.Name = "RunScanButton";
            this.RunScanButton.Size = new System.Drawing.Size(75, 23);
            this.RunScanButton.TabIndex = 0;
            this.RunScanButton.Text = "run scan";
            this.RunScanButton.UseVisualStyleBackColor = true;
            this.RunScanButton.Click += new System.EventHandler(this.RunScanButton_Click);
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.AbortButton);
            this.groupBox3.Controls.Add(this.NumToRunTextBox);
            this.groupBox3.Controls.Add(this.label1);
            this.groupBox3.Controls.Add(this.AutoRunButton);
            this.groupBox3.Location = new System.Drawing.Point(12, 159);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(250, 72);
            this.groupBox3.TabIndex = 2;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "WiRE AUTO Triggering";
            // 
            // AbortButton
            // 
            this.AbortButton.Location = new System.Drawing.Point(169, 19);
            this.AbortButton.Name = "AbortButton";
            this.AbortButton.Size = new System.Drawing.Size(75, 23);
            this.AbortButton.TabIndex = 3;
            this.AbortButton.Text = "Abort";
            this.AbortButton.UseVisualStyleBackColor = true;
            this.AbortButton.Click += new System.EventHandler(this.AbortButton_Click);
            // 
            // NumToRunTextBox
            // 
            this.NumToRunTextBox.Location = new System.Drawing.Point(120, 45);
            this.NumToRunTextBox.Name = "NumToRunTextBox";
            this.NumToRunTextBox.Size = new System.Drawing.Size(38, 20);
            this.NumToRunTextBox.TabIndex = 2;
            this.NumToRunTextBox.Text = "10";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(7, 48);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(116, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "number to auto-trigger: ";
            // 
            // AutoRunButton
            // 
            this.AutoRunButton.Location = new System.Drawing.Point(7, 19);
            this.AutoRunButton.Name = "AutoRunButton";
            this.AutoRunButton.Size = new System.Drawing.Size(75, 23);
            this.AutoRunButton.TabIndex = 0;
            this.AutoRunButton.Text = "auto run";
            this.AutoRunButton.UseVisualStyleBackColor = true;
            this.AutoRunButton.Click += new System.EventHandler(this.AutoRunButton_Click);
            // 
            // ExitButton
            // 
            this.ExitButton.Location = new System.Drawing.Point(268, 207);
            this.ExitButton.Name = "ExitButton";
            this.ExitButton.Size = new System.Drawing.Size(75, 23);
            this.ExitButton.TabIndex = 3;
            this.ExitButton.Text = "Quit";
            this.ExitButton.UseVisualStyleBackColor = true;
            this.ExitButton.Click += new System.EventHandler(this.ExitButton_Click);
            // 
            // backgroundWorker1
            // 
            this.backgroundWorker1.WorkerSupportsCancellation = true;
            this.backgroundWorker1.DoWork += new System.ComponentModel.DoWorkEventHandler(this.backgroundWorker1_DoWork);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(352, 241);
            this.Controls.Add(this.ExitButton);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = ".Net WiRE Software Trigger Demo";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label OutCountLabel;
        private System.Windows.Forms.Label OutStatusLabel;
        private System.Windows.Forms.Button RunScanButton;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Button AutoRunButton;
        private System.Windows.Forms.Button AbortButton;
        private System.Windows.Forms.TextBox NumToRunTextBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button ExitButton;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
    }
}

