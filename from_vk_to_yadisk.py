import requests
import time
import os
from datetime import datetime

disk_token = 'OAuth ****СЮДА НУЖНО ВСТАВИТЬ НОМЕР ТОКЕНА*****'
vk_id = input('Введите ID Вконтакте: ')

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


    def save_photos(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id' : 'profile',
            'extended' : 1,
            'photo_sizes' : 1,
            'count': 5,
        }
        res = requests.get(photos_url, params={**self.params, **photos_params})
        res.raise_for_status()
        photos_list = res.json()['response']['items']
        user_photos = dict()
        info_list = list()
        for picture in photos_list:
                for size in picture['sizes']:
                        info = dict()
                        if size['type'] == 'w':
                            user_photos[picture['likes']['count']] = size['url']
                            info['size'] = size['type']
                            info['file_name'] = str(picture['likes']['count']) + ".jpg"
                            info_list.append(info)
                        elif size['type'] == 'w' and picture['likes']['count'] in user_photos.keys():
                            picture['likes']['count'] = str(picture['likes']['count']) +\
                            ' дата ' + str(datetime.fromtimestamp((picture['date'])))[0:-9]
                            user_photos[picture['likes']['count']] = size['url']
                            info['size'] = size['type']
                            info['file_name'] = str(picture['likes']['count']) + ".jpg"
                            info_list.append(info)
        with open('file.json', 'wt', encoding='utf-8') as f:
            f.write(str(info_list))
        return user_photos


begemot = VkUser('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008')


class YaDiskloader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_data):
        folder_name = "Folder"
        new_folder = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={'path': folder_name},
            headers={"Authorization": self.token},
        )
        new_folder.raise_for_status()
        for key, value in file_data.items():
            file_name = str(key) + ".jpg"
            file_url = value
            print(f'Идёт загрузка файла {file_name}')
            post_url = requests.post(
                f'https://cloud-api.yandex.net/v1/disk/resources/upload',
                params={'path': os.path.join(folder_name + '/' + file_name), "url": file_url, 'overwrite': 'true'},
                headers={"Authorization": self.token},
            )
            post_url.raise_for_status()
            time.sleep(1)
            print(f'Загрузка файла {file_name} завершена')
        return f'Все фотографии загружены на Яндекс Диск в папку {folder_name}'


loader = YaDiskloader(disk_token)


sorted_photos = begemot.save_photos(vk_id)
print(loader.upload(sorted_photos))
