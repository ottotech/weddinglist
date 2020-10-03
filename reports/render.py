
# Python imports
from io import BytesIO
import os

# Django imports
from django.template.loader import get_template

# Project imports
from weddinglist.settings import STATIC_URL, STATICFILES_DIRS

# Third party imports
import xhtml2pdf.pisa as pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    sUrl = STATIC_URL
    sRoot = STATICFILES_DIRS

    # convert URIs to absolute system paths
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % sUrl)

    return path


def render_to_pdf(template_src, context_dict, request=None):
    template = get_template(template_src)
    html = template.render(context_dict, request=request)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None
