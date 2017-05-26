from PyQt5.QtCore import QObject, pyqtSignal
import pyaudio
import wave
import tempfile
import io
import subprocess
from google.cloud import speech


class SpeechRecWorker(QObject):
    speechReady = pyqtSignal(str)

    def __init__(self):
        super(SpeechRecWorker, self).__init__()
        self._audio = pyaudio.PyAudio()

    def __del__(self):
        self._audio.terminate()

    @property
    def encoding(self):
        return 'LINEAR16'

    def record(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1600
        RECORD_SECONDS = 5

        stream = self._audio.open(format=FORMAT, channels=CHANNELS,
                                  rate=RATE, input=True,
                                  frames_per_buffer=CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wave_filename = f.name

        waveFile = wave.open(wave_filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self._audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        self.speechReady.emit(wave_filename)


class RecWorker(QObject):
    speechReady = pyqtSignal(str)

    def __init__(self):
        super(RecWorker, self).__init__()

    @property
    def encoding(self):
        return 'FLAC'

    def record(self):
        with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as f:
            flac_filename = f.name

        cmd = 'rec --channels=1 --bits=16 --rate=16000 {} trim 0 5'.format(flac_filename)
        print("recording...")
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        # wait for subprocess to finished
        p.communicate()
        print("finished recording")

        self.speechReady.emit(flac_filename)

class GoogleSTTWorker(QObject):
    textReady = pyqtSignal(list)

    def __init__(self):
        super(GoogleSTTWorker, self).__init__()
        self._speechClent = speech.Client()

    def speechToText(self, audioFile, audioEncoding):
        '''

        :param audioFile: a file contain raw audio
        :param audioEncoding: is either 'LINEAR16' or 'FLAC' 
        :return: 
        '''
        with io.open(audioFile, 'rb') as audio_file:
            content = audio_file.read()
            sample = self._speechClent.sample(content,
                                              source_uri=None,
                                              encoding=audioEncoding,
                                              sample_rate=16000)

        alternatives = sample.sync_recognize('en-US', speech_context=['turn right',
                                                                      'turn left',
                                                                      'go forward',
                                                                      'go backward',
                                                                      'degree',
                                                                      'the cube',
                                                                      'metre',
                                                                      'centimetre'])
        retval = []
        for alternative in alternatives:
            retval.append(alternative.transcript)

        self.textReady.emit(retval)