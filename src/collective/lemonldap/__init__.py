# -*- coding: utf-8 -*-
from AccessControl.Permissions import add_user_folders
from collective.lemonldap import pas
from Products.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.lemonldap')

registerMultiPlugin(pas.LemonLDAPManager)


def initialize(context):
    context.registerClass(pas.LemonLDAPManager,
                          permission=add_user_folders,
                          constructors=(
                              pas.manage_addLemonLDAPManagerForm,
                              pas.manage_addLemonLDAPManager),
                          visibility=None,
                          icon='')
