# Python imports.
import sqlite3
import random

# Third-party imports.
from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSizePolicy,
    QPushButton, QScrollArea, QTextEdit, QSizePolicy, QGridLayout
)

from PySide6.QtCore import (
    QPoint, Qt, QSize, QTimer
)

from PySide6.QtGui import (
    QPixmap, QIcon
)

# Local imports.
from src.shared.objects import *
from src.shared.funcs import *
from src.application.managers.database_manager import DatabaseManager
from src.application.managers.font_manager import FontManager
from src.application.managers.colour_manager import ColourManager