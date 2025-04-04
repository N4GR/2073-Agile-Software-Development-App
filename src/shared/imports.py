# Local imports.
import sqlite3

# Third-party imports.
from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSizePolicy,
    QPushButton
)

from PySide6.QtCore import (
    QPoint, Qt
)

# Local imports.
from src.shared.objects import *
from src.application.managers.database_manager import DatabaseManager
from src.application.managers.font_manager import FontManager
from src.application.managers.colour_manager import ColourManager