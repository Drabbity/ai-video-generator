from abc import abstractmethod

from Context.videoContext import VideoContext
from .handler import Handler


class AbstractHandler(Handler):
  _next_handler : Handler = None

  def set_next(self, handler: Handler) -> Handler:
    self._next_handler = handler
    return self._next_handler

  @abstractmethod
  def handle(self, video_context: VideoContext) -> VideoContext:
    if self._next_handler:
      return self._next_handler.handle(video_context)

    return video_context