def main():
    api_key = 'AIzaSyDjekzYzkGIUAz2cBeDUtXcqdWo_H7XXuQ'
    import requests
    import speech_recognition as sr
    # import time
    # import threading
    import thread
    import pyttsx3

    api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
    history = []  
    # global next_question
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'key': api_key
    }

    # Initialize the recognizer and the text-to-speech engine
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    count = 3
    try:
        with sr.Microphone() as source:  # Keep microphone active throughout
            while True:
                print("Ask your question...")
                audio = recognizer.listen(source)

                try:
                    prompt = recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    if count < 2:
                        thread.speak_response("Could not understand audio")
                        thread.next_question = True
                        count += 1
                    continue  # Move to next iteration if speech not recognized
                print(f"Question: {prompt}")
                
                if "are you there" in prompt.lower() or "hello bot" in prompt.lower() or "hi bot" in prompt.lower():
                    engine.say("Yes, I am here")
                    engine.runAndWait()
                    thread.next_question = False
                    continue
                elif ("bye bot" in prompt.lower() or "stop bot" in prompt.lower() or prompt.lower() == "exit"):
                    engine.say("Yes, Bye Bye")
                    engine.runAndWait()
                    thread.next_question = True
                elif(thread.next_question):
                    pass
                # Recognize speech using Google Speech Recognition
                else:    
                    payload = {
                        "contents": [
                        {
                            "parts": [{"text": prompt+ ' \n Note: reply text make it short and simple. less then 40 words \n'}],
                        }
                        ]
                    }
                    response = requests.post(api_url, json=payload, headers=headers, params=params)
                    response.raise_for_status()

                    data = response.json()
                    sms = data['candidates'][0]['content']['parts'][0]['text'].replace('*', ' ')

                    # Truncate the text to the first 100 characters
                    # sms = sms[:100]
                    print(f"Response: {sms}")
                    try:
                        # thread.next_question = True

                        thread.speak_response(sms)
                        # speaking_thread = threading.Thread(target=thread.speak_response, args=(sms,)).start()
                        if (('to do list' in prompt.lower() or 'to do' in prompt.lower()) and ("note" in prompt.lower() or 'make' in prompt.lower() or 'reminder' in prompt.lower())) or (('create' in prompt.lower())):
                            print('todo')
                            with open('todo.txt', 'a') as file:
                                print('writing to file')
                                file.write(sms + ' \n \n')
                    except Exception as e:
                        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

main()

# except Exception as e:
#     print(f"Error: {e}")