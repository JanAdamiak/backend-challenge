import pytest

from src.utils import ProductReporter, BrandReporter


@pytest.fixture()
def brand_data():
    return [
        {
            'period_id': '1',
            'period_name': 'previous',
            'week_commencing_date': '25/07/2021',
            'brand_id': '1',
            'brand': 'Brand A',
            'gross_sales': '314.31',
            'units_sold': '38'
        }, 
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '25/07/2022',
            'brand_id': '1',
            'brand': 'Brand A',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '18/07/2022',
            'brand_id': '2',
            'brand': 'Brand B',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '1',
            'period_name': 'current',
            'week_commencing_date': '11/07/2022',
            'brand_id': '3',
            'brand': 'Brand C',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '1',
            'period_name': 'previous',
            'week_commencing_date': '04/07/2021',
            'brand_id': '4',
            'brand': 'Brand D',
            'gross_sales': '0',
            'units_sold': '0'
        }, 
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '04/07/2022',
            'brand_id': '4',
            'brand': 'Brand D',
            'gross_sales': '0',
            'units_sold': '0'
        },
    ]


@pytest.fixture()
def product_data():
    return [
        {
            'period_id': '1',
            'period_name': 'previous',
            'week_commencing_date': '25/07/2021',
            'barcode_no': '60988638',
            'product_name': 'Product A',
            'gross_sales': '314.31',
            'units_sold': '38'
        }, 
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '25/07/2022',
            'barcode_no': '60988638',
            'product_name': 'Product A',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '18/07/2022',
            'barcode_no': '59842899',
            'product_name': 'Product B',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '1',
            'period_name': 'current',
            'week_commencing_date': '11/07/2022',
            'barcode_no': '87149829',
            'product_name': 'Product C',
            'gross_sales': '303.78',
            'units_sold': '26'
        },
        {
            'period_id': '1',
            'period_name': 'previous',
            'week_commencing_date': '04/07/2021',
            'barcode_no': '90432853',
            'product_name': 'Product D',
            'gross_sales': '0',
            'units_sold': '0'
        }, 
        {
            'period_id': '2',
            'period_name': 'current',
            'week_commencing_date': '04/07/2022',
            'barcode_no': '90432853',
            'product_name': 'Product D',
            'gross_sales': '0',
            'units_sold': '0'
        },
    ]


@pytest.fixture()
def set_of_dates():
    return set("25/07", "18/07", "11/07", "04/07")


@pytest.fixture()
def set_of_product_identifiers():
    return set("60988638", "59842899", "87149829", "90432853")


@pytest.fixture()
def set_of_brand_identifiers():
    return set("1", "2", "3", "4")


# @pytest.fixture(autouse=True)
# def patch_product_reporter(monkeypatch, product_data, set_of_product_identifiers, set_of_dates):
#     def substitute_func(self, file_name):
#         return product_data, set_of_product_identifiers, set_of_dates
#     monkeypatch.setattr(ProductReporter, '_csv_ingester', substitute_func)


# @pytest.fixture(autouse=True)
# def patch_brand_reporter(monkeypatch, brand_data, set_of_brand_identifiers, set_of_dates):
#     def substitute_func(self, file_name):
#         return brand_data, set_of_brand_identifiers, set_of_dates
#     monkeypatch.setattr(BrandReporter, '_csv_ingester', substitute_func)
