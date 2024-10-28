import subprocess
import pyttsx3, webbrowser, os, sys, requests, json
from requests import ConnectionError
from groq import Groq
import os
import simpleaudio as sa
from pygame import mixer
import getpass
import platform
import turtle
import pyautogui
import ctypes
import shutil
import winreg
import webbrowser
import websockets
import turtle
import pytube
from bs4 import BeautifulSoup
import requests
import re
from pytube import YouTube
import time
import math
import random

class Bot:
    def __init__(self):
        mixer.init()
        self.already_started = 0
        self.db_string = ''

        self.USER = getpass.getuser()
        self.SYSTEM = platform.system() + " " + platform.release()

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)

        self.client = Groq(
            api_key=''
        )

        with open('H://MyCode//NewBot2//NewBot2//program_db.json', 'r') as f:
            db = json.load(f)
        
        for a, i in db.items():
            self.db_string += f"{a}_path = {i}. "

        chat_completion = (self.client).chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'Теперь и впредь твое имя - Алиса, ты разговариваешь только на русском языке, ты говоришь очень кратко. {self.db_string}',
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
        )
        print(chat_completion.choices[0].message.content)

    def ai(self, text):
        if ((text).upper()).find('ПРИЛ') != -1:
            chat_completion1 = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f'{text}. Если я пытаюсь открыть программу из списка: {self.db_string}, напиши только одно имя и путь к программе. Если не уверена на 100 процентов не пиши ничего.',
                    }
                ],
                model="llama-3.2-90b-vision-preview",
            )
            program_and_path = chat_completion1.choices[0].message.content
            print(program_and_path)
        else:
            program_and_path = ''
        bot_input = f'Напиши Python код для выполнения следующей команды: {text}. {program_and_path} Операционная система: {self.SYSTEM}. Имя пользователя: {self.USER}. Код должен быть качественным, без ошибок и готовым к выполнению. Код должен быть без if __name__ == "__main__":\n. Код должен быть безопастным и не удалять много файлов. Если ты считаешь что этот код может навредить компьютеру или привести к необратимым последствиям не пиши его. Пиши все названия как очень развернуто.'
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": bot_input,
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
        )

        content = (chat_completion.choices[0].message.content).replace('if __name__ == "__main__":\n    ', '')
        print(content)
        content_words = content.split()

        idx = [x[0] for x in enumerate(content_words) if x[1] == 'def']
        for _id in idx:
            content = 'global ' + content_words[_id+1].split('(')[0] + '\n' + content

        if not ctypes.windll.shell32.IsUserAnAdmin():
            if ((text).upper()).find('УДАЛ') != -1 or ((content).upper()).find('REMOV') != -1 or ((text).upper()).find('ФОРМ') != -1:
                safety = input('testYES or NO: ')
                if safety.upper() == 'YES':
                    try:
                        exec(str(content), [])
                        #speaker(chat_completion.choices[0].message.content)
                    except Exception as e:
                        print(e)
            else:
                try:
                    exec(str(content))
                    #speaker(chat_completion.choices[0].message.content)
                except Exception as e:
                    print(e)
        else:
            print('unsafety')

    def check_safety(self, code, attempt):
        attempt += 1
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": code,
                }
            ],
            model="llama-guard-3-8b",
        )
        if chat_completion.choices[0].message.content == 'safe':
            if attempt == 3:
                return True
            else:
                return self.check_safety(code, attempt)
        else:
            return False

    def speaker(self, text):
        with open('words.txt', 'w', encoding="utf-8") as text_file:
            text_file.write(text)
        with open('words.txt', 'r', encoding="utf-8") as text_file:
            if  self.already_started == 1:
                mixer.music.unload()
            os.self.SYSTEM('type H:\\MyCode\\NewBot2\\NewBot2\\words.txt | H:\\MyCode\\NewBot2\\NewBot2\\piper\\piper.exe -m H:\\MyCode\\NewBot2\\NewBot2\\piper\\ru_RU-irina-medium.onnx -c H:\\MyCode\\NewBot2\\NewBot2\\piper\\ru_ru_RU_irina_medium_ru_RU-irina-medium.onnx.json -f H:\\MyCode\\NewBot2\\NewBot2\\piper\\sound.wav')
        mixer.music.load('H:\\MyCode\\NewBot2\\NewBot2\\piper\\sound.wav')
        mixer.music.play()

        self.already_started = 1

    def visual():
        subprocess.Popen('C:\\Program Files\\Microsoft Visual Studio\\2022\Community\\Common7\\IDE\\devenv.exe')

    def youtube():
        webbrowser.open_new_tab('https://www.youtube.com/')

    def discord():
        webbrowser.open_new_tab('https://discord.com/channels/@me')

    def browser():
        webbrowser.open_new_tab('https://www.google.com/')

    def weather(self):
        try:
            city = 'Гомель'
            open_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=41af888682cb61528343b2165bb641c8'
            weather_data = requests.get(open_weather_url).json()
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])
            text_w = 'Сейчас в городе', city, str(temperature), '°C' 'Ощущается как', str(temperature_feels), '°C'
            self.engine.say(text_w)
            self.engine.runAndWait()
        except ConnectionError:
            self.engine.say('Не удалось подключиться к базе данных')

    def jokes(self):
        try:
            joke = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=11').json(strict=False)
            joke_filtred = joke['content']
            self.engine.say(joke_filtred)
            self.engine.runAndWait()
        except ConnectionError:
            self.engine.say('Не удалось подключиться к базе данных')

    def jokes_2(self):
        try:
            joke_2 = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1').json(strict=False)
            joke_2_filtred = joke_2['content']
            self.engine.say(joke_2_filtred)
            self.engine.runAndWait()
        except ConnectionError:
            self.engine.say('Не удалось подключиться к базе данных')

    def quotes(self):
        try:
            quote = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=16').json(strict=False)
            quote_filtred = quote['content']
            self.engine.say(quote_filtred)
            self.engine.runAndWait()
        except ConnectionError:
            self.engine.say('Не удалось подключиться к базе данных')

    def quotes_2(self):
        try:
            quote_2 = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=6').json(strict=False)
            quote_2_filtred = quote_2['content']
            self.engine.say(quote_2_filtred)
            self.engine.runAndWait()
        except ConnectionError:
            self.engine.say('Не удалось подключиться к базе данных')

    def pass_():
        pass