"""
These classes and functions are responsible for data ingestion, data transformation and data outputting of CSV files in certain pre-specified format.
"""


import json
from csv import DictReader
from pathlib import Path
from datetime import datetime
from operator import itemgetter

from logger import logging


class DataReporter:
    """
    This parent class should be inherited from for any new reporter's created.
    On initialisation this class will attempt to read a CSV file and collect all unique records and dates.
    """
    record_identifier = None
    record_data = None
    csv_filename = None
    list_of_dates = None
    list_of_identifiers = None

    def __init__(self):
        self.record_data, self.list_of_identifiers, self.list_of_dates = self._csv_ingester(self.csv_filename)

    def _csv_ingester(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            return self._data_parser(csv_file)

    def _data_parser(self, data):
        csv_dict_reader = DictReader(data)
        if csv_dict_reader.fieldnames is None:
            logging.warning("specified csv file is empty!")
            raise Exception("empty csv file")

        list_of_records = []
        set_of_identifiers = set()
        set_of_dates = set()

        logging.info("attempting to parse the CSV now")

        for row in csv_dict_reader:
            list_of_records.append(row)
            try:
                # grab unique identifiers for each record
                set_of_identifiers.add(row[self.record_identifier])
                # in the set only add day and month of each date
                set_of_dates.add(row['week_commencing_date'][:5])
            except KeyError as exc:
                logging.warning("specified csv file doesn't have a column like that.")
                raise KeyError("specified csv file doesn't have a column like that.") from exc

        logging.info("CSV successfully parsed")
        return list_of_records, set_of_identifiers, set_of_dates

    def calculate_data(self):
        """
        A data transformation method that holds all the private methods and then sorts the data for the users.
        """
        if self.record_data is None or self.list_of_dates is None or self.list_of_identifiers is None:
            logging.warning("record_data or list_of_dates or list_of_identifiers are not specified, can't calculate growth")
            raise Exception("record_data or list_of_dates or list_of_identifiers are not specified, can't calculate growth")
        calculated_list = []
        for identifier in self.list_of_identifiers:
            for date in self.list_of_dates:
                # This filters out relevant period of sales or 2 periods of sales, based on the identifier and dates (from both years)
                val = [row for row in self.record_data if row[self.record_identifier] == identifier and row['week_commencing_date'][:5] == date]
                if val:
                    logging.info("Results found, proceeding with data cleaning.")
                    calculated_list.append(self._clean_data(val))

        logging.debug("Unsorted data: %s", calculated_list)
        calculated_list = self._sort_data(calculated_list)
        logging.info("data successfully sorted")
        return calculated_list

    def _clean_data(self, data):
        """
        Private method to clean up data.
        It's definitely too long and could be split into 2-3 more methods, for ease of testing in the future.
        """
        returned_value = {}

        logging.debug("cleaning data array: %s", data)
        # this flow is for data with only one period
        if len(data) == 1:
            my_date = datetime.strptime(data[0]['week_commencing_date'], "%d/%m/%Y")

            if data[0]['period_id'] == '1':
                returned_value['previous_week_commencing_date'] = my_date
                # add a year to string using datetime library
                returned_value['current_week_commencing_date'] = my_date.replace(year=my_date.year + 1)
                returned_value['perc_gross_sales_growth'] = -100
                returned_value['perc_unit_sales_growth'] = -100
            else:
                returned_value['current_week_commencing_date'] = my_date
                # subtract a year to string using datetime library
                returned_value['previous_week_commencing_date'] = my_date.replace(year=my_date.year - 1)
                returned_value['perc_gross_sales_growth'] = None
                returned_value['perc_unit_sales_growth'] = None

        # this flow is for data with both periods
        else:
            for record in data:
                if record['period_id'] == '1':
                    first_period = record
                else:
                    second_period = record

            # change to datetime format
            returned_value['previous_week_commencing_date'] = datetime.strptime(first_period['week_commencing_date'], "%d/%m/%Y")
            returned_value['current_week_commencing_date'] = datetime.strptime(second_period['week_commencing_date'], "%d/%m/%Y")

            # calculate growth
            if not first_period['gross_sales'] and not second_period['gross_sales']:
                returned_value['perc_gross_sales_growth'] = None
            else:
                returned_value['perc_gross_sales_growth'] = self._calculate_growth(float(first_period['gross_sales']), float(second_period['gross_sales']))

            if not first_period['units_sold'] and not second_period['units_sold']:
                returned_value['perc_unit_sales_growth'] = None
            else:
                returned_value['perc_unit_sales_growth'] = self._calculate_growth(float(first_period['units_sold']), float(second_period['units_sold']))

        logging.debug("cleaning data before data processing hook: %s", returned_value)
        # additional processing custom for each record type
        returned_value.update(self._data_processing_hook(data[0]))
        logging.debug("cleaning data after data processing hook: %s", returned_value)
        return returned_value


    def _calculate_growth(self, previous_sales, current_sales):
        """
        Custom formula for calculating growth in percent.
        """
        logging.debug("calculating growth")
        return round(100 * (current_sales - previous_sales) / previous_sales, 2)

    def _data_processing_hook(self, data):
        """
        Hook to overload and add specific key/values for the processed data.
        """
        return {}

    def _sort_data(self, data):
        """
        Hook to overload specific sorting of data.
        """
        return data


class ProductReporter(DataReporter):
    """
    Child of DataReporter for product type of data.
    Has custom _data_processing_hook and _sort_data methods.
    """
    record_identifier = "barcode_no"
    csv_filename = "data/sales_product.csv"

    def _data_processing_hook(self, data):
        return {
            "barcode_no": data['barcode_no'],
            "product_name": data['product_name']
        }

    def _sort_data(self, data):
        return sorted(data, key=itemgetter("product_name", "current_week_commencing_date"))


class BrandReporter(DataReporter):
    """
    Child of DataReporter for brand type of data.
    Has custom _data_processing_hook and _sort_data methods.
    """
    record_identifier = "brand_id"
    csv_filename = "data/sales_brand.csv"

    def _data_processing_hook(self, data):
        return {
            "brand_id": data['brand_id'],
            "brand_name": data['brand']
        }

    def _sort_data(self, data):
        return sorted(data, key=itemgetter("brand_name", "current_week_commencing_date"))


def json_outputter():
    """
    Builds the JSON with class methods then saves the JSON file in defined location.
    """
    data = {
        "PRODUCT": ProductReporter().calculate_data(),
        "BRAND": BrandReporter().calculate_data()
    }

    # create output folder if it doesn't exist
    path = Path().absolute().as_posix()
    new_path = Path(path + '/output')
    new_path.mkdir(exist_ok=True)

    logging.info("Attempting to build a JSON file with provided data")
    with open(new_path.absolute().as_posix() + "/results.json", "w", encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, default=str)
        logging.info("JSON file successfully built")
