import pyjokes
import pyttsx3
import speech_recognition
import datetime
import webbrowser
import time
import requests
import json
import wolframalpha

wolfram_app_id = "YEAXQH-8KA4APJKXE"
weather_api_key = '6953bc3b8241f6f5cf6d20e95557d02d'

engine = pyttsx3.init("sapi5")
engine.setProperty('rate', 175)


def speak(text):
    print("\n", text)
    engine.say(text)
    engine.runAndWait()


def command():
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.6

        print("\nListening.....")
        audio = recognizer.listen(source)
        print("Working on it.....")

    try:
        text = recognizer.recognize_google(audio, language='en-in')
        print(f"You requested to : {text}")

    except Exception as e:
        print(e)
        return "None"

    return text


def start():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour <= 17:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("How may I help you...")


def wait():
    speak("How many seconds do you want me to wait?")
    seconds = command()
    i = seconds.index(" ")
    seconds = int(seconds[:i])

    while seconds:
        print("\r", seconds, end="")
        time.sleep(1)
        seconds -= 1

    speak("I am back!!!!!")


if __name__ == '__main__':
    start()

    while True:
        query = command().lower()

        if "open google" in query:
            webbrowser.get().open("http://www.google.com")

        elif "open youtube" in query:
            webbrowser.get().open("http://www.youtube.com")

        elif "open anime" in query:
            webbrowser.get().open("https://www2.kickassanime.ro/")

        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            # print(f"Time is {time}")
            speak(f"Time is {time}")

        elif "calculate" in query:
            client = wolframalpha.Client(wolfram_app_id)
            i = query.lower().split().index('calculate')
            query = query.split()[i + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak("The answer is " + answer)

        elif "temperature" in query or "weather" in query:
            i = query.index("in")
            city_name = query[i+2:]
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
            data = requests.get(url).text
            data = json.loads(data)
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            speak(f"Temperature = {temp}°C")
            speak(f"Weather description: {description.capitalize()}")

        elif "joke" in query:
            speak(pyjokes.get_joke())

        elif "wait" in query:
            wait()

        elif "quit" in query or "exit" in query or "bye" in query:
            speak("Goodbye")
            exit()
