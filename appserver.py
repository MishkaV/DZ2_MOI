from flask import Flask, render_template, redirect
from vosk import Model, KaldiRecognizer
import wave
import re
import json
import time

app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/', methods=['POST', 'GET'])
def start():
    return render_template('root.html')



@app.route('/translate', methods=['POST'])
def to_text():

    file = 'noise.wav'

    model = Model("vosk-model-small-ru-0.22")
    wf = wave.open(file, "rb")
    wf_fr = wf.getframerate() * wf.getnchannels()
    rec = KaldiRecognizer(model, wf_fr)
    res = ''
    last = False
    read_block_size = wf.getnframes()
    while True:
        data = wf.readframes(read_block_size)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())

            if res['text'] != '':
                res = res + " " + res['text']
                if read_block_size < 200000:
                    print(res['text'] + " \n")

                last = False
            elif not last:
                res += '\n'
                last = True

    res = json.loads(rec.FinalResult())
    res = res + " " + res['text']

    return '\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', res))
