import os
import pickle
from typing import Any, List, Dict


class MapJSON(object):
    """A class that generates mappable json objects.

    You can map dictionary type JSON keys and values, using CSV and Pikle file.
    In mapping, you do not have to worry about the structure of JSON.
    The format of csv needs to be a two column configuration of before,after as follows

    ---
    articleid,article_id
    ipcode,ip_code
    mediag1,media_g1
    mediag1seq,media_g1_seq
    ...
    ---

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
        for key in self._get_fields_mapper():
            try:
                key_befor = key.split(',')[map_cols[0]]
                key_after = key.split(',')[map_cols[1]]
            except Exception as e:
                raise e
            if key_befor != key_after:
                new_json_dict = self._get_dict_mapping_keys(new_json_dict, key_befor, key_after)
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

    def _get_dict_mapping_keys(self, json_dict: dict, key_befor: str, key_after: str) -> dict:
        """Get dictionary mapping JSON keys.

        Args:
            json_dict (dict): Dictionary type JSON
            key_befor (str): Dict key befor mapping
            key_after (str): Dict key after mapping

        Returns:
            dict
        """
        return_dict: Dict[str, Any] = {}
        new_dict: Dict[str, Any] = {}
        new_list: List[Any] = []
        for k, v in json_dict.items():
            if k == key_befor:
                if isinstance(v, dict):
                    new_dict = self._get_dict_mapping_keys(v, key_befor, key_after)
                    return_dict[key_after] = new_dict
                elif isinstance(v, list):
                    new_list = self._get_list_mapping_keys(v, key_befor, key_after)
                    return_dict[key_after] = new_list
                else:
                    return_dict[key_after] = v
            else:
                if isinstance(v, dict):
                    new_dict = self._get_dict_mapping_keys(v, key_befor, key_after)
                    return_dict[k] = new_dict
                elif isinstance(v, list):
                    new_list = self._get_list_mapping_keys(v, key_befor, key_after)
                    return_dict[k] = new_list
                else:
                    return_dict[k] = v
        return return_dict

    def _get_list_mapping_keys(self, dict_list: list, key_befor: str, key_after: str) -> list:
        """Get list mapping JSON keys.

        Args:
            json_dict (dict): Dictionary type JSON
            key_befor (str): Dict key befor mapping
            key_after (str): Dict key after mapping

        Returns:
            list
        """
        return_list: List[Any] = []
        new_list: List[Any] = []
        new_dict: Dict[Any, Any] = {}
        for i in dict_list:
            if isinstance(i, dict):
                new_dict = self._get_dict_mapping_keys(i, key_befor, key_after)
                return_list.append(new_dict)
            elif isinstance(i, list):
                new_list = self._get_list_mapping_keys(i, key_befor, key_after)
                return_list.append(new_list)
            else:
                return_list.append(i)
        return return_list
