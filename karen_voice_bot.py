import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests


class VirtualAssistant:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        if len(voices) > 0:
            self.engine.setProperty('voice',voices[0].id)

        self.api_key = os.environ.get('API_KEY')

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def wish_me(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak("I am Karen Sir. Please tell me how may I help you")

    def get_weather(self, location):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={self.api_key}&q={location}&units=metric"
        response = requests.get(complete_url)
        print("Status code:", response.status_code)
        print("Response content:", response.content)
        data = response.json()
        


        if "main"in data:
            main_data = data["main"]
            temperature = main_data["temp"]
            weather_description = data["weather"][0]["description"]
            self.speak(f"The temperature in {location} is {temperature}°C with {weather_description}.")
        else:
            self.speak("Sorry, I couldn't find the weather information for that location.")


    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

    def send_email(self, to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.close()

    def execute_command(self, query):
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            if query:
               results = wikipedia.summary(query, sentences=2)
               self.speak("According to Wikipedia")
               print(results)
               self.speak(results)
            else:
               self.speak("Please provide a search term for the Wikipedia command.")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        
        # Add more commands here
        elif 'weather' in query:
               query = query.replace("weather", "").strip()
               if query:
                  self.get_weather(query)
               else:
                  self.speak("Please provide a location to get the weather information.")

        elif 'exit' in query or 'quit' in query:
            self.speak("Goodbye!")
            exit()

        elif 'api key' in query:
             print("API Key:", self.api_key)

        
    def run(self):
        self.wish_me()
        while True:
              query = self.take_command().lower()
              if query is not None:
                  self.execute_command(query)
              else:
                  self.speak("I didn't understand that. Please say it again.")

if __name__ == "__main__":
    assistant = VirtualAssistant()
    assistant.run()