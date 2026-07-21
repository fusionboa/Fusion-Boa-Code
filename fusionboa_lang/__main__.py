"""
FusionBoa Language - __main__.py

Allows running FusionBoa via: python -m fusionboa_lang
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fusionboa import main
main()
