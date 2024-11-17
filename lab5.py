from flask import Blueprint, session, redirect, render_template, request, url_for
lab5 = Blueprint('lab5',__name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')