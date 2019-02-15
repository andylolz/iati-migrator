"""Public section, including homepage and signup."""
from os.path import abspath, dirname, join
from io import BytesIO
import re

from flask import Blueprint, render_template, request, flash
import iatikit
from lxml import etree


basedir = abspath(dirname(__file__))  # pylint: disable=invalid-name
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

    error_msg = None
    result = ''
    source_data = BytesIO(source.encode())
    dataset = iatikit.Dataset(source_data)
    if not dataset.validate_xml():
        error_msg = 'Input data is not valid XML.'
    elif not dataset.version.startswith('1'):
        error_msg = 'Input data is not IATI v1.0x.'
    elif not dataset.validate_iati():
        error_msg = 'Input data is not valid to the IATI schema.'
    elif not dataset.validate_codelists():
        error_msg = 'Input data uses invalid codelist values.'

    if error_msg:
        flash(error_msg, 'danger')
        return render_template('public/home.html',
                               source=source)

    xsd_path = join(basedir, '..', 'static', 'iati-activities.xsl')
    transform = etree.XSLT(etree.parse(xsd_path))
    transformed = transform(dataset.etree)
    result = str(transformed)
    result_data = BytesIO(bytes(transformed))
    dataset = iatikit.Dataset(result_data)
    if not dataset.validate_xml():
        error_msg = 'There was a problem! Result data not valid XML.'
    elif not dataset.validate_iati():
        error_msg = 'The data was migrated, but has schema validation issues'
        match_re = r'the order of elements is important\. .*? but ' + \
                   r'(.*?) is expected\.$'
        match = re.search(match_re, dataset.validate_iati().errors[0].details)
        if match:
            error_msg += ' (e.g. an activity is missing {}.)'.format(
                match.group(1))
        else:
            error_msg += '.'
    elif not dataset.validate_codelists():
        error_msg = 'The data was migrated, but has codelist issues.'

    if error_msg:
        flash(error_msg, 'danger')
        return render_template('public/home.html',
                               source=source, result=result)

    flash('Data successfully migrated!', 'success')
    return render_template('public/home.html',
                           source=source,
                           result=result)
