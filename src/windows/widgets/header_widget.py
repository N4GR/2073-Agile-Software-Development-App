from src.shared.imports import *

class HeaderWidget(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
        self.font_manager : FontManager = QApplication.instance().property("FontManager")
        
        self._set_design()
        
        # Show the label.
        self.show()
    
    def _set_design(self):
        self.setFixedWidth(self.parentWidget().width())
        self.setFixedHeight(50)
        
        # Background label.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(
            f"background-color: {self.colour_manager.header}"
        )
        
        # Logo label.
        self.logo_label = QLabel(self)
        self.logo_label.setFixedSize(
            self.height(),
            self.height()
        ) # 1:1 ratio using the height.
        self.logo_label.setPixmap(
            QPixmap(
                path("/assets/icons/weights.png")
            ).scaled(
                self.logo_label.width() - 20,
                self.logo_label.width() - 20
            )
        )
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title label.
        self.title_label = QLabel(self)
        self.title_label.move(self.logo_label.width(), 0) # Move to beside logo label.
        self.title_label.setFixedHeight(self.height())
        self.title_label.setText("GYMIFY")
        
        # Set the font.
        self.title_label.setFont(self.font_manager.geist.bold)
        self.title_label_font = self.title_label.font()
        self.title_label_font.setPointSize(20)
        self.title_label.setFont(self.title_label_font)
        
        # Add the style.
        self.title_label.setStyleSheet(f"color: {self.colour_manager.text}")