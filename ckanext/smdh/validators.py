from ckan.plugins import toolkit


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
