from __future__ import absolute_import

from ckan.plugins import toolkit

c = toolkit.c

def isAdmin():
    return c.userobj.sysadmin