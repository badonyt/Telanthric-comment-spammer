def send_message(yeaornah, video_ids):
    
    video_id = video_ids
    access_token = secret_data["secret_data"]["access_token"]
    api_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet'
    if yeaornah != 0:
        access_token = yeaornah

    
    response = requests.post(api_url, headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }, json={
        'snippet': {
            'topLevelComment': {
                'snippet': {
                    'videoId': video_id,
                    'textOriginal': secret_data["user_data"]["comment"]
                }
            },
         'channelId': '<channel ID>'
        }
    })

    
    if response.status_code == 200:
        print('Comment posted successfully!')
    else:
        print('Error posting comment', response.status_code)
        print(json.dumps(response.json(), indent=4))
    
    
    if response.status_code == 401:
        refresh_token = secret_data["secret_data"]["refresh_token"]
        client_id = secret_data["secret_data"]["client_id"]
        client_secret = secret_data["secret_data"]["client_secret"]
        token_endpoint = 'https://oauth2.googleapis.com/token'
        grant_type = 'refresh_token'
    
        response = requests.post(token_endpoint, data={
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': grant_type,
        })
    
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            send_message(access_token, video_id)    
        else:
            print('Error refreshing access token')














import json

  
# Opening JSON file
f = open('data.json')
  
# returns JSON object as 
# a dictionary
secret_data = json.load(f)

f.close()

import googleapiclient.discovery
import requests
import time
First = True
previous = 0

api_key = secret_data["secret_data"]["api_key"]
channel_id = secret_data["user_data"]["channel_id"]
while True:
    
    

    api_service_name = "youtube"
    api_version = "v3"
    
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


    
    max_results = 2 


    search_response = youtube.search().list(
        part="id",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=max_results
    ).execute()


    video_ids = [item["id"]["videoId"] for item in search_response["items"]]


    videos_response = youtube.videos().list(
        part="snippet",
        id=",".join(video_ids)
    ).execute()

    main_data =  {0: {"title": videos_response["items"][0]["snippet"]["title"],"publication":videos_response["items"][0]["snippet"]["publishedAt"],"id":videos_response["items"][0]["id"]},1: {"title": videos_response["items"][1]["snippet"]["title"],"publication":videos_response["items"][1]["snippet"]["publishedAt"],"id":videos_response["items"][1]["id"]}}

    if First == True:
        previous = main_data    
        First = False
        print(f"first \n previous:{previous} \n main_dat:{main_data}")
    elif First == False and main_data[0]["id"] != previous[0]["id"] and main_data[0]["publishedAt"] != previous[0]["publishedAt"]:
        send_message(0, previous[0]["id"])
        previous = main_data
        print("nice")
    else:
        print("failed")
    
    

    time.sleep((60 * secret_data["user_data"]["minutes"]))
    



#send_message(0,"NWvFS1-vCgs")