## App for backup profile photos from social net [vk.com](https://vk.com/) to the cloud storage [Yandex.Disk](https://disk.yandex.com/)  

The app saves VK user's profile photos to the Yandex Disk specified by the user.

The number of likes is used for photo titles, and if number of likes is the same, then it uses number of likes and upload date.

Information about uploaded photos is being saved in a json file.

### How it works: 

**User enters:**
1. user id in VK;
2. personal token from [Yandex.Disk Polygon](https://yandex.ru/dev/disk/poligon/).

**Output:**
1. Photos added to Yandex.Disk.
2. Json file with information about uploaded photos in following format:
```
      [{
      "filename": "34.jpg",
      "size": "g"
      }]
```
