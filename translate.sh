python jsonFlat2Hierarchial.py translationRules.json < climate_indices_CV21.json > climate_indices_CV21_DEF.json 2>errors.txt
python listMissingItems.py < climate_indices_CV21_DEF.json > climate_indices_CV21_DEF_missing.txt
