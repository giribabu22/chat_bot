import pyttsx3
next_question = False
engine = pyttsx3.init()

def speak_response(response):
    global next_question
    try:
        engine.say(response)
        engine.runAndWait()
        next_question = False
    except Exception as e:
        print(f"Error: {e}")
        next_question = False

def speak_response(response):
    global next_question
    try:
        engine.say(response)
        engine.runAndWait()
        next_question = False
        print('next_question', next_question)
    except Exception as e:
        print(f"Error: {e}")