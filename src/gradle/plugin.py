

from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Optional, Self, TypeAlias, TypeVar

from src.core import ProvideMetadata

from ..metadata import GradleMetadata
from ..utils import CodeBlock

class PluginType(Enum) :
    """
    Enum class representing the different types of plugins in Gradle build scripts.

    This class defines the different types of plugins that can be applied in Gradle build scripts. Each member
    represents a specific type:

    * `Id`: Represents an ID plugin, typically used for applying plugins from repositories.
    * `Kotlin`: Represents a Kotlin plugin, used for projects that are included by default in the Kotlin language.
    * `Alias`: Represents an alias plugin, used to create an alias for another plugin (Version Catalog).
    """
    Id = "id"
    Kotlin = "kotlin"
    Alias = "alias"


ReplaceAlias :TypeAlias = Optional[Callable[[Self,GradleMetadata,Any],None]]

class Plugin(ProvideMetadata) :
    """
    Class representing a Gradle plugin with its configuration options.

    This class provides a structured way to define and manage Gradle plugins. It stores the following information:

    * `type`: The type of the plugin (an instance of `PluginType`).
    * `identifier`: The identifier of the plugin (e.g., plugin ID, Kotlin DSL syntax for special plugins).
    * `version` (Optional): The version of the plugin, if applicable.
    * `apply` (Optional): Whether to automatically apply the plugin during build execution (defaults to `True`).

    The class also provides several convenience methods to create `Plugin` objects with specific types:

    * `id(identifier, version=None, apply=None)`: Creates a plugin of type `PluginType.Id`.
    * `kotlin(identifier, version=None, apply=None)`: Creates a plugin of type `PluginType.Kotlin`.
    * `alias(identifier, version=None, apply=None)`: Creates a plugin of type `PluginType.Alias`.
    """

    def __init__(self,type : PluginType ,identifier : str,version : Optional[str] = None,apply : Optional[bool] = None,replace : ReplaceAlias = None) -> None: 
        self.type = type
        self.identifier = identifier
        self.version = version
        self.apply = apply
        self.replace = replace
        
    def __str__(self) -> str :
        message = f"{self.type.value}({self.identifier if self.type is PluginType.Alias else f"\"{self.identifier}\""})"

        if self.version is not None :
            message += f" version \"{self.version}\""

        if self.apply is not None :
            message += f" apply {self.apply}"

        return message
    
    def provide_metadata(self, metadata: 'GradleMetadata') -> None:
        property = metadata.get_property(f"plugins/{self.identifier}")
        if property is not None and self.replace is not None :
            self.replace(self,metadata,property)


"""
Creates a Plugin object of type `PluginType.Id`.

This method is a convenience function to create a `Plugin` object specifically for applying plugins by ID.

Args:
    identifier (str): The ID of the plugin to apply.
    version (Optional[str], optional): The version of the plugin (defaults to None).
    apply (Optional[bool], optional): Whether to automatically apply the plugin during build execution (defaults to True).

Returns:
    Plugin: A new `Plugin` object with the specified type and configuration.

Example usage:
    >>> android_plugin = Plugin.id('com.android.application', '7.2.0')
    >>> print(android_plugin)
    id('com.android.application:7.2.0')
"""
def id(identifier : str,version : Optional[str] = None,apply : Optional[bool] = None,replace : ReplaceAlias = None) -> Self :
    return Plugin(PluginType.Id,identifier,version,apply,replace)

"""
Creates a Plugin object of type `PluginType.Kotlin`.

This method is a convenience function to create a `Plugin` object specifically for applying Kotlin plugins using the Kotlin DSL syntax.

Args:
    identifier (str): The identifier of the Kotlin plugin (e.g., 'kapt').
    version (Optional[str], optional): The version of the plugin (defaults to None).
    apply (Optional[bool], optional): Whether to automatically apply the plugin during build execution (defaults to True).

Returns:
    Plugin: A new `Plugin` object with the specified type and configuration.

Example usage:
    >>> kapt_plugin = Plugin.kotlin('kapt', '1.7.20')
    >>> print(kapt_plugin)
    kotlin("kapt") version "1.7.20"
"""
def kotlin(identifier : str,version : Optional[str] = None,apply : Optional[bool] = None,replace : ReplaceAlias = None) -> Self :
    return Plugin(PluginType.Kotlin,identifier,version,apply,replace)

"""
Creates a Plugin object of type `PluginType.Alias`.

This method is a convenience function to create a `Plugin` object for defining an alias for another plugin.

Args:
    identifier (str): The identifier of the alias to create.
    version (Optional[str], optional): The version of the plugin the alias refers to (defaults to None).
    apply (Optional[bool], optional): Whether to automatically apply the alias during build execution (defaults to True).

Returns:
    Plugin: A new `Plugin` object with the specified type and configuration.

Example usage:
    >>> my_alias = Plugin.alias('libs.datastore')
    >>> print(my_alias)
    alias(libs.datastore)
"""
def alias(identifier : str,version : Optional[str] = None,apply : Optional[bool] = None,replace : ReplaceAlias = None) -> Self :
    assert "libs" in identifier
    return Plugin(PluginType.Alias,identifier,version,apply,replace)


T = TypeVar("T")
class PluginWithCodeBlock(Plugin,CodeBlock[T]):
    """
    **PluginWithCodeBlock**

    This class inherits from the base `Plugin` class and extends its functionality by allowing embedded code blocks. These code blocks are specifically designed to resemble configuration blocks.

    **Attributes:**

    * Inherits all attributes from the base `Plugin` class.

    **Methods:**

    * Inherits all methods from the base `Plugin` class.

    **Code Blocks:**

    The `PluginWithCodeBlock` class introduces the ability to define code blocks within the plugin definition. 

    For example :

    ```kotlin
        plugins {
            alias(libs.plugins.kotlinMultiplatform)
        }
    
        // Has this code block
        kotlin {
            sourceSets {
                // ...
            }
        }
    ```    
    """
    def __init__(self,plugin : Plugin) :
        self.plugin = plugin
        super().__init__(plugin.type,plugin.identifier,plugin.version,plugin.apply,plugin.replace)    
    pass

class PluginGroup(CodeBlock[list[Plugin|PluginWithCodeBlock[Any]]],GradleMetadata,ProvideMetadata):
    """
    Class representing a group of Gradle plugins.

    This class inherits from `CodeBlock` and provides a structured way to represent and manage a collection of `Plugin` objects in Gradle build scripts.
    """
    def __init__(self,plugins : list[Plugin| PluginWithCodeBlock[Any]],parent : Optional['GradleMetadata'] = None) -> None :
        CodeBlock.__init__(self,name="plugins",arguments=None,code=plugins)
        GradleMetadata.__init__(self,parent)

    def from_singular(self,plugin : Plugin | PluginWithCodeBlock[Any],parent : Optional['GradleMetadata'] = None) -> Self :
        return PluginGroup([plugin],parent)

    def get_identifier(self) -> str:
        return "plugins"
    
    def __str__(self) -> str :
        base_plugins = []
        code_block : str = ""
        for plugin in self.code :
            if not isinstance(plugin,PluginWithCodeBlock) :
                base_plugins.append(plugin)
            else :
                code_block += str(plugin.code)
        _group = CodeBlock(self.name,base_plugins,self.arguments)
        return f"{_group}\n{code_block}"
    
    def provide_metadata(self, metadata: 'GradleMetadata') -> None:
        for plugin in self.code :
            plugin.provide_metadata(metadata)
        pass