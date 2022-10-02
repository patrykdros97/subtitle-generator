from urllib import response
from django.shortcuts import render
from .models import UploadMediaFile
from .forms import UploadMediaFileForm

import os
import traceback
import mimetypes
from datetime import datetime
from pydub import AudioSegment
import speech_recognition as sr
from googletrans import Translator
from datetime import datetime,timedelta
from pydub.silence import split_on_silence
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger(__name__)


def time_calculator(audio: str, seconds:int, microseconds:int=100000) -> str:
    if isinstance(microseconds, str):
        len_diff = 6 - len(microseconds)
        microseconds = microseconds[:6] if len_diff < 0 else microseconds + '0' * len_diff
    time_obj = datetime.strptime(audio, '%H:%M:%S,%f') + timedelta(seconds=int(seconds),
                                                                   microseconds=int(f'{int(microseconds):6d}'))
    return datetime.strftime(time_obj, f'%H:%M:%S,%f')[:-3]

@csrf_exempt
def upload_file(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        logger.info('Starting post')
        forms = UploadMediaFileForm(request.POST, request.FILES)
        if forms.is_valid():
            file = request.FILES['file']
            if file.name.lower().endswith(('.mp3', '.mp4')):
                file_to_convert = ''.join(file.name.split('.')[:-1]) + '.wav'
                os.system(f'ffmpeg -i {file.name} {file_to_convert}')
                os.system('y')
            else:
                file_to_convert = file

            context = {'form': forms}
            filepath = handle_uploaded_file(file_to_convert)
            context = {'filepath': filepath}
    return render(request, 'working_page.html', context)

def handle_uploaded_file(file, audio_begin:str='00:00:00,500', translator=Translator(), filepath:str='subtitles.txt') -> str:
    r = sr.Recognizer()
    logger.info('Processing hearing file')
    sound = AudioSegment.from_wav(file)
    logger.info('End processing hearing file')
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
                text += f'{chunk_id}\n{begin} --> {end}\n{output.text}\n\r'
                logger.info(output.text + '\n')
            except:
                logger.warning(traceback.format_exc())
            audio_begin = time_calculator(end, seconds=0)
    #return text
    with open(filepath, 'w') as file: file.write(text)
    return filepath

def download_file(request, filepath):
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    # Return the response value
    return response
        