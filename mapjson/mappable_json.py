import os
import pickle


class MapJSON(object):
    """
    Mappable JSON
    """

    json_dict = {}
    csv_path = ''
    pkl_path = ''

    def __init__(self, json_dict):
        self.json_dict = json_dict

    def set_csv_mapping(self, csv_path, pkl_path='.'):
        """
        """
        self.csv_path = csv_path
        self.pkl_path = pkl_path

    def _refresh_pickle_file(self):
        """
        """
        with open(self.csv_path, 'r') as f:
            load_list = []
            for row in f:
                load_list.append(row.strip())

            with open(self.pkl_path, mode='wb') as f:
                pickle.dump(load_list, f)

        return

    def _get_fields_mapper(self):
        """
        """
        if not os.path.isfile(self.pkl_path):
            self._refresh_pickle_file()

        with open(self.pkl_path, mode='rb') as f:
            return pickle.load(f)

    def _get_all_keys(self, key_list):
        """
        """
        new_json_dict = {}
        json_dict_value = {}

        for k, v in self.json_dict.items():
            if k == key_list[0]:
                new_json_dict[key_list[1]] = v
            else:
                if isinstance(v, dict):
                    json_dict_value = self._get_all_keys(v, key_list)
                    new_json_dict[k] = json_dict_value
                else:
                    new_json_dict[k] = v

        return new_json_dict

    def map_keys_with_csv(self):
        """
        """
        new_json_dict = self.json_dict

        for key in self._get_fields_mapper():
            key_list = key.split(',')
            new_json_dict = self._get_all_keys(key_list)

        return new_json_dict
