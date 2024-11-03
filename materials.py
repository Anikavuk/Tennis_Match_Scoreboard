# НЕ УДАЛЯТЬ
# def app(environ, start_response):
#     status = '200 OK'
#     response_headers = [('Content-type', 'text/plain')]
#     start_response(status, response_headers)
#     return [b"Hello, world4"]

#
# import itertools
#
# counter = 0
# for item in itertools.cycle(['A', 'B', 'C']):
#     if counter >= 6:
#         break
#     print(item)  # A, B, C, A, B, C
#     counter += 1
# from src.errors import InvalidPlayernameError, ErrorResponse
from src.dao.player_DAO import PlayerDAO
# def add():
#     form = {'player1': [],'player2': ['ДжекВууу']}
#
#     players_name_1 = form.get('player1')[0]
#     players_name_2 = form.get('player2')[0]
#     status = '200 OK'
#     if players_name_1 and players_name_2:
#         player1 = PlayerDAO(players_name_1).is_valid_username(players_name_1)
#         player2 = PlayerDAO(players_name_2).is_valid_username(players_name_2)
#         if player1 and player2:
#             player1 = PlayerDAO(players_name_1).save_player(players_name_1)
#             player2 = PlayerDAO(players_name_2).save_player(players_name_2)
#             if player1 == None and player2 ==None: # TODO эта строчка не рабочая
#                 print('Ошибка в дубликате')
#         else:
#             print('ошибка с цифрой')
#             error_response = InvalidPlayernameError()
#             response_body = error_response.message
#             status = ErrorResponse.error_response(exception=InvalidPlayernameError)
#     else: # ToDO ошибка не работает если имени нет
#         print('ошибка с цифрой')
#         error_response = InvalidPlayernameError()
#         response_body = error_response.message
#         status = ErrorResponse.error_response(exception=InvalidPlayernameError)
#
#     return f'Все удачно'
#     # return player1
# add()
j = 'Попецtttttt'
print(PlayerDAO(j).is_valid_username(j))
print(9999999, PlayerDAO(j).save_player(j))

# def is_valid_username(name):
#     """Проверка на валидацию введенного имени"""
#     for letter in name:
#         if not ((65 <= ord(letter) <= 90) or
#                 (97 <= ord(letter) <= 122) or
#                 (1040 <= ord(letter) <= 1103)):
#             return False
# #     return True
form = {'player1': ['Боб'], 'player2': ['Джек']}
players_names = {key: form.get(key)[0] if form.get(key) else None for key in ['player1', 'player2']}
# players = {name: PlayerDAO(name) for name in players_names.values()}
# if not all(player.is_valid_username(name) for player, name in zip(players.values(), players_names.values())):
#         print("Дубликат имени")
# print(1, players_names) #{'player1': 'Боб', 'player2': 'Джек'}
# print(2, players) # {'Боб': <src.dao.player_DAO.PlayerDAO object at 0x000001C71D2A6150>, 'Джек': <src.dao.player_DAO.PlayerDAO object at 0x000001C71D533790>}
# print(3, all(players_names.values())) # True или False
players_valid = {key: True for key,value in players_names.items() if PlayerDAO.is_valid_username(value)} # проверка на валидацию
# print(4, players_valid) # {'player1': 'Боб', 'player2': 'Джек'} - поршел проверку на буквы
# print(all(players_valid))
# if not players_valid or ('player1' not in players_valid or 'player2' not in players_valid):
#         print('ошибка на цифру')
#
#
players_save = {key: value for key, value in players_valid.items() if PlayerDAO.save_player(value)}
print(66666, players_save)
# if not players_save:
#         print("Дубликат имени")
#
# response_body = {400: 'You need to enter a different, unique nameone'}
# response = {400: 'You need to enter a different, unique nameone'}
# if type(response) == dict:
#     status = list(response.keys())[0]
#     response_body = list(response.values())[0]
#     print(status)
#     print(response_body)