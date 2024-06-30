import keys

from speechkit import configure_credentials, creds
from speechkit import model_repository

configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=keys.YANDEX
    )
)

def text_to_speech_rus(rus_phrase):

    model = model_repository.synthesis_model()

    model.voice = 'alena'

    result = model.synthesize(rus_phrase, raw_format=False)  # returns audio as pydub.AudioSegment
    result.export('./rus_audio.wav', format='wav')

def text_to_speech_uzb(uzb_phrase): 

        model = model_repository.synthesis_model()

        model.voice = 'nigora'

        result = model.synthesize(uzb_phrase, raw_format=False)  # returns audio as pydub.AudioSegment
        result.export('./uzb_audio.wav', format='wav')