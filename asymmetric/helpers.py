"""
A module for every helper of asymmetric.
"""


def http_verb(dirty):
    """
    Given a 'dirty' HTTP verb (uppercased, with trailing whitespaces), strips
    it and returns it lowercased.
    """
    return dirty.strip().lower()
