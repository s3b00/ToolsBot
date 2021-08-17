from database_handler.banlist_handle import banlist_add, banlist_remove, isInBanlist
from database_handler.limits_handle import command_limits_add, command_limits_update, getLimit, isInCommand_limits
from database_handler.key_handle import chat_keys_add, chat_keys_get, chat_keys_remove, getKey, isInChat_keys
from database_handler.pidor_handle import isInPidor_games_members, isInPidor_games_today, pidor_games_add, pidor_games_get, pidor_games_members_add, pidor_games_members_get, pidors_add, pidors_games_get_group, pidors_get_user_group
from database_handler.roulette_handle import isInRoullets, isInRoulletsGames, roullets_add, roullets_games_add, roullets_games_get_game, roullets_games_remove, roullets_get, roullets_games_get, roullets_get_game, roullets_remove
from marvel_handler.marvel import get_charter, get_comic
from weather_handler.weather import get_weather
from database_handler.blacklist_handle import blacklist_add, blacklist_get, blacklist_remove, isInBlackList
import random, vk_api, vk, sqlite3, datetime
from deep_translator import GoogleTranslator
from help_message import help_message
from vk_api.utils import get_random_id

from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_handler.handler import getUsers, sendMessage
from vk_api.utils import get_random_id


import re, requests

vk_session = vk_api.VkApi(token='9453184fa64a12c3ada4474945aef4fc9c1a94a83c0f43240e9a53c0af8d77fe835e74798544c0b284529')
longpoll = VkBotLongPoll(vk_session, 205956256)
vk = vk_session.get_api()

blacklist = blacklist_get()
roullets = roullets_get()
roullets_games = roullets_games_get()
pidor_games = pidor_games_members_get()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            try:
                if 'action' in event.message:
                    if event.message.action['type'] == 'chat_invite_user':
                        users = getUsers(event.object['message']['from_id'])[0]
                        members = vk.messages.getConversationMembers(group_id=event.chat_id, peer_id=2000000000+int(event.chat_id))['items']
                        isAdmin = False

                        for x in members:
                            if x['member_id'] == user['id'] and 'is_admin' in x:
                                isAdmin = True
                        
                        if isAdmin:
                            if isInBanlist(event.chat_id, event.message.action['member_id']):
                                banlist_remove(event.chat_id, event.message.action['member_id'])
                            else:
                                sendMessage('Его не было в банлисте!', event)
                        else:
                            vk.messages.removeChatUser(chat_id=event.chat_id, user_id=event.message.action['member_id'])
                    continue   
                
                if isInBlackList(str(event.object['message']['from_id']), str(event.chat_id)) and '/tools_suicide' not in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                        continue
                    except:
                        if not 'action' in event.message:
                            sendMessage('Я не смог удалить твое сообщение, в знак слабости убираю тебя из черного списка!', event)
                            blacklist_remove(str(event.object['message']['from_id']), event.chat_id)
                
                commands = re.findall('\/\w+ ?[\w\@\]\[\| ]*', str(event.message.text).lower())

                if commands:
                    with open('commands', 'a') as log:
                        log.write('\n' + str(event.message.text).lower())
                    
                    for command in commands[:getLimit(event.chat_id) and int(getLimit(event.chat_id)[1]) or 10]:
                        if '/t_help' in command:
                            sendMessage(help_message, event)
                            break
                        if '/t_set' in command:
                            try:
                                key = command.split(' ')[1]
                                value = ' '.join(event.message.text.split(' ')[2:])
                                print(value)

                                chat_keys_add(event.chat_id, key, value)
                                sendMessage('Ключ успешно добавлен', event)
                                break
                            except Exception as e:
                                print(e)
                                sendMessage('Ошибка. Попробуйте исправить написание команды!', event)
                        if '/t_get' in command:
                            try:
                                key = command.split(' ')[1]

                                value = getKey(event.chat_id, key)[2]
                                if value:
                                    sendMessage(value, event)
                                else:
                                    sendMessage('Такого ключа нет!', event)
                            except Exception as e:
                                print(e)
                                sendMessage('Ошибка. Попробуйте исправить написание команды!', event)
                        if '/t_remove' in command:
                            key = command.split(' ')[1]
                            if isInChat_keys(event.chat_id, key):
                                try:
                                    chat_keys_remove(event.chat_id, key)
                                    sendMessage('Ключ успешно был удален', event)
                                except Exception as e:
                                    print(e)
                                    sendMessage('Произошла ошибка при удалении! Попробуйте иначе!', event)            
                        if '/t_echo' in command:
                            sendMessage('Привет!', event)
                        if '/t_mute' in command:
                            try:
                                vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                            except:
                                id = re.search(r'id(\d+)\|', command.split(' ')[1])[1]
                                if not isInBlackList(id, str(event.chat_id)):
                                    blacklist_add(id, event.chat_id)
                                    sendMessage('Пользователь добавлен в черный список!', event)
                                else:
                                    sendMessage('❗ Этот пользователь уже в черном списке!', event)
                        if '/t_unmute' in command:
                            try:
                                vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                            except:
                                id = re.search(r'id(\d+)\|', command.split(' ')[1])[1]
                                if isInBlackList(id, str(event.chat_id)):
                                    blacklist_remove(id, event.chat_id)
                                    sendMessage('Пользователь снова может писать сюда!', event)
                                else:
                                    sendMessage('❗ Этого пользователя нет в черном списке!', event)
                        if '/t_ban' in command:
                            try:
                                receiver = re.search(r'id(\d+)\|', command.split(' ')[1])[1]
                                user = getUsers(str(event.object.message['from_id']))[0]
                                members = vk.messages.getConversationMembers(group_id=event.chat_id, peer_id=2000000000+int(event.chat_id))['items']
                                isAdmin = False
                                isReceiverAdmin = False

                                for x in members:
                                    if x['member_id'] == user['id'] and 'is_admin' in x:
                                        isAdmin = True
                                    if x['member_id'] == receiver and 'is_admin' in x:
                                        isReceiverAdmin = True
                                
                                if isAdmin:
                                    if not isReceiverAdmin:
                                        vk.messages.removeChatUser(chat_id=event.chat_id, user_id=receiver)
                                        banlist_add(event.chat_id, receiver)
                                        sendMessage('Пользователь успешно был заблокирован!', event)
                                    else:
                                        sendMessage('Пользователь является админом, его нельзя исключить и забанить!', event)
                                else:
                                    sendMessage('Вы не админ, даже не пробуйте банить!', event)
                            except Exception as e:
                                print(e)
                                sendMessage(f'Произошла ошибка при инициализации команды, попробуйте написать ее правильно! /t_ban @user', event)
                        if '/t_roullete' in command:
                            try:
                                limit = command.split(' ')[1] 
                                target = command.split(' ')[2]
                            except:
                                limit = '6'
                                target = 'mute'

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
                        if '/t_register_roullete' in command:
                            if isInRoullets(event.chat_id):
                                id = str(event.object.message['from_id'])
                                current_game_players = roullets_games_get_game(event.chat_id)
                                current_game = roullets_get_game(event.chat_id)
                                limit = int(current_game[1]) - len(current_game_players)
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
                        if '/t_start_roullete' in command:
                            if isInRoullets(event.chat_id):
                                current_game_players = roullets_games_get_game(event.chat_id)

                                if len(current_game_players) > 1:
                                    random.shuffle(current_game_players)
                                    for x in current_game_players[:-1]:
                                        user = getUsers(x[1])[0]
                                        name = user['first_name']
                                        sendMessage(f'Игрок [id{x[1]}|{name}] выживает после выстрела!', event)
                                    user = getUsers(current_game_players[-1][1])[0]
                                    name = user['first_name']
                                    sendMessage(f'Остался последний патрон, последний участник [id{current_game_players[-1][1]}|{name}]. Не повезло, ты выбываешь. Игра окончена!', event)
                                    
                                    members = vk.messages.getConversationMembers(group_id=event.chat_id, peer_id=2000000000+int(event.chat_id))['items']
                                    flag = True

                                    for x in members:
                                        if x['member_id'] == user['id'] and 'is_admin' in x:
                                            sendMessage('Проиграл администратор, отделается предупреждением!', event)
                                            flag = False

                                    if flag:
                                        current_game = roullets_get_game(event.chat_id)
                                        if current_game[2] == 'mute':
                                            blacklist_add(current_game_players[-1][1], event.chat_id)
                                        elif current_game[2] == 'kick':
                                            vk.messages.removeChatUser(chat_id=event.chat_id, user_id=current_game_players[-1][1])
                                        elif current_game[2] == 'ban':
                                            vk.messages.removeChatUser(chat_id=event.chat_id, user_id=current_game_players[-1][1])
                                            banlist_add(event.chat_id, current_game_players[-1][1])
                                            sendMessage('Пользователь был забанен в этой беседе!', event)
                                            
           
                                    for x in current_game_players:
                                        roullets_games_remove(x[1], event.chat_id)
                                    roullets_remove(event.chat_id)
                                else:
                                    sendMessage('Рулетка без игроков игроков? Так не пойдет!', event)
                            else:
                                sendMessage('Игра даже еще не зарегистрирована!', event)
                        if '/t_end_roullete' in command:
                            players = roullets_games_get_game(event.chat_id)
                            if players:
                                for x in players:
                                    roullets_games_remove(x[1], x[0])
                                
                                roullets_remove(event.chat_id)
                                sendMessage('Ваша игра закончена!', event)
                            else:
                                sendMessage('Вы даже не играли!', event)
                        if '/t_players_roullete' in command:
                            if isInRoullets(event.chat_id):
                                players = roullets_games_get_game(event.chat_id)

                                result = ['Игроки в этой рулетке:\n']
                                for x in players:
                                    user = getUsers(x[1])[0]
                                    user_first_name = user['first_name']
                                    user_id = user['id']
                                    result.append(f'\n[id{user_id}|{user_first_name}]')

                                sendMessage(''.join(result), event)
                            else:
                                sendMessage('Вы еще не запустили игру. Участников нет!', event)
                        if '/t_number' in command:
                            req = requests.get(f'http://numbersapi.com/{random.randint(1,1000)}/trivia')
                            sendMessage(GoogleTranslator(source='auto', target='ru').translate(req.text), event)
                        if '/t_random' in command:
                            sendMessage(f'[0-100]: {str(random.randint(0,100))} points', event)
                        if '/t_flip' in command:
                            sendMessage(f"Вы подбросили монету: {'Орел' if str(random.randint(0,1)) == '1' else 'Решка'}", event)
                        if '/t_suicide' in command:
                            id = str(event.object.message['from_id'])
                            if not isInBlackList(id, str(event.chat_id)):
                                blacklist_add(id, event.chat_id)
                                sendMessage('Вы заблокировали себя до моего перезапуска!', event)
                            else:
                                sendMessage('❗ Вы уже в черном списке, ЧТО?!', event)
                        if '/t_goose' in command:
                            with open('animals/goose.txt', 'r') as goose:
                                sendMessage(''.join(goose.readlines()), event)
                        if '/t_elephant' in command:
                            with open('animals/elephant.txt', 'r') as elephant:
                                sendMessage(''.join(elephant.readlines()), event)       
                        if '/t_shrek' in command:
                            with open('animals/shrek.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/t_fak' in command:
                            with open('animals/fak.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/t_kchau' in command:
                            with open('animals/kchau.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/t_yes' in command:
                            with open('animals/yes.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/t_face' in command:
                            with open('animals/face.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)
                        if '/t_anime_bitch' in command:
                            with open('animals/anime_bitch.txt', 'r') as animal:
                                sendMessage(''.join(animal.readlines()), event)        
                        if '/t_marvel_charters' in command:
                            try:
                                hero = re.search(' (.+)', command).groups()[0]
                                
                                charter_description = get_charter(hero)
                                try:
                                    sendMessage(GoogleTranslator(source='en', target='ru').translate(charter_description), event)
                                except:
                                    sendMessage(charter_description, event)
                            except Exception as e:
                                sendMessage(f'Чтобы воспользоваться этой командой, через пробел после команды напишите имя персонажа для поиска\n\n❗ KeyError: {e}', event)
                        if '/t_marvel_comics' in command:
                            try:
                                comic = re.search(' (.+)', command).groups()[0]

                                comic_search = get_comic(comic)

                                comic_description = comic_search['description']
                                desc = GoogleTranslator(source='en', target='ru').translate(comic_description)
                                comic_title = comic_search['title']
                                
                                sendMessage(f'{comic_title} \n\n {desc}', event)
                            except Exception as e:
                                sendMessage(f'❗ Чтобы воспользоваться этой командой, через пробел после команды напишите название комикса для поиска\n\n❗ KeyError: {e}', event)
                        if '/t_weather' in command:
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
                        if '/t_pidors' in command:
                            if not isInPidor_games_members(event.chat_id):
                                pidor_games_members_add(event.chat_id)
                                sendMessage('Ваша беседа успешно зарегистрировалась в пидоре дня!', event)
                            else:
                                sendMessage('Ваша беседа уже участвует в пидоре дня!', event)
                        if '/t_start_pidors' in command:
                            if isInPidor_games_members(event.chat_id):
                                now = datetime.datetime.now()
                                today = now.strftime("%d-%m-%Y")

                                # if not isInPidor_games_today(event.chat_id, today):
                                members = vk.messages.getConversationMembers(group_id=event.chat_id, peer_id=2000000000+int(event.chat_id))
                                members_in_game = members['items']
                                random_user = members_in_game[random.randint(0, int(members['count'] - 1))]
                                id = int(+random_user['member_id'])

                                pidor_games_add(event.chat_id, today, random_user['member_id'])
                                pidors_add(event.chat_id, id)

                                winner = getUsers(id)[0]
                                name = winner['first_name']
                                sendMessage(f'Сегодняшний пидор дня: [id{id}|{name}], с чем мы его и поздравляем!', event)
                                # else:
                                #     sendMessage(f'Вы уже играли в пидора дня сегодня! Текущее время на сервере: {now.strftime("%H:%M")}', event)
                            else:
                                sendMessage(f'ВЫ еще не зарегистрировались своей беседой в игре! Напишите /t_pidors!', event)
                        if '/t_stats_pidors' in command:
                            if isInPidor_games_members(event.chat_id):
                                games = pidors_games_get_group(event.chat_id)
                                if games:
                                    lastWinner = getUsers(games[-1][2])[0]
                                    last_winner_id = lastWinner['id']
                                    last_winner_name = lastWinner['first_name']

                                    winners = []

                                    for game in games:
                                        if game[2] not in winners:
                                            winners.append(game[2])
                                    
                                    winners_total = []
                                    for winner in winners:
                                        win = getUsers(abs(int(winner)))[0]
                                        win_id = win['id']
                                        win_name = win['first_name']
                                        winners_total.append(f'[id{win_id}|{win_name}]: {len(pidors_get_user_group(winner, event.chat_id))}')


                                    result_of_winners = '\n' + '\n'.join(winners_total)

                                    sendMessage(f"Количество сыгранных игр: {len(games)}\n{'' if len(games) == 0 else f'Последний победитель: [id{last_winner_id}|{last_winner_name}]'} \n\n{'' if len(games) == 0 else f'Количество побед у пользователей: {result_of_winners}'}", event)
                                else:
                                    sendMessage('Вы еще не запускали игру "пидор дня"!', event)
                            else:
                                sendMessage(f'ВЫ еще не зарегистрировались своей беседой в игре! Напишите /t_pidors!', event)
                        if '/t_currency_rates' in command:
                            b = BtcConverter()
                            c = CurrencyRates()

                            rub = c.convert('USD', 'RUB', 1)
                            eur = c.convert('USD', 'EUR', 1)

                            sendMessage(f"USD: 1 \n RUB: {rub}₽ \n EUR: {eur}€\n BTC: {b.get_latest_price('USD')}$ за 1BTC", event)
                        if '/t_commands_limit' in command:
                            try:
                                limit = command.split(' ')[1]
                                if int(limit) > 0 and int(limit) < 21:
                                    if isInCommand_limits(event.chat_id):
                                        command_limits_update(event.chat_id, limit)
                                        sendMessage('Вы успешно изменили лимит по командам за раз!', event)
                                    else:
                                        command_limits_add(event.chat_id, limit)
                                        sendMessage('Вы успешно установили лимит по командам за раз!', event)
                                else:
                                    sendMessage('Лимит может быть от 1 до 20!', event)
                            except Exception as e:
                                print(e)
                                sendMessage('Ошибка! Попробуйте вызвать меня иначе!', event)
                        if '/t_report' in command:
                            user = getUsers(str(event.object['message']['from_id']))[0]

                            message = f"От: [id{user['id']}|{user['first_name']}]\n\n" + ' '.join(event.message.text.split(' ')[1:])
                            vk.messages.send(
                                key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                server = ('https://lp.vk.com/wh205956256'),
                                ts=('2'),
                                random_id = get_random_id(),
                                message=message,
                                user_id = 307841071,
                            )
                        if '/t_ping' in command:
                            sendMessage('@all', event)
            except Exception as e:
                raise e
                sendMessage('❗ Что-то произошло, я ничего не могу с этим поделать!!', event)