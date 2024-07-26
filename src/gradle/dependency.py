from collections import UserList
from enum import Enum
from typing import Any, Callable, Optional, Self, TypeAlias

from src.core import ProvideMetadata
from src.metadata import GradleMetadata

from ..utils import CodeBlock

class DependencyTypeBase :
    """
    Base class for dependency types in Gradle.

    This class serves as the base class for all dependency types in Gradle. It does not provide any specific functionality,
    but it is used to define the structure and behavior of derived classes.

    Attributes:
        None

    Methods:
        None
    """
    pass

class DependencyType(DependencyTypeBase,Enum) :
    """
    Enum class representing the common dependency types in Gradle.

    This class extends the `Enum` class and inherits from `DependencyTypeBase`. It defines the common dependency types
    used in Gradle, such as "api" and "implementation". These types are used to specify the scope of dependencies in a
    Gradle project.
    """
    Api = "api"
    Implementation = "implementation"

    def __str__(self) -> str :
        return str(self.value)

def api(dependency : str) -> 'Dependency' :
    return Dependency(DependencyType.Api,dependency)

def api(group_id: str, artifact_id: str, version: str,replace : 'ReplaceAlias' = None) -> 'Dependency' :
    return Dependency(DependencyType.Api,group_id,artifact_id,version,replace)

def implementation(dependency : str) -> 'Dependency' :
    return Dependency(DependencyType.Implementation,dependency)

def implementation(group_id: str, artifact_id: str, version: str,replace : 'ReplaceAlias' = None) -> 'Dependency' :
    return Dependency(DependencyType.Implementation,group_id,artifact_id,version,replace)

ReplaceAlias :TypeAlias = Optional[Callable[[Self,GradleMetadata,Any],None]]

class Dependency(ProvideMetadata):
    """
    Class representing a Gradle dependency.

    This class represents a Gradle dependency and provides methods to initialize and access its properties. It supports two ways of initialization:

    1. By providing the dependency type, group ID, artifact ID, and version. In this case, the dependency string is constructed by combining the group ID, artifact ID, and version.
    2. By providing the dependency type and the dependency string.
`
    Attributes:
        type (DependencyTypeBase): The type of the dependency.
        dependency (str): The dependency string.
    """
    def from_seperated(type : DependencyTypeBase ,group_id: str, artifact_id: str, version: str,replace : ReplaceAlias = None) -> Self:
        """
        Initializes a new instance of the class.

        Args:
            type (DependencyTypeBase): The type of the dependency.
            group_id (str): The group ID of the dependency.
            artifact_id (str): The artifact ID of the dependency.
            version (str): The version of the dependency.

        Returns:
            None

        Raises:
            None

        This method initializes a new instance of the class by calling the `__init__` method with the provided parameters. It combines the `group_id`, `artifact_id`, and `version` into a single string and passes it along with the `type` parameter to the `__init__` method.

        Example:
            >>> dependency = Dependency(DependencyType.Api, "com.example", "my-library", "1.0.0")
            >>> print(dependency)
            api("com.example:my-library:1.0.0")
        """
        return Dependency(type,f"{group_id}:{artifact_id}:{version}",replace)

    def __init__(self,type : DependencyTypeBase,dependency : str,replace : ReplaceAlias = None) -> None :
        """
        Initializes a new instance of the class.

        Args:
            type (DependencyTypeBase): The type of the dependency.
            dependency (str): The dependency string.

        Returns:
            None

        This method initializes a new instance of the class by setting the `dependency` attribute to the provided value.
        """
        self.type = type
        self.dependency = dependency
        self.replace = replace

    def __str__(self) -> str:
        return f"{self.type}({self.dependency if self.dependency.startswith("libs") else f"\"{self.dependency}\""})"
  
    def provide_metadata(self, metadata: 'GradleMetadata') -> None:
        property = metadata.get_property(f"dependencies/{self.dependency}")
        if property is not None and self.replace is not None :
            self.replace(self,metadata,property)
    

class DependencyGroup(CodeBlock[list[Dependency]],GradleMetadata,ProvideMetadata):
    """
    Class representing a group of Gradle dependencies.

    This class inherits from `CodeBlock` and provides a structured way to represent and manage a collection of `Dependency` objects in Gradle build scripts.
    """
    def __init__(self,dependencies : list[Dependency]) -> None :
        CodeBlock.__init__(self,name="dependencies",arguments=None,code=dependencies)

    def from_singluar(self,dependency : Dependency) -> None :
        return Self([dependency])

    def get_identifier(self) -> str:
        return self.name
    
    def provide_metadata(self, metadata: GradleMetadata) -> None:
        for dep in self.code:
            dep.provide_metadata(metadata)
        pass

