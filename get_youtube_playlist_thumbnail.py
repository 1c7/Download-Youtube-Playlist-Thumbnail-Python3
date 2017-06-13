import requests
import os
import re
'''
下载播放列表里的所有 thumbnails (最高像素 1280x720 maxres)

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

方便排序。
'''

###### 文件夹名字写这里 (图片都会放在这个文件夹里)
dire = 'World History'

###### 字符串黏贴到这里
l='''
https://i.ytimg.com/vi/Yocja_N5s1I/maxresdefault.jpghttps://i.ytimg.com/vi/n7ndRwqJYDM/maxresdefault.jpghttps://i.ytimg.com/vi/sohXPx_XZ6Y/maxresdefault.jpghttps://i.ytimg.com/vi/Z3Wvw6BivVI/maxresdefault.jpghttps://i.ytimg.com/vi/Q-mkVSasZIM/maxresdefault.jpghttps://i.ytimg.com/vi/8Nn5uqE3C9w/maxresdefault.jpghttps://i.ytimg.com/vi/ylWORyToTo4/maxresdefault.jpghttps://i.ytimg.com/vi/0LsrkWDCvxg/maxresdefault.jpghttps://i.ytimg.com/vi/vfe-eNq-Qyg/maxresdefault.jpghttps://i.ytimg.com/vi/oPf27gAup9U/maxresdefault.jpghttps://i.ytimg.com/vi/TG55ErfdaeY/maxresdefault.jpghttps://i.ytimg.com/vi/3PszVWZNWVA/maxresdefault.jpghttps://i.ytimg.com/vi/TpcbfxtdoI8/maxresdefault.jpghttps://i.ytimg.com/vi/QV7CanyzhZg/maxresdefault.jpghttps://i.ytimg.com/vi/X0zudTQelzI/maxresdefault.jpghttps://i.ytimg.com/vi/jvnU0v6hcUo/maxresdefault.jpghttps://i.ytimg.com/vi/szxPar0BcMo/maxresdefault.jpghttps://i.ytimg.com/vi/a6XtBLDmPA0/maxresdefault.jpghttps://i.ytimg.com/vi/UN-II_jBzzo/maxresdefault.jpghttps://i.ytimg.com/vi/etmRI2_9Q_A/maxresdefault.jpghttps://i.ytimg.com/vi/NjEGncridoQ/maxresdefault.jpghttps://i.ytimg.com/vi/Vufba_ZcoR0/maxresdefault.jpghttps://i.ytimg.com/vi/HQPA5oNpfM4/maxresdefault.jpghttps://i.ytimg.com/vi/dnV_MTFEGIY/maxresdefault.jpghttps://i.ytimg.com/vi/rjhIzemLdos/maxresdefault.jpghttps://i.ytimg.com/vi/j0qbzNHmfW0/maxresdefault.jpghttps://i.ytimg.com/vi/2yXNrLTddME/maxresdefault.jpghttps://i.ytimg.com/vi/HlUiSBXQHCw/maxresdefault.jpghttps://i.ytimg.com/vi/lTTvKwCylFY/maxresdefault.jpghttps://i.ytimg.com/vi/5A_o-nU5s2U/maxresdefault.jpghttps://i.ytimg.com/vi/ZBw35Ze3bg8/maxresdefault.jpghttps://i.ytimg.com/vi/zhL5DCizj5c/maxresdefault.jpghttps://i.ytimg.com/vi/B3u4EFTwprM/maxresdefault.jpghttps://i.ytimg.com/vi/Nosq94oCl_M/maxresdefault.jpghttps://i.ytimg.com/vi/alJaltUmrGo/maxresdefault.jpghttps://i.ytimg.com/vi/_XPZQ0LAlR4/maxresdefault.jpghttps://i.ytimg.com/vi/UUCEeC4f6ts/maxresdefault.jpghttps://i.ytimg.com/vi/Q78COTwT7nE/maxresdefault.jpghttps://i.ytimg.com/vi/y9HjvHZfCUI/maxresdefault.jpghttps://i.ytimg.com/vi/T_sGTspaF4Y/maxresdefault.jpghttps://i.ytimg.com/vi/5SnR-e0S6Ic/maxresdefault.jpghttps://i.ytimg.com/vi/s_iwrt7D5OA/maxresdefault.jpg


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
