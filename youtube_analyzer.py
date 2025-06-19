import streamlit as st
import googleapiclient.discovery
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="YouTube Channel Analyzer",
    page_icon="📺",
    layout="wide"
)

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

def get_all_video_titles_and_views(youtube, channel_id, progress_bar=None, status_text=None):
    """
    Fetch all video titles and view counts from the channel.
    """
    video_data = []
    next_page_token = None
    page_count = 0

    while True:
        page_count += 1
        if status_text:
            status_text.text(f"Fetching page {page_count}...")
        
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
                id=",".join(video_ids)
            )
            video_response = video_request.execute()

            # Extract video titles, view counts, and publish dates
            for video in video_response.get("items", []):
                title = video["snippet"]["title"]
                views = int(video["statistics"]["viewCount"])
                published_at = video["snippet"]["publishedAt"]
                video_data.append((title, views, published_at))

        # Update progress bar
        if progress_bar:
            progress_bar.progress(min(len(video_data) / 1000, 1.0))  # Estimate progress

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

def create_dataframe(video_data):
    """
    Create a pandas DataFrame from video data.
    """
    df = pd.DataFrame(video_data, columns=['Title', 'Views', 'Published'])
    df['Published'] = pd.to_datetime(df['Published'])
    df['Formatted_Views'] = df['Views'].apply(format_views)
    return df.sort_values('Views', ascending=False).reset_index(drop=True)

def main():
    st.title("📺 YouTube Channel Analyzer")
    st.markdown("Analyze any YouTube channel's video performance and view statistics")

    # Sidebar for API key input
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "YouTube Data API Key", 
            type="password",
            help="Enter your YouTube Data API v3 key. Get one from Google Cloud Console."
        )
        
        if st.button("ℹ️ How to get API Key"):
            st.info("""
            1. Go to Google Cloud Console
            2. Create a new project or select existing
            3. Enable YouTube Data API v3
            4. Create credentials (API Key)
            5. Copy and paste the key here
            """)

    # Main interface
    channel_url = st.text_input(
        "🔗 YouTube Channel URL",
        placeholder="https://www.youtube.com/@channelname or https://www.youtube.com/channel/UCxxxxxxx",
        help="Enter the full URL of the YouTube channel you want to analyze"
    )

    if st.button("🔍 Analyze Channel", type="primary"):
        if not api_key:
            st.error("Please enter your YouTube Data API key in the sidebar.")
            return
        
        if not channel_url:
            st.error("Please enter a YouTube channel URL.")
            return

        try:
            # Initialize the YouTube API client
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
            
            with st.spinner("Getting channel information..."):
                # Get the channel ID from the URL
                channel_id = get_channel_id(youtube, channel_url)
                st.success(f"✅ Found channel! Channel ID: {channel_id}")

            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Fetch all video data
            with st.spinner("Fetching video data..."):
                video_data = get_all_video_titles_and_views(
                    youtube, channel_id, progress_bar, status_text
                )
            
            progress_bar.empty()
            status_text.empty()
            
            if not video_data:
                st.warning("No videos found for this channel.")
                return
            
            # Create DataFrame
            df = create_dataframe(video_data)
            
            st.success(f"📊 Analysis complete! Found {len(df)} videos.")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Videos", len(df))
            with col2:
                st.metric("Total Views", format_views(df['Views'].sum()))
            with col3:
                st.metric("Average Views", format_views(df['Views'].mean()))
            with col4:
                st.metric("Most Viewed", format_views(df['Views'].max()))
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Top Videos", "📈 View Distribution", "📅 Timeline", "💾 Download Data"])
            
            with tab1:
                st.subheader("🏆 Top Performing Videos")
                
                # Show top N videos
                top_n = st.slider("Number of top videos to show", 5, min(50, len(df)), 10)
                
                # Display top videos
                for i, row in df.head(top_n).iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{i+1}. {row['Title']}**")
                            st.write(f"📅 Published: {row['Published'].strftime('%Y-%m-%d')}")
                        with col2:
                            st.metric("Views", row['Formatted_Views'])
                        st.divider()
            
            with tab2:
                st.subheader("📊 View Count Distribution")
                
                # Histogram of view counts
                fig_hist = px.histogram(
                    df, 
                    x='Views', 
                    nbins=30,
                    title="Distribution of Video View Counts",
                    labels={'Views': 'View Count', 'count': 'Number of Videos'}
                )
                fig_hist.update_layout(showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Top videos bar chart
                top_20 = df.head(20)
                fig_bar = px.bar(
                    top_20,
                    x='Views',
                    y=top_20['Title'].str[:50],  # Truncate long titles
                    orientation='h',
                    title="Top 20 Videos by View Count",
                    labels={'Views': 'View Count', 'y': 'Video Title'},
                    hover_data=['Title']
                )
                fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                fig_bar.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Views: %{x:,}<extra></extra>')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with tab3:
                st.subheader("📅 Publishing Timeline")
                
                # Views over time
                df_time = df.sort_values('Published')
                fig_timeline = px.scatter(
                    df_time,
                    x='Published',
                    y='Views',
                    title="Video Views Over Time",
                    labels={'Published': 'Publication Date', 'Views': 'View Count'},
                    hover_data=['Title']
                )
                fig_timeline.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Published: %{x}<br>Views: %{y:,}<extra></extra>')
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Monthly upload frequency
                df['Month'] = df['Published'].dt.to_period('M')
                monthly_uploads = df.groupby('Month').size().reset_index(name='Upload_Count')
                monthly_uploads['Month'] = monthly_uploads['Month'].astype(str)
                
                fig_monthly = px.bar(
                    monthly_uploads,
                    x='Month',
                    y='Upload_Count',
                    title="Monthly Upload Frequency",
                    labels={'Month': 'Month', 'Upload_Count': 'Number of Uploads'}
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            with tab4:
                st.subheader("💾 Download Data")
                
                # Prepare CSV data
                csv_data = df[['Title', 'Views', 'Formatted_Views', 'Published']].copy()
                csv_data['Published'] = csv_data['Published'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                csv = csv_data.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"youtube_channel_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Preview of downloadable data
                st.subheader("Data Preview")
                st.dataframe(csv_data, use_container_width=True)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your API key and channel URL, then try again.")

if __name__ == "__main__":
    main()