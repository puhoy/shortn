__author__ = 'meatpuppet'
# -*- coding: utf-8 -*-

from . import main
from flask import render_template, redirect, abort, url_for, request, flash, make_response, Markup
from .forms import SubmitLinkForm

from ..shortn.shortn import shorten_url, lengthen_url, _standardize_url


@main.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    form = SubmitLinkForm()
    short_url = ''
    long_url = ''
    if form.validate_on_submit():
        short_url, long_url = shorten_url(form.link.data)
    return render_template('main_index.html', form=form, url=short_url, long_url=long_url)

@main.route('/static/about')
def about():
    return render_template('main_about.html')

@main.route('/static/apidoc')
def apidoc():
    return redirect(url_for('main.index'))

@main.route('/<path:code>')
def expand(code):
    """

    :param code:
    :return:
    """
    if code:
        print('called:' + code)
        url = lengthen_url(code)
    return redirect(url, 301)