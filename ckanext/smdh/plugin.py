import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.smdh import helpers
from ckanext.smdh import validators


logger = logging.getLogger(__name__)


class SmdhPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IValidators)

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
        return {
            'isAdmin': helpers.isAdmin,
            'getTracking': helpers.getTracking,
            'can_update_owner_org': helpers.can_update_owner_org,
            'convert_local_package_name_to_global': helpers.convert_local_package_name_to_global,
            'convert_global_package_name_to_local': helpers.convert_global_package_name_to_local,
            'ensure_global_package_name': helpers.ensure_global_package_name,
            'isPrivateDatasetEnabled': helpers.isPrivateDatasetEnabled,
        }

    # IPackageController
    def before_search(self, data_dict):
        if not data_dict.get('sort'):
            if toolkit.asbool(toolkit.config.get("ckan.tracking_enabled")):
                data_dict['sort'] = 'views_recent desc'
            else:
                data_dict['sort'] = 'score desc, date_last_modified desc'
        return data_dict

    # IValidators
    def get_validators(self):
        return {
            validators.no_update_to_model_name.__name__: validators.no_update_to_model_name,
            validators.no_update_to_resource_name.__name__: validators.no_update_to_resource_name,
            validators.no_update_to_package_owner_org.__name__: validators.no_update_to_package_owner_org,
            validators.convert_global_package_name_to_local.__name__: validators.convert_global_package_name_to_local,
            validators.ensure_global_package_name.__name__: validators.ensure_global_package_name,
        }
