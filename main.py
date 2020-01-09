# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Generate data similar to Scripts-Intent_Entity validation.xlsx
"""
import json
import random
import os
from pathlib import Path
from putput import ComboOptions, Pipeline


def main():
    """
    This function is to generate utterances for various entity types
    """
    pattern_def_folderpath = Path(__file__).parent / 'intentpatterns'

    combo_options_map = {
        'DEFAULT': ComboOptions(max_sample_size=10, with_replacement=False)
    }

    # datetime related tokens are split to make pattern building easier. When testing is performed against luis
    # days and time tokens will be remapped to datetimeV2
    dynamic_token_patterns_map = {
        'DirectionalReference': ['top right', 'left'],
    }
    random.seed(42)
    for file in os.listdir(pattern_def_folderpath):
        filepath = Path(pattern_def_folderpath, Path(file))
        pipeline = Pipeline.from_preset('LUIS',
                                        filepath,
                                        combo_options_map=combo_options_map,
                                        dynamic_token_patterns_map=dynamic_token_patterns_map)

        generator = pipeline.flow(disable_progress_bar=True)
        tests = list(generator)

        # We only want 10 tests utterance for each intent
        if len(tests) > 10:
            tests = random.sample(tests, 10)

        base = os.path.splitext(file)[0]
        jsonfilename = base + '_utterances.json'
        # Create directory if it doesn't exist
        Path('generated_json_files_for_intent').mkdir(parents=True, exist_ok=True)
        test_file = Path(__file__).parent.joinpath("generated_json_files_for_intent", jsonfilename)
        with test_file.open(mode='w', encoding='UTF-8') as file:
            json.dump(
                tests,
                file,
                indent=2,
                sort_keys=False)  # set to true before checking in tests


if __name__ == '__main__':
    main()
