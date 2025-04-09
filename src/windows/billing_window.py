from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class BillingWindow(QWidget):
    def __init__(self, parent: QWidget) -> None:
        """A subclass of QWidget, acting as the billing window widget.

        Args:
            parent (QWidget): Parent of the billing window, typically the main window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the billing window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Set background as static colour.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.background}")
    
    def _set_widgets(self):
        """A function to load the neccesary widgets into the billing window."""
        self.top_bar = TopBarWidget(self) # Top bar.