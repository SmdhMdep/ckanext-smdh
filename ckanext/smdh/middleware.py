# Uses a lot of code from ckanext-noanonaccess

import logging
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import config
import ckan.lib.base as base
logger = logging.getLogger(__name__)

# Middleware checks if users is logged in
# If user is not logged it it will limit what pages they can access
# Uses a lot of code from ckanext-noanonaccess
class AuthMiddleware(object):
    def __init__(self, app, app_conf):
        self.app = app

    def __call__(self, environ, start_response):

        pathInfo = environ['PATH_INFO']

        # if logged in via browser cookies or API key, all pages accessible    
        if 'repoze.who.identity' in environ or self._get_user_for_apikey(environ):
            return self.app(environ,start_response)

        # Allows downloads/uploads
        elif '/uploads/' in pathInfo or '/download/' in pathInfo:
            return self.app(environ,start_response)

        # Allow Resource Description Framework files
        elif (pathInfo).endswith('.rdf'):
            return self.app(environ,start_response)

        elif '/api/' in pathInfo or '/datastore/dump/' in pathInfo:
            return self.app(environ,start_response)

        # Allows css, js and other web assets
        elif (pathInfo.startswith('/webassets/') or pathInfo.startswith('/base/')
                                or pathInfo == "/example_theme.css"
                                or pathInfo == "/8KCrLBZ/made-smarter-logo-2.png"):
            return self.app(environ,start_response)

        # Allow paths used for login attempts
        elif (# Normal CKAN login paths
            pathInfo == '/user/login' or pathInfo == '/user/_logout'
            or '/user/reset' in pathInfo or pathInfo == '/user/logged_out'
            or pathInfo == '/user/logged_in' or pathInfo == '/user/logged_out_redirect'
            or pathInfo == '/user/register' 
            # SSO login paths
            or pathInfo == '/user/saml2login'
            or pathInfo == '/slo' 
            or pathInfo == '/acs'):
            return self.app(environ,start_response)
        
        # For all other paths send to login page
        else:
            # Create redirect 
            url = self.createURL(environ)
            headers = self.createHeaders(url)
            status = '307 Temporary Redirect'
            
            try:
                start_response(status, headers)
            except:
                logger.debug("SMDH IMiddleware failed to create redirect: " + headers)
            return ['']

    # Creates url for redirect
    def createURL(self, environ):
        # Create start of URL 
        url = environ.get('HTTP_X_FORWARDED_PROTO') \
            or environ.get('wsgi.url_scheme', 'http')
        url += '://'

        # Change URL based on how the CKAN is hosted
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']

        # Send to CKAN login or SSO login based on SAML2 config
        if toolkit.asbool(toolkit.config.get('ckanext.saml2auth.enable_ckan_internal_login')):
            url += '/user/login'
        else:
            url += '/user/saml2login'

        return url

    # Creates header for redirect
    def createHeaders(self, url):
        headers = [
                ('Location', url),
                ('Content-Length','0'),
                ('X-Robots-Tag', 'noindex, nofollow, noarchive')
                ]
        return headers


    def _get_user_for_apikey(self, environ):
        # Adapted from https://github.com/ckan/ckan/blob/625b51cdb0f1697add59c7e3faf723a48c8e04fd/ckan/lib/base.py#L396
        apikey_header_name = config.get(base.APIKEY_HEADER_NAME_KEY,
                                        base.APIKEY_HEADER_NAME_DEFAULT)
        apikey = environ.get(apikey_header_name, '')
        if not apikey:
            # For misunderstanding old documentation (now fixed).
            apikey = environ.get('HTTP_AUTHORIZATION', '')
        if not apikey:
            apikey = environ.get('Authorization', '')
            # Forget HTTP Auth credentials (they have spaces).
            if ' ' in apikey:
                apikey = ''
        if not apikey:
            return None
        # check if API key is valid by comparing against keys of registered users
        query = model.Session.query(model.User)
        user = query.filter_by(apikey=apikey).first()
        return user