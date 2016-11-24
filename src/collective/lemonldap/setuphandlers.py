# -*- coding: utf-8 -*-
from collective.lemonldap import config
from collective.lemonldap.pas import manage_addLemonLDAPManager
from plone.api import portal
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import re


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.lemonldap:uninstall',
        ]


def configureWebserverAuth(context):
    pas = portal.get_tool('acl_users')
    wsAuthPlugin = pas['web_server_auth']
    wsAuthPlugin._config = {
        'strip_domain_names': False,
        'username_header': config.USERNAME_HEADER,
        'authenticate_everybody': True,
        'challenge_pattern': re.compile(r'(http|https)://([^/]*)/(.*)'),
        'challenge_replacement': r'https://\2',
        'use_custom_redirection': True
    }

    interfaces = ['IAuthenticationPlugin', 'IChallengePlugin',
                  'IExtractionPlugin']
    wsAuthPlugin.manage_activateInterfaces(interfaces)
    activatePluginAndMoveTop(pas, 'web_server_auth', interfaces)


def activatePluginAndMoveTop(pas, pluginId, interfaceNames):
    plugin = getattr(pas, pluginId)
    plugin.manage_activateInterfaces(interfaceNames)
    for interfaceName in interfaceNames:
        interface_object = pas.plugins._getInterfaceFromName(interfaceName)
        pas.plugins.movePluginsTop(interface_object, [pluginId])


def setupLemonLDAPAuthentication(context):
    """
    Create and configure a lemonldap-plugin.
    """
    pas = portal.get_tool('acl_users')

    lemonLdapId = 'lemonldap'
    if lemonLdapId not in pas.objectIds():
        manage_addLemonLDAPManager(pas, lemonLdapId)
    activatePluginAndMoveTop(pas, lemonLdapId,
                             ['IRolesPlugin', 'IPropertiesPlugin'])


def post_install(context):
    """Post install script"""
    configureWebserverAuth(context)
    setupLemonLDAPAuthentication(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
