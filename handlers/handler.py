from abc import abstractmethod, ABC

from Context.videoContext import VideoContext


class Handler(ABC):

  @abstractmethod
  def set_next(self, handler : Handler) -> Handler:
    pass

  @abstractmethod
  def handle(self, video_context : VideoContext) -> VideoContext:
    pass