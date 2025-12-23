from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
from sourcefile.session import Session
from sourcefile.apigroups import API as apigroup
bp=Blueprint('dialog', __name__, url_prefix='/api/dialog')

@bp.route('/api_keys')
def api_keys_dialog():
    group=apigroup.get_all_api_keys()
    return render_template('dialogs/api_key.html',groups=group)

@bp.route('/api_key_groups')
def api_key_groups_dialog():
    return render_template('dialogs/api_key_group.html')


@bp.route('/api_key_delete/<api_key>',methods=['GET'])
def api_key_delete(api_key):
    print(api_key)
    return render_template('dialogs/delete.html',api_key=api_key)

