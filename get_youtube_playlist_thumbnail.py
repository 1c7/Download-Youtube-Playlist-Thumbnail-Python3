import requests
import os
import re
'''
http://youtubetool.net/download-thumbnail-youtube-from-playlist.html

1. 去这个网址，黏贴 Youtube 播放列表 URL 进去。
2. 得到一大堆的图片地址，是一行字符串的形式。
3. 复制过来。
4. 运行。等下载就行了。
5. 文件夹记得填名字，文件都会放在里面。

专门针对 Crash Course 做了优化。
文件名如果包含数字，最后一个数字会在前面。比如

原名是
Was Gatsby Great? The Great Gatsby Part 2 Crash Course English Literature #5

但是保存的文件名是
5. Was Gatsby Great? The Great Gatsby Part 2 Crash Course English Literature #5

是为了方便排序。
'''

dire = 'Physics'
l='''

https://i.ytimg.com/vi/ZM8ECpBuQYE/maxresdefault.jpghttps://i.ytimg.com/vi/ObHJJYvu3RE/maxresdefault.jpghttps://i.ytimg.com/vi/jLJLXka2wEM/maxresdefault.jpghttps://i.ytimg.com/vi/w3BhzYI6zXU/maxresdefault.jpghttps://i.ytimg.com/vi/kKKM8Y-u7ds/maxresdefault.jpghttps://i.ytimg.com/vi/fo_pmp5rtzo/maxresdefault.jpghttps://i.ytimg.com/vi/bpFK2VCRHUs/maxresdefault.jpghttps://i.ytimg.com/vi/7gf6YpdvtE0/maxresdefault.jpghttps://i.ytimg.com/vi/w4QFJb9a8vo/maxresdefault.jpghttps://i.ytimg.com/vi/Y-QOfc2XqOk/maxresdefault.jpghttps://i.ytimg.com/vi/fmXFWi-WfyU/maxresdefault.jpghttps://i.ytimg.com/vi/b-HZ1SZPaQw/maxresdefault.jpghttps://i.ytimg.com/vi/9cbF9A6eQNA/maxresdefault.jpghttps://i.ytimg.com/vi/b5SqYuWT4-4/maxresdefault.jpghttps://i.ytimg.com/vi/fJefjG3xhW0/maxresdefault.jpghttps://i.ytimg.com/vi/jxstE6A_CYQ/maxresdefault.jpghttps://i.ytimg.com/vi/TfYCnOvNnFU/maxresdefault.jpghttps://i.ytimg.com/vi/qV4lR9EWGlY/maxresdefault.jpghttps://i.ytimg.com/vi/XDsk6tZX55g/maxresdefault.jpghttps://i.ytimg.com/vi/6BHbJ_gBOk0/maxresdefault.jpghttps://i.ytimg.com/vi/WOEvvHbc240/maxresdefault.jpghttps://i.ytimg.com/vi/tuSC0ObB-qY/maxresdefault.jpghttps://i.ytimg.com/vi/4i1MUWJoI0U/maxresdefault.jpghttps://i.ytimg.com/vi/p1woKh2mdVQ/maxresdefault.jpghttps://i.ytimg.com/vi/TFlVWf8JX4A/maxresdefault.jpghttps://i.ytimg.com/vi/mdulzEfQXDE/maxresdefault.jpghttps://i.ytimg.com/vi/ZrMltpK6iAw/maxresdefault.jpghttps://i.ytimg.com/vi/HXOok3mfMLM/maxresdefault.jpghttps://i.ytimg.com/vi/g-wjP1otQWI/maxresdefault.jpghttps://i.ytimg.com/vi/-w-VTw0tQlE/maxresdefault.jpghttps://i.ytimg.com/vi/vuCJP_5KOlI/maxresdefault.jpghttps://i.ytimg.com/vi/s94suB5uLWw/maxresdefault.jpghttps://i.ytimg.com/vi/5fqwJyt4Lus/maxresdefault.jpghttps://i.ytimg.com/vi/pQp6bmJPU_0/maxresdefault.jpghttps://i.ytimg.com/vi/9kgzA0Vd8S8/maxresdefault.jpghttps://i.ytimg.com/vi/Jveer7vhjGo/maxresdefault.jpghttps://i.ytimg.com/vi/K40lNL3KsJ4/maxresdefault.jpghttps://i.ytimg.com/vi/Oh4m8Ees-3Q/maxresdefault.jpghttps://i.ytimg.com/vi/IRBfpBPELmE/maxresdefault.jpghttps://i.ytimg.com/vi/-ob7foUzXaY/maxresdefault.jpghttps://i.ytimg.com/vi/SddBPTcmqOk/maxresdefault.jpghttps://i.ytimg.com/vi/AInCqm5nCzw/maxresdefault.jpghttps://i.ytimg.com/vi/7kb1VT0J3DE/maxresdefault.jpghttps://i.ytimg.com/vi/qO_W70VegbQ/maxresdefault.jpghttps://i.ytimg.com/vi/lUhJL7o6_cA/maxresdefault.jpghttps://i.ytimg.com/vi/VYxYuaDvdM0/maxresdefault.jpg
'''

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

# 处理返回的 json。然后下载图片。
r = requests.get(url)
json = r.json()
for one_item in json['items']:
    title = one_item['snippet']['title'].replace(':', '')
    number_list = map(int, re.findall(r'\d+', title)) # https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python
    number_list = list(number_list)
    if len(number_list) > 0:
        filename = str(number_list[-1]) + ". " + title
    else:
        filename = title

    max_url = one_item['snippet']['thumbnails']['maxres']['url']
    wget_command = "wget -O '{}.jpg' {}".format(filename, max_url)
    print(wget_command)
    print()
    os.system(wget_command)
