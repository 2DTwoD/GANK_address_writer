from tkinter import ttk

from misc import di

from tkinter.messagebox import askyesno

class MainWindow:
    def __init__(self, window=None, title="App"):
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", lambda: self.onClose(window))
        window.title(title)
        self.status_label = ttk.Label(window, text="Готов")
        con_label = ttk.Label(window, text="Настройка COM-порта:")
        poll_label = ttk.Label(window, text="Опрос сети:")
        send_label = ttk.Label(window, text="Отправка нового адреса на устройство:")
        con_label.pack()
        con_panel = di.Container.con_panel(master=window)
        poll_label.pack()
        poll_panel = di.Container.poll_panel(master=window)
        send_label.pack()
        send_panel = di.Container.send_panel(master=window)
        self.status_label.pack()

        self.file_work = di.Container.file_work(file_name=title)
        self.file_work.readConfig()


    def setStatus(self, text: str):
        self.status_label.config(text=text)

    def onClose(self, window):
        if askyesno(title="Подтверждение", message=f"Закрыть приложение?"):
            self.file_work.saveConfig()
            window.destroy()
