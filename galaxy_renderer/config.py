from typing import Any
import numpy as np

preset: str = ''

# the number of images to generate
frames: int = 1

# regex string for data files to match
# inside the 'star_catalogues/data' folder
data_files: str = 'gaia_edr3/GaiaSource_*.csv.gz'
# how many stars to pull from each file (csv.gz files only)
# set to 0 to get all stars (not recommended)
stars_per_file: int = 100000
# file path to save star positions to
# inside the 'star_catalogues/data/generated' folder
# set to an empty string to disable saving
json_output: str = 'star_chart_gaia_edr3_rand_8000000_07-18-26.json'

# coordinates of the galactic center
# (or whatever coordinate origin you want to use)
# it's a method because i didn't just want to put
# in a bunch of random numbers and having the full
# calculations in just one line would be insane
def galactic_center() -> list[float]:
    # https://en.wikipedia.org/wiki/Sagittarius_A*
    # https://astronomy.stackexchange.com/questions/54280/how-to-get-star-position-from-the-gaia-data-set
    distance_ly: float = 26996.0
    ra: float = (360 / 24) * (17 + (45 + (40.0409) / 60) / 60) # 17h 45m 40.0409s
    dec: float = -29 - (28.118 / (3600 * 1000)) # -29* 0' 28.118"
    
    x: float = distance_ly * np.sin(np.deg2rad(ra)) * np.cos(np.deg2rad(dec))
    y: float = distance_ly * np.sin(np.deg2rad(ra)) * np.sin(np.deg2rad(dec))
    z: float = distance_ly * np.cos(np.deg2rad(ra))
    
    return [x, y, z]


PRESETS: dict[str, dict[str, Any]] = {
    '': {
        'frames': frames,
        
        'data_files': data_files,
        'stars_per_file': stars_per_file,
        'json_output': json_output,
        
        'galactic_center': galactic_center()
    },
    
    'gaia_edr3': {
        'frames': 1,
        
        'data_files': 'gaia_edr3/GaiaSource_*.csv.gz',
        'stars_per_file': 1000,
        'json_output': '',
        
        'galactic_center': [
            26996.0 * np.sin(np.deg2rad((360 / 24) * (17 + (45 + (40.0409) / 60) / 60))) * np.cos(np.deg2rad(-29 - (28.118 / (3600 * 1000)))),
            26996.0 * np.sin(np.deg2rad((360 / 24) * (17 + (45 + (40.0409) / 60) / 60))) * np.sin(np.deg2rad(-29 - (28.118 / (3600 * 1000)))),
            26996.0 * np.cos(np.deg2rad((360 / 24) * (17 + (45 + (40.0409) / 60) / 60)))
        ]
    }
}

r_sun_ly: float = 0.0000000735355
temp_to_peak_wl = lambda T: 2897772.9 / T
star_classes: list[dict[str, Any]] = [
    {
        'class': 'O',
        'radius': {
            'max': 700,
            'min': 6.6
        },
        'temp': {
            'max': 50000,
            'min': 33000
        },
        'luminosity': {
            'max': 1000000,
            'min': 30000
        },
        'weight': 3
    },
    {
        'class': 'B',
        'radius': {
            'max': 6.6,
            'min': 1.8
        },
        'temp': {
            'max': 33000,
            'min': 10000
        },
        'luminosity': {
            'max': 30000,
            'min': 25
        },
        'weight': 12000
    },
    {
        'class': 'A',
        'radius': {
            'max': 1.8,
            'min': 1.4
        },
        'temp': {
            'max': 10000,
            'min': 7300
        },
        'luminosity': {
            'max': 25,
            'min': 5
        },
        'weight': 61000
    },
    {
        'class': 'F',
        'radius': {
            'max': 1.4,
            'min': 1.15
        },
        'temp': {
            'max': 7300,
            'min': 6000
        },
        'luminosity': {
            'max': 5,
            'min': 1.5
        },
        'weight': 300000
    },
    {
        'class': 'G',
        'radius': {
            'max': 1.15,
            'min': 0.96
        },
        'temp': {
            'max': 6000,
            'min': 5300
        },
        'luminosity': {
            'max': 1.5,
            'min': 0.6
        },
        'weight': 760000
    },
    {
        'class': 'K',
        'radius': {
            'max': 0.96,
            'min': 0.7
        },
        'temp': {
            'max': 5300,
            'min': 3900
        },
        'luminosity': {
            'max': 0.6,
            'min': 0.08
        },
        'weight': 1200000
    },
    {
        'class': 'M',
        'radius': {
            'max': 0.7,
            'min': 0.001
        },
        'temp': {
            'max': 3900,
            'min': 2300
        },
        'luminosity': {
            'max': 0.08,
            'min': 0.0003
        },
        'weight': 7600000
    }
]
for c in star_classes:
    c['peak_wl'] = {
        'max': temp_to_peak_wl(c['temp']['min']),
        'min': temp_to_peak_wl(c['temp']['max'])
    }
    c['radius_ly'] = {
        'max': r_sun_ly * c['radius']['max'],
        'min': r_sun_ly * c['radius']['min']
    }
