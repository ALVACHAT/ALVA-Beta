# ALVA 2.0 - Voice-Powered Cryptocurrency Assistant

ALVA 2.0 is a cryptocurrency assistant that provides market data, trends, and price charts for popular cryptocurrencies. 
It integrates voice synthesis, speech recognition, and OpenAI's GPT-4 for enhanced interaction.
![Program](alvap.png)

## Features
- **Voice-enabled interactions**: Toggle voice synthesis for listening to responses.
- **Cryptocurrency data**: Get market trends and visual charts for supported cryptocurrencies.
- **Speech recognition**: Speak directly to the assistant for queries and commands.
- **OpenAI integration**: Use GPT-4 for general questions and crypto analysis.

---

## Installation
1. **Download Zip**:
   Download and extract zip

2. **Install Python**:  
   Download and install Python (version 3.8 or later) from the [official website](https://www.python.org/downloads/).  
   During installation, ensure you check the option **"Add Python to PATH"**.  

   Alternatively, you can use the following commands to install Python on macOS or Linux:

   - macOS:
     ```bash
     brew install python
     ```

   - Ubuntu/Debian-based Linux:
     ```bash
     sudo apt update && sudo apt install python3 python3-pip
     ```

3. **Install Dependencies**:  
   Run the following command to install all necessary Python libraries:
   ```bash
   pip install customtkinter pyttsx3 matplotlib requests SpeechRecognition openai rapidfuzz Pillow numpy

4. **Set Up API Key**:
Replace "API-OpenAI" in the code with your OpenAI API key or input it via the app's settings window.

5. **Run the Application**:
Execute the Python file in your terminal:
   ```bash
   python ALVA v2.0.py
6. **Commands**:

## Commands

### 📈 Cryptocurrency Market Analysis
- **`Analyze Bitcoin trend`**  
  Provides an analysis of the recent Bitcoin price trend.
- **`Ethereum price prediction`**  
  Predicts Ethereum's price changes based on market trends.
- **`Dogecoin market trend`**  
  Analyzes the current market trends for Dogecoin.
- **`Solana price prediction`**  
  Provides a prediction of Solana's price for the upcoming days.

### 📊 Chart Commands
- **`Show Bitcoin chart`**  
  Displays a 7-day price chart for Bitcoin.
- **`Draw Ethereum chart`**  
  Generates a 7-day price chart for Ethereum.
- **`Dogecoin price chart`**  
  Shows the historical prices of Dogecoin over the last 7 days.
- **`Cardano chart`**  
  Plots the 7-day price trend for Cardano.

### 🎤 Voice Commands
- **`Enable voice`**  
  Activates voice synthesis for spoken responses from the assistant.
- **`Disable voice`**  
  Deactivates voice synthesis.
- **`Listen to me`**  
  Enables speech recognition to accept voice input from the user.

### 🤖 General Commands
- **`What is Bitcoin?`**  
  Provides a brief explanation of Bitcoin and its use cases.
- **`Tell me about Ethereum`**  
  Shares general information about Ethereum and its technology.

### ⚙️ System Commands
- **`Settings`**  
  Opens the settings menu where you can configure your OpenAI API key and other options.
- **`Clear`**  
  Clears the chat history in the application.
- **`Close`**  
  Exits the application.

**issues**

if it doesn't work, make sure you have downloaded the latest version of python and double-click the alva.py file

