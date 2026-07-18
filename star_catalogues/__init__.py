from name_generator import generate_name
from typing import Iterator, Any
from pathlib import Path
import pandas as pd
import numpy as np
import json


def star_data(
        glob_str: str,
        out_json: str = ''
    ) -> dict[str, list[dict[str, Any]]]:
    
    stars: dict[str, list[dict[str, Any]]] = {
        'stars': []
    }
    
    data_paths: Iterator[Path] = paths(glob_str)
    for p in data_paths:
        print(f'    Reading from file {p.name}')
        match p.suffixes:
            case ['.csv', '.gz']:
                contents: pd.DataFrame = pd.read_csv(p, compression='gzip', sep=',', comment='#', on_bad_lines='skip')
                nrows: int = len(contents.index)
                
                stars_temp: list[dict[str, Any]] = []
                for i, row in contents.iterrows():
                    designation = row['designation']
                    name = generate_name()
                    
                    dec = row['dec']
                    ra = row['ra']
                    parallax = row['parallax']
                    
                    # x, y, z equations from
                    # https://astronomy.stackexchange.com/questions/54280/how-to-get-star-position-from-the-gaia-data-set
                    
                    # distance from earth to star in lightyears
                    # 1 ly = 0.3066013938 pc
                    # 1 pc = 1000 / 1 mas
                    distance_ly = 306.6013938 / parallax
                    
                    # spherical coords ftw
                    x = distance_ly * np.sin(np.deg2rad(ra)) * np.cos(np.deg2rad(dec))
                    y = distance_ly * np.sin(np.deg2rad(ra)) * np.sin(np.deg2rad(dec))
                    z = distance_ly * np.cos(np.deg2rad(ra))
                    
                    temp_star: dict[str, Any] = {
                        'designation': designation,
                        
                        'x': x,
                        'y': y,
                        'z': z
                    }
                    stars_temp.append(temp_star)
                
                stars['stars'].extend(stars_temp)
                
            case ['.json']:
                print('json file')
            case _:
                raise NotImplementedError(''.join(p.suffixes)+' files are not supported')
    
    if out_json:
        print('    Saving star data to '+out_json+'...')
        with open(out_json, 'w') as out:
            json.dump(stars, out)
        print('    Done!')
    
    return stars


def paths(glob_str: str) -> Iterator[Path]:
    p = Path(__file__).parent
    glob = p.glob(glob_str)
    return glob