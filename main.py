from tkinter import Tk

from misc import di

win_width = 400
win_height = 310

if __name__ == "__main__":
    window = Tk()
    window.title("GANK address writer")
    window.geometry(f'{win_width}x{win_height}')
    main_window = di.Container.main_window(window=window)
    window.mainloop()
