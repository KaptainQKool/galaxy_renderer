from typing import Any





presets: dict[str, dict[str, Any]] = {
    '': {}
}

star_names: dict[str, Any] = {
    'letters': [
        {
            'char': 'a',
            'weight': 8200
        },
        {
            'char': 'b',
            'weight': 1500
        },
        {
            'char': 'c',
            'weight': 2800
        },
        {
            'char': 'd',
            'weight': 4300
        },
        {
            'char': 'e',
            'weight': 12700
        },
        {
            'char': 'f',
            'weight': 2200
        },
        {
            'char': 'g',
            'weight': 2000
        },
        {
            'char': 'h',
            'weight': 6100
        },
        {
            'char': 'i',
            'weight': 7000
        },
        {
            'char': 'j',
            'weight': 160
        },
        {
            'char': 'k',
            'weight': 770
        },
        {
            'char': 'l',
            'weight': 400
        },
        {
            'char': 'm',
            'weight': 2400
        },
        {
            'char': 'n',
            'weight': 6700
        },
        {
            'char': 'o',
            'weight': 7500
        },
        {
            'char': 'p',
            'weight': 1900
        },
        {
            'char': 'q',
            'weight': 120
        },
        {
            'char': 'r',
            'weight': 6000
        },
        {
            'char': 's',
            'weight': 6300
        },
        {
            'char': 't',
            'weight': 9100
        },
        {
            'char': 'u',
            'weight': 2800
        },
        {
            'char': 'v',
            'weight': 980
        },
        {
            'char': 'w',
            'weight': 2400
        },
        {
            'char': 'x',
            'weight': 150
        },
        {
            'char': 'y',
            'weight': 2000
        },
        {
            'char': 'z',
            'weight': 74
        }
    ],
    'seps': [
        {
            'char': ' ',
            'weight': 3
        },
        {
            'char': '-',
            'weight': 1
        }
    ],
    'word_length': {
        'mean': 6,
        'stdev': 3.0,
        'min': 2
    },
    'words': {
        'mean': 2,
        'stdev': 1.0,
        'min': 1
    }
}