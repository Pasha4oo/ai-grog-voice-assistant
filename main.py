import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from scripts import *
from pygame import mixer

from get_paths import *

q = queue.Queue()

device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
print(samplerate)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return 

    data.replace(list(trg)[0], '')
    bot.ai(text=data.replace(list(trg)[0], ''))
    #text_vector = vectorizer.transform([data]).toarray()[0]
    #answer = clf.predict([text_vector])[0]
    #func_name = answer.split()[0]
    #speaker(answer.replace(func_name, ''))
    #exec(func_name + '()')

def main1234():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0],
            dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(Model('vosk_model'), samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data2 = json.loads(rec.Result())['text']
                recognize(data2, vectorizer, clf)
            # else:
                # print(rec.PartialResult())

if __name__ == '__main__':
    db = {}
    programs = get_programs_from_start_menu()
    for program in programs:
        exe_path = resolve_shortcut(program)
        if exe_path is not None:
            program = ((program.split('\\'))[-1]).replace('.lnk', '')
            db[program] = exe_path
    with open('H://MyCode//NewBot2//NewBot2//program_db.json', 'w') as f:
        json.dump(db, f)
    bot = Bot()
    main1234()