__author__ = 'meatpuppet'
# -*- coding: utf-8 -*-

"""
THE WHOLE SHORTENING CODE IS BASED ON https://github.com/jessex/shrtn/blob/master/shrtn.py !!!
"""

from . import main
from flask import render_template, redirect, abort, url_for, request, flash, make_response, Markup
from .forms import SubmitLinkForm

from .shorten import shorten_url, lengthen_url, standardize_url


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SubmitLinkForm()
    url = ''
    long_url = ''
    if form.validate_on_submit():
        code = shorten_url(form.link.data)
        long_url = standardize_url(form.link.data)
        url = url_for('main.expand', code=code, _external=True)
    return render_template('main_index.html', form=form, url=url, long_url=long_url)

@main.route('/<code>')
def expand(code=""):
    #return "" + lengthen_url(code)
    return redirect(lengthen_url(code), 301)

