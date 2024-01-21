from vosk_tts import Model, Synth

model = Model(model_name="vosk-model-tts-ru-0.5-multi")
synth = Synth(model)

synth.synth("Привет мир!", "out.wav", speaker_id=4)