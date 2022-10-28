"""
rm_missing_data_from_dist_matrix.py
CLI tool to parsimonially remove samples with missing data 
from a distance matrix.
"""

__version__ = '0.1'
__author__ = 'Marco Dorfner'
__email__ = 'marco.dorfner@ur.de'
__date__ = '2022-10-26'


import argparse
import pandas as pd
import os


class rm_missing_data_from_dist_matrix:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog = 'rm_missing_data_from_dist_matrix.py',
            description = 'CLI tool to parsimonially remove samples with missing data from a distance matrix'
        )
        self.CLI()
        self.args = self.parser.parse_args()

        self.run()

    def CLI(self):
        self.parser.add_argument(
            'dst',
            type = str,
            help = 'path to input tab-delimited distance matrix (usually .dst) file'
        )

        self.parser.add_argument(
            '-o', '--out',
            metavar = '',
            type = str,
            default = os.path.join(os.path.abspath(os.getcwd()), 'filtered_dist_mat.dst'),
            help = 'output path and name. Default in current directory.'
        )

        self.parser.add_argument(
            '-n', '--na_value',
            metavar = '',
            type = str,
            default = 'nan     ',
            help = 'String that is used to represent missing data in the input distance matrix. Default: "nan     " (nei_vcf output)'
        )

        self.parser.add_argument(
            '-v', '--version',
            action = 'version',
            version = __version__
        )

    def count_missing_data(self, df, na_value):
        '''Counts missing data occurence for each sample, row by row.
        Stored as a dict: key = row index, value = missing data occurence.
        df: pandas dataframe of infile distance matrix.
        na_value: String of the value that represents missing data in dist mat.
        '''

        missing_data = dict()

        for row in df.iterrows():
            NaN_count = row[1].iloc[1:].tolist().count(na_value)
            row_idx = row[0]

            missing_data[row_idx] = NaN_count

        return missing_data

    def rm_sample_with_most_missing_data(self, missing_data, df):
        '''Removes the sample with the most missing data and its
        corresponding columns from the infile distance matrix,
        one by one Until It's Done.
        Returns the dist mat as a pandas dataframe without missing data.
        missing_data: dict returned by "count_missing_data()".
        df: headerless pandas dataframe of the input distance matrix.'''

        while any(missing_data.values()):
            missing_data = self.count_missing_data(df, na_value = self.args.na_value)
            sample_with_most_missing_data = max(missing_data, key = missing_data.get)

            if missing_data[sample_with_most_missing_data] == 0:
                break  # stop when there is no missing data left

            print('Remove row index {} with {} missing data'.format(
                sample_with_most_missing_data, 
                missing_data[sample_with_most_missing_data]
                )
            )
            df = df.drop(labels = sample_with_most_missing_data, axis = 0)
            df = df.drop(labels = sample_with_most_missing_data+1, axis = 1)

        return df

    def write_to_file(self, df):
        '''Writes the filtered distance matrix to outfile.
        df: pandas dataframe returned by rm_sample_with_most_missing_data().'''
        
        df_no_header = self.args.dst + '_edit.dst'
        df.to_csv(df_no_header, index = False, header = False, sep = '\t')
        if os.path.exists(self.args.out):
            os.remove(self.args.out)
        with open(self.args.out, 'x') as outfile:
            outfile.write('{}\n'.format(str(len(df))))
            with open(df_no_header) as infile:
                for line in infile:
                    outfile.write(line)
        os.remove(df_no_header)
    
    def run(self):
        'main function'

        df = pd.read_csv(
            self.args.dst, 
            sep = '\t',
            skiprows = 1,
            header = None
        )

        missing_data = self.count_missing_data(
            df = df,
            na_value = self.args.na_value
        )

        df_no_missing_data = self.rm_sample_with_most_missing_data(missing_data, df)
        self.write_to_file(df_no_missing_data)


def main():
    rm_missing_data_from_dist_matrix()

if __name__ == "__main__":  
    main()
