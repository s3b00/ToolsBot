import random, vk_api, vk
import re, requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='9453184fa64a12c3ada4474945aef4fc9c1a94a83c0f43240e9a53c0af8d77fe835e74798544c0b284529')

longpoll = VkBotLongPoll(vk_session, 205956256)
vk = vk_session.get_api()
blacklist = []

with open('blacklist.txt', 'r') as bl:
    blacklist = bl.readlines()

blacklist = [x.strip() for x in blacklist] 

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            try:
                if '/tools_echo' in str(event.message.text).lower():
                    vk.messages.send(
                        key = ('df22dfea502e319ffbace71e393d331d61c85d3d'), 
                        server = ('https://lp.vk.com/wh205956256'),
                        ts=('2'),
                        random_id = get_random_id(),
                        message='Привет!',
                        chat_id = event.chat_id
                        )
                if '/tools_mute' in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                    except:
                        with open('blacklist.txt', 'a') as bl:
                            id = re.search(r'id(\d+)\|', str(event.message.text).lower().split(' ')[1])[1]
                            if id not in blacklist:
                                bl.write(id + '\n')
                                blacklist.append(id)
                                print(blacklist)
                                vk.messages.send(
                                    key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                    server = ('https://lp.vk.com/wh205956256'),
                                    ts=('2'),
                                    random_id = get_random_id(),
                                    message='Пользователь добавлен в черный список!',
                                    chat_id = event.chat_id
                                )
                            else:
                                vk.messages.send(
                                    key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                    server = ('https://lp.vk.com/wh205956256'),
                                    ts=('2'),
                                    random_id = get_random_id(),
                                    message='Этот пользователь уже в черном списке!',
                                    chat_id = event.chat_id
                                )
                if '/tools_unmute' in str(event.message.text).lower():
                    try:
                        vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
                    except:
                        with open('blacklist.txt', 'a') as bl:
                            id = re.search(r'id(\d+)\|', str(event.message.text).lower().split(' ')[1])[1]
                            if id in blacklist:
                                blacklist.remove(id)
                                with open('blacklist.txt', 'w') as bl:
                                    for x in blacklist:
                                        bl.write(x + '\n')
                                vk.messages.send(
                                    key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                    server = ('https://lp.vk.com/wh205956256'),
                                    ts=('2'),
                                    random_id = get_random_id(),
                                    message='Пользователь снова может писать сюда!',
                                    chat_id = event.chat_id
                                )
                            else:
                                vk.messages.send(
                                    key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                    server = ('https://lp.vk.com/wh205956256'),
                                    ts=('2'),
                                    random_id = get_random_id(),
                                    message='Этого пользователя нет в черном списке!',
                                    chat_id = event.chat_id
                                )
                if '/tools_number' in str(event.message.text).lower():
                    req = requests.get(f'http://numbersapi.com/{random.randint(1,1000)}/trivia')
                    vk.messages.send(
                        key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                        server = ('https://lp.vk.com/wh205956256'),
                        ts=('2'),
                        random_id = get_random_id(),
                        message=req.text,
                        chat_id = event.chat_id
                    )
                if '/tools_random' in str(event.message.text).lower():
                    vk.messages.send(
                        key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                        server = ('https://lp.vk.com/wh205956256'),
                        ts=('2'),
                        random_id = get_random_id(),
                        message=f'[0-100]: {str(random.randint(0,100))} очков',
                        chat_id = event.chat_id
                    )
                if '/tools_suicide' in str(event.message.text).lower():
                    id = str(event.object.message['from_id'])
                    if id not in blacklist:
                        with open('blacklist.txt', 'a') as bl:
                            bl.write(id + '\n')
                            blacklist.append(id)
                            print(blacklist)

                            vk.messages.send(
                                key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                                server = ('https://lp.vk.com/wh205956256'),
                                ts=('2'),
                                random_id = get_random_id(),
                                message='Вы заблокировали себя до моего перезапуска!',
                                chat_id = event.chat_id
                            )
                    else:
                        vk.messages.send(
                            key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                            server = ('https://lp.vk.com/wh205956256'),
                            ts=('2'),
                            random_id = get_random_id(),
                            message='Вы уже в черном списке, ЧТО?!',
                            chat_id = event.chat_id)
                    
                    
                #event.object['message']['from_id'] == 23922700 or s
                if str(event.object['message']['from_id']) in blacklist and '/tools_suicide' not in str(event.message.text).lower():
                    vk.messages.delete(delete_for_all=1, conversation_message_ids = [event.object.message['conversation_message_id']], peer_id=event.object.message['peer_id'])
            except:
                vk.messages.send(
                    key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
                    server = ('https://lp.vk.com/wh205956256'),
                    ts=('2'),
                    random_id = get_random_id(),
                    message='Что-то произошло, я ничего не могу с этим поделать!!',
                    chat_id = event.chat_id
                )