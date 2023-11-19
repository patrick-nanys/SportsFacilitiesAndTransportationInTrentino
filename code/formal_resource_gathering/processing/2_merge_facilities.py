import json
import pandas as pd
import pathlib

def merge(items: dict, file_path: pathlib.Path) -> dict:
    with open(file_path, 'r') as input_file:
        json_data = json.load(input_file)

    features = json_data["features"]
    features.extend(items)

    return features

if __name__ == '__main__':
    datasets_folder = pathlib.Path(__file__).parent.parent.parent.parent.resolve() / 'datasets'
    sports = ['athletics', 'climbing', 'fitness', 'soccer', 'volleyball']
    merged = {}
    for sport in sports:
        print('Processing sport:', sport)
        input_file_path = datasets_folder / 'formal' / 'sports_facilities' / f'{sport}_normalized.geojson'
        merged = merge(merged, input_file_path)

    print('Saving merged features to output file...')
    output_path = datasets_folder / 'formal' / 'sports_facilities' / 'merged_facilities.json'
    with open(output_path, 'w') as output_file:
        json.dump(merged, output_file, indent=4)
    print('Saved outputs to', output_path)
