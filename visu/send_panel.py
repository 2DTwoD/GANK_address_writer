from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno

from misc import di

from visu.entry_pair_builder import EntryPairBuilder


class SendPanel(ttk.Frame, EntryPairBuilder):
    def __init__(self, master=None):
        super().__init__(master, borderwidth=1, relief="solid", padding=10)
        self.connector = di.Container.modbus_connector()
        self.con_panel = di.Container.con_panel()
        fields_frame = ttk.Frame(self)
        self.deviceAddressField, self.deviceAddressStrVar = self._get_entry_with_str_var("Текущий адрес устр-ва: ",
                                                                                         master=fields_frame)
        self.sendAddressField, self.sendAddressStrVar = self._get_entry_with_str_var("Новый адрес устр-ва: ",
                                                                                     master=fields_frame)
        self.sendButton = ttk.Button(master=self, text="Отправить", command=lambda: self.sendAction())
        fields_frame.pack()
        self.sendButton.pack(fill=BOTH)
        self.pack()

    def sendAction(self):
        cur_addr = self._limit_address(self.getCurrentAddress())
        new_addr = self._limit_address(self.getNewAddress())
        self.deviceAddressStrVar.set(f"{cur_addr}")
        self.sendAddressStrVar.set(f"{new_addr}")
        res = askyesno(title="Подтверждение", message=f"Сейчас адрес: {cur_addr} -->  станет: {new_addr}")
        if res:
            self.connector.sendAddress(cur_addr, new_addr)

    def getCurrentAddress(self) -> int:
        return self.get_int_from_str(self.deviceAddressStrVar.get())

    def getNewAddress(self) -> int:
        return self.get_int_from_str(self.sendAddressStrVar.get())

    def lock(self):
        self.deviceAddressField.config(state='disabled')
        self.sendAddressField.config(state='disabled')
        self.sendButton.config(state='disabled')

    def unlock(self):
        self.deviceAddressField.config(state='normal')
        self.sendAddressField.config(state='normal')
        self.sendButton.config(state='normal')
