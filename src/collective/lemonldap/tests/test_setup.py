# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.lemonldap.testing import COLLECTIVE_LEMONLDAP_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.lemonldap is properly installed."""

    layer = COLLECTIVE_LEMONLDAP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.lemonldap is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.lemonldap'))

    def test_browserlayer(self):
        """Test that ICollectiveLemonldapLayer is registered."""
        from collective.lemonldap.interfaces import (
            ICollectiveLemonldapLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveLemonldapLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_LEMONLDAP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.lemonldap'])

    def test_product_uninstalled(self):
        """Test if collective.lemonldap is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.lemonldap'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveLemonldapLayer is removed."""
        from collective.lemonldap.interfaces import \
            ICollectiveLemonldapLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveLemonldapLayer, utils.registered_layers())
