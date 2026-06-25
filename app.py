from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ihk_project_secret!'
# Включаем поддержку SocketIO для работы сети в реальном времени
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # Сервер будет искать этот файл в папке templates
    return render_template('index.html')
player_board =[
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

# Слушаем тестовое событие выстрела от клиента
@socketio.on('fire_shot')
def handle_fire_shot(data):
    x = data.get('x')
    y = data.get('y')
    print(f"Сервер получил координаты выстрела: X={data['x']}, Y={data['y']}")
    current_value = player_board[y][x]
    if current_value == 2 or current_value == 3:
        status = "already_shot"
    elif current_value == 1:
        status ="hit"
        player_board[y][x] = 2
    else:
        status = "miss"
        player_board[y][x] = 3
    # Отправляем ответ обратно клиенту
    emit('shot_response', {'status': status, 'x': x, 'y': y})

if __name__ == '__main__':
    # Запускаем сервер на локальном хосте, порт 5000
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)