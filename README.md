## Overview ##

The aim of this repository is to provide a platform for thinking about, and developing, an unified view of metadata required to describe
climate indices (aka climate indicators). To facilitate data exchange and dissemination the metadata should, as far as possible, follow 
[Climate and Forecasting [CF] Convention](http://cfconventions.org/). Considering the very rich and diverse flora of climate indices this is 
however not always possible. 

This repository is in active development, and the content will frequently change. 

Currently it contains a LibreOffice Calc file, **master_table.fods**, containing several sheets.

The sheets are as follows:

* **index_table**  ---  the main table holding the metadata for the individual indices. Most of the indices developed by the 
[ETCCDI](https://www.wcrp-climate.org/etccdi) and [ET-SCI](https://climpact-sci.org/about/project/) are included, as are the ones 
produced by [ECA&D](https://www.ecad.eu/indicesextremes/index.php). However, some of the more complex indices remain to be included. 

* **variables**  ---  specification of input variables (following CMIP5/6 and CORDEX rules. This table also gives common aliases for the variable names.

* **index_functions**  ---  some details related to code snippets (external) for calculation of the indices.

* **ECA&D**  ---  list of indices produced by ECA&D. Many of these are already covered by exitisng entries in the *index_table*.

