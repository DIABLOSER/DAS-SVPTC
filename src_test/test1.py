from flask import Flask, jsonify
import matplotlib.pyplot as plt
import io
import base64
import logging
from flask_cors import CORS
# 这里存放所有的python代码，图表，后端，算法强烈写好注释以及暴露接口
# 动态分析，情感分析，主题分析，词频分析
# 算法：朴素贝叶斯，K-means等
# 设置 Matplotlib 后端为 Agg
plt.switch_backend('Agg')

app = Flask(__name__)
CORS(app)  # 允许跨域请求
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/chart')
def index2():
    # 创建折线图
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
    ax.set_title('Sample Line Chart')

    # 将图保存到内存中
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # 关闭图形对象
    plt.close(fig)

    # 将图像编码为 base64
    plot_url = base64.b64encode(img.getvalue()).decode()

    # 添加日志记录
    logging.debug(f'Generated plot_url: {plot_url}')

    return jsonify({'plot_url': plot_url})

if __name__ == '__main__':
    app.run(debug=True,ssl_context=('./ssl/server.crt','./ssl/server.key'))#使用https协议
