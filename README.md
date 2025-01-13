# SpotifyDataAnalyzer

SpotifyDataAnalyzer is a tool that utilizes user data obtained from Spotify to analyze listening habits and preferences, and then creates personalized playlists based on the analysis. It supports processing data from multiple users simultaneously.

## Features

- **Analyze Spotify Data**: Reads and processes user data provided by Spotify to extract meaningful insights.
- **Playlist Generation**: Automatically generates playlists tailored to user preferences based on the analyzed data.
- **Multi-User Support**: Allows simultaneous analysis of data from multiple users.

## Technologies Used

- **Spotify**: Integration with Spotify data export.
- **JSON**: Processes and interprets data provided in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SpotifyDataAnalyzer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd SpotifyDataAnalyzer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure you have your Spotify data ready in JSON format. You can request your Spotify data [here](https://www.spotify.com/account/privacy/).

## Usage

1. Place your Spotify data JSON file(s) in the `data/` directory(you will have to create the directory yourself).
2. Run the script:
   ```bash
   python src/main.py
   ```

## Contact

For questions or feedback, feel free to reach out on Discord: **Zancmok**.

---

Enjoy analyzing your Spotify data and discovering new insights with SpotifyDataAnalyzer!

