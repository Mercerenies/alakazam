
from __future__ import print_function
import sys
import traceback

def trace(arg, res, **kwargs):
    print(arg, **kwargs)
    return res

def traceid(res, **kwargs):
    return trace(res, res, **kwargs)

def tracestack(res, **kwargs):
    traceback.print_stack(**kwargs)
    return res
