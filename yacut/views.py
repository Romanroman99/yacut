import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    """
    Генерирует уникальный короткий идентификатор заданной длины.
    """
    characters = string.ascii_letters + string.digits
    sequence = ''.join(random.choice(characters) for _ in range(length))
    return sequence


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    """
    Отображает форму для добавления нового URL-адреса.
    """
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id and URLMap.query.filter_by(short=custom_id).first():
            flash('Пользовательская ссылка уже занята.')
            return render_template('index.html', form=form)

        short = custom_id or get_unique_short_id()
        while URLMap.query.filter_by(short=short).first():
            short = get_unique_short_id()
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        flash(url_for('index_view', short=short, _external=True))
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def index_view(short):
    """
    Функция перенаправления с короткой ссылки на длинную.
    """
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
