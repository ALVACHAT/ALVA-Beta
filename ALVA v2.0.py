import customtkinter as ctk
import pyttsx3
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speech_recognition as sr
import threading
import matplotlib.pyplot as plt
from io import BytesIO
import requests
from PIL import Image, ImageTk
from rapidfuzz import process
import openai

# Konfiguracja OpenAI
openai.api_key = "API-OpenAI"

# Lista popularnych kryptowalut
CRYPTO_NAMES = [
    "bitcoin", "ethereum", "ripple", "dogecoin", "cardano", "solana",
]

voice_enabled = True  # Domyślnie włączony głos

# Inicjalizacja silnika pyttsx3 (głos)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Możesz zmienić głos

def get_closest_crypto_name(user_input):
    closest_match = process.extractOne(user_input, CRYPTO_NAMES, score_cutoff=75)
    return closest_match[0] if closest_match else None

def speak(text):
    if voice_enabled:
        def speak_thread():
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                chat_log.insert(ctk.END, f"⚠️ Voice synthesis error: {e}\n")
        threading.Thread(target=speak_thread, daemon=True).start()

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

def fetch_crypto_data(crypto_name):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart?vs_currency=usd&days=7"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def analyze_trends(crypto_name, data):
    start_price = data['prices'][0][1]
    end_price = data['prices'][-1][1]
    price_change = (end_price - start_price) / start_price * 100
    trend = "upward" if price_change > 0 else "downward"

    prompt = f"Analyze the market trend for {crypto_name.capitalize()} based on the following data:\n"
    prompt += f"Start Price: {start_price} USD\n"
    prompt += f"End Price: {end_price} USD\n"
    prompt += f"Price Change: {price_change:.2f}%\n"
    prompt += f"Trend: {trend}\n"
    prompt += f"Provide insights on the current market trend and any possible predictions for the next 7 days."

    messages = [{"role": "system", "content": "You are a financial expert assistant."}]
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response['choices'][0]['message']['content']

import numpy as np

def calculate_ema(prices, window):
    # Współczynnik wygładzania
    alpha = 2 / (window + 1)
    
    # Inicjalizacja EMA - pierwsza wartość to zwykła cena
    ema = [prices[0]]
    
    # Obliczanie EMA dla każdej kolejnej ceny
    for price in prices[1:]:
        ema.append(alpha * price + (1 - alpha) * ema[-1])
    
    return ema

def plot_crypto_chart(crypto_name):
    data = fetch_crypto_data(crypto_name)
    if data:
        times = [datetime.fromtimestamp(item[0] / 1000) for item in data['prices']]
        prices = [item[1] for item in data['prices']]

        # Obliczanie 7-dniowej EMA
        window_size = 7  # Długość okna dla EMA (7 dni)
        if len(prices) < window_size:
            chat_log.insert(ctk.END, f"⚠️ Not enough data for 7-day EMA.\n")
            return

        ema_values = calculate_ema(prices, window_size)  # Obliczanie EMA
        ema_times = times  # Czasy dla EMA są takie same jak dla cen

        # Tworzenie wykresu
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(times, prices, label=f"{crypto_name.capitalize()} (7 Days)", color="green", linewidth=2)
        ax.plot(ema_times, ema_values, label="7-Day EMA", color="orange", linestyle="--", linewidth=2)

        # Ustawienia wykresu
        ax.set_title(f"{crypto_name.capitalize()} Price Chart (Last 7 Days)", color="white", fontsize=14)
        ax.set_xlabel("Time", color="white", fontsize=12)
        ax.set_ylabel("Price in USD", color="white", fontsize=12)
        ax.tick_params(colors="white")
        ax.legend(facecolor='gray', edgecolor='white', labelcolor='white', loc='upper left')
        ax.grid(color="gray", linestyle="--", linewidth=0.5)
        fig.patch.set_facecolor('black')
        ax.set_facecolor("black")

        # Aktualizacja GUI
        def update_gui():
            for widget in image_label.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=image_label)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        app.after(0, update_gui)
    else:
        app.after(0, lambda: chat_log.insert(ctk.END, f"⚠️ Could not fetch data for '{crypto_name}'.\n"))



def send_message(event=None):
    user_input = input_box.get("0.0", ctk.END).strip()
    if not user_input:
        return

    chat_log.insert(ctk.END, f"👤: {user_input}\n")
    input_box.delete("0.0", ctk.END)

    def process_message():
        try:
            lower_input = user_input.lower()
            chart_keywords = ["chart", "wykres", "rysuj", "narysuj"]
            trend_keywords = ["trend", "analiza", "przewidywanie", "prognoza"]

            if any(keyword in lower_input for keyword in trend_keywords):
                crypto_name = get_closest_crypto_name(lower_input)
                if crypto_name:
                    data = fetch_crypto_data(crypto_name)
                    if data:
                        analysis = analyze_trends(crypto_name, data)
                        chat_log.insert(ctk.END, f"🤖: {analysis}\n")
                        speak(analysis)
                    else:
                        chat_log.insert(ctk.END, f"⚠️ Could not fetch data for '{crypto_name}'.\n")
                else:
                    chat_log.insert(ctk.END, f"⚠️ Could not identify the cryptocurrency '{user_input}'.\n")
            elif any(keyword in lower_input for keyword in chart_keywords):
                crypto_name = get_closest_crypto_name(lower_input)
                if crypto_name:
                    plot_crypto_chart(crypto_name)
                else:
                    chat_log.insert(ctk.END, f"⚠️ Could not identify the cryptocurrency '{user_input}'.\n")
            else:
                messages = [{"role": "system", "content": "You are a helpful assistant."}]
                messages.append({"role": "user", "content": user_input})
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages
                )
                reply = response['choices'][0]['message']['content']
                chat_log.insert(ctk.END, f"🤖: {reply}\n")
                speak(reply)
        except Exception as e:
            chat_log.insert(ctk.END, f"⚠️ Błąd: {str(e)}\n\n")

    threading.Thread(target=process_message, daemon=True).start()

def open_settings():
    settings_window = ctk.CTkToplevel(app)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    
    license_label = ctk.CTkLabel(settings_window, text="License: ALVA 2.0", font=("Arial", 14))
    license_label.pack(pady=10)
    
    api_key_label = ctk.CTkLabel(settings_window, text="Enter your OpenAI API Key:", font=("Arial", 12))
    api_key_label.pack(pady=5)
    
    api_key_entry = ctk.CTkEntry(settings_window, width=300)
    api_key_entry.pack(pady=5)
    api_key_entry.insert(0, openai.api_key)
    
    def save_api_key():
        new_key = api_key_entry.get().strip()
        if new_key:
            openai.api_key = new_key
            ctk.CTkMessageBox.show_info("Success", "API Key saved successfully.")
        else:
            ctk.CTkMessageBox.show_warning("Error", "API Key cannot be empty.")
    
    save_button = ctk.CTkButton(settings_window, text="Save", command=save_api_key)
    save_button.pack(pady=10)

    close_button = ctk.CTkButton(settings_window, text="Close", command=settings_window.destroy)
    close_button.pack(pady=10)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.iconbitmap("alvalogo.ico")
app.title("ALVA 2.0")
app.geometry("600x650")

chat_log = ctk.CTkTextbox(app, width=780, height=200, wrap="word", state="normal")
chat_log.pack(pady=10)

input_box = ctk.CTkTextbox(app, height=50, width=780)
input_box.pack(pady=10)
input_box.bind("<Return>", send_message)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

voice_toggle_button = ctk.CTkSwitch(button_frame, text="Enable Voice", command=lambda: toggle_voice())
voice_toggle_button.grid(row=0, column=0, padx=5, pady=10)

clear_button = ctk.CTkButton(button_frame, text="Clear", command=lambda: chat_log.delete("1.0", ctk.END))
clear_button.grid(row=0, column=1, padx=5)

speak_button = ctk.CTkButton(button_frame, text="Speak", command=lambda: send_message(recognize_speech()))
speak_button.grid(row=0, column=2, padx=5)

settings_button = ctk.CTkButton(button_frame, text="Settings", command=open_settings)
settings_button.grid(row=0, column=3, padx=5)

image_label = ctk.CTkLabel(app)
image_label.pack(pady=10)

# Dodanie funkcji przełączania głosu
def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled  # Zmiana stanu na przeciwny
    voice_toggle_button.configure(text="Voice Enabled" if voice_enabled else "Voice Disabled")
    chat_log.insert(ctk.END, f"Voice {'enabled' if voice_enabled else 'disabled'}.\n")

# Inicjalizacja przełącznika głosu
voice_toggle_button = ctk.CTkSwitch(
    button_frame,
    text="Voice Enabled",
    command=toggle_voice
)
voice_toggle_button.grid(row=0, column=0, padx=5, pady=10)
voice_toggle_button.select()  # Domyślnie włączony


app.mainloop()
