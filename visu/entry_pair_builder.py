from tkinter import *
from tkinter import ttk


class EntryPairBuilder:
    def _get_entry_with_str_var(self, labelText, firstValue: str = 1, master=None):
        frame = ttk.Frame(master)
        label = ttk.Label(frame, text=labelText)
        strVar = StringVar(value=firstValue)
        field = ttk.Entry(frame, width=7, textvariable=strVar, validate="key",
                          validatecommand=(master.register(self.validate_entry), "%S"))
        field.config()
        label.pack(side=LEFT)
        field.pack(side=LEFT)
        frame.pack(side=LEFT)
        return field, strVar

    @staticmethod
    def _limit_address(address):
        if address < 1:
            return 1
        elif address > 247:
            return 247
        return address

    @staticmethod
    def validate_entry(txt):
        return txt.isdecimal()