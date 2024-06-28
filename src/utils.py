
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")

class CodeBlock(Generic[T]) :
    """
    This class, `CodeBlock`, represents a structured code block similar to Kotlin code blocks with names, optional arguments, and inner code content.

    **Attributes:**

    * `name` (str): The name of the code block.
    * `code` (T): The actual code content within the block. It can be any valid Python object (e.g., string, list, nested code blocks).
    * `arguments` (Optional[list[str]]): An optional list of arguments (if any) for the code block. Defaults to `None`.
    **Example Usage:**

    ```python
    code_block1 = CodeBlock("print_message", "print('Hello, world!')")
    code_block2 = CodeBlock("sum_numbers", "def add(x, y): return x + y", arguments=["x", "y"])

    print(code_block1)  # Output: print_message{    print('Hello, world!')
    print(code_block2)  # Output: sum_numbers(x, y){    def add(x, y): return x + y }
    """
    def __init__(self,name : str,code:T,arguments : Optional[list[str]] = None) -> None :
        self.name = name
        self.arguments = arguments
        self.code = code

    def __str__(self) -> str:
        string = f"{self.name}"
        if self.arguments is not None and self.arguments: 
            string += ','.join(self.arguments)
        string += " {\n\t" 
        if isinstance(self.code,list) :
            string += "\n\t".join([str(v) for v in self.code]) + "\n}"
        else :
            string += str(self.code)
        return string
