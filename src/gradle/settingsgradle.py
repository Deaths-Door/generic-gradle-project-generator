

from pathlib import Path
from typing import Optional
from src.core import FileConvertible, ProvideMetadata, catch_exception_in_all_methods
from src.gradle.plugin import PluginGroup
from src.gradle.repository import Repositories
from src.metadata import GradleMetadata, ModuleMetadata
from src.utils import CodeBlock

class PluginManagement(CodeBlock[list[Repositories | PluginGroup]],ProvideMetadata) :
    repositories : Repositories 
    plugins : Optional[PluginGroup] = None
    def __init__(self,repositories : Repositories, plugins : Optional[PluginGroup] = None) -> None :
        self.repositories = repositories
        self.plugins = plugins

        _code = [repositories]
        if plugins is not None :
            _code.append(plugins)

        CodeBlock.__init__(self,"pluginManagement",None,_code)
        pass
    
    def provide_metadata(self, metadata: 'GradleMetadata'):
        self.repositories.provide_metadata(metadata)

        if self.plugins is not None :
            self.plugins.provide_metadata(metadata)

class DependencyResolutionManagement(CodeBlock[Repositories],ProvideMetadata) :
    repositories : Repositories

    def __init__(self,repositories : Repositories) -> None :
        self.repositories = repositories
        CodeBlock.__init__(self,"dependencyResolutionManagement",None,[repositories])
        pass

    def provide_metadata(self, metadata: 'GradleMetadata'):
        self.repositories.provide_metadata(metadata)
    pass

class SettingsGradleError(Exception):
    pass

@catch_exception_in_all_methods(SettingsGradleError)
class SettingsGradle(FileConvertible) :
    def __init__(self,plugins : PluginManagement,dependencyResolutionManagement : DependencyResolutionManagement,modules : list[str | ModuleMetadata],project_metadata : Optional[ModuleMetadata] = None) -> None :
        self.plugins = plugins
        self.dependencyResolutionManagement = dependencyResolutionManagement
        self.modules = [module if isinstance(module,str) else module.name for module in modules]
        self.project_metadata = project_metadata

    def provide_metadata(self, metadata: 'GradleMetadata'):
        self.plugins.provide_metadata(metadata)
        self.dependencyResolutionManagement.provide_metadata(metadata)

    def generate_to_file(self, filepath: Path) -> None :
        import os
        file_directory = os.path.join(filepath,"settings.gradle.kts")
        with open(file_directory,"w") as file :
            file.write(str(self.plugins))
            file.write(str(self.dependencyResolutionManagement))

            if self.project_metadata is not None :
                file.write(f"rootProject.name=\"{self.project_metadata.name()}\"\n")

            
            for module in self.modules :
                file.write(f'include("{module}")\n')

    