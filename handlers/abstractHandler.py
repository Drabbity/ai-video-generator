from abc import ABC, abstractmethod
from typing import Any

from .handler import Handler


class AbstractHandler(Handler):
  _next_handler : Handler = None

  def set_next(self, handler: Handler) -> Handler:
    self._next_handler = handler
    return self._next_handler

  @abstractmethod
  def handle(self, request: Any):
    if self._next_handler:
      return self._next_handler.handle(request)

    return None