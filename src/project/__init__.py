

from pathlib import Path
from typing import Self
import os 
import shutil
from sys import platform

from src.gradle.properties import GradleProperties
from src.gradle.settingsgradle import SettingsGradle
from src.metadata import ProjectMetadata
from src.module import Module
from src.project.local import LocalProperties

class GenericProject :
    metadata : ProjectMetadata
    settings_gradle : SettingsGradle
    properties : GradleProperties
    local_properties : LocalProperties

    modules : list[Module]

    def __init__(self,metadata : ProjectMetadata,settings_gradle : SettingsGradle,properties : GradleProperties,local_properties : LocalProperties,modules : list[Module]) -> None:
        self.metadata = metadata
        self.settings_gradle = settings_gradle
        self.properties = properties
        self.local_properties = local_properties
        self.modules = modules

    def extend_generate_to_file(self, filepath: Path) -> None:
        self.settings_gradle.generate_to_file(filepath)
        self.properties.generate_to_file(filepath)
        self.local_properties.generate_to_file(filepath)

        # https://stackoverflow.com/a/66577910/20243803
        if platform.startswith('win32') or platform.startswith('win64'):
            # https://stackoverflow.com/a/48374171/20243803
            # https://www.quora.com/When-should-I-use-shutil.copyfile-vs.-shutil.copy-in-Python
            shutil.copyfile("gradlew",filepath)
            shutil.copyfile("gradlew.bat",filepath)
        pass