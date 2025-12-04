from tkinter import Tk

from misc import di

win_width = 400
win_height = 390

version = "1.1"

if __name__ == "__main__":
    window = Tk()
    title = f"GANK4 address writer v{version}"
    window.geometry(f'{win_width}x{win_height}')
    main_window = di.Container.main_window(window=window, title=title)
    window.mainloop()
