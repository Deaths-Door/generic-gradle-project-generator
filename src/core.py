from abc import ABC, abstractmethod
from functools import wraps
from pathlib import Path
from typing import Generic, TypeVar

from .metadata import GradleMetadata

class ProvideMetadata(ABC):
  """
  This trait adds an abstract method for providing metadata.
  """

  @abstractmethod
  def provide_metadata(self, metadata: 'GradleMetadata'):
    """
    This method allows receiving metadata for the object from an external source.

    (Modify this method if needed based on your use case)
    """
    pass


def catch_exception_in_all_methods(exception : Exception) :
    """
    This function defines a decorator `catch` that wraps a given function.
    The `catch` decorator catches exceptions, prints an error message, and re-raises the exception with a custom error message.
    It then applies this decorator to all methods of a given class.
    This function is used to catch exceptions in all methods of a class and handle them uniformly.

    Returns:
        apply_decorator (function): A decorator that applies the `catch` decorator to all methods of a class.
    """
    #https://stackoverflow.com/a/24025175
    def catch(func):
        import functools;
        @functools.wraps(func)
        def wrapper(*a, **kw):
            try:
                return func(*a, **kw)
            except TypeError as e:
               raise e
            except Exception as e:
                # TODO: Display the message below instead of the base exception message
                raise exception(f"Error from {e.__class__.__name__}") from e
        return wrapper

    def apply_decorator(cls):
        for k, f in cls.__dict__.items():
            import inspect;
            if inspect.isfunction(f):
                setattr(cls, k, catch(f))
        return cls
   
    return apply_decorator

class FileConvertible(ProvideMetadata):
  """
  This trait inherits from ProvideMetadata and defines methods for converting objects to and from files.
  """

  @abstractmethod
  def generate_to_file(self, filepath: Path) -> None:
    """
    Generates data specific to the object and saves it to the specified file.

    It combines the functionality of generating content and saving the object state.

    Raises:
        Exception of type E if an error occurs during the file operations.
    """
    pass
  
 # from warnings import deprecated
    
  #TODO;@deprecated("just remove this method or keep it depending on whether it has a use in the future") 
  @classmethod
  def from_file(cls, filepath: Path) -> 'FileConvertible':
    """
    This method creates a new object of the implementing class by reading data from a file.
    """
    raise NotImplementedError