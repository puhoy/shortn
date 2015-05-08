__author__ = 'meatpuppet'
# -*- coding: utf-8 -*-

from . import main
from flask import render_template, redirect, abort, url_for, request, flash, make_response, Markup, current_app, flash
from .forms import SubmitLinkForm

from ..shortn.shortn import shorten_url, lengthen_url


@main.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    """


    :return:
    """
    form = SubmitLinkForm()
    if form.validate_on_submit():
        code, long_url = shorten_url(form.link.data)
        if not code:
            flash('something went wrong...')
            return redirect(url_for('main.index'))
        form.link.data = ''
        return render_template('main_index.html',
                               form=form,
                               url=url_for('main.expand', code=code, _external=True),
                               long_url=long_url)
    return render_template('main_index.html', form=form, url='', long_url='')



@main.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

@main.route('/static/about')
def about():
    """
    path to the static about page

    :return:
    """

    return render_template('main_about.html')

@main.route('/static/apidoc')
def apidoc():
    """
    path to the api docs

    :return:
    """
    return redirect(url_for('main.index'))

@main.route('/<string:code>')
def expand(code):
    """
    expands the code to the long url and 301-redirects to the url

    :param code:
    :return:
    """
    if code:
        url = lengthen_url(code)  # TODO flash a message if not in db
        if url:
            return redirect(url, 301)
        flash('short code was not found!')
    return redirect(url_for('main.index'))
