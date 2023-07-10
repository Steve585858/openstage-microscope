// MainDlg.h : interface of the CMainDlg class
//
/////////////////////////////////////////////////////////////////////////////

#pragma once
typedef unsigned (__stdcall *LPTHREADEX_FUNC)(void*);

/** 
 * @class CMainDlg 
 *  This is a very simple dialog used to demonstrate the software triggering for WiRE
 */
class CMainDlg : public CAxDialogImpl<CMainDlg>
{
public:
	enum { IDD = IDD_MAINDLG };

    ~CMainDlg();

	BEGIN_MSG_MAP(CMainDlg)
		MESSAGE_HANDLER(WM_INITDIALOG, OnInitDialog)
		COMMAND_ID_HANDLER(IDOK, OnOK)
		COMMAND_ID_HANDLER(IDCANCEL, OnCancel)
        COMMAND_HANDLER(IDC_RUN_SCAN_BUTTON, BN_CLICKED, OnBnClickedRunScanButton)
        COMMAND_HANDLER(IDC_AUTO_RUN_BTN, BN_CLICKED, OnBnClickedAutoRunBtn)
        COMMAND_HANDLER(IDC_ABORT_BTN, BN_CLICKED, OnBnClickedAbortBtn)
    END_MSG_MAP()

// Handler prototypes (uncomment arguments if needed):
//	LRESULT MessageHandler(UINT /*uMsg*/, WPARAM /*wParam*/, LPARAM /*lParam*/, BOOL& /*bHandled*/)
//	LRESULT CommandHandler(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/)
//	LRESULT NotifyHandler(int /*idCtrl*/, LPNMHDR /*pnmh*/, BOOL& /*bHandled*/)

	LRESULT OnInitDialog(UINT /*uMsg*/, WPARAM /*wParam*/, LPARAM /*lParam*/, BOOL& /*bHandled*/);
	LRESULT OnOK(WORD /*wNotifyCode*/, WORD wID, HWND /*hWndCtl*/, BOOL& /*bHandled*/);
	LRESULT OnCancel(WORD /*wNotifyCode*/, WORD wID, HWND /*hWndCtl*/, BOOL& /*bHandled*/);

    void CreateTriggers();
    void DisplayLastError(LPCTSTR sFnName);

    void OutMonitorThread();
    void outthread_TriggerRecieved();
    int  m_outTriggerCount;
    int  m_autoRun;

    void StartThreads();
    void myEndDialog(WORD wID);
    bool m_bMonitoring;

    HANDLE m_event_in;
    HANDLE m_event_out;

    HANDLE m_hOutThread;
    LRESULT OnBnClickedRunScanButton(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/);
    LRESULT OnBnClickedAutoRunBtn(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/);
    LRESULT OnBnClickedAbortBtn(WORD /*wNotifyCode*/, WORD /*wID*/, HWND /*hWndCtl*/, BOOL& /*bHandled*/);
    void EnableButtons(BOOL autoRunOn);
};
