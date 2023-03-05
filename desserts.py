# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
my_secret_key = os.urandom(12)
app.config['SECRET_KEY'] = my_secret_key
full_recipes = []


class Recipe:
    def __init__(self, number, title, photo, text, time, place, ingredients):
        self.number = number
        self.title = title
        self.photo = photo
        self.text = text
        self.time = time
        self.place = place
        self.ingredients = ingredients


class QuestionsForm(FlaskForm):
    q1 = RadioField('Насколько хорошо вы оцениваете свои способности в готовке?',
                    coerce=int,
                    choices=[(0, 'Хорошо'), (1, 'Плохо')],
                    validators=[InputRequired()])
    q2 = RadioField('Вы хотели бы поддержать атмосферу празника или сегодня обычный день?',
                    coerce=int,
                    choices=[(0, 'Праздник'), (1, 'Обычный день')],
                    validators=[InputRequired()])
    q3 = RadioField('У вас сегодня продуктивный день или вы планировали расслабиться?',
                    coerce=int,
                    choices=[(0, 'Продуктивный день'), (1, 'Расслабиться')],
                    validators=[InputRequired()])
    q4 = RadioField('Вы раздражены или в хорошем расположении духа?',
                    coerce=int,
                    choices=[(0, 'Раздражен'), (1, 'Всё хорошо')],
                    validators=[InputRequired()])
    q5 = RadioField('Вы хотели бы поднять свое настроение или оставить как есть?',
                    coerce=int,
                    choices=[(0, 'Поднять настроение'), (1, 'Оставить как есть')],
                    validators=[InputRequired()])
    submit = SubmitField('Принять')


def load_recipes_list(recipes_file):
    with open(recipes_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    return list(data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    form = QuestionsForm()
    if form.validate_on_submit():
        recipes_list_id = \
            form.q1.data * 16 + form.q2.data * 8 + form.q3.data * 4 + form.q4.data * 2 + form.q5.data + 1
        return redirect('/recipes_list/' + str(recipes_list_id))
    return render_template('questions.html', form=form)


@app.route('/recipes_list/<int:recipes_list_id>')
def recipes_list(recipes_list_id):
    short_recipes = list((x for x in full_recipes if x['number'] == recipes_list_id))
    return render_template('recipes_list.html', recipes=short_recipes)


@app.route('/recipe_full/<string:recipe_title>')
def recipe_full(recipe_title):
    recipe = next((x for x in full_recipes if x['title'] == recipe_title), None)
    if recipe is None:
        return render_template('404.html'), 404
    return render_template('recipe_full.html', recipe=recipe)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    full_recipes = load_recipes_list('static/recipes_list.json')
    app.run(debug=True)
