# -*- coding: utf-8 -*-
def strip_rank(text):
    """
    >>> strip_rank('Value (rank)')
    >>> 'Value'
    """
    return text.split('(')[0].strip()
