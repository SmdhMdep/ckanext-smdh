import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.smdh import helpers
from ckanext.smdh import validators


logger = logging.getLogger(__name__)


class SmdhGroupFormPlugin(plugins.SingletonPlugin, toolkit.DefaultGroupForm):
    plugins.implements(plugins.IGroupForm)

    # IGroupForm

    def update_group_schema(self):
        schema = super().update_group_schema()
        schema['name'].append(validators.no_update_to_model_name('group'))
        return schema

    def is_fallback(self):
        return True

    def group_types(self):
        return []
