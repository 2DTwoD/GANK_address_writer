from tkinter import Tk, ttk

from misc import di


class MainWindow:
    def __init__(self, window=None):
        self.status_label = ttk.Label(window, text="Готов")
        com_label = ttk.Label(window, text="Настройка COM-порта:")
        poll_label = ttk.Label(window, text="Опрос сети:")
        send_label = ttk.Label(window, text="Отправка нового адреса на устройство:")
        com_label.pack()
        con_panel = di.Container.con_panel(master=window)
        poll_label.pack()
        poll_panel = di.Container.poll_panel(master=window)
        send_label.pack()
        send_panel = di.Container.send_panel(master=window)
        self.status_label.pack()

    def setStatus(self, text: str):
        self.status_label.config(text=text)
