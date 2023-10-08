from mainwindow import Window
from localmemory import LocalMemory


def main():
    local_memory = LocalMemory('db.db')
    handle = Window(local_memory)
    handle.mainloop()


if __name__ == '__main__':
    main()
