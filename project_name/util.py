# -*- coding: utf-8 -*-

'''
utility functions (used by calculator classes)

Created on  2021-10-01

@author: Meghan Correa <mportermahoney@g.harvard.edu>
@copyright: 2021 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from decimal import Decimal, ROUND_HALF_UP

def dollars(pennies):
    '''
    convert pennies to dollars if digit
    '''
    if not str(abs(int(pennies))).isdigit():
        return pennies
    cent = Decimal('0.01')
    dollars = Decimal(int(pennies)/100).quantize(cent, ROUND_HALF_UP)
    return f'${dollars}'
