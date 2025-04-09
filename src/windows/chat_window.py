from src.shared.imports import *

# Local imports.
from src.windows.widgets.topbar_widget import TopBarWidget

class ChatWindow(QWidget):
    def __init__(self, parent: QWidget) -> None:
        """A subclass of QWidget, acting as the chat window widget.

        Args:
            parent (QWidget): Parent of the chat window, typically the main window.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
        
        self.current_open_chat : OpenChat = None # Storage for currently open chat.
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
        
    def _set_design(self):
        """A function to set the design of the chat window."""
        self.setFixedSize(self.parentWidget().size()) # Fill main window.
        
        # Set background as static colour.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.background}")
    
    def _set_widgets(self):
        """A function to load the neccesary widgets into the chat window."""
        self.top_bar = TopBarWidget(self) # Top bar.
        self.chats = Chats(self)
    
    def open_chat(self, chat: Chat):
        """A function to open a chat in the current window."""
        if self.current_open_chat is not None:
            self.current_open_chat.deleteLater() # If there's a chat open, delete it.
        
        # Create an open chat widget.
        self.current_open_chat = OpenChat(self, chat)

    def open_create_chat(self):
        """A function to open the create a chat window."""
        # Create a create chat widget.
        self.current_open_chat = CreateChat(self)
    
    def refresh_chats(self):
        """A function to refresh all chats in the side bar."""
        self.chats.deleteLater() # Delete the chats window.
        self.chats = Chats(self) # Create a new object.
    
class Chats(QWidget):
    def __init__(self, parent: QWidget):
        """A subclass of QWidget, a container for buttons which are different chats the user is a part of.
        
        Args:
            parent (QWidget): Parent object of the chats widget.
        """
        super().__init__(parent)
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
        
        self._set_design()
        self._set_layout()
        self.load_chats()
        
        # Show the window.
        self.show()
    
    def _set_design(self):
        """A function to set the design of a chat widget."""
        self.setFixedSize(50, self.parentWidget().height() - self.parentWidget().top_bar.height()) # Fill height of parent, fixed width.
        self.move(0, self.parentWidget().top_bar.height()) # Move under the topbar.
        
        # Add a background to the chats widget.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.header};")
    
    def _set_layout(self):
        """A function to set the layout of a chat widget."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.content_widget = QWidget(self)
        self.content_widget.setFixedWidth(self.width())
        self.content_widget.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: transparent;")
        
        self.main_layout.addWidget(scroll_area)
            
        self.setLayout(self.main_layout)
    
    def load_chats(self):
        """A function to load all the chats the member is a part of."""
        logged_member : Member = QApplication.instance().property("LoggedMember")
        database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/chat.sqlite")
    
        chats_data = database.get_member_chats(logged_member)
        
        chats : list[Chat] = [] # Chats storage.
        for chat_data in chats_data:
            chats.append(Chat(chat_data))
        
        # Create a chat icon for each chat the member is a part of.
        for chat in chats:
            random_profile = circular_pixmap(get_random_profile_pixmap())
            button = ChatButton(self, chat, random_profile)
            
            self.add_widget(button)
        
        # Add the create chat button to the bottom.
        self.add_widget(CreateChatButton(self))
        
        # Resize the contents widget after adding widgets.
        self.content_widget.setFixedHeight(self.content_widget.sizeHint().height())
    
    def add_widget(self, widget: QWidget):
        """A function to add a widget to the scroll area."""
        self.content_layout.addWidget(widget, alignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class CreateChatButton(QPushButton):
    def __init__(self, parent: QWidget):
        """A subclass of QPushButton, used to create a chat with another user in the side bar.

        Args:
            parent (QWidget): Parent of the create chat button.
        """
        super().__init__(parent)
        self._set_design()

        # Add a clicked connection.
        self.clicked.connect(self._on_click)
    
    def _set_design(self):
        """A function to set design elements to the create chat button."""
        size = min(self.parentWidget().width(), self.parentWidget().height())
        self.setFixedSize(size, size)
        
        self.setIcon(QPixmap(path("/assets/icons/add.png")))
        self.setIconSize(QSize(self.size().height() - 5, self.size().width() - 5))
        
        self.setStyleSheet("background-color: transparent; border: none;")
    
    def _on_click(self):
        """A function called when the create a chat button is clicked."""
        window = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        
        if window.current_open_chat is not None:
            window.current_open_chat.deleteLater() # Delete the open chat.
            window.current_open_chat = None # Set it back to none.
        
        # Open the create a chat window.
        window.open_create_chat()
  
class ChatButton(QPushButton):
    def __init__(self, parent: QWidget, chat: Chat, icon_src: QPixmap):
        """A class which is a subclass of QPushButton, used to display a button for each chat.

        Args:
            parent (QWidget): Parent of the chat button, typically the chats widget.
            chat (Chat): Chat object the button belongs to.
            icon_src (QPixmap): Icon of the button, usually a profile picture.
        """
        super().__init__(parent)
        self.chat = chat
        self.icon_src = icon_src
        
        self._set_design()
        self._set_connections()
    
    def _set_design(self):
        """A function to set the design of a widget."""
        size = min(self.parentWidget().width(), self.parentWidget().height())
        self.setFixedSize(size, size)
        
        self.setIcon(self.icon_src)
        self.setIconSize(QSize(self.size().height() - 5, self.size().width()- 5))
        
        self.setStyleSheet("background-color: transparent; border: none;")
    
    def _set_connections(self):
        """A function to add connections to the button."""
        self.clicked.connect(self._on_click)
    
    def _on_click(self):
        """A function called when the chat button is clicked."""
        self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().open_chat(self.chat)
        
class OpenChat(QWidget):
    def __init__(self, parent: QWidget, chat: Chat) -> None:
        """An OpenChat QWidget subclass to display an open chat.

        Args:
            parent (QWidget): Parent of the OpenChat, typically the Chats widget.
            chat (Chat): Chat to open.
        """
        super().__init__(parent)
        self.chat = chat
        
        self._set_design()
        self._set_widgets()
        self._set_layout()
        
        # Show the widget.
        self.show()
    
    def _set_design(self):
        """A function to add design to the openchat widget."""
        parent = self.parentWidget()
        
        self.setFixedSize(parent.width() - parent.chats.width(), parent.height() - parent.top_bar.height())
        
        # Move to under top bar and beside chats.
        self.move(parent.chats.width(), parent.top_bar.height())
    
    def _set_widgets(self):
        """A function to add widgets to the openchat widget."""
        self.message_contents = self.MessageContents(self, self.chat)
        self.message_box = self.MessageBox(self)
    
    def _set_layout(self):
        """A function to set layout elements to the openchat widget."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.message_contents)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()) # Scroll to bottom.
        
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.message_box)
            
        self.setLayout(self.main_layout)
    
    def scroll_to_bottom(self):
        """A function to scroll down to the absolute bottom of the scroll area."""
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum() + 100) # Scroll to bottom.
    
    class MessageContents(QWidget):
        def __init__(self, parent: QWidget, chat: Chat):
            super().__init__(parent)
            self.chat = chat
            
            self._set_layout()
            self._set_design()
        
        def _set_layout(self):
            """A function to add layout elements to the message contents."""
            self.main_layout = QVBoxLayout(self)
            
            # For every message in the chat, add the message widget.
            for message in self.chat.messages:
                self.main_layout.addWidget(self.MessageWidget(self, message))
            
            self.setLayout(self.main_layout)
        
        def _set_design(self):
            """A function to set the design of the message contents."""
            if self.sizeHint().height() < self.parentWidget().height():
                if self.sizeHint().height() < 5:
                    self.setFixedHeight(100)
                else:
                    self.setFixedHeight(self.sizeHint().height())
            
            self.setFixedWidth(self.parentWidget().width())
        
        def update_size(self):
            """A function to update the size of the message contents."""
            self.setFixedHeight(self.sizeHint().height())
        
        class MessageWidget(QWidget):
            def __init__(self, parent: QWidget, message: Message):
                """A subclass of QWidget, used to display a message on the screen,

                Args:
                    parent (QWidget): Parent of the message widget.
                    message (Message): Message object that's being displayed.
                """
                super().__init__(parent)
                self.message = message
                self.member = self.message.member
                
                self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
                self.font_manager : FontManager = QApplication.instance().property("FontManager")
                
                self._set_design()
            
            def _set_design(self):
                """A function to set the design of the message widget."""
                self.main_layout = QVBoxLayout()
                self.top_layout = QHBoxLayout()
                
                self.profile_image = QLabel(self)
                self.profile_image.setFixedSize(50, 50)
                self.profile_image.setPixmap(
                    circular_pixmap(
                        get_random_profile_pixmap()
                    ).scaled(
                        self.profile_image.size(),
                        mode = Qt.TransformationMode.SmoothTransformation
                    )
                )
                
                self.member_name = QLabel(self)
                self.member_name.setText(f"{self.member.forename.capitalize()} {self.member.surname.capitalize()}")
                self.member_name.setFont(self.font_manager.geist.bold)
                self.member_font = self.member_name.font()
                self.member_font.setPointSize(15)
                self.member_name.setFont(self.member_font)
                self.member_name.setStyleSheet(f"color: {self.colour_manager.text};")
                
                self.text_label = QLabel(self)
                self.text_label.setText(self.message.text)
                self.text_label.setFont(self.font_manager.geist.regular)
                self.text_font = self.text_label.font()
                self.text_font.setPointSize(10)
                self.text_label.setFont(self.text_font)
                self.text_label.setStyleSheet(f"color: {self.colour_manager.text};")

                
                # Add widgets to layouts.
                self.top_layout.addWidget(self.profile_image)
                self.top_layout.addWidget(self.member_name)
        
                self.main_layout.addLayout(self.top_layout)
                self.main_layout.addWidget(self.text_label)
                
                self.setLayout(self.main_layout)

    class MessageBox(QWidget):
        def __init__(self, parent: QWidget):
            """A subclass of QWidget, used as the message box for users to type in their message.
            
            Args:
                parent (QWidget): Parent of the MessageBox, typically a QWidget.
            """
            super().__init__(parent)
            self.profile_picture : QPixmap = QApplication.instance().property("EclipseProfilePicture")
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            self.font_manager : FontManager = QApplication.instance().property("FontManager")
            
            self.setFixedWidth(self.parentWidget().width())
            self.setFixedHeight(100)
            
            self.background_label = QLabel(self)
            self.background_label.setFixedSize(self.size())
            self.background_label.setStyleSheet(f"background-color: {self.colour_manager.header};")
            
            # User profile picture.
            self.profile_label = QLabel(self)
            self.profile_label.setFixedSize(50, 50)
            self.profile_label.setPixmap(
                self.profile_picture.scaled(
                    self.profile_label.size(),
                    mode = Qt.TransformationMode.SmoothTransformation
                )
            )
            
            # Send button.
            self.send_button = QPushButton(self)
            self.send_button.setFixedSize(25, 25)
            self.send_button.setIcon(QPixmap(path("/assets/icons/send.png")))
            self.send_button.setIconSize(self.send_button.size())
            self.send_button.setStyleSheet("background-color: transparent; border: none;")
            self.send_button.clicked.connect(self._send_message)
            
            # Text edit area.
            self.text_edit = QTextEdit(self)
            self.text_edit.setFixedHeight(self.height())
            self.text_edit.setFixedWidth(self.width() - self.profile_label.width() - self.send_button.width())
            self.text_edit.move(self.profile_label.width(), 0)
            self.text_edit.setPlaceholderText("Message a friend!")
            self.text_edit.setStyleSheet(
                f"background-color: {self.colour_manager.text};"
                f"color: {self.colour_manager.header}"
            )
            self.text_edit.setFont(self.font_manager.geist.regular)
            
            self.send_button.move(self.text_edit.width() + self.profile_label.width(), 0)
        
        def _send_message(self):
            """A function to send a message to user."""
            if self.text_edit.toPlainText() == "":
                return # Return early.
            
            parent = self.parentWidget()
            message_contents = parent.message_contents
            main_layout = message_contents.main_layout
            
            message = Message(
                member = QApplication.instance().property("LoggedMember"),
                text = self.text_edit.toPlainText()
            )
            
            message_widget = message_contents.MessageWidget(message_contents, message)
            
            main_layout.addWidget(message_widget)
            
            # Push scroll area to bottom.
            QTimer.singleShot(10, message_contents.update_size)
            QTimer.singleShot(10, parent.scroll_to_bottom)
            
            # Add the message to the database.
            database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/chat.sqlite")
            database.add_message(parent.chat, message)
            
            # Clear text_edit.
            self.text_edit.clear()

class CreateChat(QWidget):
    def __init__(self, parent: QWidget):
        """A subclass of QWidget, used to create a chat to another user using their email address.
        
        Args:
            parent (QWidget): Parent object of the createchat, typically the Chat window.
        """
        super().__init__(parent)
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
    
    def _set_design(self):
        """A function to set the design of the create chat widget."""
        parent = self.parentWidget()
        self.setFixedSize(parent.width() - parent.chats.width(), parent.height() - parent.top_bar.height())
        
        self.move(parent.chats.width(), parent.top_bar.height())
    
    def _set_widgets(self):
        """A function to set relevant widgets to the create chat widget."""
        self.create_button = self.CreateButton(self)
        self.email_input = self.EmailInput(self)
        self.error_label = self.ErrorLabel(self)
    
    class EmailInput(QLineEdit):
        def __init__(self, parent: QWidget):
            """A subclass of QLineEdit, used for the user to input an email of the user they'd like to message.
            
            Args:
                parent (QWidget): Parent of the email input, typically a create chat widget.
            """
            super().__init__(parent)
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            
            self.setFixedSize(
                parent.width() - 50,
                50
            )
            
            self.setPlaceholderText("Friends email!")
            
            self.setStyleSheet(
                f"background-color: {self.colour_manager.text};"
                f"color: {self.colour_manager.header};"
                "border: none;"
            )
    
    class CreateButton(QPushButton):
        def __init__(self, parent: QWidget):
            """A subclass of QPushButton, used as a button to create a chat with another user.
            
            Args:
                parent (QWidget): Parent of the create button, typically the createChat widget.
            """
            super().__init__(parent)
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            
            self.setFixedSize(50, 50)
            self.move(parent.width() - self.width(), 0)
            
            self.setIcon(QPixmap(path("/assets/icons/add.png")))
            self.setIconSize(self.size())
            
            self.setStyleSheet(
                f"background-color: {self.colour_manager.header};"
                "border: none;"
            )
    
            self.clicked.connect(self._on_click)
        
        def _on_click(self):
            """A function called when the create button is clicked."""
            parent = self.parentWidget()
            window = parent.parentWidget()
            
            email_input : QLineEdit = parent.email_input
            error_label : QLabel = parent.error_label
            logged_member : Member = QApplication.instance().property("LoggedMember")
            
            # If there's no text entered.
            if email_input.text() == "":
                error_label.setText("NO EMAIL")
                error_label.show()
                
                error_label.update_size()
                
                return # Return early.
            
            else:
                error_label.hide()
            
            # Get the member the user is trying to add.
            database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/gym.sqlite")
            adding_member = database.get_member(email = email_input.text())
            
            # Couldn't find the user.
            if adding_member is None:
                error_label.setText("NOT FOUND")
                error_label.show()
                
                error_label.update_size()
                
                return # Return early.
            
            else:
                error_label.hide()
            
            # The user is found! continue
            
            # If the user trying to be added is themself.
            if adding_member.id == logged_member.id:
                error_label.setText("NOT YOURSELF")
                error_label.show()
                
                error_label.update_size()
                
                return # Return early.
            
            else:
                error_label.hide()
                
            # So a user has been found, it's not themselves - great, continue!
            chat_database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/chat.sqlite")
            
            # Check if the user already has a chat with the other person.
            personal_chat = chat_database.get_personal_chat(logged_member, adding_member)
            
            # They already have a chat!
            if personal_chat is not None:
                error_label.setText("ALREADY CHATTING")
                error_label.show()
                
                error_label.update_size()
                
                return # Return early.
            
            else:
                error_label.hide()
            
            # Create the chat.
            chat_database.create_chat(logged_member, adding_member)
            
            # Refresh chats sidebar.
            window.refresh_chats()
    
    class ErrorLabel(QLabel):
        def __init__(self, parent: QWidget):
            """A subclass of QLabel, used to display an error label on the creation of a chat.
            
            Args:
                parent (QWidget): Parent of the error label, typically a createChat widget.
            """
            super().__init__(parent)
            self.hide()
            self.font_manager : FontManager = QApplication.instance().property("FontManager")
            
            self.setFont(self.font_manager.geist.bold)
            font = self.font()
            font.setPointSize(10)
            self.setFont(font)
            self.setStyleSheet("color: red;")
            
            self.setText("ERROR")
            self.update_size()
        
        def update_size(self):
            """A function to update the size of the error label, usually triggered when the text is updated."""
            self.setFixedSize(self.sizeHint())
            
            self.move(self.parentWidget().email_input.width() - self.width(), 0) # Right top of email input.