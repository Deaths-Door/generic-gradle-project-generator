from typing import OrderedDict, Self
from pathlib import Path
import os 
from src.core import FileConvertible
from src.metadata import GradleMetadata

class LocalProperties(GradleMetadata,FileConvertible) :
    FILE_NAME= "gradle.properties"
    values : OrderedDict[str,str] = OrderedDict()

    def get_identifier() :
        "local.properties"

    def generate_to_file(self, filepath: Path) -> None: 
        file_directory = os.path.join(filepath,Self.FILE_NAME)

        with open(file_directory,"w") as file:
            file.write(
"""
## This file must *NOT* be checked into Version Control Systems,
# as it contains information specific to your local configuration.

# For customization when using a Version Control System, please read the
# header note.
"""
            )
            
            for key, value in self.values.items():
                file.write(f"{key}={value}\n")
            
        pass

