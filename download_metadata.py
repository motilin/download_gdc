import pandas as pd
import requests
import json
from io import StringIO

PATIENT_UUID = 'fb54458d-c373-46c2-841e-82663e13efaa'
OUTPUT_FILE = 'patient_metadata.csv'

CASES_ENDPT = 'https://api.gdc.cancer.gov/cases'
FIELDS = ['case_id', 
        'demographic.gender', 
        'demographic.year_of_birth', 
        'demographic.year_of_death', 
        'diagnoses.primary_diagnosis',
        'files.data_type',
        'files.data_format',
        'files.file_id']
filters = dict()
filters['op'] = 'in'
filters['content'] = dict()
filters['content']['field'] = 'case_id'
filters['content']['value'] = [PATIENT_UUID]
params = {
        'fields': ','.join(FIELDS),
        'filters': json.dumps(filters),
        'format': 'TSV'}
result = requests.get(CASES_ENDPT, params=params).text
text = StringIO(result)
table = pd.read_csv(text, sep='\t').T.sort_index()
print(table)
table.to_csv(OUTPUT_FILE)
