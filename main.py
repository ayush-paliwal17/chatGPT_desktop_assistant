import os
import openai
import speech_recognition as sr
import pyttsx3
import sys


#Creating an object for SR
recognizer = sr.Recognizer()

#Get a reference to a pyttsx3.Engine instance.
engine = pyttsx3.init()
engine.setProperty('rate',150)

#Getting The OpenAI API Key e.g. $Env:OPENAI_API_KEY="your api key"
openai.api_key = os.environ['OPENAI_API_KEY'] 


def speak(text):
    """
    This function is used for Text-To-Speech.
    """
    print(text)
    engine.setProperty('rate',150)
    engine.say(text)
    engine.runAndWait()


def ask_GPT(message):
    """
    This Function is used to Query any message to ChatGPT.
    """
    try:
        res = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = message,
            max_tokens = 10
        )
        return res.choices[0].text.strip()
    except:
        speak("Failed to get result from ChatGPT. Try Again")


def main():
    # speak("Hi, My name is Sam. I am Your Personal AI Desktop Asisstant.")
    while True:
        speak( "Say 'Sam' to record your Question.")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language='eng-IN')
                text = text.lower()
                print(text)
            except:
                speak("Sorry, I could not understand You. Please Try again")
                continue

            if 'quit' in text: #Quit The Assisstant If 'Quit' is spoken.
                sys.exit()

            if "sam" in text: #'Sam' is used as a wake-up word.
                speak('Ask ')
                audio = recognizer.listen(source)
            
                try:
                    text = recognizer.recognize_google(audio, language='eng-IN')
                    print("You asked :",text)
                    res = ask_GPT(text)
                    speak(res)
                except:
                    print("Could Not Understand Your Question. Try again.")


if __name__ == "__main__":
    main()