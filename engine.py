from nnpredictor import *

radiant_team = []
dire_team = []


def main():
    my_team = radiant_team
    their_team = dire_team
    print(
        f'My Team: {[get_hero_human_readable(hero_id) for hero_id in my_team]}')
    print(
        f'Their Team:{[get_hero_human_readable(hero_id) for hero_id in their_team]}')
    print('Recommend:')

    engine = Engine(NNPredictor())
    recommendations = engine.recommend(my_team, their_team)
    print(f'{[(prob, get_hero_human_readable(hero))for prob, hero in recommendations]}')


class Engine:

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def get_candidates(self, my_team, their_team):
        '''Return a list of hero_IDs to consider for recommending'''
        ids = [
            i for i in hero_ids if i not in my_team and i not in their_team and i not in missing_ids]
        return ids

    def recommend(self, my_team, their_team, human_readable=False):
        '''Return a list of (hero, probability of winning with hero_added) recommend to complete my_team'''

        assert len(
            my_team) <= 5
        assert len(their_team) <= 5

        hero_candidates = self.get_candidates(my_team, their_team)
        return self.algorithm.recommend(my_team, their_team, hero_candidates)

    def predict(self, dream_team, their_team):
        '''Return the probability of the dream_team winning against their team'''
        return self.algorithm.predict(dream_team, their_team)
