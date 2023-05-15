import pymongo
import json

def add_data_to_mongodb(database_name, collection_name, file_path):
    """
    Connects to a remote MongoDB instance, creates a collection with the specified name,
    and inserts data from a JSON file into it.

    Parameters:
        database_name (str): The name of the database to use.
        collection_name (str): The name of the collection to create or update.
        file_path (str): The path to the JSON file containing the data to insert.

    Returns:
        dict: A dictionary containing the total number of documents in the collection and the update status.

    Raises:
        Exception: If an error occurs while connecting to MongoDB or inserting data.

    Usage:
        # Add data to MongoDB
        result = add_data_to_mongodb('mydatabase', 'mycollection', 'data.json')
        print(result)
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://user:password@server:port/')
        db = client[database_name]
        collection = db[collection_name]

        # Check if the collection already exists
        if collection.count_documents({}) == 0:
            # Create the collection if it doesn't exist
            collection.insert_many(json.load(open(file_path)))
            update_status = "Collection created and data added"
        else:
            # Update the existing collection with new data, avoiding duplication
            data = json.load(open(file_path))
            for item in data:
                collection.update_one(
                    {'_id': item['_id']},
                    {'$set': item},
                    upsert=True
                )
            update_status = "Data updated"

        # Get the total number of documents in the collection
        total_documents = collection.count_documents({})

        # Disconnect from MongoDB
        client.close()

        # Return the result
        result = {
            'total_documents': total_documents,
            'update_status': update_status
        }
        return result

    except Exception as e:
        # Handle any errors that occur
        print(f"Error occurred while adding data to MongoDB: {str(e)}")
        raise e
