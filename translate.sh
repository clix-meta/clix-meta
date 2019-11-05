python jsonFlat2Hierarchial.py translationRules.json < climate_indices_CV22.json > climate_indices_CV22_DEF.json 2>errors.txt
python listMissingItems.py < climate_indices_CV22_DEF.json > climate_indices_CV22_DEF_missing.txt
