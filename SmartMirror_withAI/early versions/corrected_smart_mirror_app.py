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

        self.weather_frame = self.create_label_frame("Weather", 30)
        self.weather_label = Label(self.weather_frame, text=self.get_weather_data(), font=("Arial", 20))
        self.weather_label.pack()

        self.time_frame = self.create_label_frame("Time", 50)
        self.time_label = Label(self.time_frame, font=("Arial", 50))
        self.time_label.pack()

        self.news_frame = self.create_label_frame("News", 20)
        self.news_label = Label(self.news_frame, text=self.get_news(), font=("Arial", 12), justify=tk.LEFT)
        self.news_label.pack()

        self.calendar_frame = self.create_label_frame("Date", 20)
        self.calendar_label = Label(self.calendar_frame, text=self.get_calendar(), font=("Arial", 12), justify=tk.LEFT)
        self.calendar_label.pack()

        self.voice_button = Button(root, text='Listen', command=self.listen)
        self.voice_button.pack()

        self.response_label = Label(root, text="", font=("Arial", 12), justify=tk.LEFT)
        self.response_label.pack()

        self.update_weather()
        self.update_time()
        self.update_calendar()

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
            return f"Error with data: {e}"

    def get_news(self):
        news_feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
        try:
            feed = feedparser.parse(news_feed_url)
            entries = feed.entries[:5]
            news = "\n".join([entry.title for entry in entries])
            return news
        except Exception as e:
            return f"News error: {e}"

    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def get_calendar(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        current_day = now.day 

        cal_text = calendar.month(year, month)

        cal_lines = cal_text.split('\n')

        for i, line in enumerate(cal_lines):
            if f"{current_day:2d}" in line:
                cal_lines[i] = line.replace(f"{current_day:2d}", f"Today is {current_day:2d}")

        cal_text = '\n'.join(cal_lines)

        return cal_text

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            print(f"You said: {text}")
            response = self.process_command(text)
            self.response_label.config(text=response)
        except sr.UnknownValueError:
            self.response_label.config(text="Sorry,I didn`t get it.")
        except sr.RequestError:
            self.response_label.config(text="Can`t get an access")

    def process_command(self, command):
        command = command.lower()
        if 'weather' in command:
            return self.get_weather_data()
        elif 'news' in command:
            self.update_news_sections()
            return "Displaying news."
        elif 'time' in command:
            return self.get_time()
        elif 'calendar' in command:
            return self.get_calendar()
        else:
            return "Command not recognized."

    def update_weather(self):
        self.weather_label.config(text=self.get_weather_data())
        self.root.after(600000, self.update_weather)

    def update_time(self):
        self.time_label.config(text=self.get_time())
        self.root.after(1000, self.update_time)

    def update_calendar(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        current_day = now.day
        
        # Создайте текстовый календарь
        cal = calendar.month(year, month)
        
        # Выделите текущий день месяца, добавив символ '*'
        cal = cal.replace(f"{current_day:2d}", f"*{current_day:2d}")

        # Обновите текст календаря
        self.calendar_label.config(text=cal)

        # Запустите повторное обновление каждую минуту (или при необходимости)
        self.root.after(60000, self.update_calendar)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartMirrorApp(root)
    root.mainloop()


    def get_news_by_category(self, category):
        pass

    def update_news_sections(self):
        pass

    def add_images_and_icons(self):
        pass
    def decide_action(self):
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:
                r = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})
                print r.text
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print intent
                if intent == 'greeting':
                    self.__text_action(self.nlg.greet())
                elif intent == 'snow white':
                    self.__text_action(self.nlg.snow_white())
                elif intent == 'weather':
                    self.__weather_action(entities)
                elif intent == 'news':
                    self.__news_action()
                elif intent == 'maps':
                    self.__maps_action(entities)
                elif intent == 'holidays':
                    self.__holidays_action()
                elif intent == 'appearance':
                    self.__appearance_action()
                elif intent == 'user status':
                    self.__user_status_action(entities)
                elif intent == 'user name':
                    self.__user_name_action()
                elif intent == 'personal status':
                    self.__personal_status_action()
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return
                else: # No recognized intent
                    self.__text_action("I'm sorry, I don't know about that yet.")
                    return

            except Exception as e:
                print "Failed wit!"
                print(e)
                traceback.print_exc()
                self.__text_action("I'm sorry, I couldn't understand what you meant by that")
                return

            self.decide_action()

    def __joke_action(self):
        joke = self.nlg.joke()

        if joke is not None:
            self.__text_action(joke)
        else:
            self.__text_action("I couldn't find any jokes")

    def __user_status_action(self, nlu_entities=None):
        attribute = None

        if (nlu_entities is not None) and ("Status_Type" in nlu_entities):
            attribute = nlu_entities['Status_Type'][0]['value']

        self.__text_action(self.nlg.user_status(attribute=attribute))

    def __user_name_action(self):
        if self.nlg.user_name is None:
            self.__text_action("I don't know your name. You can configure it in bot.py")

        self.__text_action(self.nlg.user_name)

    def __appearance_action(self):
        requests.get("http://localhost:8080/face")

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __personal_status_action(self):
        self.__text_action(self.nlg.personal_status())

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)
