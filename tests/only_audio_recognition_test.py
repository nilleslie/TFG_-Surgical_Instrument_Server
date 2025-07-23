import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

with mic as source:
    print("Calibrating microphone... Speak after the message.")
    r.adjust_for_ambient_noise(source, duration=5)
    print("You may speak now.")
    try:
        audio = r.listen(source, timeout=3, phrase_time_limit=1)
        print("Recognizing...")
        text = r.recognize_google(audio, language="en-US")
        print("You said:", text)
    except sr.WaitTimeoutError:
        print("No voice was detected in time.")
    except sr.UnknownValueError:
        print("Could not understand what you said.")
    except sr.RequestError:
        print("Error connecting to the recognition service.")
