import sqlite3

import pandas as pd


def initialize_database():
    """
    Initializes the SQLite database with the required schema if it doesn't exist.
    """
    conn = sqlite3.connect('job_postings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_postings (
            id TEXT UNIQUE,        -- Job ID, unique across all platforms
            site TEXT,             -- Source site (e.g., Indeed, LinkedIn)
            job_url TEXT UNIQUE,   -- Unique job URL
            title TEXT,            -- Job title
            company TEXT,          -- Company name
            location TEXT,         -- Job location
            date_posted TEXT,      -- Date the job was posted
            job_type TEXT,         -- Job type (e.g., Full-time, Part-time)
            description TEXT,      -- Job description
            PRIMARY KEY (id)       -- Ensure id is the primary key
        )
    ''')
    conn.commit()
    conn.close()


def insert_job_postings_and_get_new(jobs):
    """
    Inserts job postings into the database and returns new postings.

    Args:
        jobs (pd.DataFrame): DataFrame containing job postings.

    Returns:
        pd.DataFrame: DataFrame of newly added job postings.
    """
    conn = sqlite3.connect('job_postings.db')
    cursor = conn.cursor()
    new_jobs = []

    for _, job in jobs.iterrows():
        try:
            # Insert job into the database
            cursor.execute('''
                INSERT INTO job_postings (id, site, job_url, title, company, location, date_posted, job_type, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.get('id'),            # Job ID (unique)
                job.get('site'),          # Source site
                job.get('job_url'),       # Unique job URL
                job.get('title'),         # Job title
                job.get('company'),       # Company name
                job.get('location'),      # Job location
                job.get('date_posted'),   # Date the job was posted
                job.get('job_type'),      # Job type (e.g., Full-time, Part-time)
                job.get('description')    # Job description
            ))
            # Add new job to the list
            new_jobs.append(job)
        except sqlite3.IntegrityError:
            # Skip duplicates (based on UNIQUE constraints)
            pass

    conn.commit()
    conn.close()

    # Return new jobs as a DataFrame
    return pd.DataFrame(new_jobs)