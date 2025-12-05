import json
from io import TextIOWrapper

from misc import di

class FileWork:
    def __init__(self, file_name=""):
        self.con_panel = di.Container.con_panel()
        self.poll_panel = di.Container.poll_panel()
        self.send_panel = di.Container.send_panel()
        self.data = {"port": "?", "baudrate": 3, "num_of_bits": 4, "parity": 0, "stop_bits": 0, "start_address": 1,
                     "stop_address": 247, "range_box": 0, "cur_address": 1, "new_address": 1}
        self.file_name = file_name + " config.json"

    def getConfig(self):
        pass

    def readConfig(self):
        new_data = {}
        try:
            file = open(f"{self.file_name}", mode='r')
            try:
                new_data = json.load(file)
            except:
                print(f"{self.file_name} trouble with parsing to dict")
            finally:
                file.close()
        except (IOError, OSError) as e:
            print(f"{self.file_name} file read error")

        if sorted(self.data.keys()) == sorted(new_data.keys()):
            apply_flag = True
            apply_flag = apply_flag and type(new_data["port"] is str)
            apply_flag = apply_flag and self._check(new_data["baudrate"], 0, 6)
            apply_flag = apply_flag and self._check(new_data["num_of_bits"], 0, 4)
            apply_flag = apply_flag and self._check(new_data["parity"], 0, 2)
            apply_flag = apply_flag and self._check(new_data["stop_bits"], 0, 1)
            apply_flag = apply_flag and self._check(new_data["start_address"], 1, 247)
            apply_flag = apply_flag and self._check(new_data["stop_address"], 1, 247)
            apply_flag = apply_flag and self._check(new_data["range_box"], 0, 1)
            apply_flag = apply_flag and self._check(new_data["cur_address"], 1, 247)
            apply_flag = apply_flag and self._check(new_data["new_address"], 1, 247)
            if apply_flag:
                self.data = new_data.copy()
                self.con_panel.setConfig(self.data)
                self.poll_panel.setConfig(self.data)
                self.send_panel.setConfig(self.data)
                self.poll_panel.updateStopSearchFieldState()
                return
        print(f"{self.file_name} wrong config")


    def saveConfig(self):
        con_panel_config = self.con_panel.getConfig()
        poll_panel_config = self.poll_panel.getConfig()
        send_panel_config = self.send_panel.getConfig()

        self.data["port"] = con_panel_config[0]
        self.data["baudrate"] = con_panel_config[1]
        self.data["num_of_bits"] = con_panel_config[2]
        self.data["parity"] = con_panel_config[3]
        self.data["stop_bits"] = con_panel_config[4]
        self.data["start_address"] = poll_panel_config[0]
        self.data["stop_address"] = poll_panel_config[1]
        self.data["range_box"] = poll_panel_config[2]
        self.data["cur_address"] = send_panel_config[0]
        self.data["new_address"] = send_panel_config[1]

        try:
            file = open(f"{self.file_name}", mode="w")
            try:
                file.write(json.dumps(self.data))
            except:
                print(f"{self.file_name} trouble with writing dict data")
            finally:
                file.close()
        except (IOError, OSError) as e:
            print(f"{self.file_name} file open for write error")
        print(self.data)

    @staticmethod
    def _check(value, minVal, maxVal) -> bool:
        return (type(value) is int) and (minVal <= value <= maxVal)
