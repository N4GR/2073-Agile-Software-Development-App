from src.windows.main_window import MainWindow
from src.application.application import Application

if __name__ == "__main__":
    application = Application([])
    main_window = MainWindow()
    
    application.exec()