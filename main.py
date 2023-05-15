import pymongo
from scrapper import scrape_data
from dbUpdate import add_data_to_mongodb

def main():
    # MongoDB connection details
    host = 'your-hostname'
    port = 27017
    username = 'your-username'
    password = 'your-password'
    database = 'your-database'

    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(host, port, username=username, password=password)
        db = client[database]
        collection_name = "your-collection"
        url = 'https://www.example.com'
        data = scrape_data(url)
        if data is not None:
            print("Scraped data:")
            print(data)
            print("Updating the database")
            result = add_data_to_mongodb(db, collection_name, data)
            print(result)
        else:
            print("Failed to scrape data.")

    except Exception as e:
        # Handle any errors that occur
        print(f"An error occurred: {str(e)}")

    finally:
        # Disconnect from MongoDB
        client.close()


if __name__ == '__main__':
    main()
