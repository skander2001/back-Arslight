import base64
import os
from io import BytesIO
from django.http import JsonResponse
from gtts import gTTS
from pydub import AudioSegment
from rest_framework.response import Response
from rest_framework.views import APIView


def convert_text_to_speech(text, language, save_path=None):
    """
    Converts text to speech and saves the audio file if save_path is provided.
    Returns the base64 encoded audio data if save_path is None.
    """
    lang_mapping = {
        'en': 'en',
        'ar': 'ar',
        'fr': 'fr',
        # Add more languages as needed
    }

    gtts_lang = lang_mapping.get(language, 'en')
    tts = gTTS(text=text, lang=gtts_lang, slow=False)

    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")

    if save_path:
        audio_segment.export(save_path, format="mp3")
    else:
        return base64.b64encode(audio_segment.raw_data).decode("utf-8")


class TextToSpeechAPI(APIView):

    def post(self, request):
        """
        API endpoint to convert text to speech and return base64 encoded audio data or save the audio file.
        """
        text = request.data.get('text')
        language = request.data.get('language')
        save_path = "/Users/skander/Desktop/pi/front/src/assets/sounds/mp3/audio.mp3"

        if not text or not language:
            return Response({'error': 'Missing required data (text or language)'}, status=400)

        try:

            convert_text_to_speech(text, language, save_path)
            return Response({'message': 'Audio file saved successfully'}, status=200)


        except Exception as e:
            return Response({'error': str(e)}, status=500)
