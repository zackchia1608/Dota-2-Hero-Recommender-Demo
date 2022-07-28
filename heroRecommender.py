# Flask implementation

from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from hero_dict import *
from engine import Engine
from nnpredictor import *


app = Flask(__name__, template_folder='html_templates')

app.config['SECRET_KEY'] = 'mysecretkey'


class HeroForm(FlaskForm):

    radiant_hero_1 = SelectField(
        u'First Radiant Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    radiant_hero_2 = SelectField(
        u'Second Radiant Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    radiant_hero_3 = SelectField(
        u'Third Radiant Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    radiant_hero_4 = SelectField(
        u'Fourth Radiant Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    radiant_hero_5 = SelectField(
        u'Fifth Radiant Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    dire_hero_1 = SelectField(u'First Dire Hero:',
                              choices=choice(heroes_json), validators=[DataRequired()])
    dire_hero_2 = SelectField(
        u'Second Dire Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    dire_hero_3 = SelectField(u'Third Dire Hero:',
                              choices=choice(heroes_json), validators=[DataRequired()])
    dire_hero_4 = SelectField(
        u'Fourth Dire Hero:', choices=choice(heroes_json), validators=[DataRequired()])
    dire_hero_5 = SelectField(u'Fifth Dire Hero:',
                              choices=choice(heroes_json), validators=[DataRequired()])
    submit = SubmitField('Recommend')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = HeroForm()
    if form.validate_on_submit():
        session['radiant_hero_1'] = form.radiant_hero_1.data
        session['radiant_hero_2'] = form.radiant_hero_2.data
        session['radiant_hero_3'] = form.radiant_hero_3.data
        session['radiant_hero_4'] = form.radiant_hero_4.data
        session['radiant_hero_5'] = form.radiant_hero_5.data
        session['dire_hero_1'] = form.dire_hero_1.data
        session['dire_hero_2'] = form.dire_hero_2.data
        session['dire_hero_3'] = form.dire_hero_3.data
        session['dire_hero_4'] = form.dire_hero_4.data
        session['dire_hero_5'] = form.dire_hero_5.data

        return redirect(url_for("recommendation"))

    return render_template('home.html', form=form)


@app.route('/recommendation')
def recommendation():

    radiant_team = (filter(lambda x: x != 'Nil', [session['radiant_hero_1'],
                                                  session['radiant_hero_2'],
                                                  session['radiant_hero_3'],
                                                  session['radiant_hero_4'],
                                                  session['radiant_hero_5']]))
    dire_team = (filter(lambda x: x != 'Nil', [session['dire_hero_1'],
                                               session['dire_hero_2'],
                                               session['dire_hero_3'],
                                               session['dire_hero_4'],
                                               session['dire_hero_5']]))
    radiant_team = [[int(s) for s in sublist] for sublist in radiant_team]
    dire_team = [[int(s) for s in sublist] for sublist in dire_team]

    my_team = radiant_team
    their_team = dire_team

    if len(my_team) >= 5:
        return 'Your Team is Full! Please remove a hero from your team for the system to recommend.'
    elif len(my_team) == 0 and len(my_team) == 0:
        return 'Your Team is Empty! Please fill in at least one hero to continue.'
    else:
        engine = Engine(NNPredictor())
        prob_recommendation_pairs = engine.recommend(my_team, their_team)
        recommendations = [hero for prob,
                           hero in prob_recommendation_pairs]
        heroes = [(hero_dictionary(heroes_json)[hero])
                  for hero in recommendations]
        prob = (round(engine.predict(my_team, their_team) * 100, 2))
        probability = f"The probability of your team winning is {prob}% with the proposed team composition."
        return render_template('recommendation.html', prediction_text=f'{heroes}. {probability}')


if __name__ == "__main__":
    app.debug = True
    app.run()
