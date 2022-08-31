# pre-load

import os
from docassemble.ALWeaver.custom_values import advertise_capabilities

if not os.environ.get('ISUNITTEST'):
  advertise_capabilities(__name__, minimum_version="1.5")