from __future__ import absolute_import

from ckan.plugins import toolkit

c = toolkit.c

def isAdmin():
    return c.userobj.sysadmin

def getTracking(packageid):
    data = {'id': packageid, "include_tracking": True}

    packageInfo = toolkit.get_action('package_show')({'ignore_auth': True}, data)

    if packageInfo["tracking_summary"]["recent"]:
        return packageInfo["tracking_summary"]["recent"]
    else:
        return False