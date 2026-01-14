import logging

from logConfig import setup_logging
from dotenv import dotenv_values
from moviepy import VideoFileClip

from handlers import *
from videoContext import VideoContext

config = dotenv_values(".env")

def main():
  setup_logging("log/VideoGenerator.log", logging.DEBUG)

  v = LoadVideoHandler("assets/BackGroundFootage.mp4")
  ctx = v.handle(VideoContext())
  print(ctx)

if __name__ == "__main__":
  main()