python jsonFlat2Hierarchial.py translationRules.json < climate_indices_CV20.json > climate_indices_CV20_DEF.json 2>errors.txt
python listMissingItems.py < climate_indices_CV20_DEF.json > climate_indices_CV20_DEF_missing.txt
