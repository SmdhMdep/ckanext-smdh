import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.smdh.middleware as smdh_middleware

class SmdhPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    #plugins.implements(plugins.IMiddleware)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'smdh')

    # IMiddleware

    #def make_middleware(self, app, config):
    #    return smdh_middleware.AuthMiddleware(app, config)

    #def make_error_log_middleware(self, app, config):
    #    return smdh_middleware.AuthMiddleware(app, config)
