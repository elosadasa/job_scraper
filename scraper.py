from jobspy import scrape_jobs
import pandas as pd
import logging

DEFAULT_RESULTS_WANTED = 20
DEFAULT_HOURS_OLD = 1

def fetch_jobs(search_term, location, country_indeed, is_remote=False):
    """
        Fetch job postings based on search term, location, and remote preference.

        Args:
            search_term (str): Job title or keywords.
            location (str): Job location.
            is_remote (bool, optional): True for remote jobs, False for on-site jobs, None for both.

        Returns:
            pd.DataFrame: DataFrame containing job postings.
        """
    try:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "google"],
            search_term=search_term,
            location=location,
            is_remote=is_remote,
            results_wanted=DEFAULT_RESULTS_WANTED,
            hours_old=DEFAULT_HOURS_OLD,
            country_indeed=country_indeed,
        )
        logging.info(f"Successfully fetched jobs for '{search_term}' in '{location}' (Remote: {is_remote})")
        return jobs
    except Exception as e:
        logging.error(f"Error fetching jobs for '{search_term}' in '{location}' (Remote: {is_remote}): {e}")
        return pd.DataFrame()  # Return an empty DataFrame to maintain consistency

def fetch_remote_jobs(job_titles):
    """
    Fetch remote job postings for specified job titles.

    Args:
        job_titles (list of str): List of job titles or keywords to search for.

    Returns:
        pd.DataFrame: DataFrame containing the aggregated remote job postings.
    """
    all_jobs = pd.DataFrame()
    for title in job_titles:
        jobs = fetch_jobs(
            search_term=title,
            location=None,          # No specific location
            country_indeed="worldwide",    # No specific country
            is_remote=True          # Filter for remote jobs
        )
        all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
    return all_jobs


def fetch_jobs_multiple_locations(job_titles, locations, country_indeed=None, is_remote=False):
    """
    Fetch job postings for specified job titles across multiple locations.

    Args:
        job_titles (list of str): List of job titles or keywords to search for.
        locations (list of str): List of locations to search within.
        country_indeed (str, optional): Country name for Indeed and Glassdoor searches.
        is_remote (bool, optional): True for remote jobs, False for on-site jobs, None for both.

    Returns:
        pd.DataFrame: DataFrame containing the aggregated job postings.
    """
    all_jobs = pd.DataFrame()
    for title in job_titles:
        for location in locations:
            jobs = fetch_jobs(
                search_term=title,
                location=location,
                country_indeed=country_indeed,
                is_remote=is_remote
            )
            all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
    return all_jobs

def fetch_combined_job_posts(job_titles, locations, country_indeed=None):
    """
    Fetch job postings for specified job titles across given locations and remote positions.

    Args:
        job_titles (list of str): List of job titles or keywords to search for.
        locations (list of str): List of locations to search within.
        country_indeed (str, optional): Country name for Indeed and Glassdoor searches.

    Returns:
        pd.DataFrame: DataFrame containing the combined job postings.
    """
    # Fetch remote job postings
    remote_jobs = fetch_remote_jobs(job_titles)

    # Fetch job postings for specified locations
    location_jobs = fetch_jobs_multiple_locations(job_titles, locations, country_indeed=country_indeed)

    # Combine the results
    combined_jobs = pd.concat([remote_jobs, location_jobs], ignore_index=True)

    # Remove duplicate job postings
    combined_jobs = combined_jobs.drop_duplicates()

    return combined_jobs

