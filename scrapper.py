import boto3
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def scrape_data(url, use_selenium=True):
    """
    Scrapes data from a webpage using either Selenium or BeautifulSoup.

    Parameters:
        url (str): The URL of the webpage to scrape.
        use_selenium (bool, optional): Specifies whether to use Selenium (default) or BeautifulSoup for scraping.

    Returns:
        dict or None: The scraped data stored in a dictionary structure, or None if an error occurred during scraping.

    Raises:
        Exception: If an error occurs during scraping.

    Usage:
        # Scrape data using Selenium (default)
        data = scrape_data('https://www.example.com')

        # Scrape data using BeautifulSoup directly
        data = scrape_data('https://www.example.com', use_selenium=False)
    """
    try:
        if use_selenium:
            # Initialize Selenium webdriver
            driver = webdriver.Chrome()  # Change this according to your browser and setup

            # Navigate to the URL
            driver.get(url)

            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(driver.page_source, 'html.parser')

        else:
            # Use BeautifulSoup directly without Selenium
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

        # Scraping logic
        # Modify this section to extract the desired data from the webpage
        title = soup.title.string.strip()
        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]

        # Upload files to Amazon S3
        s3 = boto3.client('s3')
        for file in soup.find_all('file'):
            file_url = file['src']
            file_name = file_url.split('/')[-1]
            s3.upload_file(file_url, 'your-bucket', file_name)
            file_path = f"s3://your-bucket/{file_name}"
            file['s3_filepath'] = file_path

        # Define the generic JSON structure with the scraped data and file paths
        scraped_data = {
            'title': title,
            'paragraphs': paragraphs,
            'files': [file['s3_filepath'] for file in soup.find_all('file')]
        }

        # Save scraped data as a JSON file
        with open('scraped_data.json', 'w') as file:
            json.dump(scraped_data, file, indent=4)

        return scraped_data

    except Exception as e:
        # Handle any errors that occur during scraping
        print(f"Error occurred while scraping: {str(e)}")
        return None

    finally:
        if use_selenium:
            # Cleanup Selenium webdriver
            driver.quit()
