import uuid
import feedparser
import os
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
from pytube import YouTube
from datetime import timedelta, datetime
from Mp3Data import Mp3Data, Author, DataAll, CustomEncoder
import json
from dateutil import parser
import pytz

# 替换为博主频道的 RSS 订阅链接
# RSS_FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCG6ADYIl4GxaQib1HKIsRNg'

channelList = [
    {'cnName': 'dakang',
     'name': '大康有话说',
     'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCG6ADYIl4GxaQib1HKIsRNg'
     },
    {'cnName': 'wangju',
     'name': '王局拍案',
     'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBKDRq35-L8xev4O7ZqBeLg'
     },
     {'cnName': 'laogao',
      'name': '老高和小茉',
      'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCtR5okwgTMghi_uyWvbloEg'
      },
      {'cnName': 'wutuo',
        'name': '脑洞乌托邦',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC2tQpW0dPiyWPebwBSksJ_g'
      },
      {'cnName': 'laoliang',
        'name': '老梁',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC661VQhlv-WJ5TSEU7i-sQg'
      },
      {'cnName': 'cuiyongy',
        'name': '崔永元',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCAq_xQV8pJ2Q_KOszzaYPBg'
      },
      {'cnName': 'chaijing',
        'name': '柴静',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCjuNibFJ21MiSNpu8LZyV4w'
      },
      {'cnName': 'M2dangan',
        'name': 'M2档案',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC9HOOTENXN_Q2AJ7eozWBXA'
      },
      {'cnName': 'shijiezhizuiTOP',
        'name': '世界之最TOP',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCE_4Cin3l8LwAySxEVluKDQ'
      },
#     {'cnName': 'meiguo',
#      'name': '美国之音',
#      'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCt5zpwa264A0B-gaYtv1IpA'
#      },

]
# 保存已经处理的视频
titleSet = set()


def download_first_video_as_mp3():
    ZhNow = datetime.now() + timedelta(hours=8)
    print("当前中国时间：" + str(ZhNow))
    newFilePath = "./newFile/"
    dataJsPath = "./copyYoutube/js/data.js"
    # 新建文件夹，暂存mp3
    print("创建newFile")
    if not os.path.exists(newFilePath):
        os.makedirs(newFilePath)
        print("newFile创建成功")
    # 初始化仓库中的js文件
    print("开始下载视频……")
    data_all = DataAll()
    # 写入js数据获取时间
    data_all.data_date = ZhNow.strftime('%Y-%m-%d')

    for channel in channelList:
        try:
            index = 0
            # 解析 RSS 订阅
            print("解析" + channel['name'] + "的视频……")
            # rss获取视频地址
            feed = feedparser.parse(channel['url'])
            # 循环视频列表
            # 写入js的博主信息
            author1 = Author()
            # 博主名称
            author1.author_name = channel['name']
            for entry in feed.entries:
                try:
                    # 写入js的音频信息
                    mp3_data1 = Mp3Data()
                    index += 1
                    link = entry.link
                    title = str(entry.title.replace(".", ""))
                    # 如果该视频已经下载，则无需重新下载
                    if title in titleSet:
                        continue
                    published = entry.published
                    dt_object = parser.parse(published)
                    now = datetime.utcnow().replace(tzinfo=pytz.utc)  # 将当前UTC时间转换为aware datetime
                    three_days_ago = now - timedelta(days=3)
                    print("两个时间对比")
                    print(dt_object)
                    print(three_days_ago)
                    if dt_object < three_days_ago:
                        print("视频过早，跳过")
                        continue

                    print("是昨天的数据，进行下载……")
                    # 下载
                    print("开始下载" + channel['name'] + str(index) + "……")
                    mp4FileName = download_video(link, newFilePath)

                    #print("判断视频时长，短于十分钟的不要……")
                    duration = get_video_duration(newFilePath + mp4FileName)
                    duration = int(duration)
                    #if duration < 600:
                        #print("视频短于600秒,删除视频……")
                        #os.remove(newFilePath + mp4FileName)
                        #continue
                    # 转换时长格式
                    minutes = duration // 60  # 使用整数除法得到完整的分钟数
                    remaining_seconds = duration % 60  # 使用模运算符得到剩余的秒数
                    durationStr = str(minutes) + "分" + str(remaining_seconds) + "秒"
                    print("视频时长：" + durationStr)

                    # 转音频
                    print("视频转音频……")
                    video = AudioFileClip(newFilePath + mp4FileName)
                    # 将音频写入MP3文件
                    mp3Name = channel['cnName'] + "_" + str(index) + ".mp3"
                    video.write_audiofile(newFilePath + mp3Name)
                    print("删除视频……")
                    os.remove(newFilePath + mp4FileName)
                    # 判断是否重复用的集合
                    titleSet.add(title)
                    # 修改js
                    # 写入js的音频标题
                    mp3_data1.title = title
                    # 写入js的音频地址
                    mp3_data1.url = "https://xiongood.github.io/copyYoutube/mp3/" + mp3Name
                    # 写入js的音频时长
                    mp3_data1.duration = durationStr
                    mp3_data1.published = published
                    # 音频数据 翻入到作者的音频列表中
                    author1.add_mp3_data(mp3_data1)
                except Exception as e:
                    print(e)
                    continue
            # 将作者 放入到所有作者列表中
            data_all.add_author(author1)
        except Exception as e:
            print(e)
            continue
    # 修改js文件
    # 将对象转成js
    print("将对象转成js")
    json_data = json.dumps(data_all, cls=CustomEncoder, indent=4, ensure_ascii=False)
    print("打印js")
    print(json_data)
    print("写入js")
    with open(dataJsPath, 'w', encoding='utf-8') as js_file:
        js_file.write("const dataAll=" + json_data)
    print("处理成功！")

    # 下载视频


def download_video(url, output_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if streams:
            video = streams
            filename = os.path.basename(str(uuid.uuid4())+".mp4")  # 使用视频的文件名
            video.download(output_path, filename=filename)  # 保存视频时指定文件名
            print("下载完成！")
            print("文件名称:", filename)
            return filename
        else:
            print("视频没有可用的流。")
    except Exception as e:
        print("下载出错:", e)


# 查询视频时长
def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    return duration


if __name__ == '__main__':
    download_first_video_as_mp3()
