from io import BytesIO

from os.path import abspath, dirname, join
import re

import iatikit
from lxml import etree


basedir = abspath(dirname(__file__))  # pylint: disable=invalid-name


def validate(source):
    flash_msg = None
    result = ''
    dataset = iatikit.Dataset(source)
    if not dataset.validate_xml():
        flash_msg = 'Input data is not valid XML.'
    elif not dataset.version.startswith('1'):
        flash_msg = 'Input data is not IATI v1.0x.'
    elif not dataset.validate_iati():
        flash_msg = 'Input data is not valid to the IATI schema.'
    elif not dataset.validate_codelists():
        flash_msg = 'Input data uses invalid codelist values.'

    if flash_msg:
        return {
            'success': False,
            'flash_msg': flash_msg,
            'result': result,
        }

    if dataset.filetype == 'activity':
        xsd_path = join(basedir, '..', 'static', 'iati-activities.xsl')
    else:
        xsd_path = join(basedir, '..', 'static', 'iati-organisations.xsl')
    transform = etree.XSLT(etree.parse(xsd_path))
    transformed = transform(dataset.etree)
    result = str(transformed)
    result_data = BytesIO(bytes(transformed))
    dataset = iatikit.Dataset(result_data)
    if not dataset.validate_xml():
        flash_msg = 'There was a problem! Result data not valid XML.'
    elif not dataset.validate_iati():
        print(dataset.validate_iati().errors[0].details)
        flash_msg = 'The data was transformed, but has schema validation issues'
        match_re = r'the order of elements is important\. .*? but ' + \
                   r'(.*?) is expected\.$'
        match = re.search(match_re, dataset.validate_iati().errors[0].details)
        if match:
            flash_msg += ' (e.g. an activity is missing {}.)'.format(
                match.group(1))
        else:
            flash_msg += '.'
    elif not dataset.validate_codelists():
        print(dataset.validate_codelists().errors[0].details)
        flash_msg = 'The data was transformed, but has codelist issues.'

    if flash_msg:
        return {
            'success': False,
            'flash_msg': flash_msg,
            'result': result,
        }

    return {
        'success': True,
        'flash_msg': 'Data successfully transformed!',
        'result': result,
    }
