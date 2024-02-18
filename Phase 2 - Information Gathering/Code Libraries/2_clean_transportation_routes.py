from collections import defaultdict
import pathlib
import json
from pprint import pprint

def filter_ways_from_data(file_path: pathlib.Path, output_file_path: pathlib.Path):
    # Re-loading the original GeoJSON data
    with open(file_path, 'r') as file:
        original_geojson_data = json.load(file)

    print(f'Processing {file_path}')

    missing_properties_count = defaultdict(int)
    missing_properties_count_stop = defaultdict(int)

    properties_to_retain = ['from', 'importance', 'name', 'route', 'to', 'wheelchair', 'region']
    properties_to_retain_stop = ['ref', 'lat', 'lon']

    def retain_needed_properties(element):
        if element['type'] == 'relation':
            if len(element['members']) < 2:
                return None
            element['members'] = [{k: v for k, v in member.items() if k in properties_to_retain_stop} for member in element['members']]
            element['tags'] = {name: value for name, value in element['tags'].items() if name in properties_to_retain}
            element['tags']['region'] = 'region_1'

            for prop in properties_to_retain:
                if prop not in element['tags']:
                    missing_properties_count[prop] += 1

            for member in element['members']:
                for prop in properties_to_retain_stop:
                    if prop not in member:
                        missing_properties_count_stop[prop] += 1
        return element

    # Apply the filter to all elements in the original data
    cleaned_elements = [retain_needed_properties(element) for element in original_geojson_data['elements']]
    cleaned_elements = [e for e in cleaned_elements if e is not None]


    original_geojson_data['elements'] = cleaned_elements

    print(f'Number of stops: {sum([len(members) for element in cleaned_elements for members in element['members']])}')
    for k, cnt in missing_properties_count.items():
        missing_properties_count[k] = cnt / len(cleaned_elements)
    for k, cnt in missing_properties_count_stop.items():
        missing_properties_count_stop[k] = cnt / sum([len(members) for element in cleaned_elements for members in element['members']])
    pprint(f'Missing properties: {missing_properties_count}')
    pprint(f'Missing properties stop: {missing_properties_count_stop}')

    with open(output_file_path, 'w') as output_file:
        json.dump(original_geojson_data, output_file)


if __name__ == '__main__':
    datasets_folder = pathlib.Path(__file__).parent.parent.resolve() / 'Cleaned datasets'
    transportation_data_path = datasets_folder / 'transportation'
    train_routes_json_file_path = transportation_data_path / 'train_routes_filtered.geojson'
    output_train_routes_json_file_path = transportation_data_path / 'train_routes_cleaned.geojson'
    bus_routes_json_file_path = transportation_data_path / 'bus_routes_filtered.geojson'
    output_bus_routes_json_file_path = transportation_data_path / 'bus_routes_cleaned.geojson'

    filter_ways_from_data(train_routes_json_file_path, output_train_routes_json_file_path)
    filter_ways_from_data(bus_routes_json_file_path, output_bus_routes_json_file_path)
