from PyQt5.QtCore import QObject, pyqtSignal, QThread, QMutex, QMutexLocker, QWaitCondition
import pyaudio
import wave
import tempfile
import io
import subprocess
from google.cloud import speech

class BackgroundThread(QThread):
    def __init__(self, parent=None):
        super(BackgroundThread, self).__init__(parent)

        self._mutex = QMutex()
        self._condition = QWaitCondition()

        self._activating = False
        self._input = None
        # when program is closed
        self._abort = False

    def __del__(self):
        self._mutex.lock()
        self._abort = True
        self._condition.wakeOne()
        self._mutex.unlock()

        # wait for gracefully stop
        self.wait()

    def _taskStart(self, taskInput):
        '''
        this function should not be called from outside
        :return: 
        '''
        # this must re-implemented in derived class
        pass


    def _taskEnd(self, taskOutput):
        '''
        this function should not be called from outside
        :return: 
        '''
        # this must re-implemented in derived class
        pass

    def activate(self, input = None):
        locker = QMutexLocker(self._mutex)
        if not self._activating:
            self._activating = True
            self._input = input
            # if not running than we start the thread, otherwise we wake it up
            if not self.isRunning():
                self.start()
            else:
                self._condition.wakeOne()

    def run(self):
        while True:
            if self._abort:
                return

            self._mutex.lock()
            activating = self._activating
            input = self._input
            self._mutex.unlock()

            if activating:
                # start long running task
                taskOutput = self._taskStart(input)

                # task comleted => report result
                self._taskEnd(taskOutput)

                # switch off self._activating
                self._mutex.lock()
                self._activating = False
                self._mutex.unlock()
            else:
                self._mutex.lock()
                self._condition.wait(self._mutex)
                self._mutex.unlock()


class RecThread(BackgroundThread):
    speechReady = pyqtSignal(str)

    def __init__(self, parent=None, num_secs=5):
        super(RecThread, self).__init__(parent)

        self._num_secs = num_secs

    @property
    def encoding(self):
        return 'FLAC'

    def record(self):
        self.activate()

    def _taskStart(self, input):
        with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as f:
            flacFilename = f.name
        cmd = 'rec --channels=1 --bits=16 --rate=16000 {} trim 0 {:d}'.format(flacFilename, self._num_secs)
        print("recording...")
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        # wait for subprocess to finished
        p.communicate()
        print("finished recording")
        return flacFilename

    def _taskEnd(self, flacFilename):
        self.speechReady.emit(flacFilename)

class GoogleSTTThread(BackgroundThread):
    textReady = pyqtSignal(list)

    def __init__(self, parent=None):
        super(GoogleSTTThread, self).__init__(parent)

        # create speech client
        self._speechClent = speech.Client()

    def _taskStart(self, input):
        audioFile, audioEncoding = input
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

        return retval

    def _taskEnd(self, taskOutput):
        self.textReady.emit(taskOutput)

    def speechToText(self, audioFile, audioEncoding):
        '''
        
        :param audioFile: a file contain raw audio
        :param audioEncoding: is either 'LINEAR16' or 'FLAC' 
        :return: 
        '''
        self.activate((audioFile, audioEncoding))
