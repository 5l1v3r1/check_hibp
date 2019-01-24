#!/usr/bin/env python3
import os, sys, requests, subprocess, threading, time, datetime
from tqdm import tqdm
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename # Import filedialog

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = 'Have I Been Pwned - Account breach finder ')
        self.resizable(0,0)
        #self.style = Style()
        #self.style.theme_use("clam")
        icon = PhotoImage(file='icon.png')
        self.tk.call('wm', 'iconphoto', self._w, icon)

        self.options = {
            'ufile' : StringVar(),
            'pfile' : StringVar(),
            'username' : StringVar(),
            'password' : StringVar(),
        }

        # Start time thread
        #time_thread = threading.Thread(target=self.date_time)
        #time_thread.daemon = True
        #time_thread.start()

        settings = LabelFrame(self, text = 'Data')
        settings.grid(row = 0, column = 1, columnspan = 4)

        Label(settings, text = 'Username list').grid(row = 0, column = 1)
        Entry(settings, textvariable = self.options['ufile'], width = 30).grid(row = 0, column = 2)
        browser_username_file = Button(settings, text = '...', command = self.file_browser_username, width = 5).grid(row = 0, column = 3)

        Label(settings, text = 'Password list').grid(row = 1, column = 1)
        Entry(settings, textvariable = self.options['pfile'], width = 30).grid(row = 1, column = 2)
        browse_password_file = Button(settings, text = '...', command = self.file_browser_password, width = 5).grid(row = 1, column = 3)

        Label(settings, text = 'Username').grid(row = 2, column = 1)
        Entry(settings, textvariable = self.options['username'], width = 30, show = '*').grid(row = 2, column = 2)

        Label(settings, text = 'Password').grid(row = 3, column = 1)
        Entry(settings, textvariable = self.options['password'], width = 30, show = '*').grid(row = 3, column = 2)

        result_frame = LabelFrame(self, text = 'Result Frame', height = 400, width = 1400)
        result_frame.grid(row = 1, column = 1, columnspan = 3)

        Label(result_frame, text = 'Result').grid(row = 0, column = 1)
        self.options['result'] = Listbox(result_frame, width = 120, height = 30)
        self.options['result'].grid(row = 1, column = 1)
        #self.options['result'].bind("<Double-Button-1>", self.drop_to_shell)

        run = Button(result_frame, text = 'Run...', command = self.start_thread, width = 50).grid(row = 2, column = 1)

    def file_browser_username(self):
        self.options['ufile'].set(askopenfilename())

    def file_browser_password(self):
        self.options['pfile'].set(askopenfilename())

    def search(self, account):
        breachedon = []
        dates = []

        try:
            check = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/%s' % account)
        except KeyboardInterrupt:
            tqdm.write('Stopped...'); sys.exit(0)

        try:
            for title in check.json():
                breachedon.append(title["Title"])

            for date in check.json():
                dates.append(date["BreachDate"])
                latestbreach = max(dates) # Latest breach
                breachdate = min(dates) # first breach

        except Exception:
            pass

        # Check status code
        if check.status_code == 404:
            # Not breached
            data = '%s [%s]' % (account.ljust(50), 'NOT FOUND')
            tqdm.write(data)
            self.options['result'].insert(END, data)
        elif check.status_code == 200:
            # Breached, return when and where
            data = '%s [%s] %s -> %s -> %s' % (account.ljust(50), 'BREACHED', breachdate.rjust(15), latestbreach, breachedon)
            tqdm.write(data)
            self.options['result'].insert(END, data)

        elif check.status_code == 503:
            tqdm.write('\033[31m[ERROR]\033[0m Limit reached, temporarily banned by Cloudflare. Exiting....'); sys.exit(1)
        else:
            tqdm.write('%s [NOT FOUND]' % account.ljust(50))

    def start_thread(self):
        # Start time thread
        run_thread = threading.Thread(target=self.run)
        run_thread.daemon = True
        run_thread.start()

    def run(self):
        f = self.options['ufile'].get()
        print(f)
        accounts = open(f).readlines()
        #password = open(self.options['pfile'].get().readlines())
        with tqdm(total=(len(accounts)), desc='Progress') as bar:
            for l in accounts:
                self.search(l.strip())
                bar.update(1)
                time.sleep(float('1.5'))

    def date_time(self):
        while True:
            self.title(string = 'PyPass - Encrypted Password Manager | Dashboard | %s %s' % (time.strftime('%x'), time.strftime('%X')))
            time.sleep(1)

if __name__ == '__main__':
    panel = MainWindow()
    panel = mainloop()
