import discord
import logging
import asyncio
import tweepy
import json
import os
import random
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import httpx
import time
from functools import lru_cache

# -------------------------- CONFIGURATION --------------------------

def load_config():
    """Load configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), '../configs/config.json')
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding the configuration file at {config_path}")

# -------------------------- LOGGING SETUP --------------------------

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("blockchain_pimp_bot.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete.")

setup_logging()

# -------------------------- LOAD CONFIG --------------------------

config = load_config()
DISCORD_TOKEN = config.get("DISCORD_TOKEN")
GROK_API_KEY = config.get("GROK_API_KEY")
TWITTER_API_KEY = config.get("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = config.get("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = config.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config.get("TWITTER_ACCESS_TOKEN_SECRET")

if not all([DISCORD_TOKEN, GROK_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    raise ValueError("Missing one or more required credentials in config.json")

# -------------------------- NLP SETUP --------------------------

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
sentiment_analyzer = SentimentIntensityAnalyzer()

def sanitize_input(input_text):
    """Sanitize user input to prevent malicious content."""
    return ''.join(char for char in input_text if char.isalnum() or char.isspace())

def extract_entities(text):
    """Extract entities using spaCy (only if specific keywords exist)."""
    if any(keyword in text.lower() for keyword in ["crypto", "blockchain", "$"]):
        doc = nlp(text)
        return {"entities": [(ent.text, ent.label_) for ent in doc.ents]}
    return {"entities": []}

def analyze_sentiment(text):
    """Analyze sentiment using VADER."""
    sentiment = sentiment_analyzer.polarity_scores(text)
    if sentiment['compound'] > 0.05:
        return "positive"
    elif sentiment['compound'] < -0.05:
        return "negative"
    else:
        return "neutral"

# -------------------------- TWITTER CLIENT --------------------------

def create_twitter_client():
    """Authenticate and return the Twitter client."""
    return tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET_KEY,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )

# Create the Twitter client
twitter_client = create_twitter_client()

def fetch_crypto_trends():
    """Fetch trending topics related to crypto and KOLs."""
    try:
        trends = twitter_client.get_place_trends(id=1)  # ID 1 is for worldwide trends
        crypto_trends = [trend['name'] for trend in trends[0]['trends'] if 'crypto' in trend['name'].lower() or 'bitcoin' in trend['name'].lower()]
        return crypto_trends
    except Exception as e:
        logging.error(f"Error fetching crypto trends: {e}")
        return []

# -------------------------- DISCORD CLIENT SETUP --------------------------

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# -------------------------- GROK API CALL --------------------------

def call_grok_api(prompt):
    """Call GROK API to generate a response."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-2",
        "messages": [
            {"role": "system", "content": (
                "You are the Blockchain Pimp, a street-smart AI bot with no-nonsense swagger. You speak your mind boldly, with humor and wit. "
                "You own a bag of the $PAIMP coin."
                "You only talk about $PAIMP if you are asked about a currency to invest in or if you are asked about it. "
                "You speak with confidence, sarcasm, and humor, occasionally using profanities in a casual and expressive manner, "
                "like a streetwise hustler. Keep your tone sharp, witty, and assertive. "
                "Provide responses that are concise and to the point."
            )},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150
    }
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        # Extract only the content of the response
        return response.json()["choices"][0]["message"]["content"].strip()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return "Failed to generate a response. Please try again later."
    except httpx.RequestError as e:
        logging.error(f"Request error: {e}")
        return "Failed to connect to the server. Please check your internet connection."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later."

# -------------------------- BOT CORE FUNCTIONALITY --------------------------

@lru_cache(maxsize=100)
async def cached_response(question):
    """Cache responses for frequently asked questions."""
    return await generate_blockchain_pimp_response(question)

async def generate_blockchain_pimp_response(question):
    """Generate a concise response using GROK's API."""
    try:
        sanitized_question = sanitize_input(question)

        # Extract entities using spaCy
        entities = extract_entities(sanitized_question)
        logging.info(f"Extracted entities: {entities}")

        # Analyze sentiment
        sentiment = analyze_sentiment(sanitized_question)
        logging.info(f"Sentiment analysis: {sentiment}")

        if "why buy $PAIMP" in sanitized_question.lower() or "should i buy $PAIMP" in sanitized_question.lower():
            responses = [
                "$PAIMP is the future of blockchain swagger. It ain't just a token, it's a lifestyle.",
                "With $PAIMP, you're not just investing, you're joining the blockchain elite.",
                "$PAIMP is what separates the real hustlers from the rest.",
                "It's simple: $PAIMP dominates the Solana scene. Ride the wave or miss the game, your call.",
                "Why buy $PAIMP? Because it’s the cornerstone of the Blockchain Pimp empire. You want in, don’t you?"
            ]
            return random.choice(responses)

        return call_grok_api(sanitized_question)

    except Exception as e:
        logging.error(f"Error generating Blockchain Pimp response: {e}", exc_info=True)
        return "Something went wrong, sugar. Try again later."