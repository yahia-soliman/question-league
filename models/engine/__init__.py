"""The database engines supported by the application"""


class Engine:
    """Interface for the storage Engine."""

    def get_all(self):
        pass

    def delete(self):
        pass
