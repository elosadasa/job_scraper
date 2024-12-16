# Job Scraper and Notifier

This project is a Python-based application that uses the **JobSpy** library to scrape job postings, save them to a database, and notify users of new job opportunities via Telegram. It is designed to be modular, flexible, and easy to set up, with support for Conda environments.

---

## Features
- **Job Scraping**: Uses JobSpy to fetch job postings based on configurable job titles, locations, and other parameters.
- **Database Integration**: Stores job postings in a database to avoid duplicates and track new entries.
- **Telegram Notifications**: Notifies users of new job postings with a single consolidated message.
- **Modular Configuration**: Uses an external `config.json` file to define job titles, locations, and Telegram credentials.
- **Setup Script**: Includes `setup.py` for database initialization.
- **Environment Management**: Supports Conda environments for dependency management.

---

## Requirements

### Python Version
- **Python 3.10 or higher**

### Dependencies
Install required Python libraries using Conda or pip.

#### Using Conda
```bash
conda install --file requirements.txt
```

## Configuration

The script uses a `config.json` file to define the job titles, locations, and Telegram credentials. Below is an example of the `config.json` structure:

```json
{
    "job_titles": ["Data Scientist", "Product Manager", "Business Analyst"],
    "locations": ["Galicia", "San Francisco, CA"],
    "country_indeed": "Spain",
    "telegram": {
        "bot_token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    }
}
```
Fields:
- job_titles: List of job titles or keywords to search for.
- locations: List of locations to filter job postings.
- country_indeed: Country context for job postings (e.g., “Spain”).
- telegram: Contains credentials for Telegram notifications:
  - bot_token: Token provided by Telegram’s BotFather. 
  - chat_id: Chat ID of the user or group to notify.

## Usage

### 1. Initialize the Database
Before running the main script, initialize the database by executing the `setup.py` script. This will create the necessary tables and prepare the database for storing job postings:
```bash
python setup.py
```
### 2.Set Up the Environment Using Conda

Create the Conda Environment:
```bash
conda create --name job_scraper python=3.10
```
Activate the Environment:
```bash
conda activate job_scraper
```
Install Dependencies:
```bash
conda install --file requirements.txt
```
### 3.Configure the config.json File
Update the config.json file with your desired job titles, locations, and Telegram credentials. An example configuration is provided in the Configuration section.

### 4.Run the Main Script
```bash
python main.py --config path/to/config.json
```