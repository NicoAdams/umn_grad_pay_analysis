"""merge time samples into time series and anonymize data

Columns:
  Day Date
  Normalized Hourly Base Rate
  Salary Grade
  Minimum Hourly Rate
  Midpoint Hourly Rate
  Maximum Hourly Rate
  Compa Ratio
  Normalized Annual Base Salary
  Calculated Annual P12
  Calculated Annual P10
  Calculated Annual P09
  Emplid
  Employee Record Number
  Job Code - Job Title
  Job Code Start Date
  Years in Job Code
  University Start Date
  Years at the University
  Last Name
  First Name
  Paygroup
  Empl Class
  Standard Hours
  College/Admin Unit
  ZDeptID
  Department
"""

import csv

def extract_single(in_fn, out_f, columns, manip) :
    """Extract input columns from input file and write rows to output file

    No header line is written.

    Parameters
    ----------
    in_fn : str
        input file name
    out_f : csv.writer
        output file open and writing to
    columns : list[str]
        list of columns to extract
    manip : dict
        if a column name is in this dict, apply the value of that key to the column value
        before writing to output file
    """

    with open(fn) as f :
        r = csv.DictReader(f)
        for row in r :
            out_f.writerow([manip.get(c,lambda x : return x)(row[c]) for c in columns])


def main(file_list, 
        output_file = 'merged_data.csv', 
        columns = ['Day Date','Normalized Hourly Base Rate', 'Job Code - Job Title']) :
    with open(output_file,'w',newline='') as out_file :
        out_f = csv.writer(out_file)
        out_f.writerow(columns)
        for f in file_list :
            extract_single(f, out_f, columns, {})

    return 0

if __name__ == '__main__' :
    import sys
    sys.exit(main(sys.argv))
