import openai
import speech_recognition as sr
import pyttsx3
import sys
import webbrowser
import AppOpener
from utils import yt_auto

#Creating an object for SR
recognizer = sr.Recognizer()

#Get a reference to a pyttsx3.Engine instance.
engine = pyttsx3.init()
engine.setProperty('rate',150)


#Getting The OpenAI API Key
openai.api_key = "Your Api Key"


def speak(text):
    """
    This function is used for Text-To-Speech.
    """
    print(text)
    engine.setProperty('rate',150)
    if '.' in text:
        engine.say(text[0:text.index('.')])
    else:
        engine.say(text)
    engine.runAndWait()

def recognize(audio):
    """
    This Function is used for speech recognition using Google.
    """
    try:
        text = recognizer.recognize_google(audio,language='en-IN')
        text = text.lower()
        return text
    except:
        speak("sorry, I could not understand you. Please Try again")


def ask_GPT(message):
    """
    This Function is used to Query any message to ChatGPT.
    """
    try:
        res = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = message,
            max_tokens = 400
        )
        return res.choices[0].text.strip()
    except:
        return "Failed to get result from ChatGPT. Try Again"


def main():
    speak( "Say 'Chat' to record your Question or 'Sam' for Assistant.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        text = recognize(audio)

        if not text:
            return
        print(text)

        if 'quit' in text: #Quit The Assisstant If 'Quit' is spoken.
            sys.exit()
        elif "chat" in text: #'Sam' is used as a wake-up word.
            speak('Ask ')
            audio = recognizer.listen(source)

            query = recognize(audio)
            if not query:
                return
            print(query)
            res = ask_GPT(query)
            speak(res)
        elif "sam" in text:
            speak("How Can I help you sir?")
            audio = recognizer.listen(source)
            command = recognize(audio)
            print(command)


            if 'open' in command:
                if 'website' in command:
                    list = command.split()
                    site = list[1]
                    webbrowser.open(f'https://www.{site}.com')
                    sys.exit()
                else:
                    temp = command.split()
                    app = temp[1]
                    AppOpener.open(app, match_closest= True)
                    sys.exit()
            elif 'play' and 'youtube' in command:
                command = command.replace('play ','')
                command = command.replace(' on youtube','')
                yt_auto.yt_auto(command)
                sys.exit()
            elif 'google' in command:
                command = command.replace("search","")
                temp = command.split("google")
                search = temp[1]
                webbrowser.open(f'https://www.google.com/search?q={search}')
                sys.exit()
            else:
                res = ask_GPT(command)
                speak(res)


if __name__ == "__main__":
    speak("Hi, My name is Sam. I am Your Personal AI Desktop Assistant.")
    while True:
        main()