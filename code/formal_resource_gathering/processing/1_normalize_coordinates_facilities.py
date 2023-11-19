import copy
import json
import numpy as np
import pathlib
from typing import Optional
from pprint import pprint

def normalize_coordinates(sport: str, file_path: pathlib.Path, output_file_path: Optional[pathlib.Path] = None):
    with open(file_path, 'r') as file:
        geojson_data = json.load(file)

    # Function to calculate the center of a multipolygon
    def calculate_center(multipolygon):
        # Extract all the longitude and latitude coordinates
        all_coords = np.array([coord for polygon in multipolygon for coord in polygon])
        # Calculate the mean of the coordinates
        center = np.mean(all_coords, axis=0)
        return center.tolist()

    # Modify the GeoJSON data
    new_features = []
    for feature in geojson_data["features"]:
        new_feature = copy.deepcopy(feature)
        if sport not in new_feature["properties"]:
            new_feature["properties"]["sport"] = sport
        # take the center of
        if new_feature["geometry"]["type"] == "Polygon":
            center = calculate_center(new_feature["geometry"]["coordinates"])
            new_feature["properties"]["lat"] = center[0]
            new_feature["properties"]["lon"] = center[1]
            if 'type' in new_feature["properties"]:
                del new_feature["properties"]["type"]
        elif new_feature["geometry"]["type"] == "Point":
            new_feature["properties"]["lat"] = new_feature["geometry"]["coordinates"][0]
            new_feature["properties"]["lon"] = new_feature["geometry"]["coordinates"][1]
        elif new_feature["geometry"]["type"] == "LineString":
            new_feature["properties"]["lat"] = new_feature["geometry"]["coordinates"][0][0]
            new_feature["properties"]["lon"] = new_feature["geometry"]["coordinates"][0][1]
        else:
            raise RuntimeError(f'There is an unhandled geometry type: "{new_feature["geometry"]["type"]}". File: {file_path}')
        
        del new_feature["properties"]["@id"]
        del new_feature["geometry"]
        new_features.append(new_feature)

    geojson_data["features"] = new_features

    # Save the modified GeoJSON data
    with open(output_file_path, 'w') as file:
        json.dump(geojson_data, file, indent=4)

if __name__ == '__main__':
    datasets_folder = pathlib.Path(__file__).parent.parent.parent.parent.resolve() / 'datasets'
    sports = ['athletics', 'climbing', 'fitness', 'soccer', 'volleyball']
    for sport in sports:
        print('Processing sport:', sport)
        input_file_path = datasets_folder / 'formal' / 'sports_facilities' / f'{sport}.geojson'
        output_file_path = datasets_folder / 'formal' / 'sports_facilities' / f'{sport}_normalized.geojson'
        normalize_coordinates(sport, input_file_path, output_file_path)
