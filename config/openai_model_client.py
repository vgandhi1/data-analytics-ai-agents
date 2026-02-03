from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

# Read API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your .env file or environment. "
        "You can find your API key at https://platform.openai.com/account/api-keys"
    )


def get_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model='gpt-4o',
        api_key=api_key
    )

    return openai_model_client