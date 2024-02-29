import requests
import tkinter as tk
from tkinter import Label, Button, Frame, messagebox, PhotoImage, Label
import datetime
import feedparser
import calendar
import speech_recognition as sr
from PIL import Image, ImageTk

class SmartMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mirror")
        self.api_key = "e6b658388ba7c9d64b339bc06a517ea8"
        self.city_name = "Almaty"

        self.weather_frame = self.create_label_frame("Погода", 30)
        self.weather_label = Label(self.weather_frame, text=self.get_weather_data(), font=("Arial", 20))
        self.weather_label.pack()

        self.time_frame = self.create_label_frame("Время", 50)
        self.time_label = Label(self.time_frame, font=("Arial", 50))
        self.time_label.pack()

        self.news_frame = self.create_label_frame("Новости", 20)
        self.news_label = Label(self.news_frame, text=self.get_news(), font=("Arial", 12), justify=tk.LEFT)
        self.news_label.pack()

        self.calendar_frame = self.create_label_frame("Календарь", 20)
        self.calendar_label = Label(self.calendar_frame, text=self.get_calendar(), font=("Arial", 12), justify=tk.LEFT)
        self.calendar_label.pack()

        self.voice_button = Button(root, text='Слушать', command=self.listen)
        self.voice_button.pack()

        self.response_label = Label(root, text="", font=("Arial", 12), justify=tk.LEFT)
        self.response_label.pack()

        self.update_weather()
        self.update_time()

    def create_label_frame(self, text, font_size):
        frame = Frame(self.root, bd=2, relief=tk.GROOVE)
        frame.pack(side=tk.LEFT, fill="both", expand="yes", padx=10, pady=10)

        label = Label(frame, text=text, font=("Arial", font_size), padx=10, pady=10)
        label.pack()

        return frame

    def get_weather_data(self):
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"{weather}, {temperature}°C"
        except requests.exceptions.RequestException as e:
            return f"Ошибка получения данных: {e}"

     def get_news_by_category(self, category):
        api_key = '2d8dbb4d94a54c6b916e88be7802f758'  # Замените на ваш реальный ключ API для новостей
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}&language=en'
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data['articles']
            # Извлечение заголовка первой статьи в качестве примера
            return articles[0]['title'] if articles else 'No news found'
        else:
            return 'Error fetching news'

    def update_news_sections(self):
        # Создание фреймов для каждой категории новостей
        self.sports_news_frame = Frame(self.root)
        self.sports_news_frame.pack()
        self.health_news_frame = Frame(self.root)
        self.health_news_frame.pack()
        self.politics_news_frame = Frame(self.root)
        self.politics_news_frame.pack()

        # Получение и отображение новостей для каждой категории
        sports_news = self.get_news_by_category('sports')
        health_news = self.get_news_by_category('health')
        politics_news = self.get_news_by_category('politics')

        Label(self.sports_news_frame, text='Sports: ' + sports_news).pack()
        Label(self.health_news_frame, text='Health: ' + health_news).pack()
        Label(self.politics_news_frame, text='Politics: ' + politics_news).pack()

    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def get_calendar(self):
        now = datetime.datetime.now()
        return calendar.month(now.year, now.month)

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Слушаю...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {text}")
            response = self.process_command(text)
            self.response_label.config(text=response)
        except sr.UnknownValueError:
            self.response_label.config(text="Извините, я не понял.")
        except sr.RequestError:
            self.response_label.config(text="Не могу получить доступ к сервису распознавания голоса.")

    def process_command(self, command):
        command = command.lower()
        if 'погода' in command:
            return self.get_weather_data()
        elif 'новости' in command:
            return self.get_news()
        elif 'время' in command:
            return self.get_time()
        elif 'календарь' in command:
            return self.get_calendar()
        else:
            return "Команда не распознана"

    def update_weather(self):
        self.weather_label.config(text=self.get_weather_data())
        self.root.after(600000, self.update_weather)

    def update_time(self):
        self.time_label.config(text=self.get_time())
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartMirrorApp(root)
    root.mainloop()


    # New method to get news by category using NewsAPI
    def get_news_by_category(self, category):
        api_key = '2d8dbb4d94a54c6b916e88be7802f758'
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}&language=ru'
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data['articles']
            return articles
        else:
            return "Ошибка доступа к новостям"

    # New method to update news sections on the GUI
    def update_news_sections(self):
        sports_news = self.get_news_by_category('sports')
        # Код для обновления интерфейса спортивными новостями

        health_news = self.get_news_by_category('health')
        # Код для обновления интерфейса новостями о здоровье

        politics_news = self.get_news_by_category('politics')
        # Код для обновления интерфейса политическими новостями

        # Дополнительные категории по необходимости


import pygame
import speech_recognition as sr

class SmartMirrorApp:
    # ... existing methods ...

    def setup_radio_player(self):
        pygame.mixer.init()
        self.radio_stream_url = 'http://stream-url'  # Replace with actual stream URL

    def play_radio(self):
        pygame.mixer.music.load(self.radio_stream_url)
        pygame.mixer.music.play()

    def stop_radio(self):
        pygame.mixer.music.stop()

    def listen_for_radio_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something to control the radio...")
            audio = recognizer.listen(source)

           try:
    command = recognizer.recognize_google(audio).lower()
    if 'play radio' in command:
        self.play_radio()
    elif 'stop radio' in command:
        self.stop_radio()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")

def __init__(self, root):
        # ... существующий код инициализации ...
        self.root.geometry('1024x768')  # Обновите эту строку с желаемым размером экрана

        self.add_icons()  # Вызов для добавления иконок

def add_icons(self):
        # Загрузка иконок с изменением размера
        # Иконка погоды
        weather_icon_path = r'C:\Users\Алтынхан\Desktop\BERDIBEK MAGZHAN AI AND IOT\icons\weather.png'
        weather_icon_image = Image.open(weather_icon_path)
        weather_icon_resized = weather_icon_image.resize((100, 100), Image.ANTIALIAS)
        self.weather_icon = ImageTk.PhotoImage(weather_icon_resized)
        Label(self.root, image=self.weather_icon).pack()

        # Иконка новостей
        news_icon_path = r'C:\Users\Алтынхан\Desktop\BERDIBEK MAGZHAN AI AND IOT\icons\news.png'
        news_icon_image = Image.open(news_icon_path)
        news_icon_resized = news_icon_image.resize((100, 100), Image.ANTIALIAS)
        self.news_icon = ImageTk.PhotoImage(news_icon_resized)
        Label(self.root, image=self.news_icon).pack()

        # Иконка календаря
        calendar_icon_path = r'C:\Users\Алтынхан\Desktop\BERDIBEK MAGZHAN AI AND IOT\icons\calendar.png'
        calendar_icon_image = Image.open(calendar_icon_path)
        calendar_icon_resized = calendar_icon_image.resize((100, 100), Image.ANTIALIAS)
        self.calendar_icon = ImageTk.PhotoImage(calendar_icon_resized)
        Label(self.root, image=self.calendar_icon).pack()

        # Иконка времени
        time_icon_path = r'C:\Users\Алтынхан\Desktop\BERDIBEK MAGZHAN AI AND IOT\icons\time.png'
        time_icon_image = Image.open(time_icon_path)
        time_icon_resized = time_icon_image.resize((100, 100), Image.ANTIALIAS)
        self.time_icon = ImageTk.PhotoImage(time_icon_resized)
        Label(self.root, image=self.time_icon).pack()

        Label(self.root, image=self.weather_icon).pack()  # Пример размещения иконки погоды
        # Добавьте другие иконки аналогично

 