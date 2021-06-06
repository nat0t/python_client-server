class User:
    """User class. For future expansion."""

    def __init__(self, name: str, password: str) -> None:
        self._name = name
        self._password = password

    @property
    def name(self) -> str:
        return self._name

    @property
    def password(self) -> str:
        return self._password

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @password.setter
    def password(self, password) -> None:
        self._password = password
