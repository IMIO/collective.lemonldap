====================
collective.lemonldap
====================
.. image:: https://travis-ci.org/IMIO/collective.lemonldap.svg?branch=master
    :target: https://travis-ci.org/IMIO/collective.lemonldap

Add PluggableAuthService plugin to authenticate in Plone using LemonLDAP::NG (https://lemonldap-ng.org)

Installation
------------

Install collective.lemonldap by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.lemonldap
    zcml =
        collective.lemonldap


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/IMIO/collective.lemonldap/issues
- Source Code: https://github.com/IMIO/collective.lemonldap

License
-------

The project is licensed under the GPLv2.
