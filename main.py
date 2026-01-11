from dotenv import dotenv_values
from moviepy import VideoFileClip

config = dotenv_values(".env")

def main():
  print(config["OPENAI_KEY"])

  video = VideoFileClip("assets/BackGroundFootage.mp4")

  print("Duration:", video.duration)
  print("FPS:", video.fps)
  print("Size:", video.size)

  video.close()


if __name__ == "__main__":
  main()