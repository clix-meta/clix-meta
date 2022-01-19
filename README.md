# Overview

This repository aims to provide a platform for thinking about,
and developing, a unified view of metadata elements required to
describe climate indices (aka climate indicators).

Currently, the main component is the spreadsheet file, **master_table.xls**,
that contains several tables as separate sheets. The *.xls* format should
[hopefully] be readable/editable by several common desktop office programs.

The repository also contains a small python package that can convert the
spreadsheet into a set of equivalent [yaml](https://yaml.org/) files that are
better suited for automatic processing. For more information about the python
program, take a look at the `python` sub-directory.

# Contributing

We encourage contributions via discussions in issues. If you have a suggestion
for the improvement of the metadata or the distribution of this work, please
have a look at [the issues](https://github.com/clix-meta/clix-meta/issues).
To help you starting a new issue there are three issue templates:

* **Request new climate index** --- this template is divided into two parts,
one for a general description of the new index, and one part for more precisely
specifying entries in the `index_definition` speadsheet (see below). There
is no need to complete all parts, just fill out those parts that you feel are
relevant for your proposal.
* **Correction to index definition** --- this template specifically
refers to the `index_definition` spreadsheet (see below). Here we would like
you to specify which table entries are wrong and how they should be changed.
* **General issue** --- any other issue, question or discussion.
 
Don't hesitate to open a new one to initiate a discussion on any question or
topic related to this effort!

# Download

Standard github and git approaches apply when using the green button "Code"
(above right), which does not include yaml files of the tables. To the right,
under the heading "[Releases](https://github.com/clix-meta/clix-meta/releases)"
packaged versions of the repository are available as compressed files.
These include yaml files that are up-to-date with the corresponding tables of
the spreadsheet file. The compressed files are available both for MS-DOS/Windows
line endings (`.zip`) and Linux line endings (`.gz`).

# Approach

To facilitate data exchange and dissemination the metadata should,
as far as possible, follow the
[Climate and Forecasting (CF) Conventions](http://cfconventions.org/).
Considering the very rich and diverse flora of climate indices this
is however not always possible. By collecting a wide range of
different indices it is easier to discover any common patterns and
features that are currently not well covered by the CF Conventions.

A more detailed overview of the approach towards structuring the climate index
metadata is available in this [IS-ENES3](https://is.enes.org/) technical
report [Milestone M10.3](https://is.enes.org/documents/milestones/climate-indicators-indicesand-file-metadata-specifications-and-tools/view)

Currently identified issues frequently relate to
[`standard_name`](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#standard-name)
or/and [`cell_methods`](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#cell-methods)
which both are *controlled vocabularies* of the CF Conventions.

This repository is in active development, and the content will frequently
change.

# File Format and Contents

## Spreadsheet

The metadata is contained in the spreadsheet file `master_table.xls` and its
sheets are as follows:

* **README** --- explains contents and formatting of the spreadsheet file itself.

* **index_definitions**  ---  the main table holding the metadata for the
  individual indices. Most of the indices developed by the
  [ETCCDI](https://www.wcrp-climate.org/etccdi) and [ET-SCI](https://climpact-sci.org/about/project/)
  are included, as are the ones produced by
  [ECA&D](https://www.ecad.eu/indicesextremes/index.php).
  However, some of the more complex indices remain to be included.

* **variables**  ---  specification of input variables (following CMIP5/6 and
  CORDEX rules). This sheet also gives common aliases for the variable names.

* **index_functions**  ---  contains details about the calculation methods used
  for the indices. This is referred to in the index_definitions sheet.

* **ECA&D**  ---  list of indices produced by
  [ECA&D](https://www.ecad.eu/indicesextremes/index.php). Many of these are
  already covered by existing entries in the *index_table* sheet.

## Yaml Files

The spreadsheets can be converted to a set of yaml files using the python
package found in this repository. These are automatically generated and
distributed alongside the spreadsheet in the metadata distributions linked to
above.

The purpose of the yaml files is to give the same information as in the
spreadsheet in a format that allows for a richer, hierarchical structure that
also lends itself better to automatic processing. The downside is, that this
makes it slightly more difficult to get a quick overview of all the available
information.

At the moment only the **index_definitions** and **variables** sheets of the
spreadsheet file are transformed into the corresponding `index_definitions.yml`
and `variables.yml` files.
The **README** sheet, insofar it gives information beyond the present document,
only applies to the spreadsheet. The **ECA&D** sheet mainly exists to track the
open indices of that collection until they are fully integrated into the main
table **index_definitions**. Consequently, those two sheets are not likely to be
converted in the future.
The **index_functions** sheet will be added to the yaml files in the future.

# Acknowledgement

This work is supported by the European project [IS-ENES3](https://is.enes.org/)
and by [SMHI Rossby Centre](https://www.smhi.se/en/research/research-departments/climate-research-rossby-centre2-552).


# License

**CF-index-meta** (c) 2020-2021 by *Lars Bärring* and *Klaus Zimmermann*, Rossby
Centre, Swedish Meteorological and Hydrological Institute (SMHI).

![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png) The spreadsheet and all
the metadata therein is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.
