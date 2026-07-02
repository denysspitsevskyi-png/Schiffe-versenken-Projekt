import random
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
my_board=[
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0]
]
enemy_board =[
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
# Отправляем клиенту расстановку его собственных кораблей при запросе
@socketio.on("request_my_ships")
def handle_my_ships():
    print("Клиенте запросил координаты своих кораблей")
    emit("my_ships_response", {"board": my_board})
# Слушаем тестовое событие выстрела от клиента
@socketio.on('fire_shot')
def handle_fire_shot(data):
    x = data.get('x')
    y = data.get('y')
    print(f"Сервер получил координаты выстрела: X={data['x']}, Y={data['y']}")
    current_value = enemy_board[y][x]
    if current_value == 2 or current_value == 3:
        status = "already_shot"
    elif current_value == 1:
        status ="hit"
        enemy_board[y][x] = 2
    else:
        status = "miss"
        enemy_board[y][x] = 3
    # Если игрок промахнулся,запускаем ответный выстрел бота
    if status=="miss":
        # Бот выбирает случайную клетку на твоем поле
        bot_x = random.randint(0,9)
        bot_y = random.randint(0,9)
        # Проверяем что там лежит
        target_value = my_board[bot_y][bot_x]
        if target_value == 1:
            bot_status = "hit"
            my_board[bot_y][bot_x] = 2 # Пометили что наш корабль подбит
        else:
            bot_status = "miss"
            my_board[bot_y][bot_x] = 3 # Пометили промах бота
        # Отправляем клиенту специальное событие "bot_shot"
        emit("bot_shot",{"status": bot_status,"x":bot_x,"y":bot_y})

    # Отправляем ответ обратно клиенту
    emit('shot_response', {'status': status, 'x': x, 'y': y})

if __name__ == '__main__':
    # Запускаем сервер на локальном хосте, порт 5000
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)