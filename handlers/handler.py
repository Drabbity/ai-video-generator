from abc import abstractmethod, ABC
from typing import Optional, Any


class Handler(ABC):

  @abstractmethod
  def set_next(self, handler : Handler) -> Handler:
    pass

  @abstractmethod
  def handle(self, request : Any):
    pass