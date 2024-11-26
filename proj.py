import google.generativeai as genai
import os
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to convert text to speech
def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Main loop to continuously listen for voice input
def voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise and listen for audio
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio_data = recognizer.listen(source)

        # Using Google to recognize audio
        try:
            text_output = recognizer.recognize_google(audio_data)
            text_output = text_output.lower()
            print(f"You said: {text_output}")
            speak_text(text_output)
            return text_output
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "i want to stop"

# Global API key declaration
os.environ["GOOGLE_API_KEY"] = "YOUR API KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Define chatbot attributes
class ChatBot:
    def __init__(self, sarcasm=False, poeticness=False, wisdom=False):
        self.sarcasm = sarcasm
        self.poeticness = poeticness  # Kept poeticness
        self.wisdom = wisdom  # Kept wisdom

    def generate_response(self, user_input):
        # Customize the system message based on attributes
        system_message = ""
        if self.sarcasm:
            system_message += " You have to be sarcastic."
        if self.poeticness:  
            system_message += " You are poetic."
        if self.wisdom:
            system_message += " You provide wise advice."

        # Prepare the prompt for the Gemini API
        prompt = f"{system_message}\n:User      {user_input}\nBot:"

        # Call Gemini API for response
        response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
        return response.text

def chatbot():
    # Create an instance of ChatBot with desired attributes
    my_bot = ChatBot(sarcasm=False, poeticness=True, wisdom=True)  

    print("Start chatting with the bot (say 'i want to stop'to end conversation)!")

    while True:
        user_input = voice_input()  # Call the voice_input function to get user input
        if "i want to stop"== user_input.lower() :
            break
        
        try:
            response = my_bot.generate_response(user_input)
            print(f"Bot: {response}")
            speak_text(response)  # Recite the bot's response
        except Exception as e:
            speak_text("Bot: I cannot generate a response for this input as it violates my policy")

if __name__ == "__main__":
    chatbot()
