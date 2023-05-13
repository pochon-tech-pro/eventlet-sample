from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet  # 非同期ネットワーキングと並列処理のためのライブラリ
from concurrent.futures import ThreadPoolExecutor
import time
import logging

# ログ設定
logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

# スレッドプールの作成（同時に5つのスレッドまで）
executor = ThreadPoolExecutor(max_workers=2)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_message')
def handle_message(data):
    emit('broadcast_message', data, broadcast=True)
    executor.submit(background_thread, data)


def background_thread(data):
    logging.debug(f"Received message: {data}")
    time.sleep(5)  # 模擬処理時間
    logging.debug(f"Finished processing message: {data}")


if __name__ == '__main__':
    # eventletのWSGIサーバーを起動
    # これにより、Flaskアプリケーションが非同期I/Oを使用して動作するようになる
    # app.run()だと多数のクライアントからのリクエストを同時に処理する必要があるときにネック
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8081)), app)
