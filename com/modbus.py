from threading import Thread

from pymodbus import ModbusException

from enum import Enum

from misc import di

class ModbusRequest(Enum):
    READ_ALL = 1
    SEND_ADDRESS = 2


class ModbusConnector:
    def __init__(self):
        self.active = False
        self.con_panel = None
        self.poll_panel = None
        self.send_panel = None
        self.main_window = None

    def _init_panels(self):
        self.con_panel = di.Container.con_panel()
        self.poll_panel = di.Container.poll_panel()
        self.send_panel = di.Container.send_panel()
        self.main_window = di.Container.main_window()

    def searchAll(self, start: int = 1, stop: int = 247):
        if self.active:
            return
        thread = Thread(target=self._searchThread, daemon=True, args=(ModbusRequest.READ_ALL, start, stop))
        thread.start()

    def sendAddress(self, dev_addr: int = 1, new_dev_addr: int = 1):
        if self.active:
            return
        thread = Thread(target=self._searchThread, daemon=True,
                        args=(ModbusRequest.SEND_ADDRESS, dev_addr, new_dev_addr))
        thread.start()

    def stopSearch(self):
        self.active = False

    def _lock_panels(self):
        self.con_panel.lock()
        self.poll_panel.lock()
        self.send_panel.lock()

    def _unlock_panels(self):
        self.con_panel.unlock()
        self.poll_panel.unlock()
        self.send_panel.unlock()

    def _searchThread(self, request: ModbusRequest, dev_addr: int = 1, new_dev_addr: int = 1):
        print("Поток запущен")
        self.active = True
        self._init_panels()
        self._lock_panels()
        client = self.con_panel.getModbusClient()
        if client.connect():
            print("Соединение установлено")
            self.poll_panel.clearTextArea()
            if request == ModbusRequest.READ_ALL:
                self.main_window.setStatus("Опрос сети ...")
                for i in range(dev_addr, new_dev_addr + 1):
                    cur_addr = -1
                    if not self.active:
                        break
                    try:
                        res = client.read_holding_registers(address=0, count=1, device_id=i)
                        cur_addr = client.convert_from_registers(res.registers, data_type=client.DATATYPE.INT16)
                        print(f"Нашел устройство с адресом: {i}({cur_addr})")
                        res_str = "Да"
                        if i != cur_addr:
                            res_str = f"{cur_addr}?"
                        self.poll_panel.insertToTextArea(f"{i}({res_str}), ")
                    except ModbusException:
                        print(f"Нет устройства с адресом: {i}")
                        self.poll_panel.insertToTextArea(f"{i}(Нет), ")

            elif request == ModbusRequest.SEND_ADDRESS:
                self.poll_panel.lockStopSearchButton()
                self.main_window.setStatus("Отправка адреса...")
                try:
                    client.write_register(address=0, value=new_dev_addr, device_id=dev_addr)
                except ModbusException as exc:
                    pass
            client.close()
            print("Соединение закрыто")
            self.main_window.setStatus("Готов")
        self.active = False
        self._unlock_panels()
        print("Поток остановлен")
