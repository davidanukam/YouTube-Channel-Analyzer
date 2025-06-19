import googleapiclient.discovery
import urllib.parse

# Replace with your YouTube Data API key
API_KEY = "YOUR_API_KEY_HERE"

def get_channel_id(youtube, channel_url):
    """
    Extract the channel ID from the channel URL.
    """
    if "/channel/" in channel_url:
        # If the URL contains the channel ID directly
        return channel_url.split("/channel/")[-1]
    elif "/@" in channel_url or "/c/" in channel_url:
        # If the URL contains a custom handle (e.g., @username or /c/username)
        handle = channel_url.split("/")[-1]
        request = youtube.search().list(
            q=handle,
            part="snippet",
            type="channel",
            maxResults=1
        )
        response = request.execute()
        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["channelId"]
    raise ValueError("Unable to extract channel ID from the URL.")

def get_all_video_titles_and_views(youtube, channel_id):
    """
    Fetch all video titles and view counts from the channel.
    """
    video_data = []
    next_page_token = None

    while True:
        # Fetch videos from the channel's uploads playlist
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=f"UU{channel_id[2:]}",  # Uploads playlist ID
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video IDs
        video_ids = [item["snippet"]["resourceId"]["videoId"] for item in response.get("items", [])]

        # Fetch video statistics (including view counts)
        if video_ids:
            video_request = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids))
            video_response = video_request.execute()

            # Extract video titles and view counts
            for video in video_response.get("items", []):
                title = video["snippet"]["title"]
                views = int(video["statistics"]["viewCount"])
                video_data.append((title, views))

        # Check if there are more pages
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_data

def format_views(views):
    """
    Format the view count into a human-readable format (e.g., 100k, 20M).
    """
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.0f}k"
    else:
        return str(views)

def save_titles_and_views_to_file(video_data, filename="video_titles_and_views.txt"):
    """
    Save video titles and view counts to a text file.
    """
    # Sort video data by views in descending order
    video_data.sort(key=lambda x: x[1], reverse=True)

    with open(filename, "w", encoding="utf-8") as file:
        for title, views in video_data:
            formatted_views = format_views(views)
            file.write(f"{title} - {formatted_views}\n")
    print(f"Saved {len(video_data)} video titles and views to {filename}")

def main():
    # Initialize the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    # Ask the user for the YouTube channel URL
    channel_url = input("Enter the YouTube channel URL: ").strip()

    try:
        # Get the channel ID from the URL
        channel_id = get_channel_id(youtube, channel_url)
        print(f"Channel ID: {channel_id}")

        # Fetch all video titles and view counts
        video_data = get_all_video_titles_and_views(youtube, channel_id)
        print(f"Found {len(video_data)} videos.")

        # Save titles and views to a text file
        save_titles_and_views_to_file(video_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()