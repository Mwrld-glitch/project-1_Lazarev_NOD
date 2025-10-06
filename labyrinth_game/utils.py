import math

from .constants import COMMANDS, ROOMS
from .player_actions import get_input


def describe_current_room(game_state):
    """Описание текущей комнаты"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    print(f"\n== {current_room.upper()} ==")
    print(room_data['description'])
    
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))
    
    print("Выходы:", ", ".join(room_data['exits'].keys()))
    
    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решение загадки в комнате"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, answer = room_data['puzzle']
    print(question)
    user_answer = get_input("Ваш ответ: ")
    
    # Альтернативные варианты ответов
    if answer == '10' and user_answer in ['10', 'десять']:
        user_answer = '10'
    elif answer == 'молчание' and user_answer in ['молчание', 'тишина', 'обещание']:
        user_answer = 'молчание'
    elif answer == '1 2 3 4' and user_answer in ['1 2 3 4', '1234']:
        user_answer = '1 2 3 4'
    elif answer == 'резонанс' and user_answer in ['резонанс', 'эхо']:
        user_answer = 'резонанс'
    
    if user_answer == answer:
        print("Верно! Загадка решена.")
        room_data['puzzle'] = None
        
        # Награда зависит от комнаты
        if current_room == 'hall':
            game_state['player_inventory'].append('silver_key')
            print("Вы получили silver_key!")
        elif current_room == 'trap_room':
            print("Ловушка деактивирована!")
        elif current_room == 'library':
            game_state['player_inventory'].append('ancient_scroll')
            print("Вы получили ancient_scroll!")
        elif current_room == 'guard_room':
            print("Страж пропускает вас дальше!")
        elif current_room == 'puzzle_chamber':
            print("Механизм разблокирован! Двери открываются.")
            
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытка открыть сокровище"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        choice = get_input("Сундук заперт. Попробовать ввести код? (да/нет): ")
        if choice == 'да':
            user_code = get_input("Введите код: ")
            if user_code == room_data['puzzle'][1]:
                print("Код верный! Сундук открыт!")
                if 'treasure_chest' in room_data['items']:
                    room_data['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор"""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    """Активация ловушки"""
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    if inventory:
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли: {lost_item}")
    else:
        result = pseudo_random(game_state['steps_taken'], 10)
        if result < 3:
            print("Ловушка сработала! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам повезло, вы избежали ловушки.")


def random_event(game_state):
    """Случайное событие при перемещении"""
    EVENT_PROBABILITY = 10
    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(game_state['steps_taken'], 3)
        
        if event_type == 0:
            print("Вы нашли на полу монетку!")
            current_room = game_state['current_room']
            ROOMS[current_room]['items'].append('coin')
        elif event_type == 1:
            print("Вы слышите странный шорох...")
            if 'sword' in game_state['player_inventory']:
                print("Вы отпугнули существо мечом.")
        elif event_type == 2:
            current = game_state['current_room']
            has_torch = 'torch' not in game_state['player_inventory']
            if current == 'trap_room' and has_torch:
                print("Опасность! Ловушка активирована!")
                trigger_trap(game_state)


def show_help():
    """Показать справку по командам"""
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")
