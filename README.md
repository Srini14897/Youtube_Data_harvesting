# Youtube_Data_harvesting

This project is a Streamlit application that allows users to access and analyze data from multiple YouTube channels. Users can input a YouTube channel ID to retrieve relevant data such as channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, and comments for each video. The application provides the ability to store the data in a MongoDB database as a data lake and migrate it to a SQL database for further analysis. Users can also search and retrieve data from the SQL database using various search options and view the results in a user-friendly interface.

Features
Retrieve data for a YouTube channel using the YouTube API
Store channel data in a MongoDB database as a data lake
Migrate channel data from MongoDB to a MySQL database
Search and retrieve data from the SQL database
Display query results as tables in the Streamlit application
Installation
Clone the repository

Install the required dependencies:
pip install -r requirements.txt
Set up MongoDB:

Install MongoDB and start the MongoDB server.
Update the MongoDB connection URL in the code to match your MongoDB configuration.
Set up MySQL:

Install MySQL and create a database for the project.
Update the MySQL connection URL in the code to match your MySQL configuration.
Set up the YouTube API:

Create a project on the Google Developers Console.
Enable the YouTube Data API v3 and obtain the API credentials.
Update the API credentials in the code.
Usage
Run the Streamlit application:

arduino
Copy code
streamlit run main.py
Access the application in your browser at http://localhost:8501.

Enter a YouTube channel ID and click "Retrieve Channel Data" to retrieve and save the channel data in the MongoDB data lake.

Click "Migrate Channel Data to MySQL" to migrate the channel data from the MongoDB data lake to the MySQL database.

Click "Search and Display Channel Data" to search and retrieve data from the MySQL database based on different search options.

Explore the various query results displayed as tables in the Streamlit application.

Contributing
Contributions to the YouTube Channel Analyzer project are welcome! If you find a bug or have an idea for an enhancement, please open an issue or submit a pull request on the GitHub repository.

