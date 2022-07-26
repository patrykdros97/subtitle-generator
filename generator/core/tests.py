import os
import traceback
import mimetypes
from datetime import datetime
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime,timedelta
from pydub.silence import split_on_silence

def time_calculator(audio: str, seconds:int, microseconds:int=100000) -> str:
    if isinstance(microseconds, str):
        len_diff = 6 - len(microseconds)
        microseconds = microseconds[:6] if len_diff < 0 else microseconds + '0' * len_diff
    time_obj = datetime.strptime(audio, '%H:%M:%S,%f') + timedelta(seconds=int(seconds),
                                                                   microseconds=int(f'{int(microseconds):6d}'))
    return datetime.strftime(time_obj, f'%H:%M:%S,%f')[:-3]

os.system(f'ffmpeg -i ./generator/Belgium_Law_Enforcement_Camp_2019--Day_1.mp4 ./generator/Belgium_Law_Enforcement_Camp_2019--Day_1.wav')
file = './generator/Belgium_Law_Enforcement_Camp_2019--Day_1.wav'

r = sr.Recognizer()
print('Processing hearing file')
sound = AudioSegment.from_wav(file)
print('End processing hearing file')
chunks = split_on_silence(sound,
    # experiment with this value for your target audio file
    min_silence_len = 1000,
    # adjust this per requirement
    silence_thresh = sound.dBFS-16,
    # keep the silence for 1 second, adjustable as well
    keep_silence=500,
)
text = ''
for chunk_id, chunk in enumerate(chunks, start=1):
    with sr.AudioFile(chunk.export(format="wav")) as source:
        begin = audio_begin
        end = time_calculator(begin, *str(chunk.duration_seconds).split('.'))
        audio_listened = r.record(source)
        try:
            recognize = r.recognize_google(audio_listened)
            output = translator.translate(text=recognize, dest='pl', src='auto')
            text += f'{chunk_id}\n{begin} --> {end}\n{output.text}\n'
            print(output.text + '\n')
        except:
            print(traceback.format_exc())
        audio_begin = time_calculator(end, seconds=0)