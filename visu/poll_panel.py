from tkinter import *
from tkinter import ttk, Text
from misc import di
import tkinter as tk

from visu.entry_pair_builder import EntryPairBuilder
from tkinter.messagebox import askyesno

class PollPanel(ttk.Frame, EntryPairBuilder):
    def __init__(self, master=None):
        super().__init__(master, borderwidth=1, relief="solid", padding=10)
        self.connector = di.Container.modbus_connector()
        self.con_panel = di.Container.con_panel()

        buttonFrame = ttk.Frame(master=self)
        self.startSearchField, self.startSearchStrVar = self._get_entry_with_str_var("Старт:",
                                                                                     master=buttonFrame)
        self.stopSearchField, self.stopSearchStrVar = self._get_entry_with_str_var("Стоп:", firstValue="247",
                                                                                   master=buttonFrame)

        self.startSearchButton = ttk.Button(master=buttonFrame, text="Опрос",
                                            command=lambda: self.startSearchAction(), width=7)
        self.stopSearchButton = ttk.Button(master=buttonFrame, text="Стоп", state='disabled',
                                           command=lambda: self.stopSearchAction(), width=7)
        self.rangeCheckBoxValue = tk.BooleanVar(value=False)
        self.rangeCheckBox = ttk.Checkbutton(master=buttonFrame, text="Диапазон", variable=self.rangeCheckBoxValue,
                                             command=lambda: self.updateStopSearchFieldState())
        self.updateStopSearchFieldState()

        textFrame = ttk.Frame(master=self)
        self.textArea = Text(master=textFrame, width=42, height=8, wrap="word", state="disabled")
        scroll = ttk.Scrollbar(master=textFrame, orient="vertical", command=self.textArea.yview)

        self.textArea.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        self.startSearchButton.pack(side=LEFT)
        self.stopSearchButton.pack(side=LEFT)
        self.rangeCheckBox.pack(side=LEFT)
        self.textArea["yscrollcommand"] = scroll.set

        textFrame.pack()
        buttonFrame.pack()
        self.pack()

    def startSearchAction(self):
        if self.getRangeCheckBoxState() and not askyesno(title="Подтверждение", message=f"Начать опрос устройств?"):
            return
        startAddr = self.getStartSearchAddress()
        stopAddr = self.getStopSearchAddress()
        if startAddr > stopAddr:
            stopAddr = startAddr
        self.startSearchStrVar.set(f"{startAddr}")
        if not self.getRangeCheckBoxState():
            stopAddr = startAddr
        else:
            self.stopSearchStrVar.set(f"{stopAddr}")
        self.connector.searchAll(startAddr, stopAddr)

    def stopSearchAction(self):
        if self.getRangeCheckBoxState() and not askyesno(title="Подтверждение", message=f"Завершить опрос устройств?"):
            return
        self.connector.stopSearch()

    def getStartSearchAddress(self) -> (int, bool):
        return self.get_valid_int_from_str(self.startSearchStrVar.get(), 1)

    def setStartSearchAddress(self, value: str):
        self.startSearchStrVar.set(str(self.get_valid_int_from_str(value, 1)))

    def getStopSearchAddress(self) -> (int, bool):
        return self.get_valid_int_from_str(self.stopSearchStrVar.get(), 247)

    def setStopSearchAddress(self, value: str):
        self.stopSearchStrVar.set(str(self.get_valid_int_from_str(value, 247)))

    def getRangeCheckBoxState(self) -> bool:
        return self.rangeCheckBoxValue.get()

    def setRangeCheckBoxState(self, value: bool):
        self.rangeCheckBoxValue.set(value)
        self.updateStopSearchFieldState()

    def updateStopSearchFieldState(self):
        self.stopSearchField.config(state='normal' if self.getRangeCheckBoxState() else 'disabled')

    def clearTextArea(self):
        self.textArea.configure(state='normal')
        self.textArea.delete('1.0', END)
        self.textArea.configure(state='disabled')

    def insertToTextArea(self, text: str):
        self.textArea.configure(state='normal')
        self.textArea.insert(END, text)
        self.textArea.yview(END)
        self.textArea.configure(state='disabled')

    def lock(self):
        self.startSearchButton.config(state='disabled')
        self.stopSearchButton.config(state='normal')
        self.startSearchField.config(state='disabled')
        self.stopSearchField.config(state='disabled')
        self.rangeCheckBox.config(state='disabled')

    def unlock(self):
        self.startSearchButton.config(state='normal')
        self.stopSearchButton.config(state='disabled')
        self.startSearchField.config(state='normal')
        self.updateStopSearchFieldState()
        self.rangeCheckBox.config(state='normal')

    def lockStopSearchButton(self):
        self.stopSearchButton.config(state='disabled')

    def setConfig(self, config: dict):
        self.startSearchStrVar.set(str(config["start_address"]))
        self.stopSearchStrVar.set(str(config["stop_address"]))
        self.rangeCheckBoxValue.set(bool(config["range_box"]))

    def getConfig(self):
        return int(self.startSearchStrVar.get()), int(self.stopSearchStrVar.get()), int(self.rangeCheckBoxValue.get())
