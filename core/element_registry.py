"""Safe lookup for dynamically-loaded elements (generators / effects).

import core/<package>/<name>.py and return the class named
<name> — the filename==classname convention every element follows. A strict
whitelist guarantees a hostile name can never reach importlib as anything but a
plain module lookup.
"""
import re
import importlib

_NAME_RE = re.compile(r'[a-z][a-z0-9_]*\Z')
_PACKAGES = {'generator': 'generators', 'effect': 'effects'}
_cache = {}


def get_element_class(element_type, name):
    """Return the class for an element by type ('generator'/'effect') and name."""
    key = (element_type, name)
    cls = _cache.get(key)
    if cls is None:
        package = _PACKAGES.get(element_type)
        if package is None:
            raise ValueError(f'unknown element type: {element_type!r}')
        if not _NAME_RE.fullmatch(name or ''):
            raise ValueError(f'invalid element name: {name!r}')
        module = importlib.import_module(f'{package}.{name}')
        cls = _cache[key] = getattr(module, name)
    return cls


def new_element(element_type, name):
    """Instantiate an element by type and name."""
    return get_element_class(element_type, name)()
