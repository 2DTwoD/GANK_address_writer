from tkinter import *
from tkinter import ttk


class EntryPairBuilder:
    def _get_entry_with_str_var(self, labelText, firstValue: str = 1, master=None):
        frame = ttk.Frame(master)
        label = ttk.Label(frame, text=labelText)
        strVar = StringVar(value=firstValue)

        field = ttk.Entry(frame, width=7, textvariable=strVar, validate="key",
                          validatecommand=(master.register(self.validate_entry), "%S", '%P'))
        field.config()
        label.pack(side=LEFT)
        field.pack(side=LEFT)
        frame.pack(side=LEFT)
        return field, strVar

    @staticmethod
    def _limit_address(address) -> (int, bool):
        if address < 1:
            return 1, True
        elif address > 247:
            return 247, True
        return address, False

    @staticmethod
    def validate_entry(c, txt):
        return c.isdecimal() and (len(txt) < 4)

    @staticmethod
    def get_int_from_str(txt: str) -> (int, bool):
        res = 0
        err = False
        try:
            res = int(txt)
        except:
            err = True
        return res, err

    def get_valid_int_from_str(self, txt: str, err_value: int, apply_lim: bool = True) -> int:
        result, err = self.get_int_from_str(txt)
        if err:
            result = err_value
        result, limited = self._limit_address(result)
        if limited and not apply_lim:
            return err_value
        return result
