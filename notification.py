import logging
from urllib.parse import quote

import requests


def send_combined_telegram_message(bot_token, chat_id, new_jobs):
    """
        Send all new job postings in a single Telegram message using HTML formatting.

        Args:
            bot_token (str): Telegram bot token.
            chat_id (str): Telegram chat ID.
            new_jobs (pd.DataFrame): DataFrame containing new job postings.

        Returns:
            None
        """
    # Build the message string using HTML formatting

    message_parts = []
    for _, job in new_jobs.iterrows():
        job_title = job["title"]
        job_url = quote(job["job_url"], safe=":/")

        # Construct job details with HTML tags
        message_parts.append(
            f"<b>{job_title}</b>\n"
            f"<a href='{job_url}'>View Job Posting</a>\n\n"
        )

    # Combine all job messages
    full_message = "<b>New Job Alerts!</b>\n\n" + "".join(message_parts)

    # Handle Telegram's 4096-character limit
    if len(full_message) > 4096:
        messages = [full_message[i:i + 4096] for i in range(0, len(full_message), 4096)]
    else:
        messages = [full_message]

    # Send the messages
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for message in messages:
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logging.info(f"Message sent successfully: {message[:50]}...")  # Print first 50 chars as preview
        except requests.exceptions.RequestException as e:
            logging.info(f"Failed to send Telegram message: {e}")