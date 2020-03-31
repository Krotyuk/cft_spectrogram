from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage

import librosa
import matplotlib.pyplot as plt
import librosa.display

from uploads.settings import BASE_DIR


def home(request):
    if request.method == 'POST' and request.FILES.get('audio', False) :
        audio = request.FILES['audio']
        if request.FILES['audio'].content_type == 'audio/mp3':
            fs = FileSystemStorage()
            filename = fs.save(audio.name, audio)
            uploaded_file_url = fs.url(filename)
            spectogram_url = handle_uploaded_file( BASE_DIR + uploaded_file_url)
            return render(request, 'core/home.html', {
                'uploaded_file_url': uploaded_file_url,
                'spectogram_url': spectogram_url,
            })
        else:
            not_audio = 'Вы загружаете не .mp3'
            return render(request, 'core/home.html', {
            'not_audio' : not_audio
        })
    return render(request, 'core/home.html')


def handle_uploaded_file(audio_path):
    name = audio_path[audio_path.rfind('/') + 1 : -4] + '_spectrogram'
    file = "spectrogram/{}.png".format(name)
    x , sr = librosa.load(audio_path, sr=44100)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(20, 10))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    plt.savefig(file, format='png')
    file_url = '/' + file
    return file_url