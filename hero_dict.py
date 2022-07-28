import json

heroes_json = 'heroes.json'


def choice(heroes_json):
    with open(heroes_json, 'r') as fp:
        heroes = json.load(fp)

    hero_dict = {heroes[num]['id']: heroes[num]['localized_name']
                 for num in range(0, len(heroes))}

    choices = list(hero_dict.items())
    nil_choice = ('Nil', 'Nil')
    choices.insert(0, nil_choice)
    return choices


def hero_dictionary(heroes_json):
    with open(heroes_json, 'r') as fp:
        heroes = json.load(fp)

    hero_dict = {heroes[num]['id']: heroes[num]['localized_name']
                 for num in range(0, len(heroes))}

    return hero_dict
