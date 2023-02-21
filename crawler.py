
import time
import json
import random
import requests
import pandas as pd

YouTube_API_root = "https://www.googleapis.com/youtube/v3/search?"


def fetch_channel_stat(key, channel_id):
    """
    fetech channel's statistics by its channel_id
    """
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?key={key}&id={channel_id}&part=snippet, statistics"
        re = requests.get(url)

        channel_title = re.json()["items"][0]["snippet"]["title"]
        total_view = re.json()["items"][0]["statistics"]["viewCount"]
        total_video = re.json()["items"][0]["statistics"]["videoCount"]
        total_subscriber = re.json()["items"][0]["statistics"]["subscriberCount"]
        
    except Exception as e:
        print(f"Error occured: {e}")
    
    return channel_title, total_view, total_video, total_subscriber


def fetch_video_list(key, channel_id, max_result=50, check=True):
    """
    fetch channel's video_list by its channel_id
    """
    vid_list = []
    url_list = []

    root = "https://www.youtube.com/watch?v="

    # first request
    url = f"{YouTube_API_root}key={key}&channelId={channel_id}&type=video&order=date&maxResults={max_result}"
    print(f"Start fetching video list of 【{channel_id}】")
    print(url)

    re = requests.get(url)
    data = re.json()

    for i in range(len(data["items"])):
        vid_list.append(data["items"][i]["id"]["videoId"])

    while check==True:
        try:
            # get next page token
            nextPageToken = data["nextPageToken"]
            print(f"Successfully fetched-next-page token: {nextPageToken}")

            # second request by next page token
            url = f"{YouTube_API_root}key={key}&channelId={channel_id}&type=video&order=date&maxResults={max_result}&pageToken={nextPageToken}"
            print(url)
            
            re = requests.get(url)
            data = re.json()

            for i in range(len(data["items"])):
                vid_list.append(data["items"][i]["id"]["videoId"])

            # check for duplication
            print(len(set(vid_list)))

        except Exception as e:
            check = False
            print(f"Error occured: {e}")
            print(f"No next page token, end loop")
            print(f"Total lengths: {len(set(vid_list))}")

    for i in range(len(vid_list)):
        url_list.append(root+vid_list[i])
        
    return vid_list, url_list


def fetch_video_info(key, vid_list):
    """
    fetch video's information by its ID
    """
    tags = []
    title = []
    viewCount = []
    likeCount = []
    publishedAt = []
    description = []
    commentCount = []
    channelTitle = []
    favoriteCount = []
    
    for i in range(len(vid_list)):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&key={key}&id={vid_list[i]}"
        
        re = requests.get(url)
        print(f"{i}. Crawling: {url}")

        data = re.json()

        # fetch video statistics
        try:
            viewCount.append(data["items"][0]["statistics"]["viewCount"])
        except Exception as e:
            viewCount.append(-1)
            print(f"Error occured: {e}")
        try:
            likeCount.append(data["items"][0]["statistics"]["likeCount"])
        except Exception as e:
            likeCount.append(-1)
            print(f"Error occured: {e}")
        try:
            commentCount.append(data["items"][0]["statistics"]["commentCount"])
        except Exception as e:
            commentCount.append(-1)
            print(f"Error occured: {e}")
        try:
            favoriteCount.append(data["items"][0]["statistics"]["favoriteCount"])
        except Exception as e:
            favoriteCount.append(-1)
            print(f"Error occured: {e}")


        # fetch video information
        try:
            tags.append(data["items"][0]["snippet"]["tags"])
        except Exception as e:
            tags.append(-1)
            print(f"Error occured: {e}")
        try:
            title.append(data["items"][0]["snippet"]["title"])
        except Exception as e:
            title.append(-1)
            print(f"Error occured: {e}")
        try:
            publishedAt.append(data["items"][0]["snippet"]["publishedAt"])
        except Exception as e:
            publishedAt.append(-1)
            print(f"Error occured: {e}")
        try:
            description.append(data["items"][0]["snippet"]["description"])
        except Exception as e:
            description.append(-1)
            print(f"Error occured: {e}")
        try:
            channelTitle.append(data["items"][0]["snippet"]["channelTitle"])
        except Exception as e:
            channelTitle.append(-1)
            print(f"Error occured: {e}")

        if i % 50 == 0 and i != 0:
            t = random.randint(2, 4)
            print(f"Sleep for {t} secs")
            time.sleep(t)
            
    return viewCount, likeCount, favoriteCount, commentCount, publishedAt, title, description, channelTitle, tags

