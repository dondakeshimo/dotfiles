#coding:utf-8
#!/usr/bin/python3
'''
created 2018/02/16 by shimomura
'''

import time
START=time.time()

import os
import sys
import argparse
import codecs
from collections import defaultdict
import json
from pprint import pprint
import re
import traceback
import itertools
import line_profiler
from tqdm import tqdm

from mymodule import cnvk

#自ファイルが存在するディレクトリ, スクリプト名
CURRENT_DIRECTORY=os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAME=re.sub('.py.?','',os.path.basename(__file__))

# line_profiler 用
if 'prof' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
            return inner
