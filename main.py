from filemanager import FileManager
from reconstructor import Reconstructor
import sys
from os import path
import argparse
from steps import Steps


class DataStore:
    recursive = False
    root_path = ""
    ini_path = ""


def StartReconstruction(datastore):
    reconstructor = Reconstructor()
    project_ini = reconstructor.load_project_ini(datastore.ini_path)
    reconstructor.project_ini = project_ini

    if datastore.recursive == true:
        filemanager = FileManager(datastore.root_path)
    else:
        filemanager = ["./"]

    for rel_path in filemanager:
        current_project_path = path.join(datastore.root_path, rel_path)
        rec.root_dir = current_project_path
        print("Currently working on " + current_project_path)
        reconstructor.execute_step("feature_extractor")
        reconstructor.execute_step("exhaustive_matcher")
        reconstructor.execute_step("mapper")
        reconstructor.execute_step("image_undistorter")
        reconstructor.execute_step("dense_stereo")
        reconstructor.execute_step("dense_fuser")
        reconstructor.create_statistics()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstructor Script for Colmap. Multi-Folder & Init-Parsing",
                                     add_help=True)
    parser.add_argument('--recursive', action="store_true", default=False, dest="recursive",
                        help="Start the Reconstruction of all valid folder inside a directory")
    parser.add_argument('--path', action="store", dest="root_path", help="The path to the input folder", default="./")
    parser.add_argument('--ini_path', action="store", dest="ini_path",
                        help="Path to a valid ini file",
                        default=path.join(path.dirname(path.realpath(__file__)), "default", "project.ini"))

    parser.add_argument('--path', action="store", dest="steps", help="Steps that you want to execute. "
                                                                     "Binary repesentation: 111111 is default",
                        default="111111")

    datastore = DataStore()
    datastore.__dict__ = parser.parse_args().__dict__
    datastore.steps = int(datastore.steps, 2)
    StartReconstruction(datastore)
