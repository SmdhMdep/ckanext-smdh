from ckan.plugins import toolkit

from . import helpers as h


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

def no_update_to_package_owner_org(value, context):
    model = context.get('package')
    if model and model.owner_org != value:
        raise toolkit.Invalid(
            f'Cannot change the owner organization for dataset'
        )
    return value

def convert_global_package_name_to_local(value, context):
    return h.convert_global_package_name_to_local(value)

def ensure_global_package_name(key, data, errors, context):
    model = context['model']
    session = context['session']

    if data[key] is toolkit.missing or not data[key]:
        return

    # NOTE assumes that create_unowned_dataset is False
    group = model.Group.get(data[('owner_org',)])
    if not group:
        # will be invalidated by the owner_org validation, no errors need to be reported here
        return

    try:
        data[key] = h.ensure_global_package_name(group.name, data[key])
    except ValueError:
        errors[key].append("URL must not contain '--'")
