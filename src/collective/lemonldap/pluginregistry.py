#!/usr/bin/env python
# -*- coding: utf-8 -*-


def movePluginsTop(self, plugin_type, ids_to_move):
    """ Move a plugin on the top
    """
    ids = list(self._getPlugins(plugin_type))
    indexes = list(map(ids.index, ids_to_move))
    indexes.sort()
    for i1 in indexes:
        ids.insert(0, ids.pop(i1))
    self._plugins[plugin_type] = tuple(ids)
