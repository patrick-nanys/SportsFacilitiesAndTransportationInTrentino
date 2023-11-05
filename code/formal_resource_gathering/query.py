import requests
import json
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: query.py <query_file> <output_file>")
        sys.exit(1)

    query_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # Define the Overpass API endpoint
    endpoint = "https://overpass-api.de/api/interpreter"

    # Load the query from the provided file
    with open(query_file_path, 'r') as query_file:
        query = query_file.read() 

    # Send the POST request
    response = requests.post(endpoint, data={'data': query})

    # Ensure the request was successful
    response.raise_for_status()

    # Load the response JSON
    result = response.json()

    # Save the JSON to the specified output file
    with open(output_file_path, 'w') as output_file:
        json.dump(result, output_file, indent=2)

    print(f"Data saved to {output_file_path}")
