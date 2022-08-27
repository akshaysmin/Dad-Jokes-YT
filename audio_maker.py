from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

manager = ModelManager()
MODEL_NAMES = manager.list_tts_models()

# filter out multi-speaker models and slow wavegrad vocoders
# filters = ["vctk", "your_tts", "ek1"]
# MODEL_NAMES = [model_name for model_name in MODEL_NAMES if not any(f in model_name for f in filters)]

joke = "If a serial killer is chasing you......	you're both running for your life."
model_name = "en/ek1/tacotron2"

print(f'joke : {joke}\nmodel_name : {model_name}')
