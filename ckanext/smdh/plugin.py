import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.smdh.middleware as smdh_middleware
import ckanext.smdh.helpers as helpers

class SmdhPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    #plugins.implements(plugins.IMiddleware)

    # IConfigurer

    def update_config(self, config_):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config_, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config_, 'public')

        # toolkit.add_resource('fanstatic', 'smdh')

        # Register this plugin's assets directory with CKAN.
        # Here, 'assets' is the path to the webassets directory
        # (relative to this plugin.py file), and 'smdh' is the name
        # that we'll use to refer to this assets directory from CKAN
        # templates.
        toolkit.add_resource('assets', 'smdh')

    # IMiddleware

    #def make_middleware(self, app, config):
    #    return smdh_middleware.AuthMiddleware(app, config)

    #def make_error_log_middleware(self, app, config):
    #    return smdh_middleware.AuthMiddleware(app, config)

    # ITemplateHelpers
    def get_helpers(self):
        return {'isAdmin': helpers.isAdmin}
