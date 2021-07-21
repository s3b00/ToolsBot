from marvel.marvel import Marvel

public_marvel = '8858f79742ffa4334a6a15cb0cf2a4a8'
private_marvel = 'd7246ca15fce4691230103bf782d0c571a05a3ee'
marvel = Marvel(public_marvel, private_marvel)

def get_charter(name):
    return marvel.characters.all(name=name)['data']['results'][0]['description']

def get_comic(title):
    return marvel.comics.all(title=title)['data']['results'][0]