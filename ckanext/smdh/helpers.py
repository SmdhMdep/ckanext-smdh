from __future__ import absolute_import

from ckan.plugins import toolkit
from ckan.lib.helpers import can_update_owner_org as default_can_update_owner_org

c = toolkit.c

def isAdmin():
    if c.userobj:
        return c.userobj.sysadmin
    else:
        return False

def getTracking(packageid):
    data = {'id': packageid, "include_tracking": True}

    packageInfo = toolkit.get_action('package_show')({'ignore_auth': True}, data)

    if packageInfo["tracking_summary"]["recent"]:
        return packageInfo["tracking_summary"]["recent"]
    else:
        return False

def can_update_owner_org(data, orgs):
    # This function overrides the default can_update_owner_org provided by ckan
    # to disallow update of owner org for existing packages.
    if 'id' in data:
        return False
    return default_can_update_owner_org(data, orgs)

PACKAGE_NAMESPACE_SEPARATOR = '--'

def convert_global_package_name_to_local(name):
    """
    Convert a package name from a globally unique name to a name that's only unique within the organization.

    The returned name can only be used to create packages but not to read, update or delete them.
    """
    return name.rsplit(PACKAGE_NAMESPACE_SEPARATOR, maxsplit=1)[-1]

def convert_local_package_name_to_global(organization_name, name):
    """
    Convert a package name from one that's only unique within the organization list of datasets to a globally unique name.

    The returned name can be used to perform all CRUD operations on a dataset.
    Local names cannot contain the sequence of characters '--' as they are used to add a namespace for the local package name.
    """
    if PACKAGE_NAMESPACE_SEPARATOR in name:
        raise ValueError("local package name must not contain '--'")
    return f'{organization_name}{PACKAGE_NAMESPACE_SEPARATOR}{name}'

def ensure_global_package_name(organization_name, name):
    """
    Converts a package name to a globally unique one.

    If this is a global name already the returned value is the same as `name` otherwise
    the name is converted to a global one.
    """
    namespace_prefix = f'{organization_name}{PACKAGE_NAMESPACE_SEPARATOR}'
    if name.startswith(namespace_prefix):
        name = name[len(namespace_prefix):]
    return convert_local_package_name_to_global(organization_name, name)
