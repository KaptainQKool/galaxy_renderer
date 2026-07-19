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
stars_per_file: int = 1000
# file path to save star positions to
# inside the 'star_catalogues/data/generated' folder
# set to an empty string to disable saving
json_output: str = ''

# coordinates of the galactic center
# (or whatever coordinate origin you want to use)
# method because i didn't just want to put in a
# bunch of random numbers and having the full
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