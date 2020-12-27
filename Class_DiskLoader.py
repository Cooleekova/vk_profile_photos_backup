import requests
import time
import os
import datetime
from datetime import datetime


class DiskLoader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_data):
        folder_id = file_data[1]
        current_time = datetime.now().strftime("%H.%M.%S")
        folder_name = f'Фото "{folder_id}" {current_time}'
        new_folder = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={'path': folder_name},
            headers={"Authorization": self.token},
        )
        new_folder.raise_for_status()
        for key, value in file_data[0].items():
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
        return f'Фотографии профиля {folder_id} загружены на Диск в папку {folder_name}'
