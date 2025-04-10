from src.shared.imports import *

# Widget imports.
from src.windows.widgets.header_widget import HeaderWidget

class LoginWindow(QWidget):
    def __init__(self, parent: QWidget):
        """A QWidget subclass pertaining to the login window.

        Args:
            parent (QWidget): Parent of the window, usually the main window.
        """
        super().__init__(parent)
        
        self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
    
        self._set_design()
        self._set_widgets()
        
        # Show the window.
        self.show()
    
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
        self.header = HeaderWidget(self)

class LoginPanel(QWidget):
    def __init__(self, parent: QWidget):
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
        
        # Set new size.
        self.setFixedHeight(self.sizeHint().height())
        self.background_label.setFixedSize(self.size())
        self.centre_widget(y_offset = -30)
    
    def _set_design(self):
        """A function to set the design of a widget."""
        self.setFixedSize(
            self.parentWidget().width() * 0.9, # 90% of parent width.
            self.parentWidget().height() * 0.5 # 50% of parent height.
        )
        
        # Move the widget to the centre of the window.
        self.centre_widget(y_offset = -30)
        
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
        
        self.login_input_height = 50 # When the user is logging in, the input box expands.
        self.email_input.line_edit.setFixedHeight(self.login_input_height)
        self.password_input.line_edit.setFixedHeight(self.login_input_height)
        
        # For registering a user.
        self.forename_input = self.Forename(self)
        self.forename_input.hide()
        self.surname_input = self.Surname(self)
        self.surname_input.hide()
        self.phone_input = self.Phone(self)
        self.phone_input.hide()        
        self.profile_selection = self.ProfileSelection(self)
        self.profile_selection.hide()
        
        self.buttons = self.Buttons(self)
    
    def _set_layouts(self):
        """A function to set the layouts of a widget."""
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(3, 0, 3, 0)
        
        # Add the widgets to the layouts.
        self.main_layout.addWidget(self.email_input)
        self.main_layout.addWidget(self.password_input)

        self.main_layout.addWidget(self.buttons)
        
        self.setLayout(self.main_layout)
    
    def centre_widget(self, x_offset : float = 0, y_offset : float = 0):
        """A function to move the widget in the centre with a given offset.
        
        Args:
            x_offset (float): Offset to move the x position by.
            y_offset (float): Offset to move the y position by.
        """
        self.move(
            (self.parentWidget().width() / 2)
            - (self.width() / 2) + x_offset,
            (self.parentWidget().height() / 2)
            - (self.height() / 2) + y_offset
        )
    
    def set_registering(self):
        """A function to change the login panel to a registration panel."""
        if self.registration_showing is False: 
            self.main_layout.insertWidget(2, self.forename_input)
            self.forename_input.show()
            
            self.main_layout.insertWidget(3, self.surname_input)
            self.surname_input.show()
            
            self.main_layout.insertWidget(4, self.phone_input)
            self.phone_input.show()
            
            self.main_layout.insertWidget(5, self.profile_selection)
            self.profile_selection.show()
            
            # Set the login inputs to the size of the other inputs.
            self.email_input.line_edit.setFixedHeight(self.phone_input.line_edit.height())
            self.password_input.line_edit.setFixedHeight(self.phone_input.line_edit.height())
            
            self.registration_showing = True
            
            # Make the login panel fit the new contents.
            self.setFixedHeight(self.sizeHint().height())
            self.background_label.setFixedSize(self.size())
            
            self.centre_widget(y_offset = 25)
            
        else:
            print("Registration panel already showing!")
            
            return # Exit early.
    
    def hide_registering(self):
        """A function to hide the registration window."""
        if self.registration_showing is True:
            # Remove the registration widgets from the login panel.
            self.main_layout.removeWidget(self.forename_input)
            self.main_layout.removeWidget(self.surname_input)
            self.main_layout.removeWidget(self.phone_input)
            self.main_layout.removeWidget(self.profile_selection)
            
            # Hide the widgets again.
            self.forename_input.hide()
            self.surname_input.hide()
            self.phone_input.hide()
            self.profile_selection.hide()
            
            # Reset login inputs back to their default size.
            self.email_input.line_edit.setFixedHeight(self.login_input_height)
            self.password_input.line_edit.setFixedHeight(self.login_input_height)
            
            # Set the variable back to False.
            self.registration_showing = False
            
            # Make the login panel fit the new contents.
            self.setFixedHeight(self.sizeHint().height())
            self.background_label.setFixedSize(self.size())
            
            # Move back to centre.
            self.centre_widget(y_offset = -30)
                    
        else:
            print("Can't hide the registration window if it's not showing!")
            
            return # Exit early.
    
    class UserInput(QWidget):
        def __init__(self, parent: QWidget, input_type: str):
            """A function to act as a parent class for user input.

            Args:
                parent (QWidget): Parent of the user input, typically the login panel.
                input_type (str): Type of input, password or username.
            """
            super().__init__(parent)
            self.input_type = input_type
            
            self.colour_manager : ColourManager = QApplication.instance().property("ColourManager")
            self.font_manager : FontManager = QApplication.instance().property("FontManager")
            
            # Error label to display in set_error function.
            self.error_label = QLabel(self)
            self.error_label.setFont(self.font_manager.geist.regular)
            self.error_label.setText("INVALID")
            self.error_label.setStyleSheet("color: red;")
            self.error_label.hide() # Start hidden.
            
            # Line edit to input.
            self.line_edit = QLineEdit(self)
            self.line_edit.setFixedHeight(30)
            self.line_edit.setFont(self.font_manager.geist.regular)
            self.line_edit.setPlaceholderText(self.input_type.capitalize())
            self.line_edit.setStyleSheet(
                f"background-color: {self.colour_manager.background};"
                f"color: {self.colour_manager.text};"
            )
            
            self.main_layout = QHBoxLayout()
            self.main_layout.addWidget(self.line_edit)
            
            self.error_label.raise_()
            
            self.setLayout(self.main_layout)
            
            # Move the error label centre-right of the line edit.
            self.error_label.move(
                self.sizeHint().width() - self.error_label.sizeHint().width(),
                0
            )
        
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
        
        def set_label(self, text: str) -> None:
            """A function to set the error label text to a specified string.

            Args:
                text (str): Text to set the label to.
            """
            self.error_label.setText(text)
            self.error_label.show()
            
    class Email(UserInput):
        def __init__(self, parent: QWidget):
            """A subclass of UserInput, an object pertaining to the QLineEdit input of the email.

            Args:
                parent (QWidget): Parent of the widget, usually a login panel.
            """
            super().__init__(parent, "email")
    
    class Password(UserInput):
        def __init__(self, parent: QWidget):
            """A subclass of UserInput, an object pertaining to the QLineEdit input of the password.

            Args:
                parent (QWidget): Parent of the widget, usually a login panel.
            """
            super().__init__(parent, "password")
            
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    class Forename(UserInput):
        def __init__(self, parent: QWidget):
            """A subclass of UserInput, used to display the forename of the user.

            Args:
                parent (QWidget): Parent of the Forename.
            """
            super().__init__(parent, "forename")
    
    class Surname(UserInput):
        def __init__(self, parent: QWidget):
            """A subclass of UserInput, used to display the surname of the user.

            Args:
                parent (QWidget): Parent of the surname.
            """
            super().__init__(parent, "surname")
    
    class Phone(UserInput):
        def __init__(self, parent: QWidget):
            """A subclass of UserInput, used to display the phone number of the user.

            Args:
                parent (QWidget): Parent of the phone number.
            """
            super().__init__(parent, "phone")
    
    class ProfileSelection(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.selected_profile = os.path.abspath((f"{path("/assets/profiles")}/1.png"))
            self.max_rows = 4
            self.max_columns = 4
            
            self.listed_profiles : dict = {}
            
            self._set_design()
            self._set_layout()
            
            self.add_profile_widgets()
        
        def _set_design(self):
            self.setFixedHeight(200)
        
        def _set_layout(self):
            self.main_layout = QGridLayout()
            
            self.setLayout(self.main_layout)
        
        def add_profile_widgets(self):
            """A function to add profile widgets to the grid layout."""
            profiles_dir = path("/assets/profiles")
            
            for row in range(self.max_rows):
                for column in range(self.max_columns):
                    item_count = (self.max_columns * (row) + column) + 1
                    profile_dir = os.path.abspath(f"{profiles_dir}/{item_count}.png")

                    self.listed_profiles[profile_dir] = {"row": row, "column": column}
                    
                    self.main_layout.addWidget(self.ProfileButton(self, icon_src = profile_dir), row, column)
        
        def set_selected_profile(self, profile_dir: str):
            current_selected = self.listed_profiles[self.selected_profile]
            profile_to_select = self.listed_profiles[profile_dir]
            
            if profile_dir == self.selected_profile:
                return # Return early if selecting the same profile.
            
            # Remove the old border of the old selected icon.
            old_selected = self.main_layout.itemAtPosition(current_selected["row"], current_selected["column"]).widget()
            old_selected.setStyleSheet("background-color: transparent;")
            
            # Add the new border to the new selected icon.
            new_selected = self.main_layout.itemAtPosition(profile_to_select["row"], profile_to_select["column"]).widget()
            new_selected.setStyleSheet(
                "border-radius: 12px;"
                "background-color: green;"
            )
            
            # Set the selected profile variable.
            self.selected_profile = profile_dir
        
        class ProfileButton(QPushButton):
            def __init__(self, parent: QWidget, icon_src: str):
                super().__init__(parent)
                self.icon_src = icon_src
                
                self._set_design()
                
                self.clicked.connect(self._on_click)

            def _set_design(self):
                self.setFixedSize(50, 50)
                
                self.setIcon(QPixmap(self.icon_src))
                self.setIconSize(QSize(
                    self.size().width() - 5,
                    self.size().height() - 5
                ))
                
                self.setStyleSheet(
                    "border-radius: 12px;"
                    "background-color: transparent;"
                ) # Circular border.
            
            def _on_click(self):
                """A function called when the profile button is clicked."""
                parent = self.parentWidget()
                parent.set_selected_profile(self.icon_src)

    class Buttons(QWidget):
        def __init__(self, parent: QWidget):
            """A subclass of QWidget, containing QPushButtons for the Login Panel.

            Args:
                parent (QWidget): Parent of the Buttons widget, usually a Login Panel.
            """
            super().__init__(parent)
        
            self._set_widgets()
            self._set_layouts()
        
        def _set_widgets(self):
            """A function to add widgets to the Buttons widget."""
            self.login = self.Login(self)
            self.register = self.Register(self)
        
        def _set_layouts(self):
            """A function to set the layout of the buttons widget."""
            self.main_layout = QHBoxLayout()
            self.main_layout.setContentsMargins(20, 0, 20, 10)
            self.main_layout.setSpacing(20)
        
            # Add the widgets to the layout.
            self.main_layout.addWidget(self.login)
            self.main_layout.addWidget(self.register)
            
            self.setLayout(self.main_layout)
        
        class Button(QPushButton):
            def __init__(self, parent: QWidget, button_type: str):
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
                    "border-radius: 20px"
                )    
        
        class Login(Button):
            def __init__(self, parent: QWidget):
                """A Button subclass for the login function of the buttons widget.

                Args:
                    parent (QWidget): A parent object of the login, usually the Buttons widget.
                """
                super().__init__(parent, "login")
                
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function called when the login button is clicked."""
                
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
            def __init__(self, parent: QWidget):
                """A Button subclass for the register function of the buttons widget.

                Args:
                    parent (QWidget): A parent object of the register, usually the Buttons widget.
                """
                super().__init__(parent, "register")
                
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function called when the registration button is clicked."""
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
                
                selected_profile : str = login_panel.profile_selection.selected_profile
                
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
                
                profile_file_name = os.path.basename(selected_profile)
                
                # Once all checks have complete, add the user to the database.
                current_member = database.add_member(Member(
                    id = 0,
                    forename = entered_forename,
                    surname = entered_surname,
                    email = entered_email,
                    phone = entered_phone,
                    password = entered_password,
                    is_tutor = False,
                    profile = profile_file_name
                ))
                
                # Log the user into the application.
                main_window.login_member(current_member)