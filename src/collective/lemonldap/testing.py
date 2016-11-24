# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.lemonldap


class CollectiveLemonldapLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.lemonldap)
        z2.installProduct(app, 'Products.WebServerAuth')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.lemonldap:default')


COLLECTIVE_LEMONLDAP_FIXTURE = CollectiveLemonldapLayer()


COLLECTIVE_LEMONLDAP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_LEMONLDAP_FIXTURE,),
    name='CollectiveLemonldapLayer:IntegrationTesting'
)


COLLECTIVE_LEMONLDAP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_LEMONLDAP_FIXTURE,),
    name='CollectiveLemonldapLayer:FunctionalTesting'
)


COLLECTIVE_LEMONLDAP_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_LEMONLDAP_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveLemonldapLayer:AcceptanceTesting'
)
