import logging

from handlers.closeContextHandler import CloseContextHandler
from logger.logConfig import setup_logging
from dotenv import dotenv_values

from handlers import *
from Context.videoContext import VideoContext

config = dotenv_values(".env")

def main():
  setup_logging("log/VideoGenerator.log", logging.DEBUG)

  pipeline = LoadVideoHandler("assets/BackGroundFootage.mp4")
  pipeline.set_next(CloseContextHandler())

  ctx = pipeline.handle(VideoContext())
  print(ctx)

if __name__ == "__main__":
  main()