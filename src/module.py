

from abc import abstractmethod
from pathlib import Path
from src.core import FileConvertible
from src.metadata import ModuleMetadata


class Module(FileConvertible) :
    metadata : ModuleMetadata