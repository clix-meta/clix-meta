# CF compliant metadata for the data variable in climate index netCDF files. #


## Overview ##

This repository contains the following components:

* The master table as a LibreOffice Calc **.fods** file.
* The master table in several alternative file formats intended to be **used as read-only**.
* Python helper scripts for transforming the 'flat' master table to a 'hierarchical' form
* Some other helper files.

---------------

## How to use this repository ##

**If you want to download and use the metadata:**

* Just download the table file that best meet your needs.

**If you want to contribute by adding or updating the master table**

* You need to have developer access to this repository (contact the admin)
* Git pull (clone the first time) the repository
* Add/change the information in the master table
* Run the macro in master table document. This creates the .csv and .json files
* Save/Export the master table to .fods, .ods, .xlsx files
* Run the python script jsonFlat2Hierarchial.py :
```python jsonFlat2Hierarchial.py translationRules.json < climate_indices_CV20.json > climate_indices_CV20_DEF.json 2>errors.txt```
* Run the python script listMissingItems.py
```python listMissingItems.py < climate_indices_CV20_DEF.json > climate_indices_CV20_DEF_missing.txt```
* Git commit all the files (the same as are in the repository)


## Files ##

**climate_indices_CV20.fods** This is the **master table** of index variable metadata as a LibreOffice spreadsheet file (flat XML format). This file contains a macro for exporting the table to 'flat' .json file (a .csv is created in an intermediate step). The resulting .csv and .json files will have the same name as the parent file (i.e. climate_indices_CV20.json, and climate_indices_CV20.csv


**climate_indices_CV20.ods** *'Read-only'* version of the master table in LibreOffice standard (zipped) binary format.

**climate_indices_CV20.xlsx** *'Read-only'* version of the master table in Excel (zipped) binary format produced by LibreOffice export. 

**climate_indices_CV20.csv** Intermediate file, produced by the LibreOffice macro.

**climate_indices_CV20.json** Flat .json representation of the master table, produced by the LibreOffice macro. 

**jsonFlat2Hierarchial.py** Python script for transforming the 'flat' .json (produced by the LibreOffice macro) file into a 'hierarchical' .json file. The transformation rules are specified in a separate .json file. Indices that cannot be parsed according to the rule set are logged to stderr. 

**translationRules.json** Definition of the rule set used by jsonFlat2Hierarchial.py

**climate_indices_CV20_DEF.json** The successfully translated indices produced by jsonFlat2Hierarchial.py

**errors.txt** The indices that could not be translated by jsonFlat2Hierarchial.py. In additon to a listing of the input .json text this file includes rudimentary error information.

**listMissingItems.py** Python script for listing empty/placeholder text in otherwise successfully translated indices. 

**climate_indices_CV20_DEF_missing.txt** List of missing/placeholder items.

