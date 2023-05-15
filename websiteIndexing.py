import requests
import json
from bs4 import BeautifulSoup

def fetch_website_changes(url, stored_data_file):
    """
    Fetches the changes in a website by comparing its current content with previously stored data.

    Parameters:
        url (str): The URL of the website to monitor for changes.
        stored_data_file (str): The file path to the JSON file storing the previously stored data.

    Returns:
        dict: A dictionary containing the new information fetched from the website.

    Usage:
        # Fetch website changes
        result = fetch_website_changes('https://www.example.com', 'stored_data.json')
        print(result)
    """
    try:
        # Retrieve the current content of the website
        response = requests.get(url)
        response.raise_for_status()
        current_content = response.content

        # Load previously stored data
        try:
            with open(stored_data_file, 'r') as file:
                stored_data = json.load(file)
        except FileNotFoundError:
            stored_data = {}

        # Compare current content with stored data
        if 'content' in stored_data and stored_data['content'] == current_content:
            # No changes detected
            return {}
        else:
            # Update stored data with new content
            stored_data['content'] = current_content

            # Scraping logic to extract new information
            soup = BeautifulSoup(current_content, 'html.parser')
            # Modify this section to extract the desired information from the website
            new_info = soup.find('div', {'class': 'new-info'}).text.strip()

            # Add new information to stored data
            stored_data['new_info'] = new_info

            # Save updated data to the file
            with open(stored_data_file, 'w') as file:
                json.dump(stored_data, file, indent=4)

            # Return the new information as a dictionary
            return {'new_info': new_info}

    except Exception as e:
        # Handle any errors that occur
        print(f"Error occurred while fetching website changes: {str(e)}")
        raise e
