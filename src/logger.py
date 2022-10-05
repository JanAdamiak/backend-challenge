"""
Custom logging rules.
"""
import logging


# This is just a simple logger implementation, for production setting this could have a conditional for the level argument.
logging.basicConfig(level=logging.INFO, format='%(pathname)s %(asctime)s %(levelname)s %(message)s')
