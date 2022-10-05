import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import ProductReporter, BrandReporter
from main import run


class TestBrandReporter:
	def test_basic_usage(self):
		assert BrandReporter().calculate_data() == {}


class TestProductReporter:
	def test_basic_usage(self):
		assert ProductReporter().calculate_data() == {}


def test_some():
	run()