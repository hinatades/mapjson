import os
import pickle
from typing import Any, List, Dict


class JSONMapper(object):
    """A class that generates mappable json objects.
    You can map dictionary type JSON keys and values, using CSV or Pikle file.
    In mapping, you do not have to worry about the structure of JSON.
    The format of csv needs to be a two column configuration of before,after as follows
    ---
    articleid,article_id
    mediag1,media_g1
    mediag1seq,media_g1_seq
    attach_file_g.attname,attach_file_g.name
    attach_file_g.attgroup,attach_file_g.group
    ...
    ---
    Elements connected by dots represent parent-child relationship.
    Example of json as input value:
    json_dict = {
        "hogehoge": "hogehoge",
        "hogehuga": [],
        "hugahuga": {}
    }
    Attributes:
        json_dict (dict): Dictionary type JSON
        csv_path (str): Path of mapping csv file
        pk._path (str): Path of mapping pikle file
    """

    json_dict: Dict[str, Any] = {}
    csv_path: str = ''
    pkl_path: str = ''
    map_cols: List[int] = []

    def __init__(self, json: dict) -> None:
        self.json_dict = json

    def map_keys_with_csv(self, csv_path: str, pkl_path: str='.', map_cols: list=[0, 1]) -> dict:
        """Map JSON keys with CSV file
        CSV is used to create a dictionary with keys after mapping
        It is written as key_dict below.
        key_dict = {
            "parent_field_1": "parent_field_2",
            "child_field_1": {
                "parent_field_a_1" : "child_field_a_2",
                "parent_field_b_1" : "child_field_b_2,
            }
        }
        Args:
            csv_path (str): Path of mapping CSV file
            pkl_path (str): Path of mapping Pikle file
            map_cols (list) CSV column number before and after mapping
        Return:
            dict:
        """
        self.csv_path = csv_path
        self.pkl_path = pkl_path
        self.map_cols = map_cols
        new_json_dict = self.json_dict

        key_dict = {}
        for key in self._get_fields_mapper():
            try:
                key_before = key.split(',')[map_cols[0]]
                key_after = key.split(',')[map_cols[1]]
            except Exception as e:
                raise e
            if len(key_before.split('.')) == 1 and len(key_after.split('.')) == 1:
                key_dict[key_before] = key_after
            elif len(key_before.split('.')) == 2 and len(key_after.split('.')) == 2:
                parent_key_before = key_before.split('.')[0]
                child_key_before = key_before.split('.')[1]
                parent_key_after = key_after.split('.')[0]
                child_key_after = key_after.split('.')[1]
                if parent_key_before not in key_dict.keys():
                    key_dict[parent_key_before] = parent_key_after
                if child_key_before not in key_dict.keys():
                    child_dict = {}
                    child_dict[parent_key_before] = child_key_after
                    key_dict[child_key_before] = child_dict
                elif child_key_before in key_dict.keys():
                    if key_dict[child_key_before].get(parent_key_before):
                        pass
                    else:
                        key_dict[child_key_before][parent_key_before] = child_key_after
                else:
                    raise Exception
            else:
                raise Exception

        my_parent_key = ''
        new_json_dict = self._get_dict_mapping_keys(
            new_json_dict, my_parent_key, key_dict
        )
        return new_json_dict

    def _get_fields_mapper(self) -> str:
        """Load CSV file mapping JSON keys.
        if no pickle, make it.
        """
        if not os.path.isfile(self.pkl_path):
            self._refresh_pickle_file()
        with open(self.pkl_path, mode='rb') as f:
            return pickle.load(f)

    def _refresh_pickle_file(self) -> None:
        """Write out pickle from csv."""
        with open(self.csv_path, 'r') as f:
            load_list = []
            for row in f:
                load_list.append(row.strip())
            with open(self.pkl_path, mode='wb') as f:  # type: ignore
                pickle.dump(load_list, f)  # type: ignore

    def _update_return_dict(self, return_dict: dict, return_dict_key: str, value_before_map, my_parent_key: str, key_dict: dict) -> None:
        """Update return_dict based on dictionary value
        Args:
            return_dict (dict): Return dictionary
            return_dict_key (): Key of return dictionary
            value_before_map (dict, list, str): Value of the key before mappping
            my_parent_key (str): parent Dict key before mapping
            key_dict (dic) Dictionary with keys after mapping
        Returns:
            None
        """
        if isinstance(value_before_map, dict):
            return_dict[return_dict_key] = self._get_dict_mapping_keys(value_before_map, my_parent_key, key_dict)
        elif isinstance(value_before_map, list):
            return_dict[return_dict_key] = self._get_list_mapping_keys(value_before_map, my_parent_key, key_dict)
        else:
            return_dict[return_dict_key] = value_before_map

    def _get_dict_mapping_keys(self, json_dict: dict, my_parent_key: str, key_dict: dict) -> dict: # flake8: NOQA
        """Get dictionary mapping JSON keys.
        Args:
            json_dict (dict): Dictionary type JSON
            my_parent_key (str): parent Dict key before mapping
            key_dict (dic) Dictionary with keys after mapping
        Returns:
            dict
        """
        return_dict: Dict[str, Any] = {}
        for k, v in json_dict.items():
            if k in key_dict.keys():
                if isinstance(key_dict[k], str):
                    self._update_return_dict(return_dict, key_dict[k], v, k, key_dict)
                elif isinstance(key_dict[k], dict):
                    if my_parent_key in key_dict[k].keys():
                        self._update_return_dict(return_dict, key_dict[k][my_parent_key], v, k, key_dict)
                    else:
                        self._update_return_dict(return_dict, k, v, k, key_dict)
                else:
                    raise Exception
            else:
                self._update_return_dict(return_dict, k, v, k, key_dict)
        return return_dict

    def _get_list_mapping_keys(self, dict_list: list, my_parent_key: str, key_dict: dict) -> list:
        """Get list mapping JSON keys.
        Args:
            json_dict (dict): Dictionary type JSON
            my_parent_key (str): parent Dict key before mapping
            key_dic (dict): Dictionary with keys after mapping
        Returns:
            list
        """
        return_list: List[Any] = []
        new_list: List[Any] = []
        new_dict: Dict[Any, Any] = {}
        for i in dict_list:
            if isinstance(i, dict):
                new_dict = self._get_dict_mapping_keys(i, my_parent_key, key_dict)
                return_list.append(new_dict)
            elif isinstance(i, list):
                new_list = self._get_list_mapping_keys(i, my_parent_key, key_dict)
                return_list.append(new_list)
            else:
                return_list.append(i)
        return return_list
