"""Public section, including homepage and signup."""

from io import BytesIO

from flask import Blueprint, render_template, request, flash, Response
import requests

from .utils import validate


blueprint = Blueprint('public', __name__,  # pylint: disable=invalid-name
                      static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Show the home page."""
    if request.method == 'POST':
        form_data = request.form
    else:
        form_data = request.args
    source = form_data.get('source')
    if not source:
        return render_template('public/home.html')

    source_data = BytesIO(source.encode())
    response = validate(source_data)
    flash_msg_type = 'success' if response['success'] else 'danger'
    flash(response['flash_msg'], flash_msg_type)
    return render_template('public/home.html',
                           source=source,
                           result=response['result'])


@blueprint.route('/transform')
def transform():
    url = request.args.get('url')
    r = requests.get(url)
    source = r.content.decode()
    source_data = BytesIO(r.content)
    response = validate(source_data)
    if response['success']:
        return Response(response['result'], mimetype='text/xml')

    if request.args.get('fallback') == 'true':
        return Response(source, mimetype='text/xml')

    flash_msg_type = 'success' if response['success'] else 'danger'
    flash(response['flash_msg'], flash_msg_type)
    return render_template('public/home.html',
                           source=source,
                           result=response['result'])
