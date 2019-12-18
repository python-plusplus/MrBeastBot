from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import random
import time
CLIENT_SECRET_FILE = 'client2.json'
SCOPE = ['https://www.googleapis.com/auth/youtube.force-ssl']

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPE)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)


def insert_comment(youtube, video_id, text):
    insert_result = youtube.commentThreads().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                videoId=video_id,
                topLevelComment=dict(
                    snippet=dict(
                        textOriginal=text)
                )
            )
        )
    ).execute()

    comment = insert_result["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("Inserted comment for %s: %s" % (author, text))


def check_activity(youtube, channel_id, max_results):
    list_result = youtube.activities().list(
        part='contentDetails',
        channelId=channel_id,
        maxResults=max_results
    ).execute()

    activity_resources = list_result['items']
    videoId = activity_resources[0]['contentDetails']['upload']['videoId']
    print(videoId)
    return videoId


for a in range(10000):
    video_id = check_activity(youtube, 'UC2UfdGz8-fdBzjT_0eh23Dg', 1)
    if video_id == 'kSMi35oazWs':
        insert_comment(youtube, video_id, str(random.randint(1, 50)))
        time.sleep(1)
