# -*- coding: utf-8 -*-

import logging
import secrets
from flask import Flask, redirect, flash
from flask import render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired
from recipes import Recipe

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

csrf = CSRFProtect(app)
csrf.init_app(app)

logging.basicConfig(filename='error.log', level=logging.DEBUG)
full_recipes = Recipe.load_json('static/recipes_list.json')


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


@app.route('/')
def index():
    flash(str(len(full_recipes)))
    return render_template('index.html')


@app.route('/questions', methods=['GET', 'POST'])
@csrf.exempt
def questions():
    form = QuestionsForm()
    if form.validate_on_submit():
        recipes_list_id = \
            form.q1.data * 16 + form.q2.data * 8 + form.q3.data * 4 + form.q4.data * 2 + form.q5.data + 1
        flash('recipes_list_id = ' + str(recipes_list_id))
        return redirect('/recipes_list/' + str(recipes_list_id))
        # return redirect(url_for('index'))
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
    app.run(debug=True)
