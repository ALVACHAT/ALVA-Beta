import customtkinter as ctk
from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import threading

# Inicjalizacja OpenAI
client = OpenAI(api_key="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")

# Wiadomości początkowe
messages = [
    {"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"},
]

# Funkcja do mówienia (pyttsx3 w wątku)
def speak(text):
    def speak_thread():
        engine = pyttsx3.init()
        # Ustawienie głosu męskiego z amerykańskim akcentem
        voices = engine.getProperty('voices')
        for voice in voices:
            if "en_US" in voice.id and "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            engine.setProperty('voice', voices[0].id)  # Domyślny głos w razie braku odpowiedniego
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=speak_thread, daemon=True).start()

# Funkcja do rozpoznawania mowy
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            chat_log.insert(ctk.END, "🎤 Adjusting for background noise...\n")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            chat_log.insert(ctk.END, "🎤 Listening...\n")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            user_input = recognizer.recognize_google(audio)
            chat_log.insert(ctk.END, f"👤: {user_input}\n")
            return user_input
    except sr.WaitTimeoutError:
        chat_log.insert(ctk.END, "⚠️ Timeout: No speech detected.\n")
    except sr.UnknownValueError:
        chat_log.insert(ctk.END, "⚠️ Could not understand audio.\n")
    except sr.RequestError as e:
        chat_log.insert(ctk.END, f"⚠️ Speech recognition error: {e}\n")
    return ""

# Funkcja do wysyłania zapytań do OpenAI
def send_message(event=None):  # Obsługa Enter jako eventu
    user_input = input_box.get("0.0", ctk.END).strip()  # Pobranie tekstu z pola
    if not user_input:
        return

    chat_log.insert(ctk.END, f"👤: {user_input}\n")  # Wyświetlenie pytania w logu
    input_box.delete("0.0", ctk.END)  # Wyczyść pole tekstowe

    def process_message():
        try:
            # Zastąpienie historii dialogiem
            messages.clear()
            messages.append({"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"})
            messages.append({"role": "user", "content": user_input})

            # Wysłanie zapytania do OpenAI
            chat_completion = client.chat.completions.create(
                model="gpt-4o",  # Użycie modelu GPT-4
                messages=messages
            )

            # Pobranie odpowiedzi
            reply = chat_completion.choices[0].message.content
            chat_log.insert(ctk.END, f"🤖: {reply}\n\n")  # Wyświetlenie odpowiedzi
            messages.append({"role": "assistant", "content": reply})  # Zapisanie odpowiedzi w historii

            # Mówienie odpowiedzi w tle
            speak(reply)
        except Exception as e:
            chat_log.insert(ctk.END, f"⚠️ Error: {str(e)}\n\n")  # Wyświetlenie błędu w logu

    # Przetwarzanie wiadomości w osobnym wątku
    threading.Thread(target=process_message, daemon=True).start()

# Funkcja do obsługi głosowej interakcji
def voice_interaction():
    def voice_thread():
        user_input = recognize_speech()
        if user_input:
            send_message(user_input)

    # Uruchomienie rozpoznawania mowy w osobnym wątku
    threading.Thread(target=voice_thread, daemon=True).start()

# Funkcja czyszczenia logu
def clear_log():
    chat_log.delete("0.0", ctk.END)
    messages.clear()
    messages.append({"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"})

# Tworzenie głównego okna aplikacji
ctk.set_appearance_mode("system")  # Dopasowanie do motywu systemowego
ctk.set_default_color_theme("blue")  # Kolor akcentu
app = ctk.CTk()
app.title("ChatGPT GUI")
app.geometry("600x600")

# Pole wyświetlające rozmowę
chat_log = ctk.CTkTextbox(app, width=580, height=400, wrap="word", state="normal")
chat_log.pack(pady=10)

# Pole tekstowe do wpisywania wiadomości
input_box = ctk.CTkTextbox(app, height=50, width=580)
input_box.pack(pady=10)
input_box.bind("<Return>", send_message)  # Wiązanie klawisza Enter z wysyłaniem wiadomości

# Przyciski
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

voice_button = ctk.CTkButton(button_frame, text="Speak", command=voice_interaction)
voice_button.grid(row=0, column=0, padx=5)

clear_button = ctk.CTkButton(button_frame, text="Clear", command=clear_log)
clear_button.grid(row=0, column=1, padx=5)

# Rozpoczęcie pętli aplikacji
app.mainloop()
