import pymongo


def search_data_in_mongodb(database_name, collection_name, keyword):
    """
    Connects to a remote MongoDB instance, searches for documents containing the specified keyword,
    and returns the matching documents.

    Parameters:
        database_name (str): The name of the database to use.
        collection_name (str): The name of the collection to search in.
        keyword (str): The keyword to search for in the documents.

    Returns:
        list: A list of documents that match the given keyword.

    Raises:
        Exception: If an error occurs while connecting to MongoDB or searching for documents.

    Usage:
        # Search for documents containing the keyword
        result = search_data_in_mongodb('mydatabase', 'mycollection', 'keyword')
        for document in result:
            print(document)
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://user:password@server:port/')
        db = client[database_name]
        collection = db[collection_name]

        # Search for documents containing the keyword
        query = {'$text': {'$search': keyword}}
        result = list(collection.find(query))

        # Disconnect from MongoDB
        client.close()

        # Return the matching documents
        return result

    except Exception as e:
        # Handle any errors that occur
        print(f"Error occurred while searching data in MongoDB: {str(e)}")
        raise e


