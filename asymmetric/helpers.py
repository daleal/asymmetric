"""
A module for every helper of asymmetric.
"""


def http_verb(dirty: str) -> str:
    """
    Given a 'dirty' HTTP verb (uppercased, with trailing whitespaces), strips
    it and returns it lowercased.
    """
    return dirty.strip().lower()


def humanize(module_name: str) -> str:
    """Transforms a module name into a pretty human-likable string."""
    module_name = module_name.lower()
    module_name = module_name.replace("_", " ").replace("-", " ")
    module_name = module_name.title()
    return module_name
