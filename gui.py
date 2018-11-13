from tkinter import messagebox as mb
import manager_bot as m
import tkinter as tk


class ManagerBot(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        root.configure(background='DeepSkyBlue3')
        self.init_manager_bot()
        self.SETTINGS = {
            'timer': 0,
            'workers_min': 0,
            'workers_max': 0,
            'productivity_min': 0,
            'productivity_max': 0,
            'tasks_min': 0,
            'tasks_max': 0,
            'complexity_min': 0,
            'complexity_max': 0
        }
        self.workers = None
        self.tasks = None
        self.timer = None
        self.count = 1

        def on_closing():
            if mb.askokcancel('Выход', 'Вы уверены?'):
                if self.timer is not None:
                    self.timer.cancel()
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

    def init_manager_bot(self):
        bg = 'DeepSkyBlue3'
        fg = 'white'
        font = ("Helvetica", 16)
        # frames
        buttons_frame = tk.Frame(root)
        workers_frame = tk.LabelFrame(root, text='workers',
                                      bg=bg, fg=fg, font=font)
        task_worker_frame = tk.LabelFrame(root, text='task worker',
                                          bg=bg, fg=fg, font=font)
        info_frame = tk.LabelFrame(root, text='info',
                                   bg=bg, fg=fg, font=font)

        # buttons
        button_new = tk.Button(
            buttons_frame,
            text='New',
            command=self.new,
            bg=fg, font=14
        )
        button_pause = tk.Button(
            buttons_frame,
            text='Pause',
            command=self.pause,
            bg=fg, font=14
        )
        button_resume = tk.Button(
            buttons_frame,
            text='Resume',
            command=self.resume,
            bg=fg, font=14)
        button_settings = tk.Button(
            buttons_frame,
            text='Settings',
            command=self.settings_view,
            bg=fg, font=14)

        buttons_frame.pack(side=tk.TOP, pady=20)
        button_new.pack(side=tk.LEFT)
        button_pause.pack(side=tk.LEFT)
        button_resume.pack(side=tk.LEFT)
        button_settings.pack(side=tk.LEFT)

        # scrollbar workers
        wx_scrollbar = tk.Scrollbar(master=workers_frame, orient=tk.HORIZONTAL,
                                    bg=fg)
        wx_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        wy_scrollbar = tk.Scrollbar(master=workers_frame, bg=fg)
        wy_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # scrollbar tasks
        tx_scrollbar = tk.Scrollbar(master=task_worker_frame,
                                    orient=tk.HORIZONTAL, bg=fg)
        tx_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        ty_scrollbar = tk.Scrollbar(master=task_worker_frame, bg=fg)
        ty_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # scrollbar info
        ix_scrollbar = tk.Scrollbar(master=info_frame, orient=tk.HORIZONTAL, bg=fg)
        ix_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        iy_scrollbar = tk.Scrollbar(master=info_frame, bg=fg)
        iy_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # lists
        width = 33
        height = 16
        self.list_workers = tk.Listbox(master=workers_frame, width=width,
                                       height=height,
                                       xscrollcommand=wx_scrollbar.set,
                                       yscrollcommand=wy_scrollbar.set,
                                       bg='DeepSkyBlue2', fg=fg, font=14)
        self.list_task_worker = tk.Listbox(master=task_worker_frame, width=width,
                                           height=height,
                                           xscrollcommand=tx_scrollbar.set,
                                           yscrollcommand=ty_scrollbar.set,
                                           bg='DeepSkyBlue2', fg=fg, font=14)
        self.list_info = tk.Listbox(master=info_frame, width=width, height=height,
                                    xscrollcommand=ix_scrollbar.set,
                                    yscrollcommand=iy_scrollbar.set,
                                    bg='DeepSkyBlue2', fg=fg, font=14)

        # pack
        workers_frame.pack(side=tk.LEFT)
        task_worker_frame.pack(side=tk.LEFT)
        info_frame.pack(side=tk.LEFT)
        self.list_workers.pack(side=tk.LEFT)
        self.list_task_worker.pack(side=tk.LEFT)
        self.list_info.pack(side=tk.LEFT)

        wx_scrollbar.config(command=self.list_workers.xview)
        wy_scrollbar.config(command=self.list_workers.yview)
        tx_scrollbar.config(command=self.list_task_worker.xview)
        ty_scrollbar.config(command=self.list_task_worker.yview)
        ix_scrollbar.config(command=self.list_info.xview)
        iy_scrollbar.config(command=self.list_info.yview)

        # binds
        self.list_workers.bind('<<ListboxSelect>>', self.add_list_tasks)

    # settings_window
    def settings_view(self):
        SettingsWindow(self)

    def settings_data(self, data):
        self.SETTINGS = data

    # clear_list
    @staticmethod
    def clear_list(listbox):
        listbox.delete(0, tk.END)

    # timer
    def start_timer(self):
        self.timer = m.InfiniteTimer(self.SETTINGS['timer'], self.run)
        self.timer.start()

    def pause(self):
        self.timer.cancel()

    def resume(self):
        self.start_timer()

    # add_lists
    def add_list_workers(self):
        for index, worker in enumerate(self.workers):
            if not worker['tasks']:
                task_name = 'Нет больше задач'
                task_complexity = ''
            else:
                task_name = worker['tasks'][0]['name']
                task_complexity = worker['tasks'][0]['complexity']

            worker = '{}.{}({}) - {}({})'.format(
                index + 1,
                worker['name'],
                worker['productivity'],
                task_name,
                task_complexity
            )
            self.list_workers.insert(tk.END, worker)

    def add_list_tasks(self, event):
        worker = event.widget.curselection()
        if self.list_task_worker.size():
            self.clear_list(self.list_task_worker)

        if not worker:
            return False
        else:
            worker = worker[0]
            for index, task in enumerate(self.workers[worker]['tasks']):
                task = '{}.{}({})'.format(
                    index + 1,
                    task['name'],
                    task['complexity'],
                )
                self.list_task_worker.insert(tk.END, task)

    def add_list_info(self, worker, task, count):
        worker = '№{} {} - {}'.format(
            count,
            worker['name'],
            task['name']
        )
        self.list_info.insert(tk.END, worker)

    def update_listbox(self, listbox):
        self.clear_list(listbox)
        self.add_list_workers()

    # buttons
    def new(self):
        self.workers = m.generate_workers(
            (self.SETTINGS['workers_min'], self.SETTINGS['workers_max']),
            (self.SETTINGS['productivity_min'], self.SETTINGS['productivity_max'])
        )
        self.tasks = m.generate_tasks(
            (self.SETTINGS['tasks_min'], self.SETTINGS['tasks_max']),
            (self.SETTINGS['complexity_min'], self.SETTINGS['complexity_max'])
        )
        m.round_robin(self.workers, self.tasks)
        self.add_list_workers()
        self.start_timer()

    def run(self):
        for worker in self.workers:
            if worker['tasks']:
                    worker['tasks'][0]['complexity'] = (
                        worker['tasks'][0]['complexity'] - worker['productivity'])

                    if worker['tasks'][0]['complexity'] <= 0:
                        self.add_list_info(worker, worker['tasks'].pop(0), self.count)

        if m.randint(0, 1) == 1:
            m.redistributes_tasks(self.workers)
        print('Номер моделирования: {}', self.count, sep='')
        self.count += 1
        self.update_listbox(self.list_workers)
        if not any([bool(worker['tasks']) for worker in self.workers]):
            return True


class SettingsWindow(tk.Toplevel):
    def __init__(self, app):
        self.app = app
        super().__init__(root)
        self.init_settings()

    @staticmethod
    def correct(text):
        if text.isdigit():
            return True
        elif text is '':
            return True
        else:
            return False

    def init_settings(self):
        bg = 'DeepSkyBlue3'
        fg = 'white'
        font = ("Helvetica", 16)
        self.configure(background=bg)
        self.title('Settings')
        self.geometry(count_center(650, 200))
        self.resizable(False, False)
        self.grab_set()
        self.focus_get()

        # bg = 'cornflower blue'
        reg = self.register(self.correct)
        width = 5

        self.timer = tk.Entry(self, width=width, validate='key',
                              validatecommand=(reg, '%P'))
        self.workers_min = tk.Entry(self, width=width)
        self.workers_max = tk.Entry(self, width=width)
        self.productivity_min = tk.Entry(self, width=width)
        self.productivity_max = tk.Entry(self, width=width)
        self.tasks_min = tk.Entry(self, width=width)
        self.tasks_max = tk.Entry(self, width=width)
        self.complexity_min = tk.Entry(self, width=width)
        self.complexity_max = tk.Entry(self, width=width)

        button_ok = tk.Button(self, text='Ok', command=self.button_ok, width=10, bg=fg, font=14)

        label_timer = tk.Label(self,
                               text='время срабатывания таймера (сек):',
                               bg=bg, fg=fg, font=font)
        label_workers = tk.Label(self,
                                 text='количество исполнителей:',
                                 bg=bg, fg=fg, font=font)
        label_workers_min = tk.Label(self, text='min', bg=bg, fg=fg, font=font)
        label_workers_max = tk.Label(self, text='max', bg=bg, fg=fg, font=font)
        label_productivity = tk.Label(
            self,
            text='мин и макс производительность исполнителя:',
            bg=bg, fg=fg, font=font)
        label_productivity_min = tk.Label(self, text='min', bg=bg, fg=fg, font=font)
        label_productivity_max = tk.Label(self, text='max', bg=bg, fg=fg, font=font)
        label_tasks = tk.Label(self,
                               text='мин и макс количество задач:',
                               bg=bg, fg=fg, font=font)
        label_tasks_min = tk.Label(self, text='min', bg=bg, fg=fg, font=font)
        label_tasks_max = tk.Label(self, text='max', bg=bg, fg=fg, font=font)
        label_complexity = tk.Label(self,
                                    text='мин и макс сложность задачи:',
                                    bg=bg, fg=fg, font=font)
        label_complexity_min = tk.Label(self, text='min', bg=bg, fg=fg, font=font)
        label_complexity_max = tk.Label(self, text='max', bg=bg, fg=fg, font=font)

        label_timer.grid(row=0, column=0, sticky=tk.W)
        label_workers.grid(row=1, column=0, sticky=tk.W)
        label_workers_min.grid(row=1, column=1, sticky=tk.W)
        label_workers_max.grid(row=1, column=3, sticky=tk.W)
        label_productivity.grid(row=2, column=0, sticky=tk.W)
        label_productivity_min.grid(row=2, column=1, sticky=tk.W)
        label_productivity_max.grid(row=2, column=3, sticky=tk.W)
        label_tasks.grid(row=3, column=0, sticky=tk.W)
        label_tasks_min.grid(row=3, column=1, sticky=tk.W)
        label_tasks_max.grid(row=3, column=3, sticky=tk.W)
        label_complexity.grid(row=4, column=0, sticky=tk.W)
        label_complexity_min.grid(row=4, column=1, sticky=tk.W)
        label_complexity_max.grid(row=4, column=3, sticky=tk.W)

        self.timer.grid(row=0, column=2, sticky=tk.E)
        self.workers_min.grid(row=1, column=2, sticky=tk.E)
        self.workers_max.grid(row=1, column=4, sticky=tk.E)
        self.productivity_min.grid(row=2, column=2, sticky=tk.E)
        self.productivity_max.grid(row=2, column=4, sticky=tk.E)
        self.tasks_min.grid(row=3, column=2, sticky=tk.E)
        self.tasks_max.grid(row=3, column=4, sticky=tk.E)
        self.complexity_min.grid(row=4, column=2, sticky=tk.E)
        self.complexity_max.grid(row=4, column=4, sticky=tk.E)
        button_ok.grid(row=5, column=0, pady=20)

    def button_ok(self):
        settings = {
            'timer': self.timer.get(),
            'workers_min': self.workers_min.get(),
            'workers_max': self.workers_max.get(),
            'productivity_min': self.productivity_min.get(),
            'productivity_max': self.productivity_max.get(),
            'tasks_min': self.tasks_min.get(),
            'tasks_max': self.tasks_max.get(),
            'complexity_min': self.complexity_min.get(),
            'complexity_max': self.complexity_max.get()
        }
        if '' in settings.values():
            mb.showerror("Ошибка", "Должно быть введено число", parent=self)
        else:
            self.app.settings_data({k: int(v) for k, v in settings.items()})
            self.destroy()


def count_center(w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws//2) - (w//2)
    y = (hs//2) - (h//2)

    return '{}x{}+{}+{}'.format(w, h, x, y)


if __name__ == '__main__':
    root = tk.Tk()
    app = ManagerBot(root)
    root.title('Менеджер бот')
    root.geometry(count_center(1050, 450))
    root.resizable(False, False)
    root.mainloop()
