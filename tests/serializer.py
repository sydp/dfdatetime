#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the date and time values serializer."""

import unittest

from dfdatetime import fat_date_time
from dfdatetime import posix_time
from dfdatetime import rfc2579_date_time
from dfdatetime import semantic_time
from dfdatetime import serializer
from dfdatetime import time_elements


class SerializerTest(unittest.TestCase):
  """Tests for the date and time values serializer."""

  def testConvertDateTimeValuesToDict(self):
    """Test ConvertDateTimeValuesToDict function."""
    posix_time_object = posix_time.PosixTime(timestamp=1281643591)

    expected_json_dict = {
        '__class_name__': 'PosixTime',
        '__type__': 'DateTimeValues',
        'timestamp': 1281643591}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        posix_time_object)
    self.assertEqual(json_dict, expected_json_dict)

    posix_time_object.is_local_time = True

    expected_json_dict = {
        '__class_name__': 'PosixTime',
        '__type__': 'DateTimeValues',
        'is_local_time': True,
        'timestamp': 1281643591}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        posix_time_object)
    self.assertEqual(json_dict, expected_json_dict)

    never_time_object = semantic_time.Never()

    expected_json_dict = {
        '__class_name__': 'Never',
        '__type__': 'DateTimeValues',
        'string': 'Never'}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        never_time_object)
    self.assertEqual(json_dict, expected_json_dict)

    fat_date_time_object = fat_date_time.FATDateTime(fat_date_time=0xa8d03d0c)

    expected_json_dict = {
        '__class_name__': 'FATDateTime',
        '__type__': 'DateTimeValues',
        'fat_date_time': 2832219404}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        fat_date_time_object)
    self.assertEqual(json_dict, expected_json_dict)

    rfc2579_date_time_object = rfc2579_date_time.RFC2579DateTime(
        rfc2579_date_time_tuple=(2010, 8, 12, 20, 6, 31, 6, '+', 2, 0))

    expected_json_dict = {
        '__class_name__': 'RFC2579DateTime',
        '__type__': 'DateTimeValues',
        'rfc2579_date_time_tuple': (2010, 8, 12, 20, 6, 31, 6),
        'time_zone_offset': 120}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        rfc2579_date_time_object)
    self.assertEqual(json_dict, expected_json_dict)

    time_elements_object = time_elements.TimeElements(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31))

    expected_json_dict = {
        '__class_name__': 'TimeElements',
        '__type__': 'DateTimeValues',
        'time_elements_tuple': (2010, 8, 12, 20, 6, 31)}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        time_elements_object)
    self.assertEqual(json_dict, expected_json_dict)

    time_elements_object = time_elements.TimeElementsInMilliseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 546))

    expected_json_dict = {
        '__class_name__': 'TimeElementsInMilliseconds',
        '__type__': 'DateTimeValues',
        'time_elements_tuple': (2010, 8, 12, 20, 6, 31, 546)}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        time_elements_object)
    self.assertEqual(json_dict, expected_json_dict)

    time_elements_object = time_elements.TimeElementsInMicroseconds(
        time_elements_tuple=(2010, 8, 12, 20, 6, 31, 429876))

    expected_json_dict = {
        '__class_name__': 'TimeElementsInMicroseconds',
        '__type__': 'DateTimeValues',
        'time_elements_tuple': (2010, 8, 12, 20, 6, 31, 429876)}

    json_dict = serializer.Serializer.ConvertDateTimeValuesToDict(
        time_elements_object)
    self.assertEqual(json_dict, expected_json_dict)


if __name__ == '__main__':
  unittest.main()