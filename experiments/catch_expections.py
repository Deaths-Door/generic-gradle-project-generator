from typing import Self
from src.core import FileConvertible, FileConvertibleError, catch_exception_in_all_methods;
from src.gradle.properties import GradleProperties
from src.metadata import GradleMetadata


class WrapError(Exception):
    def __init__(self, m):
        super().__init__(m)
        self.message = m

    def __str__(self):
        return self.message
    

class FuckError(Exception):pass

class TestFailed(Exception):
    def __str__(self) :
        
        return self.args.__str__() + self.__traceback__.__str__()


@catch_exception_in_all_methods(TestFailed)
class WrapErrorTest(FileConvertible):       
    def generate_to_file(self, filepath: str) -> None:
        raise FuckError("Test error")      

    def from_file(cls, filepath: str) -> 'GradleProperties':
        pass

    def provide_metadata(self, metadata: 'GradleMetadata') -> None:
        pass

    
if __name__ == "__main__" :
    try :
        WrapErrorTest().generate_to_file("test.txt")
    except TestFailed as e :
        print("succes with error : ", e.__cause__)
        import traceback
        print(traceback.format_exc())
        pass
   # except Exception as e :
    #    print(type(e))
    #except FileConvertibleError as e :
   #     print("succes with error : ", e)
   # except WrapError as e :
   #     print("succes with error : ", e)
   # except TypeError as e :
   #     print("succes with error : ", e)   
   # except ValueError as e :
   #     print("failed with error : ", e)
