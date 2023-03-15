import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.smdh.helpers as helpers

class SmdhPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

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

    # ITemplateHelpers
    def get_helpers(self):
        return {'isAdmin': helpers.isAdmin,
        'getTracking': helpers.getTracking
        }
