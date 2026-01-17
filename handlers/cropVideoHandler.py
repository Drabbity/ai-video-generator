import logging
from asyncio.windows_events import NULL
from typing import override

from PIL.ImageOps import scale
from moviepy import VideoFileClip
from moviepy.video.fx import Crop

from Context.videoContext import VideoContext
from handlers import AbstractHandler


class CropVideoHandler(AbstractHandler):
  def __init__(self, resolution_x : int, resolution_y : int):
    self.resolution_x = resolution_x
    self.resolution_y = resolution_y

  @override
  def handle(self, video_context: VideoContext) -> VideoContext:
    try:
      size = video_context.clip.size

      crop = Crop(x_center=size[0]//2, y_center=size[1]//2, width=self.resolution_x, height=self.resolution_y)

      video_context.clip = crop.apply(video_context.clip)
      logging.info(f"Cropped video '{video_context.clip.filename}' at {video_context.clip.size[0]} x {video_context.clip.size[1]}")

      return super().handle(video_context)
    except Exception as error:
      logging.exception(f"Couldn't crop video '{video_context.clip.filename}': {error}")
      raise
