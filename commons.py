# -*- coding: utf-8 -*-
import pathlib
import calendar
from datetime import datetime, date
import json
from typing import Optional, Union
from dateutil import parser, rrule


class ComplexEncoder(json.JSONEncoder):
    """Json Complex EnCoding Rules
    """

    def default(self, obj):
        """Overloaded conversion rule

        :param obj: object
        :return: Formatted string content
        """

        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif (isinstance(obj, list) or
              isinstance(obj, tuple) or
              isinstance(obj, dict) or
              isinstance(obj, set)):
            return json.JSONEncoder.default(self, obj)
        else:
            return str(obj)


def read_json(path) -> dict:
    """From json file read data to a dict object

    :param path: json file path
    :return: None
    """
    with open(str(path), "r", encoding='utf8') as fp:
        return json.load(fp)


def write_json(path, json_obj: Union[dict, str, list], prettify=False):
    """Write python object to json file

    :param path: json file path
    :param json_obj: python obj (such as dict, str, list)
    :param prettify: if you want to fit for human observation, set it True, default is False
    :return: None
    """
    if prettify:
        indent = 4
    else:
        indent = None
    if isinstance(json_obj, str):
        json_obj = json.loads(json_obj)
    with open(str(path), "w", encoding='utf8') as fp:
        json.dump(json_obj, fp, indent=indent, cls=ComplexEncoder)


def dict2json(content: Optional[Union[dict, list]], prettify=False):
    """Write python object to json string object

    :param content: python obj (such as dict, list)
    :param prettify: if you want to fit for human observation, set it True, default is False
    :return: None
    """
    if prettify:
        indent = 4
    else:
        indent = None
    return json.dumps(content, indent=indent, cls=ComplexEncoder)


def mkdir(path):
    """Is a simple way to create directory

    :param path: directory path
    :return: None
    """
    p = pathlib.Path(path)
    p.mkdir(parents=True, exist_ok=True)


def parse_datetime(input_date):
    """Parse datetime from input string and datetiem type,
    this can recognize the vast majority of time formats

    :param input_date: time formats data (such as string or datetime)
    :return: datetime if parsing success, else is None
    """
    if isinstance(input_date, str):
        if input_date == "0000-00-00 00:00:00":
            return parser.parse("0001-01-01")
        return parser.parse(input_date)
    if isinstance(input_date, datetime):
        return input_date
    return None


def get_month_days(year, month):
    """By this function, you can get how many days are there in a month

    :param year: The number of days in the month varies from year to year
    :param month: select a month
    :return: days in a month
    """
    monthrange = calendar.monthrange(year, month)
    return monthrange[1]


if __name__ == '__main__':
    pass
