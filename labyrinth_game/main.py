#!/usr/bin/env python3
from .player_actions import get_input, move_player, show_inventory, take_item, use_item
from .utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle


def process_command(game_state, command):
    """Обработка команд пользователя"""
    parts = command.split()
    if not parts:
        return
    
    cmd = parts[0]
    
    # Односложные команды движения
    if cmd in ['north', 'south', 'east', 'west']:
        move_player(game_state, cmd)
        return
    
    match cmd:
        case 'look':
            describe_current_room(game_state)
        case 'go' if len(parts) > 1:
            move_player(game_state, parts[1])
        case 'take' if len(parts) > 1:
            if parts[1] == 'treasure_chest':
                print("Вы не можете поднять сундук, он слишком тяжелый.")
            else:
                take_item(game_state, parts[1])
        case 'use' if len(parts) > 1:
            use_item(game_state, parts[1])
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'help':
            show_help()
        case 'quit' | 'exit':
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    """Основная функция игры"""
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
