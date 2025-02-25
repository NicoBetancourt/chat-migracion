from openai import OpenAI


def whisper_transcription(audio_file):
    """
    Transcribe an audio file using the OpenAI API.

    :param audio_file: Binary file of
    :return: Transcription of the audio file

    """
    client = OpenAI()

    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    return transcription.text
