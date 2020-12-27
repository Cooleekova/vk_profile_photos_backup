from Class_DiskLoader import DiskLoader
from Class_VkUser import VkUser


disk_token = 'OAuth ****СЮДА НУЖНО ВСТАВИТЬ НОМЕР ТОКЕНА*****'
key_id = str(input('Введите идентификатор пользователя VK или короткое имя (screen_name): '))


test_user = VkUser('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008')
loader = DiskLoader(disk_token)

if __name__ == "__main__":
    sorted_photos = test_user.save_photos(key_id)
    print(loader.upload(sorted_photos))
