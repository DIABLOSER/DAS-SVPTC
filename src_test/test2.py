from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
import io
import base64
import logging
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
import requests
import json

# 设置 Matplotlib 后端为 Agg
plt.switch_backend('Agg')

app = Flask(__name__)
CORS(app)  # 允许跨域请求
logging.basicConfig(level=logging.DEBUG)

# 示例数据
text_data = [
    "I love programming in Python",
    "Flask is a great web framework",
    "Machine learning is fascinating",
    "Data science is the future",
    "I hate traffic jams"
]
# 请求评论数据
def query_comments():
    
# 情感分析
@app.route('/api/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    data = request.json
    text = data.get('text', '')
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    logging.debug(f'Sentiment analysis result for "{text}": {sentiment}')
    return jsonify({'sentiment': sentiment})

# 词频分析
@app.route('/api/word_frequency', methods=['POST'])
def word_frequency():
    data = request.json
    text = data.get('text', '')
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text])
    word_freq = dict(zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0)))
    logging.debug(f'Word frequency analysis result for "{text}": {word_freq}')
    return jsonify({'word_frequency': word_freq})

# 主题分析
@app.route('/api/topic_modeling', methods=['POST'])
def topic_modeling():
    data = request.json
    texts = data.get('texts', [])
    n_topics = data.get('n_topics', 2)
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    topics = []
    for index, topic in enumerate(lda.components_):
        top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]
        topics.append({'topic': index, 'top_words': top_words})
    logging.debug(f'Topic modeling result: {topics}')
    return jsonify({'topics': topics})

# 朴素贝叶斯分类
@app.route('/api/naive_bayes', methods=['POST'])
def naive_bayes():
    data = request.json
    texts = data.get('texts', [])
    labels = data.get('labels', [])
    test_text = data.get('test_text', '')
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(texts)
    y_train = labels
    model = MultinomialNB()
    model.fit(X_train, y_train)
    X_test = vectorizer.transform([test_text])
    prediction = model.predict(X_test)[0]
    logging.debug(f'Naive Bayes prediction for "{test_text}": {prediction}')
    return jsonify({'prediction': prediction})

# K-means聚类
@app.route('/api/kmeans_clustering', methods=['POST'])
def kmeans_clustering():
    data = request.json
    texts = data.get('texts', [])
    n_clusters = data.get('n_clusters', 2)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    cluster_dict = {}
    for i, cluster in enumerate(clusters):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(texts[i])
    logging.debug(f'K-means clustering result: {cluster_dict}')
    return jsonify({'clusters': cluster_dict})

# 图表生成
@app.route('/api/chart')
def generate_chart():
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
    app.run(debug=True, ssl_context=('./ssl/server.crt', './ssl/server.key'))  # 使用 HTTPS 协议