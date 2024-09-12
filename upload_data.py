from pymongo import MongoClient
import pandas as pd
import json


# MongoDB connection string (ensure credentials are correct)
url = 'mongodb+srv://vuser:1234@cluster0.mqtvo.mongodb.net/?retryWrites=true&w=majority'

# Connect to MongoDB
client = MongoClient(url)

# Create database and collection
db = client['Data']
collection = db['wafers_fault']

# Read the CSV file (ensure the path is correct)
csv_file_path = 'notebooks/wafer.csv'  # Correct the path if needed
df = pd.read_csv(csv_file_path)


# Convert the DataFrame to JSON format for MongoDB insertion
data_json = json.loads(df.to_json(orient='records'))

# Insert the data into MongoDB
collection.insert_many(data_json)

print("Data inserted successfully!")