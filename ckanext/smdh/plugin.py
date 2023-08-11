import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.smdh.helpers as helpers


logger = logging.getLogger(__name__)


class SmdhPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IGroupForm)
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

    # IValidators
    def get_validators(self):
        return {
            no_update_to_model_name.__name__: no_update_to_model_name,
            no_update_to_resource_name.__name__: no_update_to_resource_name,
        }

    # IDatasetForm & IGroupForm
    def _update_schema(self, schema, model):
        validator = toolkit.get_validator(no_update_to_model_name.__name__)(model)
        schema['name'].append(validator)
        return schema

    def update_package_schema(self):
        schema = self._update_schema(super().update_package_schema(), 'package')
        validator = toolkit.get_validator(no_update_to_resource_name.__name__)
        schema['resources']['name'].append(validator)
        return schema

    def update_group_schema(self):
        return self._update_schema(super().update_package_schema(), 'group')

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def group_types(self):
        return []


def no_update_to_model_name(model_key: str):
    def validator(value, context):
        model = context.get(model_key)
        if model and model.name != value:
            raise toolkit.Invalid(
                f'Cannot change value of key from {model.name} to {value}. This key is read-only'
            )
        return value
    return validator

def no_update_to_resource_name(key, data, errors, context):
    resource_id = data.get(key[:-1] + ('id',))
    if not resource_id:
        return

    session = context['session']
    model = context['model']
    before_name = session.query(model.Resource.name).filter_by(id=resource_id).first()
    if before_name and before_name[0] != data[key]:
        errors[key].append(
            f'Cannot change value of key from {before_name[0]} to {data[key]}. This key is read-only'
        )
