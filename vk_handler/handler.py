import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token='9453184fa64a12c3ada4474945aef4fc9c1a94a83c0f43240e9a53c0af8d77fe835e74798544c0b284529')
vk = vk_session.get_api()

def sendMessage(message: str, event):
    vk.messages.send(
        key = ('df22dfea502e319ffbace71e393d331d61c85d3d'),      
        server = ('https://lp.vk.com/wh205956256'),
        ts=('2'),
        random_id = get_random_id(),
        message=message,
        chat_id = event.chat_id
    )

def getUsers(id: str):
    return vk.users.get(user_ids=id)
