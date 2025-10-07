from .constants import ROOMS


def show_inventory(game_state):
    """Показать инвентарь игрока"""
    inventory = game_state['player_inventory']
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> "):
    """Получить ввод от пользователя"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещение игрока"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        next_room = room_data['exits'][direction]
        
        # Проверка для guard_room - страж не выпускает
        if current_room == 'guard_room' and next_room == 'hall' \
        and room_data['puzzle'] is not None:
            print("Страж-скелет скрежещет костями и не пропускает тебя!")
            print("Придется решить его загадку командой 'solve'.")
            return

        # Проверка для treasure_room
        if next_room == 'treasure_room' \
        and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен rusty_key чтобы пройти дальше.")
            return
        
        if next_room == 'treasure_room':
            print("Вы используете ключ, чтобы открыть путь.")
        
        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        
        # Случайное событие после перемещения
        from .utils import random_event
        random_event(game_state)
        
        from .utils import describe_current_room
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if item_name in room_data['items']:
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    
    if item_name == 'torch':
        print("Факел зажжен. Стало светлее.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность с мечом в руках.")
    elif item_name == 'bronze_box':
        print("Вы открыли шкатулку и нашли treasure_key!")
        game_state['player_inventory'].append('treasure_key')
        game_state['player_inventory'].remove('bronze_box')
    else:
        print("Вы не знаете, как это использовать.")