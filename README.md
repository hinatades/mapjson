# mapjson

![PyPI](https://img.shields.io/pypi/v/mapjson.svg?style=flat-square)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)

`mapjson` is mappable JSON object.

## Installation

Using pip

```
$ pip install git+https://github.com/hinatades/mapjson.git
```

or using pip with PyPI: https://pypi.python.org/pypi/mapjson

```
$ pip install mapjson
```

## Usage

```python
import mapjson

json_data = {}
mapjson = MapJSON(json_data)
```

## Example

### map json keys with CSV

```python
new_input_data = mapjson.map_keys_with_csv(
    'MAPPING_CSV_PATH',
    'MAPPING_PKL_PATH',
    [1, 0]
)
```

## Author

@hinatades (<hnttisk@gmail.com>)
