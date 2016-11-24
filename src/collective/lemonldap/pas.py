# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from collective.lemonldap.config import USERNAME_HEADER
from collective.lemonldap.interfaces import ILemonLDAPManager
from collective.lemonldap.interfaces import IUserPropertyFilter
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from zope.component import queryAdapter

import logging
import zope.interface


logger = logging.getLogger('collective.lemonldap')
manage_addLemonLDAPManagerForm = PageTemplateFile('www/LemonLDAPManagerForm',
                                                  globals())


def manage_addLemonLDAPManager(self, id='shibrole', title='', REQUEST=None):
    """Add a  to a Pluggable Auth Service.
    """
    rm = LemonLDAPManager(id, title)
    self._setObject(rm.getId(), rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('{0}/manage_workspace'
                                     '?manage_tabs_message='
                                     'LemonLDAPManager+added.'
                                     .format(self.absolute_url()))


@zope.interface.implementer(ILemonLDAPManager)
@zope.interface.implementer(IRolesPlugin)
@zope.interface.implementer(IPropertiesPlugin)
class LemonLDAPManager(BasePlugin):
    """
    A PAS plugin for LemonLDAP
    """

    security = ClassSecurityInfo()
    meta_type = 'LemonLDAPManager'
    manage_options = BasePlugin.manage_options

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    # IRolesPlugin
    #
    @security.private
    def getRolesForPrincipal(self, user, request=None):
        """ Fullfill RolesPlugin requirements """
        if request is None:
            if hasattr(self, 'REQUEST'):  # noqa
                request = self.REQUEST
            else:
                return ()
        if user.getId() == request.environ.get(USERNAME_HEADER):
            return ('Member', 'Authenticated')
        else:
            return ()

    def _getShibProperties(self, userId):
        userProperties = {}
        for propertyDict in self._propertyMap():
            propertyName = propertyDict.get('id')
            propertyValue = self.getProperty(propertyName)
            requestValue = self.REQUEST.environ.get(propertyName)
            requestValue = queryAdapter(requestValue, IUserPropertyFilter,
                                        name=propertyName,
                                        default=requestValue)

            if requestValue:
                userProperties[propertyValue] = requestValue
            else:
                logger.warning('Property {0} has no value for user {1}'.format(
                    propertyName, userId))
        return userProperties

    #
    # IPropertiesPlugin implementation
    #

    def getPropertiesForUser(self, user, request=None):
        """

        o User will implement IPropertiedUser.

        o Plugin should return a dictionary or an object providing
          IPropertySheet.

        o Plugin may scribble on the user, if needed (but must still
          return a mapping, even if empty).

        o May assign properties based on values in the REQUEST object, if
          present
        """
        if request is None:
            if hasattr(self, 'REQUEST'):  # noqa
                request = self.REQUEST
            else:
                return {}
        userId = user.getId()
        if userId == request.environ.get(USERNAME_HEADER):
            return UserPropertySheet(user.id,
                                     **self._getShibProperties(userId))
        else:
            return {}


InitializeClass(LemonLDAPManager)
