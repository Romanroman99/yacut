import random
import string

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    sequence = ''.join(random.choice(characters) for _ in range(length))
    return sequence


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
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
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
