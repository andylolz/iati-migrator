"""Public section, including homepage and signup."""

from urllib.parse import urlencode
from io import BytesIO

from flask import Blueprint, render_template, request, redirect, \
    flash, Response, url_for
import requests

from .utils import validate


blueprint = Blueprint('public', __name__,  # pylint: disable=invalid-name
                      static_folder='../static')


@blueprint.route('/')
def home():
    return render_template('public/home.html')


@blueprint.route('/paste', methods=['GET', 'POST'])
def paste():
    """Show the home page."""
    if request.method == 'POST':
        form_data = request.form
    else:
        form_data = request.args
    source = form_data.get('source')
    if not source:
        return render_template('public/paste.html')

    source_data = BytesIO(source.encode())
    response = validate(source_data)
    flash_msg_type = 'success' if response['success'] else 'danger'
    flash(response['flash_msg'], flash_msg_type)
    return render_template('public/paste.html',
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

    if not response['transformed']:
        flash(response['flash_msg'], 'danger')
        return redirect(url_for('public.home'))

    source_url = url_for('public.force_transform', url=url, _external=True)
    validate_url = 'http://iati.cove.opendataservices.coop/?' + \
        urlencode({'source_url': source_url})

    msg = '{} <a href="{}" target="_blank">Validate transformed data with CoVE</a>.'.format(
        response['flash_msg'],
        validate_url,
    )
    flash(msg, 'danger')

    return render_template('public/paste.html',
                           source=source,
                           validate_url=validate_url,
                           result=response['result'])


@blueprint.route('/transform.xml')
def force_transform():
    url = request.args.get('url')
    r = requests.get(url)
    source_data = BytesIO(r.content)
    response = validate(source_data)
    return Response(response['result'], mimetype='text/xml')
