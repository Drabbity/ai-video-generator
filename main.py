import logging

from logger.logConfig import setup_logging
from dotenv import dotenv_values

from handlers import *
from Context.videoContext import VideoContext

config = dotenv_values(".env")

def main():
  setup_logging("log/VideoGenerator.log", logging.DEBUG)

  pipeline = LoadVideoHandler("assets/BackGroundFootage.mp4")
  (pipeline.set_next(CutVideoHandler(10))
          .set_next(CropVideoHandler(resolution_x=594, resolution_y=1056))
          .set_next(VideoRenderHandler("assets/render.mp4", preset="ultrafast"))
          .set_next(CloseContextHandler()))

  ctx = pipeline.handle(VideoContext())
  print(ctx)

if __name__ == "__main__":
  main()