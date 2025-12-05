from dependency_injector import containers, providers

from com.modbus import ModbusConnector
from misc.file_work import FileWork
from visu.con_panel import ConnectionPanel
from visu.main_window import MainWindow
from visu.poll_panel import PollPanel
from visu.send_panel import SendPanel


class Container(containers.DeclarativeContainer):
    main_window = providers.Singleton(MainWindow)
    con_panel = providers.Singleton(ConnectionPanel)
    poll_panel = providers.Singleton(PollPanel)
    send_panel = providers.Singleton(SendPanel)
    modbus_connector = providers.Singleton(ModbusConnector)
    file_work = providers.Singleton(FileWork)
