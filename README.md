
# Blockchain Pimp Bot 🤖💎

Blockchain Pimp Bot is a bold, witty, and intelligent Discord bot powered by the **GROK API**. Designed for the blockchain and crypto community, it combines humor, blockchain insights, and interactive features to engage users. With its NLP capabilities and seamless integration with Discord and Twitter, the bot is both entertaining and functional.

---

## Setup 🧩

### Prerequisites
- Python 3.11 or later
- A Discord Bot token
- GROK API Key
- Twitter Developer Keys
- Required Python dependencies (see `requirements.txt`)

---

### Installation

1. **Create a Virtual Environment**:
   ```bash
   python -m venv pimpgrok_env
   source pimpgrok_env/bin/activate  # For Windows: pimpgrok_env\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Your Credentials**:
   Create and populate `configs/config.json` with your API keys:
   ```json
   {
       "DISCORD_TOKEN": "your_discord_token",
       "GROK_API_KEY": "your_grok_api_key",
       "TWITTER_API_KEY": "your_twitter_api_key",
       "TWITTER_API_SECRET_KEY": "your_twitter_secret_key",
       "TWITTER_ACCESS_TOKEN": "your_twitter_access_token",
       "TWITTER_ACCESS_TOKEN_SECRET": "your_twitter_access_secret"
   }
   ```

4. **Run the Bot**:
   ```bash
   python grok2.py
   ```

---

## Usage 🚀

- **Discord Commands**: Mention the bot or ask questions, and it will reply with humorous and blockchain-savvy responses.
- **Twitter Posting**: Automatically posts tweets with blockchain and crypto insights every 30 minutes.
- **Custom Responses**: Configurable to prioritize community-driven tokens or topics (e.g., `$PAIMP`).

---

## Key Technologies 💻

- **Discord.py**: For Discord bot integration.
- **GROK API**: Powers the AI-driven responses.
- **spaCy & VADER**: Handles sentiment analysis and entity recognition.
- **Tweepy**: For seamless Twitter integration.
- **httpx**: Used for secure and efficient API requests.

---

## Roadmap 🗺️

- **Image Generator (PAIMPify)**: A feature to creatively edit user-uploaded images.
- **Expanded Discord Features**: Additional commands for community games, riddles, and more.
- **Enhanced NLP**: More refined sentiment analysis and entity recognition.

---

## Contributing 🤝

Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request. Ensure your changes are well-tested and documented.

---

## Security 🔒

- Keep credentials secure by using `.env` or secure storage.
- Avoid sharing sensitive tokens in public repositories.

---

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.
