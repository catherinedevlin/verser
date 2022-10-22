import pdb
import sys
import traceback

from . import all_sources
from .models import *


def ingest():
    try:
        for source in all_sources:
            source.ingest()
    except:
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
