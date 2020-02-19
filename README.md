## Overview ##

This repository aims to provide a platform for thinking about, and developing, a unified view of metadata elements required to describe
climate indices (aka climate indicators). 

To facilitate data exchange and dissemination the metadata should, as far as possible, follow 
[Climate and Forecasting [CF] Conventions](http://cfconventions.org/). Considering the very rich and diverse flora of climate indices this is 
however not always possible. By collecting a wide range of different indices it is easier to discover any common patterns and features that 
is currently not covered by the CF Conventions. Currently identified issues frequently relate to `standard_name` and `cell_methods` which both 
are *controlled vocabularies* in the CF Conventions.

This repository is in active development, and the content will frequently change. 

Currently it contains a LibreOffice Calc file, **master_table.fods**, containing several sheets.

The sheets are as follows:

* **index_table**  ---  the main table holding the metadata for the individual indices. Most of the indices developed by the 
[ETCCDI](https://www.wcrp-climate.org/etccdi) and [ET-SCI](https://climpact-sci.org/about/project/) are included, as are the ones 
produced by [ECA&D](https://www.ecad.eu/indicesextremes/index.php). However, some of the more complex indices remain to be included. 

* **variables**  ---  specification of input variables (following CMIP5/6 and CORDEX rules). This sheet also gives common aliases for the variable names.

* **index_functions**  ---  some details related to code snippets (external) for calculation of the indices.

* **ECA&D**  ---  list of indices produced by [ECA&D](https://www.ecad.eu/indicesextremes/index.php). Many of these are already covered by existing entries in the *index_table* sheet.



This work is supported by European project [IS-ENES3](https://is.enes.org/) and [SMHI Rossby Centre](https://www.smhi.se/en/research/research-departments/climate-research-rossby-centre2-552)
