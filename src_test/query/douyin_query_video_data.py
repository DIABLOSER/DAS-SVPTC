from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 查询授权账号下的视频数据
@app.route('/query_video_data', methods=['GET'])
def query_video_data():
    # 获取请求参数
    open_id = request.args.get('open_id', 'ba253642-0590-40bc-9bdf-9a1334b94059')
    cursor = int(request.args.get('cursor', 0))
    count = int(request.args.get('count', 10))

    # 定义请求的URL和参数
    url = 'https://open.douyin.com/api/douyin/v1/video/video_list/'
    params = {
        'open_id': open_id,
        'cursor': cursor,
        'count': count
    }
    headers = {
        'access-token': 'act.1d1021d2aee3d41fee2d2add43456badMFZnrhFhfWotu3Ecuiuka27L56lr'
    }

    # 发起GET请求
    response = requests.get(url, params=params, headers=headers)

    # 返回响应内容
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)