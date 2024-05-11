# copyYoutube
## 介绍
把youtube的视频，转成音频后，上传到该仓库，实现不用梯子也能订阅youtube频道功能！
使用rss订阅+python+Github Actions+Github Pages功能，
## 实现过程
- 通过rss订阅来找到视频源
- 在Github Action 设置定时任务，定时爬取视频源中的视频
- Github Action 执行python脚本，对视频进行下载，后转成MP3格式（我怎么看视频）
- 将mp3上传到一个开通了Github Pages 服务的仓库中
- 用一个播放音频的页面来播放mp3
## 其他说明
  可以不转音频，而直接上传视频，但是需要重新写一个播放视频的页面
  我设置的时候音频一天一清楚，太多了我也听不过来，如果有需要可以自行修改普通脚本

