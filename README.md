# rm_missing_data_from_dist_mat

A Python Command Line Tool to remove missing data values from a genetic distance matrix.

---------------
### Installation and running the tool

Option 1: Use [pyinstaller](https://pyinstaller.org/en/stable/) to create a usable package without the need of a Python interpreter and run the tool in your terminal by typing ```./rm_missing_data_from_dist_mat```.

Option 2: Run the tool in your terminal with Python installed by typing ```python ./rm_missing_data_from_dist_mat```.

---------------
### Usage
```
positional arguments:
  dst               path to input tab-delimited distance matrix (usually .dst) file

options:
  -h, --help        show this help message and exit
  -o , --out        output path and name. Default in current directory.
  -n , --na_value   String that is used to represent missing data in the input distance matrix. Default: "nan " (nei_vcf output)
  -v, --version     show program's version number and exit
```
