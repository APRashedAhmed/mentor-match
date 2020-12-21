"""Script to output the matches"""
import re
import argparse
from pathlib import Path

import pandas as pd

def pd_load(path, index_col=0, *args, **kwargs):
    path = Path(path)
    if path.suffix in ('.xls', '.xlsx', '.xlsm'):
        return pd.read_excel(path, index_col=index_col, *args, **kwargs)
    elif path.suffix == '.csv':
        return pd.read_csv(path, index_col=index_col, *args, **kwargs)
        
def main(args):
    # Get the data csvs
    dir_file = Path(__file__).resolve().parent # Where are we
    dir_data = dir_file / 'data'               # Data dir

    # Most recently downloaded files
    df_mentee = pd_load(list(dir_data.glob(f'*{args.mentee_csv}*'))[0])
    df_mentor = pd_load(list(dir_data.glob(f'*{args.mentor_csv}*'))[0])
    
    # Turn columns into ints
    args.mentee_columns = [int(c) for c in args.mentee_columns]
    args.mentor_columns = [int(c) for c in args.mentor_columns]

    # Get the names of the relevant columns
    columns_mentee = list(df_mentee.columns[args.mentee_columns])
    columns_mentor = list(df_mentor.columns[args.mentor_columns])

    # Turn NaNs into empty strs
    df_mentee[columns_mentee] = df_mentee[columns_mentee].fillna('')
    df_mentor[columns_mentor] = df_mentor[columns_mentor].fillna('')

    # Define a join func
    join = lambda series: ', '.join(filter(None, series))
    
    # Create the combinations of interests
    combined_interests_mentee = df_mentee[columns_mentee].agg(join, axis=1)
    combined_interests_mentor = df_mentor[columns_mentor].agg(join, axis=1)

    # Get the column of names
    names_mentee = df_mentee[[c for c in df_mentee.columns if 'Name' in c]]
    names_mentor = df_mentor[[c for c in df_mentor.columns if 'Name' in c]]

    # Make those easier to work with
    names_mentee = [name[0].strip() for name in names_mentee.values]
    names_mentor = [name[0].strip() for name in names_mentor.values]

    # Turn into a sets
    set_combined_interests_mentee = pd.DataFrame(
        {'Interests' : combined_interests_mentee.apply(
            lambda x: set(re.split(',|;', x))),
         'Name' : names_mentee}).reset_index(drop=True)
    set_combined_interests_mentor = pd.DataFrame(
        {'Interests' : combined_interests_mentor.apply(
            lambda x: set(re.split(',|;', x))),
         'Name' : names_mentor}).reset_index(drop=True)
    
    # Merge Interests of people who have multiple entries
    set_combined_interests_mentee = set_combined_interests_mentee.groupby(
        'Name')['Interests'].apply(
            lambda interests: set().union(*interests)).to_frame()
    set_combined_interests_mentor = set_combined_interests_mentor.groupby(
        'Name')['Interests'].apply(
            lambda interests: set().union(*interests)).to_frame()
        
    # Create a new df that will house the similarities
    df_similarities = pd.DataFrame(
        columns=[f'Rank {i+1}' for i in range(len(
            set_combined_interests_mentor))],
        index=set_combined_interests_mentee.index,
    )
    
    # Compare each mentee to every mentor and get percent overlap
    for mentee in names_mentee:
        mentee_interests = set_combined_interests_mentee.loc[
            mentee].values[0]
        # Dict of similarities
        mentor_similarity = {}
        # Loop through and compare each mentor
        for mentor in names_mentor:
            mentor_interests = set_combined_interests_mentor.loc[
                mentor].values[0]
            mentor_similarity[mentor] = (
                len(mentee_interests.intersection(mentor_interests)) /
                len(mentee_interests))

        # Sort by decreasing similarity
        mentor_similarity = {n: s for n, s in sorted(
            mentor_similarity.items(), key=lambda item: item[1], reverse=True)}

        # Add to the big dataframe
        df_similarities.loc[mentee] = [f'{name}-{similarity:.2f}'
                                       for name, similarity
                                       in mentor_similarity.items()]

    # Save things
    df_similarities.to_csv(str(dir_data / f'{args.output_name.lower()}.csv'))

    # Start ipython if desired
    if args.ipy:
        import IPython; IPython.embed()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ipdb', action='store_true',
                        help='Starts ipdb if there is an error')
    parser.add_argument('--mentee_columns', nargs='+', default=[6,7,8],
                        help='Index of columns to use in the mentee csv')
    parser.add_argument('--mentor_columns', nargs='+', default=[3,4,5],
                        help='Index of columns to use in the mentee csv')
    parser.add_argument('--mentee_csv', type=str,
                        default='Student Sign Up Form (Responses)',
                        help='Base name of the student csv')
    parser.add_argument('--mentor_csv', type=str,
                        default='Mentor matching survey (Responses)',
                        help='Base name of the mentor csv')
    parser.add_argument('--output_name', type=str,
                        default='mentor_similarities',
                        help='Name of the file to dump results into')
    parser.add_argument('--ipy', action='store_true',
                        help='Start an IPython shell at the end of the script')

    # Parse the options
    args = parser.parse_args()

    # If running with test_run or ipdb
    if args.ipdb:
        import ipdb
        with ipdb.launch_ipdb_on_exception():
            main(args)
    else:
        main(args)
    
