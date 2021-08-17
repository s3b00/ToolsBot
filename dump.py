from database_handler.blacklist_handle import blacklist_get, blacklist_remove
from database_handler.banlist_handle import banlist_get, banlist_remove
from database_handler.key_handle import chat_keys_get, chat_keys_remove
from database_handler.limits_handle import command_limits_get, command_limits_remove
from database_handler.pidor_handle import pidor_games_members_get, pidor_games_members_remove, pidor_games_get, pidor_games_remove, pidors_get, pidors_remove
from database_handler.roulette_handle import roullets_get, roullets_remove, roullets_games_get, roullets_games_remove

records = blacklist_get()
for record in records:
    blacklist_remove(record[0], record[1])

print(records)

records = banlist_get()
for record in records:
    banlist_remove(record[0], record[1])

print(records)

records = chat_keys_get()
for record in records:
    chat_keys_remove(record[0], record[1])
    
print(records)

records = command_limits_get()
for record in records:
    command_limits_remove(record[0])
    
print(records)

records = pidor_games_members_get()
for record in records:
    pidor_games_members_remove(record[0])
    
print(records)

records = pidor_games_get()
for record in records:
    pidor_games_remove(record[0])
    
print(records)

records = pidors_get()
for record in records:
    pidors_remove(record[0], record[1])
    
print(records)

records = roullets_get()
for record in records:
    roullets_remove(record[0])
    
print(records)

records = roullets_games_get()
for record in records:
    roullets_games_remove(record[1], record[0])
    
print(records)