import pandas as pd


if __name__ == '__main__':

    # Read the CSV file
    df = pd.read_csv("../Phase 3 - Language Definition/concept_mapping.csv")
    # Define a function to replace old values with new values
    def replace_values(text):
        for new_value, old_value in df.itertuples(index=False):
            text = text.replace(old_value, new_value)
        return text

    for f in ['ontology', 'teleology', 'teleontology']:
        with open(f'{f}.rdf', 'r') as input_file:
            text = input_file.read()

            # Replace the old values with the new values
            processed_text = replace_values(text)

            with open(f'{f}_processed.rdf', 'w') as output_file:
                output_file.write(processed_text)

