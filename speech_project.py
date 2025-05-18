import time
from threading import Thread
import speech_recognition as sr

filler_words = [
     "er", "like", "you know", "so", "basically", 
     "ah", "ohh", "umm","kind of","literally"
]

def speech_callback(transcription):
    """
    Process transcribed speech and trigger vibration if filler words are detected.
    Also shows filler percentage and cleaned-up sentence if threshold exceeded.
    """
    if not transcription:
        return

    words = transcription.lower().split()
    total_words = len(words)
    filler_count = 0
    detected_fillers = []
    clean_words = []

    for word in words:
        
        word_stripped = word.strip(".,!?\"'")

        if word_stripped in filler_words:
            filler_count += 1
            detected_fillers.append(word_stripped)
            vibrate_device()
            time.sleep(0.2)
        else:
            clean_words.append(word)

    if detected_fillers:
        print(f"Detected filler words: {detected_fillers}")

    percentage = (filler_count / total_words) * 100 if total_words > 0 else 0
    print(f"Filler word percentage: {percentage:.2f}%")

    threshold = 20  
    if percentage > threshold:
        cleaned_sentence = ' '.join(clean_words)
        print(f"Cleaned sentence (fillers removed): {cleaned_sentence}")

 
def vibrate_device():
    """
    Simulate device vibration - placeholder for real implementation.
    """
    try:
        
        print("Vibrating...")  
    except Exception as e:
        print(f"Vibration failed: {e}")

def start_speech_recognition():
    """
    Start real-time speech recognition and pass results to callback.
    """
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for speech... Speak into the microphone.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            while True:
                audio = recognizer.listen(source, timeout=None)
                try:
                    transcription = recognizer.recognize_google(audio)
                    print(f"Heard: {transcription}")
                    speech_callback(transcription)
                except sr.UnknownValueError:
                    print("Couldn’t understand the audio.")
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
    except Exception as e:
        print(f"Error starting recognition: {e}")


if __name__ == "__main__":
    recognition_thread = Thread(target=start_speech_recognition)
    recognition_thread.daemon = True  
    recognition_thread.start()

    
    while True:
        time.sleep(1)
