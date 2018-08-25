# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.getcwd())

from mapjson import MapJSON
from unittest import mock


class TestMapJSON(unittest.TestCase):
    """Test of MapJSON
    """

    path = os.path.dirname(os.path.abspath(__file__))
    FIELDS_MAPPING_csv = os.path.join(path, 'FIELDS_MAPPING.csv')
    FIELDS_MAPPING_pkl = os.path.join(path, 'FIELDS_MAPPING.pkl')

    def _get_response(self):
        """Get response before mapping.
        """
        return {
            "article": {
                "total": 955,
                "offset": 0,
                "response_cnt": 1,
                "hits": [
                    {
                        "articleid": "NKM100000000000",
                        "_score": 386.92987,
                        "baitai_kind": "NKM",
                        "dukebi2": "2015-09-25T00:00:00+09:00:00",
                        "addtime2": "2015-09-25T15:00:11+09:00:00",
                        "updatetime2": "2015-09-25T15:00:11+09:00:00",
                        "headline": "This is a headline",
                    }
                ]
            }
        }

    def _get_mapping_response(self):
        """Get response after mapping.
        """
        return {
            "article": {
                "total": 955,
                "offset": 0,
                "response_cnt": 1,
                "hits": [
                    {
                        "article_id": "NKM100000000000",
                        "_score": 386.92987,
                        "media_code": "NKM",
                        "publish_datetime": "2015-09-25T00:00:00+09:00:00",
                        "add_datetime": "2015-09-25T15:00:11+09:00:00",
                        "update_datetime": "2015-09-25T15:00:11+09:00:00",
                        "headline": "This is a headline",
                    }
                ]
            }
        }

    def test_mapping(self):
        """
        Test whether it is mapped as intended.
        """
        mapjson = MapJSON(self._get_response())
        new_json_dict = mapjson.map_keys_with_csv(
            self.FIELDS_MAPPING_csv,
            self.FIELDS_MAPPING_pkl,
        )
        self.assertEqual(
            new_json_dict,
            self._get_mapping_response()
        )

    def test_invalid_csv(self):
        """
        Test when the configuration of csv is different from the specified format.
        A case where there is a row in which csv has only one column.
        """
        key_list = ['hogehoge', 'huag, hoge']
        path = 'mapjson.MapJSON._get_fields_mapper'
        with mock.patch(path) as res_mock:
            res_mock.return_value = key_list
            mapjson = MapJSON(self._get_response())
            with self.assertRaises(Exception):
                new_json_dict = mapjson.map_keys_with_csv(
                    self.FIELDS_MAPPING_csv,
                    self.FIELDS_MAPPING_pkl,
                )  # flake8: NOQA
