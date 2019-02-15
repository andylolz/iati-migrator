"""Public section, including homepage and signup."""
from os.path import abspath, dirname, join
from io import BytesIO

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

    source_data = BytesIO(source.encode())
    dataset = iatikit.Dataset(source_data)
    if not dataset.validate_xml():
        flash('Data is not valid XML', 'danger')
        return render_template('public/home.html',
                               source=source)
    if not dataset.version.startswith('1'):
        flash('Data is not IATI v1.0x', 'danger')
        return render_template('public/home.html',
                               source=source)
    if not dataset.validate_iati():
        flash('Data is not valid IATI', 'danger')
        return render_template('public/home.html',
                               source=source)
    if not dataset.validate_codelists():
        flash('Data uses invalid codelist values', 'danger')
        return render_template('public/home.html',
                               source=source)
    xsd_path = join(basedir, '..', 'static', 'iati-activities.xsl')
    transform = etree.XSLT(etree.parse(xsd_path))
    transformed = transform(dataset.etree)
    result = str(transformed)
    result_data = BytesIO(bytes(transformed))
    dataset = iatikit.Dataset(result_data)
    if not dataset.validate_xml():
        flash('There was a problem! Result not valid XML', 'danger')
        return render_template('public/home.html',
                               source=source, result=result)
    print(dataset.validate_iati().errors[0].details)
    if not dataset.validate_iati():
        flash('The data was migrated, but has schema validation issues', 'danger')
        return render_template('public/home.html',
                               source=source, result=result)
    if not dataset.validate_codelists():
        flash('The data was migrated, but has codelist issues', 'danger')
        return render_template('public/home.html',
                               source=source, result=result)

    flash('Successfully migrated!', 'success')
    return render_template('public/home.html',
                           source=source,
                           result=result)
