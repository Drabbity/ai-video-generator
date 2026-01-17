import logging

from moviepy import VideoFileClip
from typing_extensions import override

from handlers import AbstractHandler
from Context.videoContext import VideoContext


class CloseContextHandler(AbstractHandler):

  @override
  def handle(self, video_context : VideoContext) -> VideoContext:
    if video_context.clip:
      video_context.clip.close()

      logging.info(f"Closing clip: {video_context.clip.filename}")

    return super().handle(video_context)
