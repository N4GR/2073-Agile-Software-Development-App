from src.shared.imports import *

class LoginWindow(QWidget):
    def __init__(
            self,
            parent: QWidget
    ):
        """A QWidget subclass pertaining to the login window.

        Args:
            parent (QWidget): Parent of the window, usually the main window.
        """
        super().__init__(parent)
        
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        """A function to set the design of a widget."""
        self.setFixedSize(self.parentWidget().size()) # Set the login window to fill the parent.
        
        # Create a background for the widget with a fixed colour.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size())
        self.background_label.setStyleSheet(f"background-color: {self.colour_manager.background};")
        
    def _set_widgets(self):
        """A function to set the relevant widgets to the login window."""
        self.login_panel = LoginPanel(self)

class LoginPanel(QWidget):
    def __init__(
            self,
            parent: QWidget
    ):
        """A subclass of QWidget, containing the panel for users to login and register.

        Args:
            parent (QWidget): Parent of the login panel, usually the login window.
        """
        super().__init__(parent)
        
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
        
        # Keep track of if the registration menu is showing or not.
        self.registration_showing = False
        
        self._set_design()
        self._set_widgets()
        self._set_layouts()
    
    def _set_design(self):
        """A function to set the design of a widget."""
        self.setFixedSize(
            self.parentWidget().width() * 0.9, # 90% of parent width.
            self.parentWidget().height() * 0.5 # 50% of parent height.
        )
        
        # Move the widget to the centre of the window.
        self.move(
            (self.parentWidget().width() / 2)
            - (self.width() / 2),
            (self.parentWidget().height() / 2)
            - (self.height() / 2)
            - 30 # -30px offset.
        )
        
        # Create a background label for the widget with a fixed colour.
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(self.size()) # Fill widget.
        self.background_label.setStyleSheet(
            f"background-color: {self.colour_manager.panel};"
            f"border: 1px solid {self.colour_manager.border};"
            "border-radius: 10px"
        )
    
    def _set_widgets(self):
        """A function to set the widgets related to the widget."""
        self.email_input = self.Email(self)
        self.password_input = self.Password(self)
        
        # For registering a user.
        self.forename_input = self.Forename(self)
        self.forename_input.hide()
        self.surname_input = self.Surname(self)
        self.surname_input.hide()
        self.phone_input = self.Phone(self)
        self.phone_input.hide()
        
        self.buttons = self.Buttons(self)
    
    def _set_layouts(self):
        """A function to set the layouts of a widget."""
        self.main_layout = QVBoxLayout()
        
        # Add the widgets to the layouts.
        self.main_layout.addWidget(self.email_input)
        self.main_layout.addWidget(self.password_input)

        self.main_layout.addWidget(self.buttons)
        
        self.setLayout(self.main_layout)
    
    def set_registering(self):
        """A function to change the login panel to a registration panel."""
        if self.registration_showing is False:
            # Make the login panel larger to fit the new inputs.
            self.setFixedHeight(
                self.parentWidget().height() * 0.7 # 70% of parent height.
            )
            
            # Move the widget to accomodate for the new size.
            self.move(
                (self.parentWidget().width() / 2)
                - (self.width() / 2),
                (self.parentWidget().height() / 2)
                - (self.height() / 2)
                - 30 # -30px offset.
            )
            
            # Resize the background label to accomodate for the new size.
            self.background_label.setFixedSize(self.size())
            
            self.main_layout.insertWidget(2, self.forename_input)
            self.forename_input.show()
            
            self.main_layout.insertWidget(3, self.surname_input)
            self.surname_input.show()
            
            self.main_layout.insertWidget(4, self.phone_input)
            self.phone_input.show()
            
            self.registration_showing = True
            
        else:
            print("Registration panel already showing!")
            
            return # Exit early.
    
    def hide_registering(self):
        if self.registration_showing is True:
            # If the registration window is showing.
            self.setFixedSize(
                self.parentWidget().width() * 0.9, # 90% of parent width.
                self.parentWidget().height() * 0.5 # 50% of parent height.
            )
            
            # Move the widget to the centre of the window.
            self.move(
                (self.parentWidget().width() / 2)
                - (self.width() / 2),
                (self.parentWidget().height() / 2)
                - (self.height() / 2)
                - 30 # -30px offset.
            )
            
            # Resize the background label to accomodate for the new size.
            self.background_label.setFixedSize(self.size())
            
            # Remove the registration widgets from the login panel.
            self.main_layout.removeWidget(self.forename_input)
            self.main_layout.removeWidget(self.surname_input)
            self.main_layout.removeWidget(self.phone_input)
            
            # Hide the widgets again.
            self.forename_input.hide()
            self.surname_input.hide()
            self.phone_input.hide()
            
            # Set the variable back to False.
            self.registration_showing = False
                    
        else:
            print("Can't hide the registration window if it's not showing!")
            
            return # Exit early.
    
    class UserInput(QWidget):
        def __init__(
                self,
                parent: QWidget,
                input_type: str
        ):
            """A function to act as a parent class for user input.

            Args:
                parent (QWidget): Parent of the user input, typically the login panel.
                input_type (str): Type of input, password or username.
            """
            super().__init__(parent)
            self.input_type = input_type
            
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            self.font_manager : FontManager = QApplication.instance().property("FontManager")
            
            # Label for the name of the input type.
            self.name_label = QLabel(self)
            self.name_label.setFont(self.font_manager.geist.bold)
            self.name_label_font = self.name_label.font()
            self.name_label_font.setPointSize(15)
            self.name_label.setFont(self.name_label_font)
            self.name_label.setText(self.input_type.upper())
            self.name_label.setStyleSheet(f"color: {self.colour_manager.text}")
            
            # Error label to display in set_error function.
            self.error_label = QLabel(self)
            self.error_label.setFont(self.font_manager.geist.regular)
            self.error_label.setText("INVALID")
            self.error_label.setStyleSheet("color: red;")
            self.error_label.hide() # Start hidden.
            
            # Layout for the labels.
            self.label_layout = QHBoxLayout()
            self.label_layout.addWidget(self.name_label, alignment = Qt.AlignmentFlag.AlignLeft)
            self.label_layout.addWidget(self.error_label, alignment = Qt.AlignmentFlag.AlignRight)
            
            # Line edit to input.
            self.line_edit = QLineEdit(self)
            self.line_edit.setFont(self.font_manager.geist.regular)
            self.line_edit.setPlaceholderText(self.input_type.capitalize())
            self.line_edit.setStyleSheet(
                f"background-color: {self.colour_manager.background};"
                f"color: {self.colour_manager.text};"
            )
            
            # Main layout.
            self.main_layout = QVBoxLayout()
            self.main_layout.addLayout(self.label_layout)
            self.main_layout.addWidget(self.line_edit, alignment = Qt.AlignmentFlag.AlignTop)
            
            self.setLayout(self.main_layout)
        
        def set_error(self):
            """A function to set the user input error label to be shown."""
            self.error_label.show()
        
        def set_none_found(self):
            """A function to show a none found label above the user input."""
            self.error_label.setText("NONE FOUND")
            self.error_label.show()
        
        def set_invalid_password(self):
            """A function to show a invalid password label above the password input."""
            self.error_label.setText("INVALID PASSWORD")
            self.error_label.show()
        
        def set_label(
                self,
                text: str
        ) -> None:
            """A function to set the error label text to a specified string.

            Args:
                text (str): Text to set the label to.
            """
            self.error_label.setText(text)
            self.error_label.show()
            
    class Email(UserInput):
        def __init__(
                self,
                parent: QWidget
        ):
            """A subclass of UserInput, an object pertaining to the QLineEdit input of the email.

            Args:
                parent (QWidget): Parent of the widget, usually a login panel.
            """
            super().__init__(parent, "email")
    
    class Password(UserInput):
        def __init__(
                self,
                parent: QWidget
        ):
            """A subclass of UserInput, an object pertaining to the QLineEdit input of the password.

            Args:
                parent (QWidget): Parent of the widget, usually a login panel.
            """
            super().__init__(parent, "password")
            
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    class Forename(UserInput):
        def __init__(
                self,
                parent: QWidget
        ):
            super().__init__(parent, "forename")
    
    class Surname(UserInput):
        def __init__(
                self,
                parent: QWidget
        ):
            super().__init__(parent, "surname")
    
    class Phone(UserInput):
        def __init__(
                self,
                parent: QWidget
        ):
            super().__init__(parent, "phone")
    
    class Buttons(QWidget):
        def __init__(
                self,
                parent: QWidget
        ):
            """A subclass of QWidget, containing QPushButtons for the Login Panel.

            Args:
                parent (QWidget): Parent of the Buttons widget, usually a Login Panel.
            """
            super().__init__(parent)
        
            self._set_widgets()
            self._set_layouts()
        
        def _set_widgets(self):
            self.login = self.Login(self)
            self.register = self.Register(self)
        
        def _set_layouts(self):
            self.main_layout = QHBoxLayout()
        
            # Add the widgets to the layout.
            self.main_layout.addWidget(self.login)
            self.main_layout.addWidget(self.register)
            
            self.setLayout(self.main_layout)
        
        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    button_type: str
            ):
                """A subclass of QPushButton, acting as the parent class of a button within the login panel.

                Args:
                    parent (QWidget): Parent of the widget, usually the Buttons QWidget.
                    button_type (str): Type of button, login or register?
                """
                super().__init__(parent)
                self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
                self.font_manager : FontManager = QApplication.instance().property("FontManager")
                
                self.setMinimumHeight(50)
            
                self.setText(button_type.upper())
                self.setFont(self.font_manager.geist.bold)
                self.setStyleSheet(
                    f"background-color: {self.colour_manager.background};"
                    f"color: {self.colour_manager.text};"
                    "border: 15px"
                )    
        
        class Login(Button):
            def __init__(
                    self,
                    parent: QWidget
            ):
                """A Button subclass for the login function of the buttons widget.

                Args:
                    parent (QWidget): A parent object of the login, usually the Buttons widget.
                """
                super().__init__(parent, "login")
                
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                print("Login clicked!")
                
                database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/gym.sqlite")
                
                login_panel = self.parentWidget().parentWidget()
                
                email_input : QWidget = login_panel.email_input
                password_input : QWidget = login_panel.password_input
                
                email_line : QLineEdit = email_input.line_edit
                password_line : QLineEdit = password_input.line_edit
                
                # If registration window is showing, set the window back to login panel.
                if login_panel.registration_showing is True:
                    login_panel.hide_registering()
                    
                    return # Exit early.
                
                # If there's no email entered.
                if email_line.text() == "":
                    email_input.set_error()
                    
                    return # Exit early.
                
                # If there's no password entered.
                if password_line.text() == "":
                    password_input.set_error()

                    return # Exit early.

                ## Check if the email and password is valid to the database.
                member = database.get_member(email = email_line.text())
                
                # If no member was found.
                if member is None:
                    email_input.set_none_found()
                    
                    return # Exit early.
                
                # If the password entered is invalid.
                if password_line.text() != member.password:
                    password_input.set_invalid_password()
                    
                    return # Exit early.
                
                else:
                    # If the password was valid - it's a successful login!
                    print("Successful login!")
                    
                    login_panel.parentWidget().parentWidget().login_member(member)
        
        class Register(Button):
            def __init__(
                    self,
                    parent: QWidget
            ):
                """A Button subclass for the register function of the buttons widget.

                Args:
                    parent (QWidget): A parent object of the register, usually the Buttons widget.
                """
                super().__init__(parent, "register")
                
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                print("Register clicked!")
                
                database : DatabaseManager = QApplication.instance().property("DatabaseManager")("data/gym.sqlite")
                
                # Check if the email and password fields are filled.
                login_panel = self.parentWidget().parentWidget()
                login_window = login_panel.parentWidget()
                main_window = login_window.parentWidget()
                
                # Transform the login panel to a registration panel.
                if login_panel.registration_showing is False:
                    # If the panel isn't showing.
                    login_panel.set_registering()
                    
                    return # Exit early.
                
                # Create references to the inputs and lines within the login panel.
                email_input : QWidget = login_panel.email_input
                email_line : QLineEdit = email_input.line_edit
                entered_email = email_line.text()
                
                password_input : QWidget = login_panel.password_input
                password_line : QLineEdit = password_input.line_edit
                entered_password = password_line.text()
                
                forename_input : QWidget = login_panel.forename_input
                forename_line : QLineEdit = forename_input.line_edit
                entered_forename = forename_line.text()
                
                surname_input : QWidget = login_panel.surname_input
                surname_line : QLineEdit = surname_input.line_edit
                entered_surname = surname_line.text()
                
                phone_input : QWidget = login_panel.phone_input
                phone_line : QLineEdit = phone_input.line_edit
                entered_phone = phone_line.text()
                
                # Check if there's an entered email.
                if entered_email == "":
                    email_input.set_none_found()
                    
                    return # Return early.
                
                else:
                    email_input.error_label.hide() # Hide if showing.
                
                # Check if the email is in the database already or not.
                if database.get_member(email = entered_email) is not None:
                    email_input.set_label("USER EXISTS")
                    
                    return # Return early.v
                
                else:
                    email_input.error_label.hide() # Hide if showing.
                
                # Check if there's an entered password.
                if entered_password == "":
                    password_input.set_none_found()
                    
                    return # Return early.
                
                else:
                    password_input.error_label.hide() # Hide if showing.
                
                # Check if there's an entered forename.
                if entered_forename == "":
                    forename_input.set_none_found()
                    
                    return # Return early.
                
                else:
                    forename_input.error_label.hide() # Hide if showing.
                
                # Check if there's an entered surname.
                if entered_surname == "":
                    surname_input.set_none_found()
                    
                    return # Return early.
                
                else:
                    surname_input.error_label.hide() # Hide if showing.
                
                # Check if there's an entered phone number.
                if entered_phone == "":
                    phone_input.set_none_found()
                    
                    return
                
                else:
                    phone_input.error_label.hide() # Hide if showing.
                
                # Once all checks have complete, add the user to the database.
                current_member = database.add_member(Member(
                    id = 0,
                    forename = entered_forename,
                    surname = entered_surname,
                    email = entered_email,
                    phone = entered_phone,
                    password = entered_password
                ))
                
                # Log the user into the application.
                main_window.login_member(current_member)