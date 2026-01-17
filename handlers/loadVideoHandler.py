import logging

from moviepy import VideoFileClip
from typing_extensions import override

from handlers import AbstractHandler
from Context.videoContext import VideoContext


class LoadVideoHandler(AbstractHandler):
  def __init__(self, video_path : str) -> None:
    self.video_path = video_path

  @override
  def handle(self, video_context : VideoContext) -> VideoContext:
    try:
      clip = VideoFileClip(self.video_path)
      video_context.clip = clip
      logging.info(f"Loaded video from {self.video_path}")

      return super().handle(video_context)
    except Exception:
      logging.exception(f"Couldn't load video from '{self.video_path}'")
      raise
