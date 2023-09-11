import eng_to_ipa as ipa

from english.celery import app


@app.task
def get_transcription_task(word: str) -> str:
    """Returns transcription for given word."""
    transcription = "-"
    if ipa.isin_cmu(word):
        if len(word.split()) == 1:
            transcription = " | ".join(ipa.ipa_list(word)[0])
        else:
            transcription = ipa.convert(word)
    return transcription
