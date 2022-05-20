from urllib.parse import urljoin
from django.utils.encoding import iri_to_uri
from django.conf import settings

def build_absolute_uri(location):
    host = settings.SITE_HOST
    protocol = 'https' if settings.ENABLE_SSL else 'http'
    current_uri = '%s://%s' % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)

def make_email_body_with_template(main_text):
    template_body = "LandLim \n" + main_text + '\nIf you have any questions, please send them to the contact form instead of replying to this email. \nお問い合わせはこのメールの返信ではなくお問い合わせフォームにお送り下さい。'
    return template_body