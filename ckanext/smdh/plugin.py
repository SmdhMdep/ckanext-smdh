import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.smdh.helpers as helpers

class SmdhPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config_, u'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config_, u'public')

        # toolkit.add_resource('fanstatic', 'smdh')

        # Register this plugin's assets directory with CKAN.
        # Here, 'assets' is the path to the webassets directory
        # (relative to this plugin.py file), and 'smdh' is the name
        # that we'll use to refer to this assets directory from CKAN
        # templates.
        toolkit.add_resource(u'assets', u'smdh')

    # ITemplateHelpers
    def get_helpers(self):
        return {'isAdmin': helpers.isAdmin,
        'getTracking': helpers.getTracking
        }

    # IPackageController
    def before_search(self, data_dict):
        if not data_dict.get('sort'):
            if toolkit.asbool(toolkit.config.get("ckan.tracking_enabled")):
                data_dict['sort'] = 'views_recent desc'
            else:
                data_dict['sort'] = 'score desc, date_last_modified desc'
        return data_dict