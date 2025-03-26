class Member:
    def __init__(
        self,
        id: int,
        forename: str,
        surname: str,
        email: str,
        phone: str,
        password: str
    ):
        """An object containing data related to a member.

        Args:
            id (int): ID of the user.
            forename (str): Forename of the user.
            surname (str): Surname of the user.
            email (str): Email of the user.
            phone (str): Phone number of the user.
        """
        self.id = id
        self.forename = forename
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password