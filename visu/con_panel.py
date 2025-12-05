import serial.tools.list_ports
import threading
from tkinter import ttk
from tkinter import *

from pymodbus.client import ModbusSerialClient

baud_list = ["1200", "4800", "9600", "19200", "38400", "57600", "115200"]
num_of_bits_list = ["4", "5", "6", "7", "8"]
parity_list = ["Нет", "Чет.", "Нечет."]
stop_bits_list = ["1", "2"]


class ConnectionPanel(ttk.Frame):


    def __init__(self, master=None):
        super().__init__(master, borderwidth=1, relief="solid", padding=10)
        self.ports_list = ["?"]
        self.port_combo = self._get_combo_pair("Порт:", self.ports_list, 0)
        self.baud_combo = self._get_combo_pair("Скорость:", baud_list, 3)
        self.num_of_bits_combo = self._get_combo_pair("Число бит:", num_of_bits_list, 4)
        self.parity_combo = self._get_combo_pair("Четность:", parity_list, 0)
        self.stop_bits_combo = self._get_combo_pair("Стоп-биты:", stop_bits_list, 0)
        self.pack()
        self.update_ports_list()

    def _get_combo_pair(self, label_text: str, combo_list: list, select_index: int):
        frame = ttk.Frame(master=self)
        label = ttk.Label(master=frame, text=label_text)
        combo = ttk.Combobox(master=frame, values=combo_list, state="readonly", width=8)
        combo.set(combo_list[select_index])
        label.pack()
        combo.pack()
        frame.pack(side=LEFT)
        return combo

    def update_ports_list(self):
        timer = threading.Timer(2.0, self.update_ports_list)
        timer.daemon = True
        timer.start()
        self.ports_list = ["?"]
        for p in serial.tools.list_ports.comports():
            self.ports_list.append(p.name)
        self.port_combo.config(values=sorted(self.ports_list))

    def get_port(self) -> str:
        return self.port_combo.get()

    def get_baud(self) -> int:
        return int(self.baud_combo.get())

    def get_num_of_bits(self) -> int:
        return int(self.num_of_bits_combo.get())

    def get_parity(self) -> str:
        if self.parity_combo.get() == parity_list[0]:
            return 'N'
        elif self.parity_combo.get() == parity_list[1]:
            return 'E'
        elif self.parity_combo.get() == parity_list[2]:
            return 'O'

    def get_stop_bits(self) -> int:
        return int(self.stop_bits_combo.get())

    def getModbusClient(self) -> ModbusSerialClient:
        return ModbusSerialClient(
            port=self.get_port(),
            baudrate=self.get_baud(),
            parity=self.get_parity(),
            stopbits=self.get_stop_bits(),
            timeout=1,
            retries=1
        )

    def lock(self):
        self.port_combo.config(state="disabled")
        self.baud_combo.config(state="disabled")
        self.num_of_bits_combo.config(state="disabled")
        self.parity_combo.config(state="disabled")
        self.stop_bits_combo.config(state="disabled")


    def unlock(self):
        self.port_combo.config(state="normal")
        self.baud_combo.config(state="normal")
        self.num_of_bits_combo.config(state="normal")
        self.parity_combo.config(state="normal")
        self.stop_bits_combo.config(state="normal")

    def setConfig(self, config: dict):
        self.port_combo.set(config["port"])
        self.baud_combo.current(config["baudrate"])
        self.num_of_bits_combo.current(config["num_of_bits"])
        self.parity_combo.current(config["parity"])
        self.stop_bits_combo.current(config["stop_bits"])

    def getConfig(self):
        return self.port_combo.get(), self.baud_combo.current(), self.num_of_bits_combo.current(), self.parity_combo.current(), self.stop_bits_combo.current()
