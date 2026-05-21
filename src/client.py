import os
from anthropic import Anthropic
from dotenv import load_dotenv
import httpx

load_dotenv()
anthropic_client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    timeout=30.0,
    http_client=httpx.Client(limits=httpx.Limits(max_keepalive_connections=0)),
)
