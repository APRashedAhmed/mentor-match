# Mentor Match

Script that outputs the percent positive matches between multiple columns
in one csv and multiple columns in another.

## Setup

Create the conda environment required to run everything:

	$ conda env create --file environment.yml
	
And then activate the environment:

	$ conda activate match
	
## Usage

Place the mentor and mentee data in the `data` folder, and then run the script:

	$ python match.py
	
The results will be outputted to a file in the `data` directory and named 
according to the default or passed output name.
	
If you need to change the columns that are used to compare, or the names of the
files, pass the desired values as options according to the following:

```
usage: match.py [-h] [--ipdb] [--mentee_columns MENTEE_COLUMNS [MENTEE_COLUMNS ...]] [--mentor_columns MENTOR_COLUMNS [MENTOR_COLUMNS ...]] [--mentee_csv MENTEE_CSV] [--mentor_csv MENTOR_CSV]
                [--output_name OUTPUT_NAME] [--ipy]

optional arguments:
  -h, --help            show this help message and exit
  --ipdb                Starts ipdb if there is an error (default: False)
  --mentee_columns MENTEE_COLUMNS [MENTEE_COLUMNS ...]
                        Index of columns to use in the mentee csv (default: [6, 7, 8])
  --mentor_columns MENTOR_COLUMNS [MENTOR_COLUMNS ...]
                        Index of columns to use in the mentee csv (default: [3, 4, 5])
  --mentee_csv MENTEE_CSV
                        Base name of the student csv (default: Student Sign Up Form (Responses))
  --mentor_csv MENTOR_CSV
                        Base name of the mentor csv (default: Mentor matching survey (Responses))
  --output_name OUTPUT_NAME
                        Name of the file to dump results into (default: mentor_similarities)
  --ipy                 Start an IPython shell at the end of the script (default: False)
```

This help command will also appear if you run:

	$ python match.py --help
