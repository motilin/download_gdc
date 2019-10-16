import json, requests, time, os, re, glob, copy
from typing import List, Any

TOKEN_FILE = './gdc-user-token.txt'
OUTPUT_DIR = './files'
FILE_ID_LIST = ['dd5046df-c55e-40c7-b1a7-62ec9f027670',
        '28164436-36d5-4a5e-8ae5-a55abc216348']

def download_files(file_id_list: list, bulk: int = 10) -> list:
    """
    :param file_id_list: list of file ids to be downloaded
    :type bulk: int
    """
    print('\nDownloading files. This may take several minutes.')
    dir_name = OUTPUT_DIR + "/" + time.strftime("%Y%m%d-%H%M%S")
    os.system("mkdir " + dir_name)
    reminder: List[Any] = copy.deepcopy(list(FILE_ID_LIST))
    while len(reminder) > bulk:
        sub_list = reminder[:bulk]
        del reminder[:bulk]
        download_bulk(sub_list, dir_name)
    download_bulk(reminder, dir_name)
    tar_gz_files = glob.glob(dir_name + "/*.tar.gz")
    for tar_gz_file in tar_gz_files:
        os.system("tar xvzf " + tar_gz_file + " -C " + dir_name)
    gz_files = glob.glob(dir_name + "/*/*.gz")
    for gz_file in gz_files:
        os.system("gunzip " + gz_file)
    files = glob.glob(dir_name + "/*/*")
    return files

def download_bulk(file_id_list: list, dir_name: str):
    """
    :param fileId_id_ist: list of file ids to be downloaded
    :type dir_name: str
    """
    with open(TOKEN_FILE) as f:
        token = str(f.read().strip())
    data_endpt = 'https://api.gdc.cancer.gov/data'
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    params = {
        "ids": file_id_list
    }
    response = requests.post(data_endpt, data=json.dumps(params), headers=headers)
    response_head_cd = response.headers["Content-Disposition"]
    file_name = re.findall("filename=(.+)", response_head_cd)[0]
    file_name = dir_name + "/" + time.strftime("%Y%m%d-%H%M%S") + "_" + file_name
    with open(file_name, "wb") as output_file:
        output_file.write(response.content)

print('file ids requested:')
print('\n'.join(FILE_ID_LIST))
files = download_files(FILE_ID_LIST)
print('\nfiles location:')
print('\n'.join(files))
