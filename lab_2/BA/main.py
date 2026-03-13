#!/usr/bin/env python
"""Точка входа в программу"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from BooleanAnalyzer.Main import main

if __name__ == "__main__":
    main()