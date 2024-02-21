import json
import d6tflow
import pickle
import os
from dotenv import load_dotenv
from playlist_download import download_transcript
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import TranscriptsDisabled

load_dotenv()
# List of Video IDs
video = []
# The Video ID For A Single Video Stored In .env
stored_video = os.environ['YOUTUBE_VIDEO_ID']


def format_to_json(transcript, vid, course):
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)
    file = vid
    if not os.path.exists(f'{course}/json'):
        os.makedirs(f'{course}/json')
    with open(f'{course}/json/{file}.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)

# Make the call


def get_from_json(plist):
    with open(f'playlists_json/{plist}.json', 'rb') as f:
        data = json.load(f)
        p_videos = []
        for i in data['items']:
            v = i['snippet']['resourceId']['videoId']
            p_videos.append(v)
        f.close()
        return p_videos


playlist = 'psych_significance_biblical_stories'
course = 'psych_significance_biblical_stories'

videos = get_from_json(playlist)


class DownloadTranscriptTask(d6tflow.tasks.TaskPickle):
    language_code = 'en'

    def output(self):
        return d6tflow.targets.PickleTarget(f'{course}/{course}.pkl')

    def run(self):
        if isinstance(videos, list):
            transcripts_pkl = {}
            for vid in videos:
                video_id = vid
                try:
                    transcripts_pkl[vid] = download_transcript(video_id, self.language_code)
                    format_to_json(transcripts_pkl[vid], video_id, course)
                except TranscriptsDisabled:
                    print(f'Transcripts are disabled for video {video_id}')
                    pass
            self.save(transcripts_pkl)

'''
To handle a .pkl you'll need to read and write it. LoadDataTask handles write and read calls to/from handle_pickle(). 
d6tflow is a wrapper for luigi, so you'll need to use luigi's .load() method to read the .pkl.
d6tflow input and output is handy for tracking dependencies, but you can also use luigi's .requires() method to
handle dependencies.
'''


class LoadDataTask(d6tflow.tasks.TaskJson):
    def output(self):
        return d6tflow.targets.JsonTarget('video.json')

    def run(self):
        file = handle_pickle()
        with open("video.json", 'w') as f:
            json.loads(file)
            print(f)
            f.write(file)
            f.close()

# Pickle helper READ function


def handle_pickle():
    # Manually input a pickle file to dump to video.json when prompted
    file = input('Give me a pickle to dump to video.json: ')
    with open(file, 'rb') as f:
        data = pickle.load(f)
        json_string = json.dumps(data)
        f.close()
    return json_string


flow = d6tflow.Workflow()
flow.run(DownloadTranscriptTask)

# videos = get_from_json(playlist)
