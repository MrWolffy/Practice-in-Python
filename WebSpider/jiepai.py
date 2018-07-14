import requests
import os
from urllib.parse import urlencode
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    param = {
        "offset": offset,
        "format": "json",
        "keyword": "街拍",
        "autoload": "true",
        "count": "20",
        "cur_tab": "3",
        'from': 'gallery',
    }
    url = "http://www.toutiao.com/search_content/?" + urlencode(param)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    data = json.get("data")
    if data:
        for item in data:
            image_list = item.get("image_list")
            title = item.get("title")
            if image_list:
                for image in image_list:
                    yield {
                        "image": image.get("url"),
                        "title": title
                    }


def save_image(item):
    if not os.path.exists(item.get("title")):
        os.mkdir(item.get("title"))
    try:
        local_image_url = item.get('image')
        new_image_url = local_image_url.replace('list', 'large')
        response = requests.get('http:' + new_image_url)
        if response.status_code == 200:
            file_path = str.format("{0}/{1}.jpg", item.get("title"), md5(response.content).hexdigest())
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(response.content)
            else:
                print("Already Downloaded", file_path)
    except requests.ConnectionError:
        print("Failed to Save Image")


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 5

if __name__ == "__main__":
    pool = Pool()
    groups = (x * 20 for x in range(GROUP_START, GROUP_END + 1))
    pool.map(main, groups)
    pool.close()
    pool.join()
    '''for i in range(GROUP_START, GROUP_END + 1):
        main(i * 20)'''
