#!/usr/bin/env python
import matplotlib.pyplot as plt
from typing import Any
import numpy as np
import json
import sys
import os

module_path = os.path.dirname(os.path.dirname(os.path.abspath(".")))

# to make it work out of the box in interactive shells
if module_path not in sys.path:
  sys.path.insert(0, module_path)