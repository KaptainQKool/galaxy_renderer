import name_generator.name_generator as namegen
from galaxy_renderer.config import star_classes
from typing import Iterator, Any
from copy import deepcopy
from pathlib import Path
import pandas as pd
import numpy as np
import json


def star_data(
        glob_str: str,
        stars_per_file: int = 0,
        out_json: str = '',
        origin: list[float] | None = None,
        max_distance: float = 0
    ) -> dict[str, list[dict[str, Any]]]:
    
    stars: dict[str, list[dict[str, Any]]] = {
        'stars': []
    }
    
    data_paths_2: Iterator[Path] = paths(glob_str)
    n_files: int = sum(1 for _ in data_paths_2)
    nf: int = 1
    data_paths: Iterator[Path] = paths(glob_str)
    for p in data_paths:
        print(f'    {str(nf).rjust(len(str(n_files)))}/{n_files} - Reading from file {p.name}', end='')
        match p.suffixes:
            case ['.csv', '.gz']:
                contents: pd.DataFrame = pd.read_csv(p, compression='gzip', sep=',', comment='#', on_bad_lines='skip')
                nrows: int = len(contents.index)
                print(f' ({nrows} rows)')
                
                stars_temp: list[dict[str, Any]] = []
                contents_shuffled = contents.sample(frac=1).reset_index()
                for i, row in contents_shuffled.iterrows():
                    if stars_per_file > 0 and int(i) >= stars_per_file:
                        break
                    
                    designation = row['designation']
                    name = namegen.generate(save_output=False, print_output=False)

                    class_weights = [c['weight'] for c in star_classes[:]]
                    class_weights_n = [float(i)/sum(class_weights) for i in class_weights]
                    class_index = np.random.choice(len(star_classes), 1, p=class_weights_n)[0]
                    star_class = star_classes[class_index]

                    class_id = star_class['class']
                    radius = np.random.uniform(star_class['radius_ly']['min'], star_class['radius_ly']['max'])
                    luminosity = np.random.uniform(star_class['luminosity']['min'], star_class['luminosity']['max'])
                    peak_wl = np.random.uniform(star_class['peak_wl']['min'], star_class['peak_wl']['max'])
                    wl_var = np.random.uniform(star_class['wl_var']['min'], star_class['wl_var']['max'])
                    
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
                    
                    if origin:
                        x -= origin[0]
                        y -= origin[1]
                        z -= origin[2]
                    distance_from_center = np.sqrt(x**2 + y**2 + z**2)

                    discard = (np.isnan(x) or np.isnan(y) or np.isnan(z)) or (max_distance > 0 and distance_from_center > max_distance)
                    if not discard:
                        temp_star: dict[str, Any] = {
                            'designation': designation,
                            'name': name,

                            'class': class_id,
                            'radius': radius,
                            'luminosity': luminosity,
                            'peak_wl': peak_wl,
                            'wl_var': wl_var,
                            
                            'x': x,
                            'y': y,
                            'z': z
                        }
                        stars_temp.append(temp_star)
                
                print(f'    {''.rjust(4 + 2*len(str(n_files)))}Got {len(stars_temp)} stars from {p.name}')
                stars['stars'].extend(stars_temp)
                
            case ['.json']:
                with open(p) as in_json:
                    stars_temp_json = json.load(in_json)
                print(f'\n    Got {len(stars_temp_json['stars'])} stars from {p.name}')
                stars['stars'].extend(stars_temp_json)
                
            case _:
                raise NotImplementedError(''.join(p.suffixes)+' files are not supported')
        
        nf += 1
    
    if out_json:
        print('    Saving star data to '+out_json+'...')
        with open(str(Path(__file__).parent)+'/data/generated/'+out_json, 'w') as out:
            json.dump(stars, out, indent=2)
        print('    Done!')
    
    return stars


def paths(glob_str: str) -> Iterator[Path]:
    p = Path(__file__).parent
    glob = p.glob('data/'+glob_str)
    return glob