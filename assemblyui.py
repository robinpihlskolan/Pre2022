import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "3358a388a59e480c920325eb02482b05"

# URL of the file to transcribe
#FILE_URL = "https://assembly.ai/wildfires.mp3"

# You can also transcribe a local file by passing in a file path
FILE_URL = './Matematik – Ämnesplan Gy2025_ Skolverkets Utdrag.wav'

#transcriber = aai.Transcriber()
#transcript = transcriber.transcribe(FILE_URL)
#

#if transcript.status == aai.TranscriptStatus.error:
#    print(transcript.error)
#else:
#    print(transcript.text)

# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "3358a388a59e480c920325eb02482b05"

# URL of the file to transcribe
#FILE_URL = "https://assembly.ai/wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

config = aai.TranscriptionConfig(speaker_labels=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(
  FILE_URL,
  config=config
)

for utterance in transcript.utterances:
  print(f"Speaker {utterance.speaker}: {utterance.text}")
