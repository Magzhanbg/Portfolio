import requests
import tkinter as tk
from tkinter import Label, Button, Frame, messagebox
import datetime
import feedparser
import calendar
import speech_recognition as sr

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

    def get_news(self):
        news_feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
        try:
            feed = feedparser.parse(news_feed_url)
            entries = feed.entries[:5]
            news = "\n".join([entry.title for entry in entries])
            return news
        except Exception as e:
            return f"Ошибка получения новостей: {e}"

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
