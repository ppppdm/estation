# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# parentPath.py for the test file in this floder to include parent module
'''

import os
import sys

def impt():
    parent_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(parent_path)
