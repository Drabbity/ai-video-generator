import logging
import os

from moviepy import VideoFileClip
from typing_extensions import override

from handlers import AbstractHandler
from Context.videoContext import VideoContext


class VideoRenderHandler(AbstractHandler):
  def __init__(self, video_write_path : str, fps : float = 30, threads : int = 8, codec : str = "libx264", preset : str = "medium") -> None:
    self.video_write_path = video_write_path
    self.fps = fps
    self.threads = threads
    self.codec = codec
    self.preset = preset

  @override
  def handle(self, video_context : VideoContext) -> VideoContext:
    try:
      save_path = os.path.dirname(self.video_write_path)
      if save_path:
        os.makedirs(save_path, exist_ok=True)

      video_context.clip.write_videofile(filename=self.video_write_path, threads=self.threads, fps=self.fps, codec=self.codec, preset=self.preset)
      logging.info(f"Video written to file. Path: {self.video_write_path}")

      return super().handle(video_context)
    except Exception as error:
      logging.exception(f"Couldn't write video '{self.video_write_path}: {error}'")
      raise
