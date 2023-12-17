import pathlib
import json

def filter_ways_from_data(file_path: pathlib.Path, output_file_path: pathlib.Path):
    # Re-loading the original GeoJSON data
    with open(file_path, 'r') as file:
        original_geojson_data = json.load(file)

    # Function to filter out 'way' types from an element, including within relations
    def filter_ways_from_element(element):
        if element['type'] == 'relation':
            # Filter out 'way' types from members of the relation
            element['members'] = [member for member in element['members'] if member['type'] != 'way']
        return element

    # Apply the filter to all elements in the original data
    filtered_elements = [filter_ways_from_element(element) for element in original_geojson_data['elements']]

    original_geojson_data['elements'] = filtered_elements

    with open(output_file_path, 'w') as output_file:
        json.dump(original_geojson_data, output_file)


if __name__ == '__main__':
    datasets_folder = pathlib.Path(__file__).parent.parent.parent.parent.resolve() / 'datasets'
    transportation_data_path = datasets_folder / 'formal' / 'transportation'
    train_routes_json_file_path = transportation_data_path / 'train_routes.geojson'
    output_train_routes_json_file_path = transportation_data_path / 'train_routes_filtered.geojson'
    bus_routes_json_file_path = transportation_data_path / 'bus_routes.geojson'
    output_bus_routes_json_file_path = transportation_data_path / 'bus_routes_filtered.geojson'

    filter_ways_from_data(train_routes_json_file_path, output_train_routes_json_file_path)
    filter_ways_from_data(bus_routes_json_file_path, output_bus_routes_json_file_path)
