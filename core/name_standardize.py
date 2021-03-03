# Extract files from LearnUs assignment compilation zip file.
# author: Hanju Yoo (hanju.yoo@yonsei.ac.kr)
# version: 1.0.0 (2021-03-03)

import os
import zipfile
import re

class StudentInfo:
    def __init__(self, stu_name, stu_id):
        self.stu_name = stu_name
        self.stu_id = stu_id

class Extractor:
    def __init__(self, source:str, workdir:str):
        '''
        source: str = directory path of zip file from LearnUs
        to: str = work directory
        source zip structure:

        source.zip
          ㄴSTUDENTNAME-STUDENTNO_SUBMISSIONNO_assignsubmission_file_
            ㄴsubmitted_filename.zip

        This extractor considers three types of submission:
        A. SUBMISSION_FOLDER/FILENAME.zip
        B. SUBMISSION_FOLDER/PYTHON_FILE.py(s)
        C. SUBMISSION_FOLDER/FILENAME (no extensions)
            - checks if it could be decoded with UTF-8
            - otherwise, print error
        '''
        if not os.path.isfile(source):
            raise FileNotFoundError(f"{source} not found")

        self.source = source
        self.workdir = workdir

    def run(self):
        # root zip extraction
        self.extract_zip(self.source, self.workdir)
        print(f'info: workdir is {os.path.abspath(self.workdir)}')

        # folder rename
        files = os.listdir(self.workdir)
        for directory in files:
            if os.path.isdir(f'{self.workdir}/{directory}'):
                stu_name, stu_id = self.get_info_from_submission(directory)
                if not stu_name:
                    continue

                student = StudentInfo(stu_name, stu_id)
                self.process_submission(f'{self.workdir}/{directory}', student)
            else:
                print(f'warning: {directory} is not a directory')


    def process_submission(self, dir:str, student:StudentInfo):
        files = os.listdir(dir)

        # Extract all .zips
        for file in files:
            _, ext = os.path.splitext(file)
            if ext == '.zip':
                self.extract_zip(f'{dir}/{file}', dir)

        # C. SUBMISSION_FOLDER/FILENAME (no extensions)
        #    - checks if it could be decoded with UTF-8
        #    - otherwise, print error
        submissions = os.listdir(dir)
        for file in submissions:
            file = f'{dir}/{file}'
            try:
                _, filename_w_ext = os.path.split(file)
                filename, ext = os.path.splitext(filename_w_ext)
                if ext == '.zip':
                    continue
                elif os.path.isdir(file):
                    subdir = file
                    parentdir = os.path.dirname(subdir)
                    for subfile in os.listdir(subdir):
                        os.rename(f'{subdir}/{subfile}', f'{parentdir}/{subfile}')
                    os.rmdir(file)
                elif ext == '':
                    try:
                        f = open(file, encoding='utf-8')
                        f.close()
                    except UnicodeDecodeError:
                        print(f'warning: invalid py file {file}')
                        continue
                
                # file name normalization
                if len(filename) > 1 and filename[0] == 'p' and \
                filename[1:].isdigit() and ext == '.py':
                    pass
                else:
                    problem_no_lst = re.findall(r'\d+', filename)
                    if problem_no_lst:
                        os.rename(file, f'{dir}/p{problem_no_lst[0]}.py')
                    else:
                        print(f'warning: invalid file name {file}')
            except Exception as e:
                print(f'error: something went wrong on {file}')
                print(e)
                continue
        
        
        # folder name normalization
        base_dir, _ = os.path.split(dir)
        os.rename(dir, f'{base_dir}/{student.stu_id}')
        

    def get_info_from_submission(self, filename):
        # STUDENT_NAME-STUDENT_NO-SUBMISSION_NO-assignsubmission_file_
        try:
            stu_name, stu_id = filename.split('_')[0].split('-')
        except:
            print(f'error: invalid submission folder {filename}')
            return None, None

        return stu_name, stu_id

    def extract_zip(self, source:str, to:str):
        zip = zipfile.ZipFile(source)
        zip.extractall(to)
        zip.close()
    
