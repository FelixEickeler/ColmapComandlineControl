import shutil
from os import path

class FileManager:#

    def __init__(self, project_path, ignore_folders):
        self.project_path = project_path

    def __iter__(self):
        return self

    def next(self):
        subdirs = next(os.walk(rootdir))[1]
        for project_path in sorted(subdirs):
            fullpath = path.abspath(project_path)
            yield project_path
