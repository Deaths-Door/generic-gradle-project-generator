from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class GradleMetadata(ABC):
    """
    Abstract base class representing metadata for a Gradle project.

    This class provides utilities to access specific metadata, allowing hierarchical 
    metadata structures where a class can have a parent metadata. It supports 
    retrieving metadata values using a key format that specifies the scope of 
    the metadata.

    Attributes:
        parent (Optional[GradleMetadata]): The parent metadata object, if any.
        metadata (Dict[str, Any]): Dictionary to store metadata key-value pairs.

    Methods:
        get_identifier() -> str:
            Abstract method that should return an identifier for the scope-specific 
            metadata. This identifier is used to access metadata values.

        get_property(key: str) -> Optional[Any]:
            Retrieves the value of the specified metadata key. The key can be 
            in the format "$identifier/$key" to search in the current and parent 
            metadata, or "$key" to search only in the current metadata.

        get_project_metadata() -> 'ProjectMetadata':
            Retrieves the top-level project metadata. If the current instance is 
            a ProjectMetadata, it returns itself. Otherwise, it recursively 
            retrieves the project metadata from the parent.
    """
    
    def __init__(self,parent: Optional['GradleMetadata'] = None):
        """
        Initializes a new instance of GradleMetadata.

        Args:
            parent (Optional[GradleMetadata]): The parent metadata object, if any.
        """
        self.parent = parent
        self.metadata: Dict[str, Any] = {}

    @abstractmethod
    def get_identifier(self) -> str:
        """
        Returns an identifier for the scope-specific metadata.

        This identifier is used to access metadata values in a hierarchical structure.

        Returns:
            str: The identifier for the scope-specific metadata.
        """
        pass

    def get_project_metadata(self) -> 'ProjectMetadata' :
        """
        Retrieves the top-level project metadata.

        If the current instance is a ProjectMetadata, it returns itself. Otherwise, 
        it recursively retrieves the project metadata from the parent.

        Returns:
            ProjectMetadata: The top-level project metadata.

        Raises:
            AttributeError: If there is no parent metadata to retrieve from.
        """
        if isinstance(self, ProjectMetadata):
            return self
        
        if self.parent:
            return self.parent.get_project_metadata()
        
        raise AttributeError("No parent metadata available to retrieve project metadata.")

    def get_property(self, key: str) -> Optional[Any]:
        """
        Retrieves the value of the specified metadata key.

        The key can be in the format "$identifier/$key" to search in the current 
        and parent metadata, or "$key" to search only in the current metadata.

        Args:
            key (str): The metadata key to search for.

        Returns:
            Optional[Any]: The value of the specified metadata key, or None if not found.
        """
        if '/' in key:
            identifier, actual_key = key.split('/', 1)
            if identifier == self.get_identifier():
                return self.metadata.get(actual_key)
            elif self.parent is not None:
                return self.parent.get_property(key)
        else:
            return self.metadata.get(key)
        
        return None
    
class ProjectMetadata(GradleMetadata):
    """
    Represents project metadata for a Gradle project.

    This class extends GradleMetadata and provides specific metadata fields
    such as base namespace, version, and group ID.

    Attributes:
        metadata (Dict[str, Any]): Dictionary to store metadata key-value pairs,
            including 'base_namespace', 'version', and 'group_id'.

    Methods:
        __init__(base_namespace: str, version: str, group_id: str):
            Initializes the object with the provided base namespace, version, and group ID.

        get_identifier() -> str:
            Returns the identifier for the scope-specific metadata ('project-metadata').

        get_project_metadata() -> 'ProjectMetadata':
            Returns itself, as this class represents the top-level project metadata.

    Example:
        >>> project_metadata = ProjectMetadata(
        ...     base_namespace="com.deathsdoor.gradle.generator",
        ...     version="1.0.0",
        ...     group_id="io.github.deathsdoor.gradle.generator"
        ... )
        >>> project_metadata.get_property('version')
        '1.0.0'
    """
    def __init__(self,name:str, base_namespace: str, version: str, group_id: str):
        """
        Initializes the object with the provided base namespace, version, and group id.

        Parameters:
            base_namespace (str): The base namespace for the project.
            version (str): The version of the project.
            group_id (str): The group id of the project.
        """
        self.metadata['name'] = base_namespace
        self.metadata['base_namespace'] = base_namespace
        self.metadata['version'] = version
        self.metadata['group_id'] = group_id

    def get_identifier(self) -> str:
        return "project-metadata"

    def get_project_metadata(self) -> 'ProjectMetadata' :
        return self
    
    def name(self) -> str:
        return self.metadata['name']
    

    def base_namespace(self) -> str:
        return self.metadata['base_namespace']
    
    def version(self) -> str:
        return self.metadata['version']
    
    def group_id(self) -> str:
        return self.metadata['group_id']

class ModuleMetadata(GradleMetadata) :
    def __init__(self,name : str,namespace : str, parent: GradleMetadata | None = None):
        self.metadata['name'] = name
        self.metadata['namespace'] = namespace
        super().__init__(parent)

    def namespace_from(project_metadata : ProjectMetadata,module_name : str) -> str:
        return f"{project_metadata.base_namespace()}.{module_name.replace("-",".").replace(":",".")}"
    
    def get_identifier(self) -> str:
        return self.name

    def name(self) -> str:
        return self.metadata['name']
    
    def namespace(self) -> str:
        return self.metadata['namespace']