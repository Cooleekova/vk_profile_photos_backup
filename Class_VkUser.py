import requests
import datetime
from datetime import datetime
import json


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token: str, version='5.126'):
        self.token = token
        self.version = version
        self.params = {
            "access_token": self.token,
            'v': self.version,
        }
        self.owner_id = requests.get(self.url+'users.get', self.params).json()['response'][0]['id']

    def save_photos(self, user_id=None, size=None):
        if user_id is None:
            user_id = self.owner_id
        else:
            user_id = requests.get(
                self.url + 'users.get',
                params={**self.params, 'user_ids': user_id}).json()['response'][0]['id']
        input_count = int(input('Введите максимальное количество загружаемых фотографий\n'
                                '(число от 1 до 1000): '))
        quantity = int(input_count)
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': quantity,
        }
        res = requests.get(photos_url, params={**self.params, **photos_params})
        res.raise_for_status()
        photos_list = res.json()['response']['items']
        user_photos = dict()
        info_list = list()
        for picture in photos_list:
            pic_name = picture['likes']['count']
            new_date = str(datetime.fromtimestamp((picture['date'])))
            new_pic_name = str(pic_name) + ' дата ' + new_date[0:-9]
            if pic_name in user_photos.keys():
                pic_name = new_pic_name
            elif pic_name not in user_photos.keys():
                pic_name = pic_name
            info = dict()
            for size in picture['sizes']:
                if size['type'] == 'x':
                    user_photos[pic_name] = size['url']
                elif size['type'] == 'y':
                    user_photos[pic_name] = size['url']
                elif size['type'] == 'z':
                    user_photos[pic_name] = size['url']
                elif size['type'] == 'w':
                    user_photos[pic_name] = size['url']
            info['file_name'] = str(pic_name) + ".jpg"
            info['size'] = size['type']
            info_list.append(info)
        with open('file.json', 'w', encoding='utf-8') as f:
            json.dump(info_list, f, ensure_ascii=False, indent=2)
        return user_photos, user_id
