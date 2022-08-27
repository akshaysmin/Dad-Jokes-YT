# from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
# import tempfile

manager = ModelManager()
MODEL_NAMES = manager.list_tts_models()

# filter out multi-speaker models and slow wavegrad vocoders
# filters = ["vctk", "your_tts", "ek1"]
# MODEL_NAMES = [model_name for model_name in MODEL_NAMES if not any(f in model_name for f in filters)]

joke = "If a serial killer is chasing you......	you're both running for your life."

speaker_idx = ""

# model info
model_name = "en/ljspeech/glow-tts"
# model_path = "C:\\Users\\user\\AppData\\Local\\tts\\tts_models--en--ljspeech--glow-tts\\model_file.pth"
# config_path = "C:\\Users\\user\\AppData\\Local\\tts\\tts_models--en--ljspeech--glow-tts\\config.json"
# model_item = manager.models_dict['tts_models']['en']['ljspeech']['glow-tts']
model_path, config_path, model_item = manager.download_model(
    f"tts_models/{model_name}")

vocoder_name = model_item['default_vocoder']
vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

print(f'joke : {joke}\nmodel_name : {model_name}')
print(
    f'model_name : \n{model_name}\n model_path : \n{model_path}\nconfig_path : \n{config_path}\nmodel_item : {model_item}')

synthesizer = Synthesizer(
    model_path, config_path, None, None, vocoder_path, vocoder_config_path,
)

wavs = synthesizer.tts(joke)

with open('test.mp4', 'wb') as fp:
    synthesizer.save_wav(wavs, fp)

# just a line
