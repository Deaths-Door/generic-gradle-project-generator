from typing import Any
from src.core import ProvideMetadata
from src.metadata import GradleMetadata
from src.utils import CodeBlock

class Repository(ProvideMetadata) :
    pass

class MavenCentral(Repository):
    def __str__(self) -> str:
        return f"mavenCentral()"

class Google(Repository):
    def __str__(self) -> str:
        return f"google()"
    
class MavenLocal(Repository):
    def __str__(self) -> str:
        return f"mavenLocal()"
    
class MavenUrl(Repository):
    url : str
    def __init__(self,url : str) -> None:
        super().__init__()
        self.url = url

    def __str__(self) -> str:
        return f"maven(\"{self.url}\")"
    
    def provide_metadata(self, metadata: 'GradleMetadata'):
        pass


class Repositories(CodeBlock[list[Repository]],ProvideMetadata): 
    def __init__(self,repositories : list[Repository]) -> None:
        CodeBlock.__init__(self,name="repositories",arguments=None,code=repositories)
    
    def provide_metadata(self, metadata: 'GradleMetadata'):
        for repo in self.code:
            repo.provide_metadata(metadata)
        pass