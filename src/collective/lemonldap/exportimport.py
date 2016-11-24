#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.lemonldap.interfaces import ILemonLDAPManager
from collective.lemonldap.pas import manage_addLemonLDAPManager
from Products.GenericSetup.interfaces import IFilesystemExporter
from Products.GenericSetup.interfaces import IFilesystemImporter
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import PropertyManagerHelpers
from Products.GenericSetup.utils import XMLAdapterBase
from zope.component import adapts
from zope.interface import implements

import os
import plone.api.portal


class LemonLDAPUserPropertiesExportImport(object):
    implements(IFilesystemExporter, IFilesystemImporter)

    def __init__(self, context):
        self.context = context

    def export(self, export_context, subdir, root=False):
        exportObjects(self.context, subdir + os.sep, export_context)

    def import_(self, import_context, subdir, root=False):
        importObjects(self.context, subdir + os.sep, import_context)

    def listExportableItems(self):
        return ()


class LemonLDAPPropertiesXMLAdapter(XMLAdapterBase, PropertyManagerHelpers):
    adapts(ILemonLDAPManager, ISetupEnviron)
    name = 'lemonproperties'
    _LOGGER_ID = 'lemonproperties'
    _encoding = 'utf-8'

    def _exportNode(self):
        node = self._doc.createElement('lemonproperties')
        node.appendChild(self._extractProperties())
        self._logger.info('Site properties exported.')
        return node

    def _importNode(self, node):
        purge = self.environ.shouldPurge()
        if node.getAttribute('purge'):
            purge = self._convertToBoolean(node.getAttribute('purge'))
        if purge:
            self._purgeProperties()
        self._initProperties(node)


def importLemonLDAPPropertiesSettings(context):
    container = plone.api.portal.get()
    uf = getattr(aq_base(container), 'acl_users', None)

    if uf is not None:
        lemonLdapId = 'lemonldap'
        if lemonLdapId not in uf.objectIds():
            manage_addLemonLDAPManager(uf, lemonLdapId)
        shibproperties = getattr(uf, lemonLdapId)
        importObjects(shibproperties, '', context)
