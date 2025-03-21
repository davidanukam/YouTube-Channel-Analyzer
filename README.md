# YouTube Channel Video Stats Fetcher

Easily fetch all video titles and view counts from any public YouTube channel using the YouTube Data API. This tool extracts video information and saves it to a neatly formatted text file, sorted by view counts in descending order.

## 🚀 Features
- Extract video titles and view counts from any YouTube channel URL.
- Supports standard, custom, and handle-based YouTube URLs.
- Saves data to a `.txt` file, formatted for easy reading.
- Sorts videos by view count (highest to lowest).
- Converts large numbers into human-readable formats (e.g., 100k, 2.5M).

## 📄 Example Output:
Video Title 1 - 2.5M
Video Title 2 - 150k
Video Title 3 - 980

## 🛠️ Requirements
- Python 3.x
- Google API Client Library

Install dependencies:
```bash
pip install google-api-python-client
```

## 🔑 Setup

Get your YouTube Data API v3 key:

- Visit the Google Cloud Console.
- Enable the YouTube Data API v3.
- Create an API key.

Replace the API_KEY variable in main.py with your key:
```python
API_KEY = "YOUR_API_KEY_HERE"
```
## 📂 Usage
Run the script:
```bash
python main.py
```
Then enter the URL of the YouTube channel when prompted (supports /channel/, /c/, and /@ URLs).

The script will:
- Extract the channel ID
- Fetch all videos and their view counts
- Save the data to video_titles_and_views.txt in the project directory

## ⚙️ File Structure
```css
📁 YouTube-Channel-Video-Stats-Fetcher
├── main.py
├── video_titles_and_views.txt  # Output file
└── README.md
```

## 📌 Future Improvements (Ideas)

- Export to CSV or Excel format
- Add support for fetching other stats (likes, comments)
- Create a simple GUI version
- Add progress bar and estimated time

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 💡 Enjoyed using this tool? Star ⭐️ the repo and share it with others!