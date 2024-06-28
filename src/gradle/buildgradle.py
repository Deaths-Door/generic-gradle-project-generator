from pathlib import Path
from typing import Any, Optional
from os.path import join as join_path;
from src.core import FileConvertible, catch_exception_in_all_methods
from src.gradle.dependency import DependencyGroup
from src.gradle.plugin import PluginGroup
from src.metadata import GradleMetadata, ModuleMetadata

class ModuleBuildGradleError(Exception):
    pass

@catch_exception_in_all_methods(ModuleBuildGradleError)
class ModuleBuildGradle(FileConvertible) :
    def __init__(self,plugins : PluginGroup,dependencies : DependencyGroup,other : Optional[list[Any]] = None,module_metadata : Optional[ModuleMetadata] = None) -> None:
        self.plugins = plugins
        self.dependencies = dependencies
        self.module_metadata = module_metadata
        self.other = other

        if module_metadata is not None :
            self.plugins.provide_metadata(module_metadata)
            self.dependencies.provide_metadata(module_metadata)

    def provide_metadata(self, metadata: GradleMetadata) -> None:
        self.plugins.provide_metadata(metadata)
        self.dependencies.provide_metadata(metadata)
    

    def __str__(self) -> str:
        representation = f"{self.plugins}\n{self.dependencies}"
        if self.other is not None:
            representation += f"{self.other}"
            
        return representation
    
    def generate_to_file(self, filepath: Path) -> None:
        file_directory = join_path(filepath,"build.gradle.kts")

        with open(file_directory,"w") as file :
            file.write(str(self.plugins))
            file.write(str(self.dependencies))
            if self.other is not None:
                file.write(str(self.other))
  