import os
import sys
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import unittest
from youku import YoukuUpload

class YoutubeToYouku(unittest.TestCase):

    def __init__(self):
        url_video = 'https://www.youtube.com/watch?v=B7bqAsxee4I'
        # replace with your youtube download path. use comolete file path, not use ~/video/youtube
        dowload_path = '/home/fxt0706/video/youtube'
        # change video_name to your onine title of YouTube video
        video_name = 'your video name'
        # replace client_id and refresh_token with your parameter
        client_id = '999*******0b'
        refresh_token = 'c8*************81'
        upload_path = dowload_path + '/' + video_name + '.mp4'

        # input the info of video
        self.video_info = {
            'title' : u'your video name',
            'tags' : 'Google',
            'description' : '',
            'category' : ''
        }

        self.url_renew = 'https://api.youku.com/oauth2/token.json'
        self.payloads_renew = {'grant_type':'refresh_token'}
        self.payloads_renew['client_id'] = client_id
        self.payloads_renew['refresh_token'] = refresh_token


        if(self.dowload(dowload_path,url_video) == True):
            print('Start upload')
            self.get_access_token()
            youku_obj = YoukuUpload(client_id, self.my_access_token, upload_path)
            youku_obj.upload(self.video_info)
            youku_obj.check()
            youku_obj.commit()


    def dowload(self,dowload_path, url_video):
        # if GFW existed, use proxychains to download or add HTTP proxy to var cmd like
        # ... +'-x 127.0.0.1:8087'
        cmd = 'proxychains you-get --itag=18 -o ' + dowload_path + ' \'' + url_video + '\''
        print(cmd)
        cmd_re = subprocess.call(cmd, shell=True)
        if (cmd_re == 0):
            return True
        else:
            print("Download failed. \nPlease make sure your internet connected and check the url again")


    def get_access_token(self):
        json_renew = requests.post(url=self.url_renew, data=self.payloads_renew).json()
        print(json_renew)
        self.my_access_token = json_renew['access_token']


if __name__ == '__main__':
    YoutubeToYouku()
