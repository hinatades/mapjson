# -*- coding: utf-8 -*-

from articles.edits import MapJSON
from unittest import mock


class TestMapJSON(TestCase):
    """
    MapJSONのテスト
    """

    def _get_response(self):
        """
        Get response before mapping.
        """
        return {
            "article": {
                "total": 955,
                "offset": 0,
                "response_cnt": 1,
                "hits": [
                    {
                    }
                ]
            }
        }

    def _get_mapping_response(self):
        """
        Get response after mapping.
        """
        return {
            "article": {
                "total": 955,
                "offset": 0,
                "response_cnt": 1,
                "hits": [
                    {
                    }
                ]
            }
        }

    # TODO: Add test csv.

    # def test_mapping(self):
    #     """
    #     Test whether it is mapped as intended.
    #     """
    #     mapjson = MapJSON(self._get_response())
    #     new_json_dict = mapjson.map_keys_with_csv(
    #         settings.FIELDS_MAPPING_CSV_PATH,
    #         settings.FIELDS_MAPPING_PKL_LIST_PATH
    #     )
    #     self.assertEqual(
    #         new_json_dict,
    #         self._get_mapping_response()
    #     )

    # def test_invalid_csv(self):
    #     """
    #     [異常系]

    #     Test when the configuration of csv is different
    #     from the specified format.
    #     A case where there is a row in which csv has only one column.
    #     """
    #     key_list = ['hogehoge', 'huag, hoge']
    #     path = 'articles.edits.MapJSON._get_fields_mapper'
    #     with mock.patch(path) as res_mock:
    #         res_mock.return_value = key_list
    #         mapjson = MapJSON(self._get_response())
    #         with self.assertRaises(Exception):
    #             new_json_dict = mapjson.map_keys_with_csv(
    #                 settings.FIELDS_MAPPING_CSV_PATH,
    #                 settings.FIELDS_MAPPING_PKL_LIST_PATH
    #             )  # flake8: NOQA
