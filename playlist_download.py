from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
load_dotenv()
channel_name = 'JordanBPeterson'
# channel_name = 'mitocw'
# channel_name = 'mom_harvard'
api_key = os.environ['YOUTUBE_API_KEY']
youtube = build("youtube", "v3", developerKey=api_key)
# Return the transcript as a list of dicts


def download_transcript(video_id, language_code):
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=[language_code])
    return transcript_data


def get_playlist(playlist_id):
    playlist = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50,
    )
    response = playlist.execute()
    with open(f"{channel_name}.json", "w") as outfile:
        json.dump(response, outfile, indent=4)
    return response


# Get the Maps of Meaning playlist
# get_playlist(playlist_id='PL22J3VaeABQCn5nTAx65NRlh1EsKD0UQD')
# Get the MIT OpenCourseWare playlist -> store file in playlists_json
# get_playlist(playlist_id='PLUl4u3cNGP615Y1j9Ok3szAH5DxhFjTHo')
# Get the Harvard MOM playlist
# get_playlist(playlist_id='PLfo-E0A2eFB3tIt913OKAImS-8_q47dpb')
# Get Education and Academia playlist from Dr. Jordan Peterson
# get_playlist(playlist_id='PL22J3VaeABQBl2rBbTaIq-yPWQl09vtfE')
# Get the Meaning, Religion, and Culture playlist
# get_playlist(playlist_id='PL22J3VaeABQC9Rs3rLn5NdVzm4QEkq8hL')
# get The Psychological Significance of the Biblical Stories: Genesis
get_playlist(playlist_id='PL22J3VaeABQD_IZs7y60I3lUrrFTzkpat')
