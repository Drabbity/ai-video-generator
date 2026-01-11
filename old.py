from pathlib import Path
from random import uniform
from tkinter import CENTER
from moviepy.editor import *
from moviepy.video.fx.all import crop
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
import PIL

config = dotenv_values(".env")

def main():
  gptClient = OpenAI(
    config["OPENAI_KEY"])

  story = ReadStory()
  audio = GenerateAudio(story)
  video = LoadClip(audio.duration)

  video.audio = (CompositeAudioClip([audio]))

  MainVideo(gptClient, video)
  ShortVideo(gptClient, video)


def MainVideo(gptClient: OpenAI, video: VideoClip):
  clips = [video]

  transcript = GetTranscript(gptClient, "segment")

  clips = CreateSubtitles(transcript, clips)

  mainVideo = CompositeVideoClip(clips)
  mainVideo.write_videofile("Youtube/fullVideo.mp4")


def ShortVideo(gptClient: OpenAI, video: VideoClip):
  (w, h) = video.size

  newWidth = (w * 9 / 16) / 2
  x1 = (w - newWidth) // 2
  x2 = (w + newWidth) // 2

  video = crop(video, x1=x1, x2=x2)

  clips = [video]

  transcript = GetTranscript(gptClient, "word")
  clips = CreateSingleSubtitles(transcript, clips)

  shortVideo = CompositeVideoClip(clips)
  shortVideo.write_videofile("Youtube/short.mp4")


def ReadStory() -> str:
  storyFile = open('StoryText.txt', 'r')

  Lines = storyFile.readlines()
  storyText = ''.join(Lines)

  storyText.replace('“', '"')
  storyText.replace('”', '"')

  return storyText


def GenerateAudio(storyText) -> AudioFileClip:
  client = OpenAI(config["OPENAI_KEY"])

  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
      model="tts-1-hd",
      voice="onyx",
      input=storyText
  )

  response.stream_to_file(speech_file_path)

  audio = AudioFileClip("speech.mp3")
  return audio


def LoadClip(duration: float) -> VideoFileClip:
  footage = VideoFileClip("Media\BackGroundFootage.mp4", audio=False)
  clipStart = uniform(1, footage.duration - duration - 1)
  clipEnd = clipStart + duration

  return footage.subclip(clipStart, clipEnd)


def GetTranscript(client: OpenAI, form):
  audio_file = open("speech.mp3", "rb")

  transcript = client.audio.transcriptions.create(
      file=audio_file,
      model="whisper-1",
      response_format="verbose_json",
      timestamp_granularities=[form]
  )

  return transcript


def CreateSubtitles(transcript, clips):
  for segment in transcript.segments:
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]

    text = SplitUpText(text)

    textClip = TextClip(txt=text, color='white', font="Kaapeli-Heavy",
                        stroke_color='black', stroke_width=5,
                        fontsize=100).set_position((CENTER, CENTER))
    textClip = textClip.set_start(start)
    textClip = textClip.set_duration(end - start)
    clips.append(textClip)

  return clips


def CreateSingleSubtitles(transcript, clips):
  subs = []

  for word in transcript.words:

    if not subs:
      lastText, lastStart, lastEnd = "", -1, -1
    else:
      lastText, lastStart, lastEnd = subs[-1]

    start = word["start"]
    end = word["end"]
    text = word["word"]

    if start - lastStart < 0.1:
      subs.pop()
      text = lastText + '\n' + text
      start = lastStart

    subs.append((text, start, end))

  for sub in subs:
    text, start, end = sub

    textClip = TextClip(txt=text, color='white', font="Kaapeli-Heavy",
                        stroke_color='black', stroke_width=5,
                        fontsize=100).set_position((CENTER, CENTER))
    textClip = textClip.set_start(start)
    textClip = textClip.set_duration(end - start)

    clips.append(textClip)
  return clips


def SplitUpText(text: str):
  if len(text) < 25:
    return text

  middle = int(len(text) / 2)

  textList = list(text)

  for i in range(0, middle):
    if textList[middle + i] == ' ':
      textList[middle + i] = '\n'
      break
    if textList[middle - i] == ' ':
      textList[middle - i] = '\n'
      break

  return ''.join(textList)


if __name__ == "__main__":
  main()
