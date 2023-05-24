import streamlit as st
import pymongo
import mysql.connector
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# MongoDB Configuration
MONGO_CONNECTION_STRING = "mongodb+srv://admin:admin1234@cluster0.txdimal.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "youtube_data"
MONGO_COLLECTION_NAME = "channels"

# YouTube API Configuration
YOUTUBE_API_KEY = "AIzaSyBO1xxTFn4K_jVD_Bfb6LFPpPjAxx1GhDo"

# Initialize MongoDB client
mongo_client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
mongo_db = mongo_client[MONGO_DB_NAME]
mongo_collection = mongo_db[MONGO_COLLECTION_NAME]

# Set up MySQL connection
mysql_conn = mysql.connector.connect(
  host="localhost",
  database='youtubeapi',
  user="root",
  password="admin123"
)
mysql_cursor = mysql_conn.cursor()


def get_youtube_data(channel_id):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        response = youtube.channels().list(part="snippet,statistics", id=channel_id).execute()

        channel_data = response["items"][0]
        channel_name = channel_data["snippet"]["title"]
        subscribers = channel_data["statistics"]["subscriberCount"]
        video_count = channel_data["statistics"]["videoCount"]

        # Retrieve playlist ID
        playlist_response = youtube.playlists().list(part="snippet", channelId=channel_id).execute()
        playlist_id = playlist_response["items"][0]["id"]

        return {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "subscribers": subscribers,
            "video_count": video_count,
            "playlist_id": playlist_id
        }
    except HttpError as e:
        st.error(f"An error occurred while accessing the YouTube API: {e}")
        return None


def store_in_mongodb(data):
    mongo_collection.insert_one(data)


def migrate_to_mysql():
    mysql_cursor.execute(f"CREATE TABLE IF NOT EXISTS youtube_api"
                         "(channel_id VARCHAR(255), channel_name VARCHAR(255), "
                         "subscribers INT, video_count INT, playlist_id VARCHAR(255))")

    mongo_cursor = mongo_collection.find()
    for document in mongo_cursor:
        channel_id = document["channel_id"]
        channel_name = document["channel_name"]
        subscribers = document["subscribers"]
        video_count = document["video_count"]
        playlist_id = document["playlist_id"]

        mysql_cursor.execute(f"INSERT INTO youtube_api "
                             "(channel_id, channel_name, subscribers, video_count, playlist_id) "
                             "VALUES (%s, %s, %s, %s, %s)",
                             (channel_id, channel_name, subscribers, video_count, playlist_id))
    mysql_conn.commit()


def search_from_mysql(channel_id):
    mysql_cursor.execute(f"SELECT * FROM youtube_api WHERE channel_id = %s", (channel_id,))
    return mysql_cursor.fetchall()

##------------------------------------------change made--------------------------------#########
# Streamlit App
st.title("YouTube Data Analysis")

channel_id = st.text_input("Enter YouTube Channel ID:")

if st.button("Retrieve Data"):
    channel_data = get_youtube_data(channel_id)
    if channel_data:
        st.success("Data retrieved successfully!")
        store_in_mongodb(channel_data)

if st.button("Migrate Data to MySQL"):
    migrate_to_mysql()
    st.success("Data migrated to MySQL successfully!")

if st.button("Search Data from MySQL"):
    results = search_from_mysql(channel_id)
    if len(results) > 0:
        st.table(results)
    else:
        st.warning("No data found for the provided channel ID in MySQL.")
#------------------------------------sql questions--------------

def search_channel_data():
    # ...

    display_video_channel_names()
    display_channels_with_most_videos()
    display_top_10_viewed_videos()
    display_comments_per_video()
    display_videos_with_most_likes()
    display_total_likes_dislikes_per_video()
    display_total_views_per_channel()
    display_channels_published_in_2022()
    display_average_duration_per_channel()
    display_videos_with_most_comments()

# SQL query outputs as tables
def display_video_channel_names():
    query = """
    SELECT v.video_name, c.channel_name
    FROM videos v
    JOIN channels c ON v.channel_id = c.channel_id
    """
    result = mysql_conn.execute(query)
    st.subheader("Video and Channel Names")
    st.table(result)

def display_channels_with_most_videos():
    query = """
    SELECT c.channel_name, COUNT(v.video_id) as video_count
    FROM channels c
    JOIN videos v ON c.channel_id = v.channel_id
    GROUP BY c.channel_name
    ORDER BY video_count DESC
    """
    result = mysql_conn.execute(query)
    st.subheader("Channels with Most Videos")
    st.table(result)

def display_top_10_viewed_videos():
    query = """
    SELECT v.video_name, c.channel_name, v.views
    FROM videos v
    JOIN channels c ON v.channel_id = c.channel_id
    ORDER BY v.views DESC
    LIMIT 10
    """
    result = mysql_conn.execute(query)
    st.subheader("Top 10 Most Viewed Videos")
    st.table(result)

def display_comments_per_video():
    query = """
    SELECT v.video_name, COUNT(c.comment_id) as comment_count
    FROM videos v
    JOIN comments c ON v.video_id = c.video_id
    GROUP BY v.video_name
    """
    result = mysql_conn.execute(query)
    st.subheader("Comments per Video")
    st.table(result)

def display_videos_with_most_likes():
    query = """
    SELECT v.video_name, c.channel_name, v.likes
    FROM videos v
    JOIN channels c ON v.channel_id = c.channel_id
    ORDER BY v.likes DESC
    LIMIT 10
    """
    result = mysql_conn.execute(query)
    st.subheader("Videos with Most Likes")
    st.table(result)

def display_total_likes_dislikes_per_video():
    query = """
    SELECT v.video_name, v.likes, v.dislikes
    FROM videos v
    """
    result = mysql_conn.execute(query)
    st.subheader("Total Likes and Dislikes per Video")
    st.table(result)

def display_total_views_per_channel():
    query = """
    SELECT c.channel_name, SUM(v.views) as total_views
    FROM channels c
    JOIN videos v ON c.channel_id = v.channel_id
    GROUP BY c.channel_name
    """
    result = mysql_conn.execute(query)
    st.subheader("Total Views per Channel")
    st.table(result)

def display_channels_published_in_2022():
    query = """
    SELECT c.channel_name
    FROM channels c
    JOIN videos v ON c.channel_id = v.channel_id
    WHERE YEAR(v.publish_date) = 2022
    GROUP BY c.channel_name
    """
    result = mysql_conn.execute(query)
    st.subheader("Channels Published Videos in 2022")
    st.table(result)

def display_average_duration_per_channel():
    query = """
    SELECT c.channel_name, AVG(v.duration) as avg_duration
    FROM channels c
    JOIN videos v ON c.channel_id = v.channel_id
    GROUP BY c.channel_name
    """
    result = mysql_conn.execute(query)
    st.subheader("Average Duration per Channel")
    st.table(result)

def display_videos_with_most_comments():
    query = """
    SELECT v.video_name, c.channel_name, COUNT(c.comment_id) as comment_count
    FROM videos v
    JOIN channels c ON v.channel_id = c.channel_id
    JOIN comments cm ON v.video_id = cm.video_id
    GROUP BY v.video_name
    ORDER BY comment_count DESC
    LIMIT 10
    """
    result = mysql_conn.execute(query)
    st.subheader("Videos with Most Comments")
    st.table(result)


