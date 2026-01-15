from typing import Optional
from moviepy import VideoFileClip


class VideoContext:
  def __init__(self) -> None:
    self.clip : Optional[VideoFileClip] = None
    self.story = None
    self.audio = None
    self.transcript = None