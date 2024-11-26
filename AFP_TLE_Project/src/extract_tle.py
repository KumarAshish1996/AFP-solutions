import afp
import pandas as pd
import os
def extract_tle_from_afp(file_path, max_tle_count=None):
    # Open the AFP file
    with open(file_path, 'rb') as afp_file:
        # Parse the AFP file using stream
        afp_document = afp.stream(afp_file, allow_unknown_fields=True, allow_unknown_triplets=True, allow_unknown_functions=True, strict=False)

        data = []

        for i, page in enumerate(afp_document):
            for key, value in page.items():
                if key == 'Triplets' and len(value) > 1:
                    triplet_value = value
                    for triplet_content in triplet_value:
                        if 'FQName' in triplet_content:
                            fq_name = triplet_content['FQName']
                            next_index = triplet_value.index(triplet_content) + 1
                            if next_index < len(triplet_value) and 'AttVal' in triplet_value[next_index]:
                                att_val = triplet_value[next_index]['AttVal']
                                data.append({'FQName': fq_name, 'AttVal': att_val})
                                if max_tle_count is not None and len(data) >= max_tle_count:
                                    break
                    if max_tle_count is not None and len(data) >= max_tle_count:
                        break
            if max_tle_count is not None and len(data) >= max_tle_count:
                break

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    output_file_path = os.path.join(os.path.dirname(file_path), f'{os.path.splitext(os.path.basename(file_path))[0]}.xlsx')
    df.to_excel(output_file_path, index=False)
    return output_file_path