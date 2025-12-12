from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
from sourcefile.session import Session
bp=Blueprint('dialog', __name__, url_prefix='/api/dialog')

@bp.route('/api_keys')
def api_keys_dialog():
    return render_template('dialogs/api_key.html')

@bp.route('/api_key_groups')
def api_key_groups_dialog():
    return render_template('dialogs/api_key_group.html')

