# mapjson

`mapjson` is mappable JSON object.

### Install

Using pip

```
pip install git+https://github.com/hinatades/mapjson.git
```

or using pip with PyPI: https://pypi.python.org/pypi/mapjson

```
pip install mapjson
```

### Usage

```
import mapjson

json_data = {}
mapjson = MapJSON(json_data)
```

### Example

#### map json keys with CSV

```
new_input_data = mapjson.map_keys_with_csv(
    'MAPPING_CSV_PATH',
    'MAPPING_PKL_PATH',
    [1, 0]
)
```

### Author

@hinatades (<hnttisk@gmail.com>)
