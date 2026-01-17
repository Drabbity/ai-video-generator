import logging
from random import uniform
from typing import override, Optional

from moviepy import VideoFileClip

from Context.videoContext import VideoContext
from handlers import AbstractHandler


class CutVideoHandler(AbstractHandler):
  def __init__(self, clip_duration : float, clip_start : Optional[float] = None) -> None:
    self.clip_start = clip_start
    self.clip_duration = clip_duration

  @override
  def handle(self, video_context : VideoContext) -> VideoContext:
    try:
      if self.clip_start is None:
        self.clip_start = self.__calculate_random_clip_start(video_context.clip, self.clip_duration)

      video_context.clip = video_context.clip.subclipped(start_time=self.clip_start, end_time=self.clip_start + self.clip_duration)
      logging.info("video cut")

      return super().handle(video_context)
    except Exception as error:
      logging.exception(f"Couldn't cut video '{video_context.clip.filename}': {error}")
      raise

  @staticmethod
  def __calculate_random_clip_start(video_clip : VideoFileClip, duration : float) -> float:
    rnd_clip_start = uniform(0, video_clip.duration - duration)
    if rnd_clip_start < 0:
      raise Exception("Duration of the video must be greater than requested duration")
    return rnd_clip_start