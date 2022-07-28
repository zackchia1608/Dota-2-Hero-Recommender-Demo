import tensorflow as tf
import numpy as np
import json


with open('heroes.json', 'r') as fp:
    heroes = json.load(fp)
    hero_ids = [hero['id'] for hero in heroes]


def get_hero_human_readable(hero_id):
    for hero in heroes:
        if hero['id'] == hero_id:
            return hero['localized_name']
    return 'Unknown hero: %d' % hero_id


FINAL_HERO_ID = int(hero_ids[-1])
NUM_FEATURES = FINAL_HERO_ID * 2
ENV_PATH = 'model.h5'

missing_ids = []
for num in range(0, FINAL_HERO_ID):
    if num not in hero_ids:
        missing_ids.append(num)


class NNPredictor:
    '''Load Model from the environment path for us to train'''

    def __init__(self, env_path=ENV_PATH):
        self.model = tf.keras.models.load_model(env_path)

    def transform(self, my_team, their_team):
        '''Transform our inputs into the tensorflow input array of shape (1, 246). Slice list of IDs from heroes list '''
        X = np.zeros((1, (NUM_FEATURES+1)))
        '''Slice hero_id chosen onto the array, add number of heroes to hero_id for dire team'''
        for hero_id in my_team:
            X[0][(hero_id)] = 1

        map(lambda x: x + FINAL_HERO_ID, their_team)

        for hero_id in their_team:
            X[0][(hero_id)] = 1

        missing_ids = []
        for num in range(0, FINAL_HERO_ID):
            if num not in hero_ids:
                missing_ids.append(num)

        dire_ids = []
        for id in missing_ids:
            if id > 0:
                dire_id = id + FINAL_HERO_ID
                dire_ids.append(dire_id)

        missing_ids = missing_ids + dire_ids

        X = np.delete(X, missing_ids, axis=1)
        return X

    def recommend(self, my_team, their_team, hero_candidates):
        team_possibilities = [(candidate, my_team + [candidate])
                              for candidate in hero_candidates]

        prob_candidate_pairs = []
        for candidate, team in team_possibilities:
            query = self.transform(team, their_team)
            prob = self.score(query)
            prob_candidate_pairs.append((prob, candidate))
        prob_candidate_pairs = sorted(prob_candidate_pairs, reverse=True)[0:3]
        return prob_candidate_pairs

    def score(self, query):
        rad_prob_1 = self.model.predict(query, verbose=False)[0][0]
        return rad_prob_1

    def predict(self, dream_team, their_team):
        '''Returns the probability of the dream_team winning against their_team.'''
        dream_team_query = self.transform(dream_team, their_team)
        return self.score(dream_team_query)
