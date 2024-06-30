from google.cloud import speech
import keys

client = speech.SpeechClient.from_service_account_file(keys.GOOGLE_GLOUD_JSON)

def audio_transcription(file_name, language):
  with open(f'{file_name}', 'rb') as f:
    mp3_data = f.read()

  audio_file = speech.RecognitionAudio(content = mp3_data)

  config = speech.RecognitionConfig(
      sample_rate_hertz=44100,
      enable_automatic_punctuation=True,
      language_code=language
  )

  response = client.recognize(
      config=config,
      audio=audio_file
  )

  for result in response.results:
    transcript = result.alternatives[0].transcript
    print(f'TRANSCRIPT {transcript}')
    return transcript