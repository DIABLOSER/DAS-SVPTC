#服务端
from flask import Flask, jsonify, request, send_file, Response, make_response
import requests
from flask_cors import CORS
import time
from io import BytesIO
import logging
import os
import json
import hashlib
import urllib.parse
#数据可视化部分依赖
import re
import jieba
from wordcloud import WordCloud
from io import BytesIO
import base64
import matplotlib.pyplot as plt

from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)

# 设置日志级别为 DEBUG
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.WARNING)
# 设置 Matplotlib 后端为 Agg
plt.switch_backend('Agg')
# 允许跨域请求，并支持携带凭证
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {
        "origins": ["http://localhost:5173"],  # 替换为你的前端域名
        "allow_headers": ["*"]
    }}
)
# Bilibili API 密钥（需定期更新）
APP_KEY = "aae92bc66f3edfab"
APP_SEC = "af125a0d5279fd576c1b4418a3e8276d"

# 生成签名
def generate_sign(params: dict) -> str:
    """生成 Bilibili API 签名"""
    params_str = ""
    for key in sorted(params.keys()):
        params_str += f"{key}={urllib.parse.quote(str(params[key]))}&"
    params_str = params_str[:-1]
    sign_str = params_str + APP_SEC
    return hashlib.md5(sign_str.encode("utf-8")).hexdigest()
# 获取 Bilibili 登录二维码
@app.route('/api/get_qr_code', methods=['GET'])
def get_qr_code():
    try:
        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())  # 转发 Bilibili API 的响应
        else:
            logging.error(f"Failed to get QR code from Bilibili: {response.status_code} {response.text}")
            return jsonify({"error": "Failed to get QR code from Bilibili"}), 500
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 检查二维码状态
@app.route('/api/check_qr_code', methods=['POST'])
def check_qr_code():
    try:
        data = request.get_json()
        logging.debug(f"收到的二维码校验请求数据: {data}")

        oauth_key = data.get("oauthKey")
        logging.debug(f"oauthKey: {oauth_key}")
        if not oauth_key:
            logging.error("oauthKey 为空")
            return jsonify({"error": "Missing oauthKey"}), 400

        url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={oauth_key}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/"
        }

        response = requests.get(url, headers=headers)
        result = response.json()
        logging.debug(f"Bilibili API 响应: {result}")

        if result.get('code') == 0:
            logging.info("二维码扫描成功，登录完成")
            return jsonify({"code": 0, "message": "登录成功", "status": True, "data": result.get('data')}), 200
        elif result.get('code') == 86038:
            logging.info("二维码未扫描，等待扫码")
            return jsonify({"code": 86038, "message": "等待扫码", "status": False}), 200
        elif result.get('code') == 200000:
            logging.info("二维码已过期")
            return jsonify({"code": 200000, "message": "二维码已过期", "status": False}), 200
        else:
            logging.error(f"未知错误: {result}")
            return jsonify({"error": "未知错误", "status": False}), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 获取用户信息
@app.route("/api/user_info", methods=["GET"])
def get_user_info():
    try:
        # 从请求参数中获取 DedeUserID 和 SESSDATA
        dede_user_id = request.args.get("DedeUserID")
        sessdata = request.args.get("SESSDATA")

        if not dede_user_id or not sessdata:
            logging.error("缺少 DedeUserID 或 SESSDATA")
            return jsonify({"error": "缺少 DedeUserID 或 SESSDATA"}), 400

        # 调用 Bilibili 获取用户信息的 API
        url = "https://api.bilibili.com/x/web-interface/nav"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
            "Cookie": f"DedeUserID={dede_user_id}; SESSDATA={sessdata};"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            if user_info.get("code") == 0:
                return jsonify({"code": 0, "data": user_info.get("data")}), 200
            else:
                logging.error(f"获取用户信息失败: {user_info.get('message')}")
                return jsonify({"error": "获取用户信息失败", "message": user_info.get("message")}), 500
        else:
            logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
            return jsonify({"error": "Bilibili API 请求失败"}), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 获取用户投稿视频
@app.route("/api/user_videos", methods=["GET"])
def get_user_videos():
    try:
        # 从请求参数中获取用户 ID 和页码
        mid = request.args.get("mid")
        pn = request.args.get("pn", default=1, type=int)
        ps = request.args.get("ps", default=30, type=int)

        if not mid:
            logging.error("缺少用户 ID (mid)")
            return jsonify({"error": "缺少用户 ID (mid)"}), 400

        # 增加延迟，降低请求频率
        time.sleep(3)  # 延迟 3 秒

        # 调用 Bilibili API 获取用户投稿视频
        url = "https://api.bilibili.com/x/space/arc/search"
        params = {
            "mid": mid,
            "pn": pn,
            "ps": ps,
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
        }

        response = requests.get(url, params=params, headers=headers)
        logging.debug(f"Bilibili API 响应: {response.json()}")  # 打印 API 响应
        if response.status_code == 200:
            video_data = response.json()
            if video_data.get("code") == 0:
                return jsonify({"code": 0, "data": video_data.get("data")}), 200
            elif video_data.get("code") == -799:
                # 请求过于频繁，返回友好提示
                logging.warning("请求过于频繁，返回友好提示")
                return jsonify({"error": "请求过于频繁，请稍后再试"}), 429
            else:
                logging.error(f"获取视频数据失败: {video_data.get('message')}")
                return jsonify({"error": "获取视频数据失败", "message": video_data.get("message")}), 500
        else:
            logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
            return jsonify({"error": "Bilibili API 请求失败"}), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 搜索视频
@app.route("/api/search_videos", methods=["GET"])
def search_videos():
    try:
        # 获取搜索关键词和分页参数
        keyword = request.args.get("keyword")
        pn = request.args.get("pn", default=1, type=int)
        ps = request.args.get("ps", default=20, type=int)

        if not keyword:
            logging.error("缺少搜索关键词")
            return jsonify({"error": "缺少搜索关键词"}), 400

        # 校验 Cookie
        cookie = request.headers.get("Cookie", "")
        if 'SESSDATA' not in cookie or 'DedeUserID' not in cookie:
            logging.error("未登录或 Cookie 无效")
            return jsonify({"error": "未登录或 Cookie 无效"}), 401

        # 调用 Bilibili API 搜索视频
        url = "https://api.bilibili.com/x/web-interface/search/type"
        params = {
            "keyword": keyword,
            "search_type": "video",
            "page": pn,
            "page_size": ps,
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
            "Cookie": cookie,  # 传递完整 Cookie
            "Origin": "https://www.bilibili.com"
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            search_data = response.json()
            if search_data.get("code") == 0:
                return jsonify({"code": 0, "data": search_data.get("data")}), 200
            else:
                logging.error(f"搜索视频失败: {search_data.get('message')}")
                return jsonify({"error": "搜索视频失败", "message": search_data.get("message")}), 500
        else:
            logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
            return jsonify({"error": "Bilibili API 请求失败"}), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 获取点赞数排行前 N 的评论
@app.route("/api/top_liked_comments", methods=["GET"])
def get_top_liked_comments():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        n = request.args.get("n", default=10, type=int)
        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd
        df = pd.read_csv(csv_file)
        top_comments = df.nlargest(n, '点赞数')[['评论内容', '点赞数']].to_dict('records')

        return jsonify({"code": 0, "data": top_comments}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 获取视频评论数据
@app.route("/api/video_comments", methods=["GET"])
def get_video_comments():
    try:
        # 获取参数
        oid = request.args.get("oid")
        if not oid:
            logging.error("Missing oid parameter")
            return jsonify({"error": "Missing oid parameter"}), 400

        pn = request.args.get("pn", 1, type=int)
        ps = request.args.get("ps", 20, type=int)
        sort = request.args.get("sort", 0, type=int)
        type_ = request.args.get("type", 1, type=int)

        # 校验 Cookie
        cookie = request.headers.get("Cookie", "")
        if 'SESSDATA' not in cookie or 'DedeUserID' not in cookie:
            logging.error("未登录或 Cookie 无效")
            return jsonify({"error": "未登录或 Cookie 无效"}), 401

        # 增加请求间隔，避免触发安全策略
        #time.sleep(3)  # 增加3秒延迟

        # 生成签名参数
        params = {
            "oid": oid,
            "type": type_,
            "pn": pn,
            "ps": ps,
            "sort": sort,
            "appkey": APP_KEY,
            "ts": int(time.time()),
            "platform": "web",
            "build": "1000"
        }
        params["sign"] = generate_sign(params)

        # 调用 Bilibili API，增加重试机制
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://www.bilibili.com/",
                    "Cookie": cookie,  # 传递完整 Cookie
                    "Origin": "https://www.bilibili.com",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Connection": "keep-alive"
                }
                response = requests.get("https://api.bilibili.com/x/v2/reply", params=params, headers=headers)
                
                if response.status_code == 200:
                    try:
                        comment_data = response.json()
                        logging.debug(f"Bilibili API 响应内容: {comment_data}")  # 打印响应内容

                        if comment_data.get("code") == 0:
                            # 获取 replies 字段
                            replies = comment_data.get("data", {}).get("replies", [])

                            # 如果 replies 为空列表，表示没有评论
                            if not replies:
                                logging.info(f"视频 ID {oid} 没有评论数据")
                                return jsonify({"code": 0, "data": {"replies": []}}), 200

                            return jsonify({"code": 0, "data": comment_data.get("data")}), 200
                        else:
                            logging.error(f"获取评论数据失败: {comment_data.get('message')}")
                            return jsonify({"error": "获取评论数据失败", "message": comment_data.get("message")}), 500
                    except ValueError as e:
                        logging.error(f"JSON 解析错误: {str(e)}")
                        return jsonify({"error": "JSON 解析错误"}), 500
                else:
                    logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
                    retry_count += 1
                    time.sleep(5)  # 增加重试间隔
            except requests.exceptions.RequestException as e:
                logging.error(f"请求 Bilibili API 时发生网络错误: {str(e)}")
                retry_count += 1
                time.sleep(5)  # 增加重试间隔

        return jsonify({"error": "请求失败，请稍后再试"}), 500

    except Exception as e:
        logging.error(f"服务器内部错误: {str(e)}", exc_info=True)
        return jsonify({"error": "服务器内部错误", "message": str(e)}), 500

# 获取视频全部评论数据
@app.route("/api/all_video_comments", methods=["GET"])
def get_all_video_comments():
    session = None
    try:
        # Step 1: 参数校验
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)
        try:
            oid = int(oid)
        except ValueError:
            return error_response("Invalid oid parameter", 400)

        cookie = request.headers.get("Cookie", "")
        if 'SESSDATA' not in cookie or 'DedeUserID' not in cookie:
            return error_response("未登录或 Cookie 无效", 401)

        # Step 2: 初始化
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Cookie": cookie,
            "Origin": "https://www.bilibili.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }

        # Step 3: 获取第一页
        def fetch_page(pn):
            time.sleep(3)  # 增加请求间隔，避免触发安全策略
            params = {
                "oid": oid, "pn": pn, "ps": 20, "sort": 0, "type": 1,
                "appkey": APP_KEY, "ts": int(time.time()),
                "platform": "web", "build": "1000"
            }
            params["sign"] = generate_sign(params)
            resp = session.get("https://api.bilibili.com/x/v2/reply", params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()

        first_page = fetch_page(1)
        if first_page.get("code") != 0:
            return error_response("获取评论数据失败: " + str(first_page.get("message")), 500)

        data = first_page.get("data", {})
        all_comments = data.get("replies", [])
        total_count = data.get("page", {}).get("count", 0)
        total_pages = (total_count + 20 - 1) // 20

        # Step 4: 并发获取剩余页
        def fetch_and_extract(pn):
            try:
                result = fetch_page(pn)
                return result.get("data", {}).get("replies", [])
            except Exception as e:
                logging.warning(f"第 {pn} 页获取失败: {e}")
                raise e  # 抛出异常，中断并发任务

        if total_pages > 1:
            with ThreadPoolExecutor(max_workers=2) as executor:  # 减少并发数
                try:
                    for comments in executor.map(fetch_and_extract, range(2, total_pages + 1)):
                        all_comments.extend(comments)
                except Exception as e:
                    logging.error(f"获取评论数据时发生错误: {e}")
                    # 在发生错误时，直接返回已经获取的数据

        # Step 5: 保存并返回
        save_comments_to_csv(all_comments, oid)
        return success_response({"replies": all_comments})

    except Exception as e:
        logging.error("服务器内部错误", exc_info=True)
        return error_response("服务器内部错误: " + str(e), 500)

    finally:
        if session:
            session.close()  # 防止资源泄漏

# 封装返回方法
def success_response(data):
    return jsonify({"code": 0, "data": data}), 200

def error_response(message, code):
    return jsonify({"error": message, "code": code}), code


def save_comments_to_file(comment_data, oid, pn, ps):
    try:
        # 创建保存评论数据的目录（如果不存在）
        comments_dir = os.path.join(os.getcwd(), "comments")
        if not os.path.exists(comments_dir):
            os.makedirs(comments_dir)

        # 构建文件名
        filename = f"comments_oid_{oid}_pn_{pn}_ps_{ps}.json"
        file_path = os.path.join(comments_dir, filename)

        # 将评论数据保存为 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(comment_data, f, ensure_ascii=False, indent=4)

        logging.info(f"评论数据已保存到 {file_path}")
    except Exception as e:
        logging.error(f"保存评论数据到文件时出错: {str(e)}")


def save_comments_to_csv(comments, oid):
    try:
        import csv
        from datetime import datetime
        # 创建保存评论数据的目录（如果不存在）
        comments_dir = os.path.join(os.getcwd(), "comments")
        if not os.path.exists(comments_dir):
            os.makedirs(comments_dir)

        # 构建文件名
        filename = f"comments_oid_{oid}.csv"
        file_path = os.path.join(comments_dir, filename)

        # 将评论数据保存为 CSV 文件
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['用户ID', '用户名', '性别', '位置', '评论内容', '点赞数', '评论时间']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for comment in comments:
                # 提取位置数据中的省份信息
                location = comment.get("reply_control", {}).get("location", "")
                if location and "IP属地：" in location:
                    location = location.split("IP属地：")[1]+"省"

                # 将时间戳转换为 yyyy-MM-dd hh-mm-ss 格式
                ctime = comment.get("ctime", "")
                if ctime:
                    ctime = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")

                writer.writerow({
                    '用户ID': comment.get("member", {}).get("mid", ""),
                    '用户名': comment.get("member", {}).get("uname", ""),
                    '性别': comment.get("member", {}).get("sex", ""),
                    '位置': location,
                    '评论内容': comment.get("content", {}).get("message", ""),
                    '点赞数': comment.get("like", ""),
                    '评论时间': ctime
                })

        logging.info(f"评论数据已保存到 {file_path}")
    except Exception as e:
        logging.error(f"保存评论数据到 CSV 文件时出错: {str(e)}")


# 获取视频详情
@app.route("/api/video_details", methods=["GET"])
def get_video_details():
    try:
        # 从请求参数中获取视频 ID
        aid = request.args.get("aid")
        bvid = request.args.get("bvid")

        if not aid and not bvid:
            logging.error("缺少视频 ID (aid 或 bvid)")
            return jsonify({"error": "缺少视频 ID (aid 或 bvid)"}), 400

        # 调用 Bilibili API 获取视频详情
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {
            "aid": aid,
            "bvid": bvid,
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
        }

        response = requests.get(url, params=params, headers=headers)
        logging.debug(f"Bilibili API 响应: {response.json()}")  # 打印 API 响应
        if response.status_code == 200:
            video_data = response.json()
            if video_data.get("code") == 0:
                video_info = video_data["data"]

                # 尝试从根级别获取 cid
                cid = video_info.get("cid")

                # 如果根级别没有 cid，则从 pages 数组中获取
                if not cid:
                    pages = video_info.get("pages")
                    if pages and len(pages) > 0:
                        cid = pages[0].get("cid")  # 获取第一个分段的 cid
                    if not cid:
                        logging.error("无法找到 cid 字段")
                        return jsonify({"error": "无法找到 cid 字段"}), 500

                # 获取视频播放 URL
                playurl_url = "https://api.bilibili.com/x/player/playurl"
                playurl_params = {
                    "bvid": video_info["bvid"],
                    "cid": cid,
                    "qn": 116,  # 116 表示 1080P 高清
                    "fnval": 0,  #16 支持 DASH 格式
                    "fnver": 0,  #16 支持 DASH 格式"
                    "fourk": 1,  # 支持 4K 分辨率
                }
            
                playurl_response = requests.get(playurl_url, params=playurl_params, headers=headers)
                if playurl_response.status_code == 200:
                    playurl_data = playurl_response.json()
                    if playurl_data.get("code") == 0:
                        if playurl_data["data"].get("durl"):
                            video_info["playurl"] = playurl_data["data"]["durl"][0]["url"]
                        elif playurl_data["data"].get("dash"):  # 如果有 DASH 格式
                            video_info["playurl"] = playurl_data["data"]["dash"]["video"][0]["baseUrl"]
                        return jsonify({"code": 0, "data": video_info}), 200
                    else:
                        logging.error(f"获取视频播放 URL 失败: {playurl_data.get('message')}")
                        return jsonify({"error": "获取视频播放 URL 失败", "message": playurl_data.get("message")}), 500
                else:
                    logging.error(f"Bilibili API 请求失败: {playurl_response.status_code} {playurl_response.text}")
                    return jsonify({"error": "Bilibili API 请求失败"}), 500
            else:
                logging.error(f"获取视频详情失败: {video_data.get('message')}")
                return jsonify({"error": "获取视频详情失败", "message": video_data.get("message")}), 500
        else:
            logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
            return jsonify({"error": "Bilibili API 请求失败"}), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 推荐视频
@app.route("/api/recommended_videos", methods=["GET"])
def get_recommended_videos():
    try:
        # 从请求参数中获取分页参数
        pn = request.args.get("pn", default=1, type=int)
        ps = request.args.get("ps", default=10, type=int)
        mid = request.args.get("mid")  # 新增：获取用户 mid

        # 校验 Cookie
        cookie = request.headers.get("Cookie", "")
        if 'SESSDATA' not in cookie or 'DedeUserID' not in cookie:
            logging.error("未登录或 Cookie 无效")
            return jsonify({"error": "未登录或 Cookie 无效"}), 401

        # 调用 Bilibili API 获取推荐视频
        url = "https://api.bilibili.com/x/web-interface/index/top/feed/rcmd"
        params = {
            "pn": pn,
            "ps": ps,
            "mid": mid  # 新增：传递用户 mid
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",
            "Cookie": cookie,  # 传递完整 Cookie
            "Origin": "https://www.bilibili.com"
        }

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            video_data = response.json()
            if video_data.get("code") == 0:
                # 确保返回的数据格式正确
                return jsonify({
                    "code": 0,
                    "data": video_data.get("data", {}).get("item", [])  # 获取推荐视频列表
                }), 200
            else:
                logging.error(f"获取推荐视频失败: {video_data.get('message')}")
                return jsonify({
                    "code": video_data.get("code"),
                    "error": "获取推荐视频失败",
                    "message": video_data.get("message")
                }), 500
        else:
            logging.error(f"Bilibili API 请求失败: {response.status_code} {response.text}")
            return jsonify({
                "code": response.status_code,
                "error": "Bilibili API 请求失败"
            }), 500
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({
            "code": 500,
            "error": "服务器错误",
            "message": str(e)
        }), 500

# 代理图片
@app.route('/api/proxy_image', methods=['GET'])
def proxy_image():
    try:
        image_url = request.args.get('url')
        if not image_url:
            logging.error("Missing image URL")
            return jsonify({"error": "Missing image URL"}), 400

        response = requests.get(image_url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/"
        })

        if response.status_code == 200:
            return send_file(BytesIO(response.content), mimetype='image/jpeg')
        else:
            logging.error(f"Failed to fetch image: {response.status_code} {response.text}")
            return jsonify({"error": "Failed to fetch image", "status_code": response.status_code}), response.status_code
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 代理视频
@app.route('/api/proxy_video', methods=['GET'])
def proxy_video():
    try:
        video_url = request.args.get('url')
        if not video_url:
            logging.error("Missing video URL")
            return jsonify({"error": "Missing video URL"}), 400

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/",  # 添加 Referer 验证
            "Origin": "https://www.bilibili.com/",   # 添加 Origin 验证
            "Range": request.headers.get("Range", "")  # 支持范围请求
        }

        # 发起流式请求
        response = requests.get(video_url, headers=headers, stream=True)
        if response.status_code == 200 or response.status_code == 206:  # 支持部分内容响应
            # 返回流式响应
            return Response(
                response.iter_content(chunk_size=1024),
                content_type=response.headers["Content-Type"],
                headers={"Accept-Ranges": "bytes"}  # 表明支持范围请求
            )
        else:
            return jsonify({"error": "Failed to fetch video", "status_code": response.status_code}), response.status_code
    except Exception as e:
        logging.error(f"服务器错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 生成词云图
@app.route("/api/generate_wordcloud", methods=["GET"])
def generate_wordcloud_from_csv_api():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        # 调用 generate_wordcloud_from_csv 
        plt_url = generate_wordcloud_from_csv(csv_file)
        if not plt_url:
            return error_response("生成词云图失败", 500)

        return jsonify({"code": 0, "data": {"plt_url": plt_url}}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 生成词云图
def generate_wordcloud_from_csv(csv_file):
    """从 CSV 文件生成词云图"""
    import csv
    from wordcloud import WordCloud
    from io import BytesIO
    import base64
    import os
    import matplotlib.pyplot as plt
    import platform

    # 检查 CSV 文件是否存在
    if not os.path.exists(csv_file):
        logging.error(f"CSV 文件不存在: {csv_file}")
        return None

    try:
        comments = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                comments.append(row["评论内容"])

        # 如果评论数据为空，返回空值
        if not comments:
            logging.warning("评论数据为空")
            return None

        # 清洗评论数据并去重
        cleaned_comments = list(set([clean_text(comment) for comment in comments]))  # 使用集合去重
        text = " ".join(cleaned_comments)

        # 根据操作系统选择字体
        system = platform.system()
        if system == "Windows":
            font_path = "C:/Windows/Fonts/simhei.ttf"  # Windows 系统字体路径
        elif system == "Darwin":  # macOS
            font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"  # macOS 系统字体路径
        else:
            font_path = None  # 其他系统默认不指定字体

        if not os.path.exists(font_path):
            logging.error(f"字体文件不存在: {font_path}")
            # 尝试从系统字体目录获取字体
            import matplotlib.font_manager as fm
            font_path = fm.findfont(fm.FontProperties(family='SimHei' if system == "Windows" else 'Songti SC'))
            if not font_path:
                logging.error("无法找到合适的字体")
                return None

        # 生成词云图
        wordcloud = WordCloud(
            font_path=font_path,  # 使用中文字体
            width=800,
            height=400,
            background_color="white",
            max_words=200,  # 限制最大词数
            collocations=False,  # 禁用词语搭配
            prefer_horizontal=0.8,  # 水平显示比例
            scale=2  # 提高分辨率
        ).generate(text)

        # 使用 matplotlib 绘制词云图
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # 不显示坐标轴

        # 将图像保存到 BytesIO 对象中
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0, dpi=300)
        img.seek(0)

        # 将图像转换为 base64 编码
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        # 返回 base64 编码的图片数据
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        logging.error(f"生成词云图时出错: {str(e)}")
        return None

# 生成性别饼状图
@app.route("/api/generate_gender_pie", methods=["GET"])
def generate_gender_pie():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd

        df = pd.read_csv(csv_file)
        gender_counts = df['性别'].value_counts().to_dict()
        gender_data = [{"name": gender, "value": count} for gender, count in gender_counts.items()]

        return jsonify({"code": 0, "data": {"genders": gender_data}}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 生成日期评论数量折线图
@app.route("/api/generate_date_line", methods=["GET"])
def generate_date_line():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd

        df = pd.read_csv(csv_file)
        df['评论时间'] = pd.to_datetime(df['评论时间'])
        date_counts = df.resample('D', on='评论时间').size()
        dates = date_counts.index.strftime('%Y-%m-%d').tolist()
        counts = date_counts.values.tolist()

        return jsonify({"code": 0, "data": {"dates": dates, "counts": counts}}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 生成评论情感极性分数图
@app.route("/api/generate_sentiment_bar", methods=["GET"])
def generate_sentiment_bar():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd
        from snownlp import SnowNLP

        df = pd.read_csv(csv_file)
        df['情感分数'] = df['评论内容'].apply(lambda x: SnowNLP(x).sentiments)
        sentiment_counts = df['情感分数'].value_counts(bins=20, sort=False)
        sentiments = [f"{int(interval.left * 100)}-{int(interval.right * 100)}" for interval in sentiment_counts.index]
        counts = sentiment_counts.values.tolist()

        return jsonify({"code": 0, "data": {"sentiments": sentiments, "counts": counts}}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 生成地区分布图
@app.route("/api/generate_region_map", methods=["GET"])
def generate_region_map():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd

        df = pd.read_csv(csv_file)
        
        # 确保 '位置' 列存在
        if '位置' not in df.columns:
            return error_response("CSV 文件中缺少 '位置' 列", 400)

        # 过滤掉位置为空的数据
        df = df[df['位置'].notna()]
        
        # 统计各地区评论数量
        region_counts = df['位置'].value_counts().to_dict()
        regions = [{"name": region, "value": count} for region, count in region_counts.items()]

        return jsonify({"code": 0, "data": {"regions": regions, "values": list(region_counts.values())}}), 200
    except Exception as e:
        return error_response(str(e), 500)

# 生成 KMeans 聚类图
@app.route("/api/generate_kmeans_cluster", methods=["GET"])
def generate_kmeans_cluster():
    try:
        oid = request.args.get("oid")
        if not oid:
            return error_response("Missing oid parameter", 400)

        csv_file = os.path.join("comments", f"comments_oid_{oid}.csv")
        if not os.path.exists(csv_file):
            return error_response("CSV 文件不存在", 404)

        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA

        # 读取 CSV 文件
        df = pd.read_csv(csv_file)
        comments = df['评论内容'].tolist()

        # 文本向量化
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(comments)

        # KMeans 聚类，显式设置 n_init 参数
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)  # 显式设置 n_init
        kmeans.fit(X)
        labels = kmeans.labels_.astype(int)  # 将 int32 转换为 int

        # 降维
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X.toarray())

        # 准备 ECharts 数据
        data = []
        for i in range(len(X_pca)):
            data.append({
                "name": comments[i],
                "value": [float(X_pca[i][0]), float(X_pca[i][1]), int(labels[i])]  # 确保所有数值类型为 float 或 int
            })

        return jsonify({
            "code": 0,
            "data": {
                "points": data,
                "clusters": [int(cluster) for cluster in set(labels)]  # 将 clusters 转换为 int
            }
        }), 200
    except Exception as e:
        logging.error(f"生成 KMeans 聚类图时出错: {str(e)}", exc_info=True)
        return error_response(str(e), 500)

# 数据清洗
def clean_text(text):
    """清洗文本数据，去除标点符号、表情、停用词等"""

   # 去除@用户（@开头，直到第一个空格为止，同时去掉空格）
    text = re.sub(r"@\S+\s*", "", text)

    # 去除表情符号（包括中括号及其中内容）
    text = re.sub(r"\[[^\]]+\]", "", text)

    # 去除多余的空格（如果 @ 用户后还有空格残留）
    text = re.sub(r"\s+", " ", text).strip()
    
    # 去除标点符号和特殊字符
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", " ", str(text))
    # 分词
    words = jieba.cut(text)
    
    # 去除停用词
    stopwords = set()
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        for line in f:
            stopwords.add(line.strip())
    
    cleaned_words = [word for word in words if word not in stopwords and len(word) > 1]  # 增加长度过滤
    
    return " ".join(cleaned_words)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)