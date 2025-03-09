import abc
from src.settings_system import SettingsSystem

class Service(abc.ABC):

    def __init__(self, settings_system: SettingsSystem) -> None:
        self.settings_system = settings_system
        self.update_settings()

    @abc.abstractmethod
    def update_settings(self):
        """
        Updates the service settings.
        """
        pass