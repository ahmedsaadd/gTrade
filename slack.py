from urllib.error import URLError
from slack_sdk import WebClient
from datetime import datetime
import pytz, time
import config

client = WebClient(token=config.SLACK_BOT_TOKEN)

def get_time():
    timeInCairo = datetime.now(pytz.timezone("Africa/Cairo") )
    currentTimeInCairo = timeInCairo.strftime("%I:%M:%p")
    return currentTimeInCairo

def send_message(message, channel):
    max_retries = 3
    retry_delay = 5  # In seconds

    for i in range(max_retries):
        try:
            client.chat_postMessage(channel=f"#{channel}", text=message)
            break
        except URLError as e:
            print(f"Error sending message to Slack: {e}. Retrying in {retry_delay} seconds... (Attempt {i + 1}/{max_retries})")
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Failed to send message to Slack after all retries.")
