from django.shortcuts import render
from .forms import UploadMediaFileForm
from .models import UploadMediaFile

import speech_recognition as sr
import traceback
from pydub import AudioSegment
from pydub.silence import split_on_silence
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def start_page(request, *args, **kwargs):
    return render(request, 'main_page.html', {})

@csrf_exempt
def wav_files(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        forms = UploadMediaFileForm(request.POST, request.FILES)
        if forms.is_valid():
            print(request.FILES['file'].size)
            instance = UploadMediaFile(file=request.FILES['file'])
            instance.save()
            context = {'form': forms}
            handle_uploaded_file(request.FILES['file'])
        
    return render(request, 'working_page.html', context)

def another_files(request, *args, **kwargs):
    return render(request, 'working_page.html', {})

def handle_uploaded_file(file):
    r = sr.Recognizer()
    print('Processing hearing file')
    sound = AudioSegment.from_wav(file)
    print('End processing hearing file')
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    for chunk in chunks:
        with sr.AudioFile(chunk.export(format="wav")) as source:
            
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
                print(text + '\n')
            except:
                print(traceback.format_exc())
        