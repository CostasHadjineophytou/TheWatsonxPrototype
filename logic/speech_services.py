from backend.text_speech_services import TextSpeechServices
from backend.account_info import AccountInfo

account_info = AccountInfo()
text_speech_services = TextSpeechServices(account_info)

def synthesize_text(text, voice='en-US_AllisonV3Voice', accept='audio/wav', pitch='0', speed='0'):
    text_to_speech = text_speech_services.init_text_to_speech_service()
    if text_to_speech is None:
        print("Error: Text to Speech service initialisation failed.")
        return None
    return text_speech_services.synthesize_text(text, text_to_speech, voice, accept, pitch, speed)

def transcribe_audio(file_path):
    speech_to_text = text_speech_services.init_speech_to_text_service()
    if speech_to_text is None:
        print("Error: Speech to Text service initialisation failed.")
        return None
    return text_speech_services.transcribe_audio(file_path, speech_to_text)

def get_available_voices():
    text_to_speech = text_speech_services.init_text_to_speech_service()
    if text_to_speech is None:
        print("Error: Text to Speech service initialisation failed.")
        return []
    voices = text_speech_services.list_voices(text_to_speech)
    return [voice['name'] for voice in voices]