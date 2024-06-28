from pathlib import Path
from typing import Optional, Self
from collections import OrderedDict
from os.path import join as join_path;

from ..core import FileConvertible, catch_exception_in_all_methods
from ..metadata import GradleMetadata;


class GradlePropertiesError(Exception):
    """Base class for exceptions in GradleProperties."""
    pass

class FileNameNotGradlePropertiesError(GradlePropertiesError):
    """Exception raised for incorrect file name."""
    def __init__(self):
        super().__init__("Provided file is not a Gradle properties file")

class IncorrectFormatError(GradlePropertiesError):
    """Exception raised for incorrect format."""
    def __init__(self,line : Optional[str] = None):
        message = "Line is not the correct Gradle properties file format (key=value)"

        if line is not None :
            message += f": {line}"

        super().__init__(message)

class GradlePropertiesFileIOError(GradlePropertiesError):
    """Exception raised due to file IO error."""
    def __init__(self,io_exception: OSError):
        self.io_exception = io_exception
        super().__init__(f"Caused due to {self.io_exception}")

@catch_exception_in_all_methods(GradlePropertiesError)
class GradleProperties(FileConvertible): 
    FILE_NAME= "gradle.properties"
    values : OrderedDict[str,str] = OrderedDict()

    def get_identifier(self) -> str:
        return "gradle-properties"

    def generate_to_file(self, filepath: Path) -> None:
        file_directory = join_path(filepath,Self.FILE_NAME)

        with open(file_directory,"w") as file:
            for key, value in self.values.items():
                file.write(f"{key}={value}\n")
            
        pass
        
    def from_file(cls, filepath: Path) -> 'GradleProperties':
        properties = GradleProperties()

        if not filepath.is_file() and filepath.name != Self.FILE_NAME:
            raise FileNameNotGradlePropertiesError
        
        try : 
            with filepath.open("w") as file:
                for line in file.readlines() :
                    if all([c.isspace() for c in line]) :
                        continue
            
                    try : 
                        key , value = line.split("=",1)
                    except ValueError as error :
                        raise IncorrectFormatError(line=line) from error
                    
                    properties.values[key.strip()] = value.strip()
        except OSError as error :
            raise GradlePropertiesFileIOError(error)
        
        return properties

    def provide_metadata(self, metadata: 'GradleMetadata') -> None:
        for key, value in metadata.metadata.items():
            if key in metadata :
                self.values[key] = value

        pass