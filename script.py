from marvel_handler.marvel import get_charter, get_comic
from weather_handler.weather import get_weather
from database_handler.blacklist_handle import blacklist_add, blacklist_get, blacklist_remove, isInBlackList
import random, vk_api, vk, sqlite3
from deep_translator import GoogleTranslator

from vk_handler.handler import sendMessage

import re, requests

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



vk_session = vk_api.VkApi(token='9453184fa64a12c3ada4474945aef4fc9c1a94a83c0f43240e9a53c0af8d77fe835e74798544c0b284529')
longpoll = VkBotLongPoll(vk_session, 205956256)
vk = vk_session.get_api()

blacklist = blacklist_get()


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            try:
                if isInBlackList(str(event.object['message']['from_id']), str(event.chat_id)) and '/tools_suicide' not in str(event.message.text).lower():
                    vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])

                if '/tools_echo' in str(event.message.text).lower():
                    sendMessage('Привет!', event)
                if '/tools_mute' in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                    except:
                        id = re.search(r'id(\d+)\|', str(event.message.text).lower().split(' ')[1])[1]
                        if not isInBlackList(id, str(event.chat_id)):
                            blacklist_add(id, event.chat_id)
                            sendMessage('Пользователь добавлен в черный список!', event)
                        else:
                            sendMessage('❗ Этот пользователь уже в черном списке!', event)
                if '/tools_unmute' in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                    except:
                        id = re.search(r'id(\d+)\|', str(event.message.text).lower().split(' ')[1])[1]
                        if isInBlackList(id, str(event.chat_id)):
                            blacklist_remove(id, event.chat_id)
                            sendMessage('Пользователь снова может писать сюда!', event)
                        else:
                            sendMessage('❗ Этого пользователя нет в черном списке!', event)
                if '/tools_number' in str(event.message.text).lower():
                    req = requests.get(f'http://numbersapi.com/{random.randint(1,1000)}/trivia')
                    sendMessage(GoogleTranslator(source='auto', target='ru').translate(req.text), event)
                if '/tools_random' in str(event.message.text).lower():
                    sendMessage(f'[0-100]: {str(random.randint(0,100))} points', event)
                if '/tools_suicide' in str(event.message.text).lower():
                    id = str(event.object.message['from_id'])
                    if not isInBlackList(id, str(event.chat_id)):
                        blacklist_add(id, event.chat_id)
                        sendMessage('Вы заблокировали себя до моего перезапуска!', event)
                    else:
                        sendMessage('❗ Вы уже в черном списке, ЧТО?!', event)
                if '/tools_goose' in str(event.message.text).lower():
                    with open('goose.txt', 'r') as goose:
                        sendMessage(''.join(goose.readlines()), event)
                if '/tools_elephant' in str(event.message.text).lower():
                    with open('elephant.txt', 'r') as elephant:
                        sendMessage(''.join(elephant.readlines()), event)              
                if '/tools_marvel_charters' in str(event.message.text).lower():
                    try:
                        hero = re.search(' (.+)', str(event.message.text).lower()).groups()[0]
                        
                        charter_description = get_charter(hero)
                        sendMessage(GoogleTranslator(source='auto', target='ru').translate(charter_description), event)
                    except Exception as e:
                        sendMessage(f'Чтобы воспользоваться этой командой, через пробел после команды напишите имя персонажа для поиска\n\n❗ KeyError: {e}', event)
                if '/tools_marvel_comics' in str(event.message.text).lower():
                    try:
                        comic = re.search(' (.+)', str(event.message.text).lower()).groups()[0]

                        comic_search = get_comic(comic)

                        comic_description = comic_search['description']
                        desc = GoogleTranslator(source='auto', target='ru').translate(comic_description)
                        comic_title = comic_search['title']
                        
                        sendMessage(f'{comic_title} \n\n {desc}', event)
                    except Exception as e:
                        sendMessage(f'❗ Чтобы воспользоваться этой командой, через пробел после команды напишите название комикса для поиска\n\n❗ KeyError: {e}', event)
                if '/tools_weather' in str(event.message.text).lower():
                    try:
                        city = re.search(' (.+)', str(event.message.text)).groups()[0]
                        try:
                            weather = get_weather(city)
                            temperature = weather['main']['temp'] 
                            status = weather['weather'][0]['description'].title()
                            sendMessage(f'Погода в городе {city}: {temperature} °C, {status}', event)
                        except Exception as f:
                            sendMessage(f'Не получилось получить данные о погоде в городе {city} :(', event)
                            print(f)
                    except Exception as e:
                        sendMessage(f'❗ Что-то пошло не так, попробуйте написать город через пробел после команды!\n\n', event)
            
            except Exception as e:
                print(e)
                sendMessage('❗ Что-то произошло, я ничего не могу с этим поделать!!', event)