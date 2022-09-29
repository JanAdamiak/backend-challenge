import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import run


def test_skeleton_code_returns_true():
	"""
	Example test 

	Please replace with your tests
	"""

	assert run() is True
