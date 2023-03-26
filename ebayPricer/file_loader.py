import hashlib
import os
import glob
import pandas as pd
import warnings
import openpyxl

from bson import ObjectId

from ebayPricer import data_objects


def ingest_excel_sheets():
    files = {}
    loaded = []
    ignored = []

    data_objects.clear_file_imports()

    path_name = os.path.join(os.getcwd(), "imports")
    for filename in glob.glob(os.path.join(path_name, '*.xlsx')):
        with open(filename, 'r') as f:
            warnings.simplefilter(action='ignore', category=UserWarning)
            df = pd.read_excel(io=filename, sheet_name='Comics', engine='openpyxl')
            df = df[df.filter(regex='^(?!Unnamed)').columns]
            comix = []
            for idx, row in df.iterrows():
                comic_id = ObjectId()
                df.loc[idx, 'ID'] = comic_id
                comic = {'_id': comic_id, 'graded': row['graded'], 'Grade': row['Grade'], 'publisher': row['Publisher'],
                         'series_title': row['Series Title'], 'issue_number': str(row['Issue Number']),
                         'Professional_Grader': row['Professional Grader'], 'Variant': row['Variant']}
                comix.append(comic)

            file_import = {'hash': md5(filename), 'filename': filename}
            if len(comix) > 0:
                df.to_excel(filename, sheet_name='Comics', index=False)
                data_objects.add_item_list_records(comix)
                data_objects.add_file_import(file_import)
                loaded.append(file_import)
            else:
                ignored.append(file_import)

    files['loaded'] = loaded
    files['ignored'] = ignored
    return files


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


