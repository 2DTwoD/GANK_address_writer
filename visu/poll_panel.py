from tkinter import *
from tkinter import ttk, Text
from misc import di
from visu.entry_pair_builder import EntryPairBuilder


class PollPanel(ttk.Frame, EntryPairBuilder):
    def __init__(self, master=None):
        super().__init__(master)
        self.connector = di.Container.modbus_connector()
        self.con_panel = di.Container.con_panel()

        buttonFrame = ttk.Frame(master=self)
        self.startSearchField, self.startSearchStrVar = self._get_entry_with_str_var("Старт:",
                                                                                     master=buttonFrame)
        self.stopSearchField, self.stopSearchStrVar = self._get_entry_with_str_var("Стоп:", firstValue="247",
                                                                                   master=buttonFrame)

        self.startSearchButton = ttk.Button(master=buttonFrame, text="Опрос сети",
                                       command=lambda: self.searchAction())
        self.stopSearchButton = ttk.Button(master=buttonFrame, text="Остановить опрос", state='disabled',
                                           command=lambda: self.connector.stopSearch())

        textFrame = ttk.Frame(master=self)
        self.textArea = Text(master=textFrame, width=45, height=8, wrap="word", state="disabled")
        scroll = ttk.Scrollbar(master=textFrame, orient="vertical", command=self.textArea.yview)

        self.textArea.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        self.startSearchButton.pack(side=LEFT)
        self.stopSearchButton.pack(side=LEFT)
        self.textArea["yscrollcommand"] = scroll.set

        textFrame.pack()
        buttonFrame.pack()
        self.pack()

    def searchAction(self):
        startAddr = self._limit_address(self.getStartSearchAddress())
        stopAddr = self._limit_address(self.getStopSearchAddress())
        if startAddr > stopAddr:
            startAddr = stopAddr
        self.startSearchStrVar.set(f"{startAddr}")
        self.stopSearchStrVar.set(f"{stopAddr}")
        self.connector.searchAll(startAddr, stopAddr)

    def getStartSearchAddress(self) -> int:
        return int(self.startSearchStrVar.get())

    def getStopSearchAddress(self) -> int:
        return int(self.stopSearchStrVar.get())

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

    def unlock(self):
        self.startSearchButton.config(state='normal')
        self.stopSearchButton.config(state='disabled')
        self.startSearchField.config(state='normal')
        self.stopSearchField.config(state='normal')

    def lockStopSearchButton(self):
        self.stopSearchButton.config(state='disabled')
