# YouTube Channel Analyzer

A comprehensive tool to analyze any public YouTube channel's video performance and statistics. Available as both a command-line script and an interactive web application built with Streamlit.

## 🚀 Features

### 📊 **Web App (Streamlit)**

- **Interactive Dashboard**: Modern web interface with real-time analytics
- **Visual Analytics**: Charts and graphs showing view distributions, trends over time
- **Comprehensive Metrics**: Total videos, views, averages, and top performers
- **Timeline Analysis**: Publication dates and monthly upload frequency
- **Data Export**: Download results as CSV with timestamps
- **Progress Tracking**: Real-time progress indicators during data fetching

### 💻 **Command Line Tool**

- Extract video titles and view counts from any YouTube channel URL
- Supports standard, custom, and handle-based YouTube URLs (`/channel/`, `/c/`, `/@`)
- Saves data to formatted text files, sorted by view counts
- Converts large numbers into human-readable formats (e.g., 100k, 2.5M)

## 📊 Example Output

### Web App Dashboard:

- **Metrics Overview**: Total Videos: 248 | Total Views: 15.2M | Average Views: 61.3k
- **Interactive Charts**: View distribution histograms, top video rankings
- **Timeline Visualization**: Scatter plots of views over publication dates

### Command Line Output:

```
Video Title 1 - 2.5M
Video Title 2 - 150k
Video Title 3 - 980
```

## 🛠️ Requirements

### For Web App:

```bash
pip install streamlit googleapiclient-discovery pandas plotly
```

### For Command Line Tool:

```bash
pip install google-api-python-client
```

## 🔑 Setup

### Get your YouTube Data API v3 key:

1. Visit the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Copy your API key

### For Command Line Tool:

Replace the API_KEY variable in `main.py`:

```python
API_KEY = "YOUR_API_KEY_HERE"
```

### For Web App:

Enter your API key directly in the web interface sidebar (secure input field).

## 📂 Usage

### 🌐 **Web Application (Recommended)**

```bash
streamlit run youtube_analyzer.py
```

1. Open your browser to the provided URL (usually http://localhost:8501)
2. Enter your YouTube Data API key in the sidebar
3. Paste any YouTube channel URL
4. Click "Analyze Channel" and explore the interactive dashboard

### 💻 **Command Line Tool**

```bash
python youtube_analyzer_terminal.py
```

Enter the YouTube channel URL when prompted. Supports:

- `https://www.youtube.com/channel/UCxxxxxxx`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/@username`

## ⚙️ File Structure

```
📁 YouTube-Channel-Analyzer
├── 🌐 youtube_analyzer.py           # Streamlit web app
├── 💻 youtube_analyzer_terminal.py  # Command line tool
├── 📄 video_titles_and_views.txt    # CLI output file
├── 📊 exported_data.csv             # Web app export files
└── 📖 README.md
```

## 🎯 Use Cases

- **Content Creators**: Analyze competitor channels and trending content
- **Marketers**: Research popular video topics and engagement patterns
- **Researchers**: Study YouTube content trends and viewer behavior
- **Data Analysis**: Export data for further statistical analysis
- **Channel Optimization**: Identify successful content patterns

## 🆕 What's New in Web Version

- **Real-time Progress Tracking**: See fetch progress with live updates
- **Interactive Visualizations**: Plotly charts for better data exploration
- **Advanced Filtering**: View top N videos, timeline analysis
- **Export Capabilities**: Download data in CSV format with timestamps
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Error Handling**: User-friendly error messages and validation

## 📈 Analytics Features

### 📊 **View Distribution Analysis**

- Histogram of video view counts
- Top 20 videos bar chart with hover details
- Statistical insights (mean, median, max views)

### 📅 **Timeline Analysis**

- Scatter plot of views vs. publication date
- Monthly upload frequency charts
- Trend identification over time

### 🏆 **Top Performers**

- Configurable top N videos display
- View count metrics and publication dates
- Easy identification of viral content

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to:

- Open a pull request with improvements
- Report bugs or suggest features in Issues
- Share your analytics insights and use cases

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 🔮 Future Roadmap

- [ ] **Enhanced Analytics**: Like/dislike ratios, comment analysis
- [ ] **Batch Processing**: Analyze multiple channels simultaneously
- [ ] **API Integration**: Direct integration with other analytics platforms
- [ ] **Machine Learning**: Content performance prediction
- [ ] **Scheduling**: Automated periodic channel monitoring
- [ ] **Mobile App**: Native mobile application

## ⭐️ Support

**Enjoyed using this tool?**

- Star ⭐️ the repository
- Share it with fellow creators and analysts
- Follow for updates on new features

---

**Built with ❤️ for the YouTube analytics community**
