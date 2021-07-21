from database_handler.roulette_handle import isInRoullets, isInRoulletsGames, roullets_add, roullets_games_add, roullets_games_get_game, roullets_games_remove, roullets_get, roullets_games_get, roullets_get_game, roullets_remove
from marvel_handler.marvel import get_charter, get_comic
from weather_handler.weather import get_weather
from database_handler.blacklist_handle import blacklist_add, blacklist_get, blacklist_remove, isInBlackList
import random, vk_api, vk, sqlite3
from deep_translator import GoogleTranslator

from vk_handler.handler import getUsers, sendMessage

import re, requests

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



vk_session = vk_api.VkApi(token='9453184fa64a12c3ada4474945aef4fc9c1a94a83c0f43240e9a53c0af8d77fe835e74798544c0b284529')
longpoll = VkBotLongPoll(vk_session, 205956256)
vk = vk_session.get_api()

blacklist = blacklist_get()
roullets = roullets_get()
roullets_games = roullets_games_get()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            try:
                commands = re.findall('\/\w+ ?[\w\@\]\[\| ]*', str(event.message.text).lower())
                if isInBlackList(str(event.object['message']['from_id']), str(event.chat_id)) and '/tools_suicide' not in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                    except:
                        sendMessage('Я не смог удалить твое сообщение, в знак слабости убираю тебя из черного списка!', event)
                        blacklist_remove(str(event.object['message']['from_id']), event.chat_id)

                if commands:
                    for command in commands:
                        if '/tools_echo' in command:
                            sendMessage('Привет!', event)
                        if '/tools_mute' in command:
                            try:
                                vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                            except:
                                print(f'-{command}-')

                                id = re.search(r'id(\d+)\|', command.split(' ')[1])[1]
                                if not isInBlackList(id, str(event.chat_id)):
                                    blacklist_add(id, event.chat_id)
                                    sendMessage('Пользователь добавлен в черный список!', event)
                                else:
                                    sendMessage('❗ Этот пользователь уже в черном списке!', event)
                        if '/tools_unmute' in command:
                            try:
                                vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                            except:
                                id = re.search(r'id(\d+)\|', command.split(' ')[1])[1]
                                if isInBlackList(id, str(event.chat_id)):
                                    blacklist_remove(id, event.chat_id)
                                    sendMessage('Пользователь снова может писать сюда!', event)
                                else:
                                    sendMessage('❗ Этого пользователя нет в черном списке!', event)
                        if '/tools_roullete' in command:
                            try:
                                limit = command.split(' ')[1] 
                                target = command.split(' ')[2]
                            except:
                                limit = '6'
                                target = 'mute'

                            print(limit, target)
                            if not isInRoullets(event.chat_id):
                                if target:
                                    roullets_add(event.chat_id, limit, target)
                                else:
                                    roullets_add(event.chat_id, limit)
                                roullets_games_add(event.chat_id, str(event.object.message['from_id']),)
                                message = '' if target != 'mute' else '\n\n По умолчанию установлен режим выстрела на мут, однако вы можете изменить это, используя третий параметр, который может быть mute, ban, warn'
                                sendMessage(f'Вы начали игру в русскую рулетку, лимит игроков: {limit} и вы уже в ней зарегистрированы!{message}', event)
                            else:
                                sendMessage('У вас уже запущена игра! Сначала следует доиграть ее!', event)
                        if '/tools_register_roullete' in command:
                            id = str(event.object.message['from_id'])
                            current_game_players = roullets_games_get_game(event.chat_id)
                            current_game = roullets_get_game(event.chat_id)
                            limit = int(current_game[1]) - len(current_game_players)
                            if isInRoullets(event.chat_id):
                                if limit > 0:
                                    if not isInRoulletsGames(event.chat_id, id):
                                        roullets_games_add(event.chat_id, id)
                                        sendMessage(f'Вы успешно зарегистрировались в игре! Осталось игроков: { limit - 1 }', event)
                                    else:
                                        sendMessage(f'Вы уже зарегистрированы в текущей игре, ожидайте!', event)
                                else:
                                    sendMessage('Лимит игроков в этой игре исчерпан!', event)
                            else:
                                sendMessage('В этой беседы русская рулетка еще не запущена для старта!', event)
                        if '/tools_start_roullete' in command:
                            if isInRoullets(event.chat_id):
                                current_game_players = roullets_games_get_game(event.chat_id)

                                if len(current_game_players) > 0:
                                    random.shuffle(current_game_players)
                                    print(current_game_players)
                                    for x in current_game_players[:-1]:
                                        user = getUsers(x[1])[0]
                                        name = user['first_name']
                                        sendMessage(f'Игрок [id{x[1]}|{name}] выживает после выстрела!', event)
                                    user = getUsers(current_game_players[-1][1])[0]
                                    name = user['first_name']
                                    sendMessage(f'Остался последний патрон, последний участник [id{current_game_players[-1][1]}|{name}]. Не повезло, ты выбываешь. Игра окончена!', event)
                                    
                                    current_game = roullets_get_game(event.chat_id)
                                    if current_game[2] == 'mute':
                                        blacklist_add(current_game_players[-1][1], event.chat_id)
                                    elif current_game[2] == 'ban':
                                        vk.messages.removeChatUser(chat_id=event.chat_id, user_id=current_game_players[-1][1])
           
                                    for x in current_game_players:
                                        roullets_games_remove(x[1], event.chat_id)
                                    roullets_remove(event.chat_id)
                                else:
                                    sendMessage('Рулетка на ноль игроков? Так не пойдет!', event)

                        if '/tools_number' in command:
                            req = requests.get(f'http://numbersapi.com/{random.randint(1,1000)}/trivia')
                            sendMessage(GoogleTranslator(source='auto', target='ru').translate(req.text), event)
                        if '/tools_random' in command:
                            sendMessage(f'[0-100]: {str(random.randint(0,100))} points', event)
                        if '/tools_suicide' in command:
                            id = str(event.object.message['from_id'])
                            if not isInBlackList(id, str(event.chat_id)):
                                blacklist_add(id, event.chat_id)
                                sendMessage('Вы заблокировали себя до моего перезапуска!', event)
                            else:
                                sendMessage('❗ Вы уже в черном списке, ЧТО?!', event)
                        if '/tools_goose' in command:
                            with open('animals/goose.txt', 'r') as goose:
                                sendMessage(''.join(goose.readlines()), event)
                        if '/tools_elephant' in command:
                            with open('animals/elephant.txt', 'r') as elephant:
                                sendMessage(''.join(elephant.readlines()), event)       
                        if '/tools_shrek' in command:
                            with open('animals/shrek.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/tools_fak' in command:
                            with open('animals/fak.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/tools_kchau' in command:
                            with open('animals/kchau.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/tools_yes' in command:
                            with open('animals/yes.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/tools_face' in command:
                            with open('animals/face.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/tools_anime_bitch' in command:
                            with open('animals/anime_bitch.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)        
                        if '/tools_marvel_charters' in command:
                            try:
                                hero = re.search(' (.+)', command).groups()[0]
                                
                                charter_description = get_charter(hero)
                                sendMessage(GoogleTranslator(source='auto', target='ru').translate(charter_description), event)
                            except Exception as e:
                                sendMessage(f'Чтобы воспользоваться этой командой, через пробел после команды напишите имя персонажа для поиска\n\n❗ KeyError: {e}', event)
                        if '/tools_marvel_comics' in command:
                            try:
                                comic = re.search(' (.+)', command).groups()[0]

                                comic_search = get_comic(comic)

                                comic_description = comic_search['description']
                                desc = GoogleTranslator(source='auto', target='ru').translate(comic_description)
                                comic_title = comic_search['title']
                                
                                sendMessage(f'{comic_title} \n\n {desc}', event)
                            except Exception as e:
                                sendMessage(f'❗ Чтобы воспользоваться этой командой, через пробел после команды напишите название комикса для поиска\n\n❗ KeyError: {e}', event)
                        if '/tools_weather' in command:
                            try:
                                city = re.search(' (.+)', command).groups()[0]
                                try:
                                    weather = get_weather(city)
                                    temperature = weather['main']['temp'] 
                                    status = weather['weather'][0]['description'].title()
                                    sendMessage(f'Погода в городе {city.title()}: {temperature} °C, {status}', event)
                                except Exception as f:
                                    sendMessage(f'Не получилось получить данные о погоде в городе {city} :(', event)
                                    print(f)
                            except Exception as e:
                                sendMessage(f'❗ Что-то пошло не так, попробуйте написать город через пробел после команды!\n\n', event)
        
            except Exception as e:
                print(e)
                sendMessage('❗ Что-то произошло, я ничего не могу с этим поделать!!', event)