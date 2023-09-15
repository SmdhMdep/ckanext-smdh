import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.smdh import validators


logger = logging.getLogger(__name__)


class SmdhDatasetFormPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)

    # IDatasetForm

    def update_package_schema(self):
        schema = super().update_package_schema()
        schema['name'].append(validators.no_update_to_model_name('package'))
        schema['resources']['name'].append(validators.no_update_to_resource_name)
        schema['owner_org'].append(validators.no_update_to_package_owner_org)
        return schema

    def create_package_schema(self):
        schema = super().create_package_schema()
        schema['name'].insert(0, validators.ensure_global_package_name)
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []
