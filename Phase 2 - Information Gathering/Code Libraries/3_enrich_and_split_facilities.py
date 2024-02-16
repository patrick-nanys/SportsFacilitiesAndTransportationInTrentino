import pandas as pd
import pathlib
import json
from pprint import pprint
import os

if __name__ == '__main__':
    datasets_folder = pathlib.Path(__file__).parent.parent.parent.parent.resolve() / 'datasets'
    sports_facilities_directory = datasets_folder / 'formal' / 'sports_facilities'
    merged_path = sports_facilities_directory / 'merged_facilities.json'

    # Step 1: Read the json data and convert it to a DataFrame
    with open(merged_path, 'r') as input_file:
        json_data = json.load(input_file)

    # Converting JSON data to a DataFrame
    # Extract properties and add 'type' and 'id' from the main dictionary
    df_data = []
    for feature in json_data:
        properties = feature["properties"]
        properties["type"] = feature["type"]
        properties["id"] = feature["id"]
        df_data.append(properties)

    # Creating the DataFrame
    data = pd.DataFrame(df_data)

    # Step 2: Identify and remove columns where the number of non-NaN values is exactly 1
    columns_with_single_non_nan = data.columns[data.notna().sum() == 1].tolist()
    data_cleaned = data.drop(columns=columns_with_single_non_nan)

    # Step 3: Drop cases where 'leisure' is NaN, 'sport' is 'climbing', and 'building' is 'yes'
    data_filtered = data_cleaned.drop(data_cleaned[
        (data_cleaned['leisure'].isna()) & 
        (data_cleaned['sport'] == 'climbing') & 
        (data_cleaned['building'] == 'yes')
    ].index)

    # Step 4: Drop where leisure is NaN and sport is either athletics, fitness, volleyball, or soccer
    sports_to_drop = ['athletics', 'fitness', 'volleyball', 'soccer']
    data_filtered = data_filtered.drop(data_filtered[
        (data_filtered['leisure'].isna()) & 
        (data_filtered['sport'].isin(sports_to_drop))
    ].index)

    # Step 5: Naming cases where 'leisure' is NaN but 'sport' is 'climbing' as "Outdoor Climbing Area"
    data_filtered.loc[data_filtered['leisure'].isna() & (data_filtered['sport'] == 'climbing'), 'leisure'] = 'outdoor_climbing_area'

    # Step 6: Apply the concrete threshold filtering for each leisure category
    filtered_dataframes_final = {}
    minimum_entries_threshold = 10

    # Calculate non-NaN counts for each leisure category again
    non_nan_counts_by_leisure_final = {leisure_category: data_filtered[data_filtered['leisure'] == leisure_category].notna().sum() 
                                        for leisure_category in data_filtered['leisure'].unique()}

    # Apply the concrete number threshold for each leisure category
    for leisure_category, counts in non_nan_counts_by_leisure_final.items():
        # Filter the dataset for the current leisure category 
        category_data = data_filtered[data_filtered['leisure'] == leisure_category]

        # total_entries = category_data.shape[0]
        # if total_entries > 10:
        #     columns_to_keep = counts[counts >= minimum_entries_threshold].index.tolist()
        #     filtered_dataframes_final[leisure_category] = category_data[columns_to_keep]
        # else:
        #     category_data_no_nan = category_data.dropna(axis=1, how='all')
        #     filtered_dataframes_final[leisure_category] = category_data_no_nan

        category_data = category_data.dropna(axis=1, how='all')
        columns_to_keep = ["leisure", "name", "lon", "lat", "id", "surface"]
        if leisure_category == "fitness_centre" or leisure_category == "sports_centre":
            columns_to_keep.extend(["opening_hours"])
        final_columns = [col for col in category_data.columns if col in columns_to_keep]
        filtered_dataframes_final[leisure_category] = category_data[final_columns]

    # Step 7: Saving the separate dataframes to separate files with tab separators
    output_file_paths = {}

    for leisure_category, df in filtered_dataframes_final.items():
        # Constructing the file name based on the leisure category
        file_name = f"{leisure_category}_data.tsv"
        save_directory = sports_facilities_directory / 'cleaned'
        save_directory.mkdir(exist_ok=True)
        file_path = save_directory / file_name

        # Saving the dataframe to a file
        df.to_csv(file_path, sep='\t', index=False, encoding="utf-8")

        # Storing the file path in the dictionary for reference
        output_file_paths[leisure_category] = str(file_path)

    print('Enriched and split files saved at:')
    pprint(output_file_paths)
