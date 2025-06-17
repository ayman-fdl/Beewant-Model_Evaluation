from dotenv import load_dotenv
import os 

load_dotenv(override=True)

API_URL = "https://beewant.com/api/new-chat"
API_TOKEN = os.getenv('BEEWANT_API_TOKEN')

CHAT_MODELS = ["GPT4.1", "mistral", "llama3.3", "claude-3.7", "r1", "qwen3"]

CHAT_MODEL = 'qwen3'
EVALUATOIN_MODEL = 'claude-3.7'