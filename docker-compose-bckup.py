"""
Python Script for backing up a set of files to a Git repo.

Currently configured to find all my docker-compose files
"""

import shutil
import datetime
from os import chdir, environ
from git import Repo

from pathlib import Path

BACKUP_DIR = Path(environ.get('DATA_DIR'))
SEARCH_DIR = Path(environ.get('SEARCH_DIR', '/')) 
SEARCH_FILE = 'docker-compose.yml'
COMMIT_MSG = f'Backup {datetime.datetime.now()}'


def get_file_name(file: Path) -> str:
    return str(file.relative_to(SEARCH_DIR)).replace('/', '-')

def copy(files: list[Path]) -> None:
    for file in files:
        print('Moving file:', file)
        shutil.copyfile(file, BACKUP_DIR / get_file_name(file))


def commit() -> list:
    chdir(BACKUP_DIR)
    repo = Repo(BACKUP_DIR)
    repo.git.add(A=True)
    if repo.is_dirty(untracked_files=True):
        repo.index.commit(COMMIT_MSG)
        origin = repo.remote(name='origin')
        return origin.push()

def main():
    file_paths: list[Path] = [file for file in SEARCH_DIR.rglob(SEARCH_FILE) if file.is_file()]
    copy(file_paths)
    results = commit()
    print(results)
        
if __name__ == '__main__':
    main()

