import logging
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment
from backend.account_info import AccountInfo

class TextSpeechServices:
    def __init__(self, account_info):
        self.account_info = account_info

    def init_text_to_speech_service(self):
        # This is the function to initialise the TTS service.
        try:
            iam_token = self.account_info.get_iam_token()
            credentials = self.account_info.get_service_credentials(iam_token, "Text to Speech")
            if credentials:
                authenticator = IAMAuthenticator(credentials['apikey'])
                text_to_speech = TextToSpeechV1(authenticator=authenticator)
                text_to_speech.set_service_url(credentials['url'])
                return text_to_speech
            else:
                raise Exception("Failed to retrieve or create service credentials.")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def synthesize_text(self, text, text_to_speech, voice='en-US_AllisonV3Voice', accept='audio/wav', pitch='0', speed='0'):
        # This is the inference function for TTS.
        try:
            ssml_text = f"<prosody pitch='{pitch}%' rate='{speed}%'>{text}</prosody>"
            response = text_to_speech.synthesize(
                ssml_text,
                voice=voice,
                accept=accept
            ).get_result().content

            # Save the synthesized audio to a file
            audio_path = "temp/output.wav"
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response)

            return audio_path
        except Exception as e:
            print(f"Error: {e}")
            return None

    def init_speech_to_text_service(self):
        # This is the function to initialise the STT service.
        try:
            iam_token = self.account_info.get_iam_token()
            credentials = self.account_info.get_service_credentials(iam_token, "Speech to Text")
            if credentials:
                authenticator = IAMAuthenticator(credentials['apikey'])
                speech_to_text = SpeechToTextV1(authenticator=authenticator)
                speech_to_text.set_service_url(credentials['url'])
                return speech_to_text
            else:
                raise Exception("Failed to retrieve or create service credentials.")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def transcribe_audio(self, file_path, speech_to_text):
        # This is the inference function for STT.
        if speech_to_text is None:
            print("Error: Speech to Text service is not initialised.")
            return None

        try:
            # Check if the file is already in WAV format
            if file_path.endswith('.wav'):
                # Transcribe audio using IBM Watson
                with open(file_path, 'rb') as audio_file:
                    response = speech_to_text.recognize(
                        audio=audio_file,
                        content_type='audio/wav'
                    ).get_result()

                # Extract the transcribed text
                transcriptions = response['results']
                transcription_text = " ".join([result['alternatives'][0]['transcript'] for result in transcriptions])

                return transcription_text
            else:
                try:
                    audio = AudioSegment.from_file(file_path)
                    wav_path = file_path.rsplit('.', 1)[0] + '.wav'
                    audio.export(wav_path, format='wav')
                    file_path = wav_path
                except FileNotFoundError as e:
                    print(f"Error: {e}")
                    return None

                # Transcribe audio using IBM Watson
                with open(file_path, 'rb') as audio_file:
                    response = speech_to_text.recognize(
                        audio=audio_file,
                        content_type='audio/wav'
                    ).get_result()

                # Extract the transcribed text
                transcriptions = response['results']
                transcription_text = " ".join([result['alternatives'][0]['transcript'] for result in transcriptions])

                return transcription_text
        except Exception as e:
            print(f"Error: {e}")
            return None

    def list_voices(self, text_to_speech):
        try:
            voices = text_to_speech.list_voices().get_result()
            return voices['voices']
        except Exception as e:
            print(f"Error: {e}")
            return []