import requests
import os
import re


'''
https://developers.google.com/youtube/v3/quickstart/python
'''


###### 文件夹名字写这里 (图片都会放在这个文件夹里)
dire = 'World History'

###### 字符串黏贴到这里

# 改目录，待会可是要下载文件的。
if not os.path.exists(dire):
    os.makedirs(dire)
os.chdir(dire)

# 去掉回车
s = l.replace('\r', '').replace('\n', '').split('https://')
# 去掉列表空元素
str_list = filter(None, s)
# 拿到逗号拼起来的 id list

id_list = []
for one in str_list:
    one_url_list =  one.split('/')
    i = one_url_list[2]
    id_list.append(i)
join_id = ",".join(id_list)
# 拼到 url 里去。
url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key=AIzaSyBYQ9t7cv64bKkB4g_bZOyrawlLHLwyqu0".format(join_id)

r = requests.get(url)

# 处理返回的 json。然后下载图片。
json = r.json()
for one_item in json['items']: # 假设了每个 items 就是一个视频。
    title = one_item['snippet']['title'].replace(':', '')
    number_list = map(int, re.findall(r'\d+', title)) # https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python
    number_list = list(number_list)

    # 有时文件名里一个数字也没有
    if len(number_list) > 0:
        filename = str(number_list[-1]) + ". " + title
    else:
        filename = title

    # 有时视频会没有 maxres, 那就只能求次了。
    try:
        image_url = one_item['snippet']['thumbnails']['maxres']['url']
    except KeyError:
        image_url = one_item['snippet']['thumbnails']['standard']['url']

    wget_command = "wget -O '{}.jpg' {}".format(filename, image_url)
    print(wget_command)
    print()
    os.system(wget_command)


# 有时候会变成发请求循环文件名了，要看看哪里错了。有空的话。
