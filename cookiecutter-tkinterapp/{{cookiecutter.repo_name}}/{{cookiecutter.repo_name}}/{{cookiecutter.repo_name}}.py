#!/usr/bin/env python3

import os
import sys
from configparser import ConfigParser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from frames import *


def config(cfg_file):
    '''
    Function for loading configuration parameters
    Returns a dictionary of information
    '''
    required_sections = ['PROJECTINFO', 'APPINFO']
    cfg_parser = ConfigParser()
    cfg_parser.read(cfg_file)

    # get section, default to postgresql
    cfg_dict = {}
    if all([s in cfg_parser.sections() for s in required_sections]):
        for k, v in cfg_parser.items():
            cfg_dict[k] = v
    else:
        raise Exception(
            f'Section {[s for s in required_sections if s not in cfg_parser.sections]} not found in the {filename} file')

    return cfg_dict


_default_cfg_path = './config/configuration.ini'

cfg = config(_default_cfg_path)

__author__ = cfg['author']
__email__ = cfg['email']
__version__ = cfg['version']


class {{cookiecutter.application_name}}(tk.Tk):
    '''
    Main GUI interface
    Initialize codes:
        app = {{cookiecutter.application_name}}()
        app.mainloop()
    '''

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=cfg['icon'])
        tk.Tk.wm_title(self, f"{_app_name} - {__version__}")

        self.geometry(f"{cfg['width']}x{cfg['height']}+10+10")
        self.resizable(
            tuple(True if b == "True" else False for b in cfg['resizable'].split(",")))
        self.minsize(int(cfg['min_width']), int(cfg['min_height']))

        style = ttk.Style(self)
        # TODO: to make configurable styles

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage):

            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # --- Create Menu bar --- #
        # self.menubar = tk.Menu(self)
        # filemenu = tk.Menu(self.menubar, tearoff=0)
        # filemenu.add_command(
        #     label="Start", command=lambda: self.show_frame(StartPage))
        # filemenu.add_command(
        #     label="Inventory", command=lambda: self.show_frame(TrackInvPage))
        # filemenu.add_command(
        #     label="Tyre", command=lambda: self.show_frame(TrackTyrePage))
        # filemenu.add_command(
        #     label="Dashboard", command=lambda: self.show_frame(DashboardPage))
        # filemenu.add_separator()
        # filemenu.add_command(label="Exit", command=lambda: self.on_exit())
        # self.menubar.add_cascade(label="Navigate", menu=filemenu)

        # settingmenu = tk.Menu(self.menubar, tearoff=0)
        # settingmenu.add_command(
        #     label="Configure", command=lambda: self.show_frame(ConfigPage))
        # self.menubar.add_cascade(label="Settings", menu=settingmenu)

        # helpmenu = tk.Menu(self.menubar, tearoff=0)
        # helpmenu.add_command(
        #     label="Open Install Directory", command=self.open_dir)
        # helpmenu.add_command(label="View Logs", command=self.open_logs_dir)
        # helpmenu.add_command(label="Documentation", command=self.docs)
        # helpmenu.add_command(label="About", command=self.about)

        # self.menubar.add_cascade(label="Help", menu=helpmenu)

        # self.config(menu=self.menubar)
        # --- End Create Menu bar --- #

        self.protocol('WM_DELETE_WINDOW', self.on_exit)

    def start_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def show_frame(self, dst_cont):

        frame = self.frames[dst_cont]
        frame.tkraise()

    def on_exit(self):
        if tkMessageBox.askyesno('System Warning', 'Do you want to quit the application?'):
            self.destroy()
            sys.exit()
        else:
            pass


class StartPage(tk.Frame):
    '''
    The initialize page of the app with 3 selections
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(height=str(controller.winfo_height() - 10),
                       width=str(controller.winfo_width() - 10), background='#00000')
        self.grid(column='0', row='0', sticky='n')
