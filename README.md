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

Market Analysis
"Analyze Bitcoin trend": Analyzes the price trend of Bitcoin.
"Ethereum price prediction": Provides a price prediction for Ethereum.
"Dogecoin market trend": Analyzes the market trend for Dogecoin.
"Solana price prediction": Provides a price prediction for Solana.
Chart Commands
"Show Bitcoin chart": Displays the price chart for Bitcoin for the last 7 days.
"Draw Ethereum chart": Generates the price chart for Ethereum for the last 7 days.
"Dogecoin price chart": Displays the Dogecoin price chart for the last 7 days.
"Cardano chart": Shows the price chart for Cardano for the last 7 days.
Voice Commands
"Enable voice": Turns on voice synthesis for spoken responses.
"Disable voice": Turns off voice synthesis.
"Listen to me": Activates speech recognition to allow voice input from the user.
General Commands
"What is Bitcoin?": Provides an explanation of Bitcoin.
"Tell me about Ethereum": Provides general information about Ethereum.
System Commands
"Settings": Opens the settings window, where you can change your API key.
"Clear": Clears the chat window.
"Close": Closes the application.

