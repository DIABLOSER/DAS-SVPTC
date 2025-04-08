# 🎬 短视频文本评论动态分析系统

> 基于哔哩哔哩开放 API 的短视频评论情感与行为数据可视化平台

本项目致力于构建一个面向 **Bilibili 短视频平台** 的评论数据动态分析系统，采用 **前后端分离架构**，实现对用户评论内容的实时采集、智能分析与交互式可视化展示，帮助用户更全面地洞察观众反馈、舆情变化及潜在热点内容。

项目涵盖从登录认证、视频内容获取到评论文本深度挖掘与图形展示的完整数据流程，适用于数据分析、自然语言处理、用户研究等多个场景。

---

## 🧰 技术栈

| 层级   | 技术框架 |
|--------|----------|
| 前端   | Vue3 + Element Plus + ECharts |
| 后端   | Python Flask + Requests + SnowNLP |
| 数据源 | Bilibili 开放 API（模拟扫码登录 + 视频/评论接口） |

---

## 🚀 核心功能一览

### ✅ 用户操作
- [x] 支持哔哩哔哩扫码登录  
- [x] 获取登录用户的基本信息（昵称、头像、UID 等）  

### 🎞 视频数据模块
- [x] 获取推荐视频列表  
- [x] 根据关键词搜索视频  
- [x] 获取指定视频的详细信息  
- [x] 支持在线播放与本地下载功能  

### 💬 评论分析模块
- [x] 获取视频下的所有评论（支持分页加载）  
- [x] 评论数据实时刷新与缓存机制  
- [x] 评论数据多维度分析与可视化：

---

## 📊 评论数据可视化分析

| 模块           | 描述 |
|----------------|------|
| 🌥 **词云图**       | 直观展示评论中出现频率最高的关键词 |
| 👥 **性别分布**     | 根据评论者信息统计性别占比，展示受众画像 |
| ⏱ **评论趋势**     | 评论数量随时间的波动趋势图，辅助分析热度变化 |
| 😊 **情感分析**     | 基于 SnowNLP 模型判别评论情绪，分类为正面、中性、负面 |
| 🌍 **地区分布**     | 根据 IP 归属地绘制中国地图热力分布图 |
| 🧠 **KMeans 聚类** | 使用 KMeans 算法对评论语义进行聚类，挖掘热门话题 |
| 👍 **点赞排行榜**   | 展示点赞量最高的评论列表，体现用户关注点 |

---

## 📸 项目界面展示

> 以下为系统各功能页面的展示图，包括首页、搜索、视频详情、用户中心及评论分析模块：

<div align="center">
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_login.png" alt="登录页" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_home.png" alt="首页" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_search.png" alt="搜索页" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_video.png" alt="视频页" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_mine.png" alt="我的页面" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_about.png" alt="关于页" width="400"/>
  <br/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse1.png" alt="可视化分析1" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse2.png" alt="可视化分析2" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse3.png" alt="可视化分析3" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse4.png" alt="可视化分析4" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse5.png" alt="可视化分析5" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse6.png" alt="可视化分析6" width="400"/>
  <img src="https://github.com/DIABLOSER/DAS-SVPTC/blob/main/raw/screenshot_analyse7.png" alt="可视化分析7" width="400"/>
</div>

---

## 🧪 项目亮点

- 🔐 支持扫码登录，模拟真实用户身份获取个性化数据
- 📈 实时评论数据采集 + NLP 分析，动态刷新图表
- 🎨 高度交互的前端界面，操作体验流畅美观
- 🌐 多图表联动展示，快速洞察评论行为与情绪倾向
- 🧩 模块化设计，便于扩展和部署

---

## ⚠️ 免责声明

本项目仅供 **学术研究与学习使用**，所有数据均来自哔哩哔哩官方公开 API，不涉及任何商业用途或隐私数据抓取。如有侵权或违反平台规定，请及时联系作者处理。

---

## 📬 联系作者

如有建议或合作意向，欢迎通过以下方式与我联系：

- 📧 Email：`daboluo719@gmail.com`
- 🔗 项目地址：[GitHub - DAS-SVPTC](https://github.com/DIABLOSER/DAS-SVPTC)

---

> 如果你喜欢这个项目，欢迎 ⭐Star 和 🍴Fork！你的支持是我持续优化的最大动力！



