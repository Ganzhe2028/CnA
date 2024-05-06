# import the OpenAI Python library for calling the OpenAI API
class OpenAI:
    pass


from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

