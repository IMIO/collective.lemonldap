# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveLemonldapLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ILemonLDAPManager(Interface):
    """
    Shibboleth user role manager marker interface
    """


class IUserPropertyFilter(Interface):
    """
    Filter user properties content
    """
