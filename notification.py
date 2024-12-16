import requests
import logging
from urllib.parse import quote


def build_job_message(job):
    """
    Build a single job message using HTML formatting.

    Args:
        job (dict): A dictionary representing a job with 'title' and 'job_url'.

    Returns:
        str: HTML-formatted string for a single job.
    """
    job_title = job["title"]
    job_url = quote(job["job_url"], safe=":/")
    return f"<b>{job_title}</b>\n<a href='{job_url}'>View Job Posting</a>\n\n"


def combine_messages(new_jobs):
    """
    Combine all job postings into a single HTML-formatted message.

    Args:
        new_jobs (pd.DataFrame): DataFrame containing new job postings.

    Returns:
        str: Combined HTML-formatted string of all jobs.
    """
    message_parts = [build_job_message(job) for _, job in new_jobs.iterrows()]
    return "<b>New Job Alerts!</b>\n\n" + "".join(message_parts)


def split_message(message, max_length=4096):
    """
    Split a long message into smaller chunks without breaking HTML tags.

    Args:
        message (str): The full message to split.
        max_length (int): Maximum allowed length for a single message.

    Returns:
        list: List of message chunks.
    """
    if len(message) <= max_length:
        return [message]

    parts = message.split("\n\n")
    chunks = []
    current_chunk = ""

    for part in parts:
        if len(current_chunk) + len(part) + 2 <= max_length:  # +2 for "\n\n"
            current_chunk += part + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = part + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def send_telegram_message(bot_token, chat_id, message):
    """
    Send a single Telegram message.

    Args:
        bot_token (str): Telegram bot token.
        chat_id (str): Telegram chat ID.
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info(f"Message sent successfully: {message[:50]}...")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram message: {e}")
        logging.error(f"Payload: {payload}")
        return False


def send_combined_telegram_message(bot_token, chat_id, new_jobs):
    """
    Send all new job postings in a single or multiple Telegram messages using HTML formatting.

    Args:
        bot_token (str): Telegram bot token.
        chat_id (str): Telegram chat ID.
        new_jobs (pd.DataFrame): DataFrame containing new job postings.

    Returns:
        None
    """
    # Step 1: Combine all job postings into a single message
    full_message = combine_messages(new_jobs)

    # Step 2: Split the message if it exceeds Telegram's character limit
    messages = split_message(full_message)

    # Step 3: Send each message chunk
    for message in messages:
        send_telegram_message(bot_token, chat_id, message)