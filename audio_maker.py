# from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import tempfile

manager = ModelManager()
MODEL_NAMES = manager.list_tts_models()

# filter out multi-speaker models and slow wavegrad vocoders
# filters = ["vctk", "your_tts", "ek1"]
# MODEL_NAMES = [model_name for model_name in MODEL_NAMES if not any(f in model_name for f in filters)]


def tell_jokes(joke_list, model_name="en/ljspeech/glow-tts", speaker_idx="", delete_outfile=True):
    '''
    Input : list of sentences
    Output : list of tempfiles of speeches
    '''
    global wavs, synthesizer

    speeches = []
    wavs = []

    for joke in joke_list:
        # model info
        model_path, config_path, model_item = manager.download_model(
            f"tts_models/{model_name}")

        vocoder_name = model_item['default_vocoder']
        vocoder_path, vocoder_config_path, _ = manager.download_model(
            vocoder_name)

        print(f'joke : {joke}\nmodel_name : {model_name}')
        print(
            f'model_name : \n{model_name}\n model_path : \n{model_path}\nconfig_path : \n{config_path}\nmodel_item : {model_item}')

        synthesizer = Synthesizer(
            model_path, config_path, None, None, vocoder_path, vocoder_config_path,
        )

        wav = synthesizer.tts(joke, speaker_idx)
        wavs.append(wav)

        if delete_outfile == False:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=delete_outfile) as fp:
                synthesizer.save_wav(wavs, fp)
                speeches.append(fp.name)

    if delete_outfile == False:
        return speeches
    else:
        return wavs, synthesizer


if __name__ == '__main__':
    wavs = 0
    jokes = [
        "If a serial killer is chasing you......	you're both running for your life."]
    speeches = tell_jokes(jokes, delete_outfile=False)
    print(f'file saved at : {speeches}')
