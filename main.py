from filemanager import FileManager
from reconstructor import Reconstructor
import sys
from os import path
import argparse
from steps import Steps, MatchingStrategy


class DataStore:
    recursive = False
    root_path = ""
    ini_path = ""
    steps = "111111"
    matching_strategy = ""


def StartReconstruction(datastore):
    reconstructor = Reconstructor()
    project_ini = reconstructor.load_project_ini(path.realpath(datastore.ini_path))
    reconstructor.project_ini = project_ini

    rp = path.realpath(datastore.root_path)
    if datastore.recursive == True:
        filemanager = FileManager(rp)
    else:
        filemanager = [rp]

    for cnt, rel_path in enumerate(filemanager):
        current_project_path = path.join(datastore.root_path, rel_path) if datastore.root_path != "./" else "./"
        reconstructor.root_dir = current_project_path
        print("#" + (cnt + 1).__str__() + "# " + "Working on " + current_project_path)
        print(datastore.steps)
	steps = Steps.fromBinaryString(datastore.steps)

        if Steps.matcher in steps :
            matcher_index = steps.index(Steps.matcher)
            steps[matcher_index].matching_strategy = MatchingStrategy[datastore.matching_strategy]

        [reconstructor.execute_step(s) for s in steps]

        # reconstructor.execute_step("feature_extractor")
        # reconstructor.execute_step("exhaustive_matcher")
        # reconstructor.execute_step("mapper")
        # reconstructor.execute_step("image_undistorter")
        # reconstructor.execute_step("dense_stereo")
        # reconstructor.execute_step("dense_fuser")
        # reconstructor.create_statistics()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstructor Script for Colmap. Multi-Folder & Init-Parsing",
                                     add_help=True)
    parser.add_argument('--recursive', action="store_true", default=False, dest="recursive",
                        help="Start the Reconstruction of all valid folder inside a directory")
    parser.add_argument('--path', action="store", dest="root_path", help="The path to the input folder", default="./")
    parser.add_argument('--ini_path', action="store", dest="ini_path",
                        help="Path to a valid ini file",
                        default=path.join(path.dirname(path.realpath(__file__)), "settings", "default.ini"))

    parser.add_argument('--steps', action="store", dest="steps",
                        help="Steps that you want to execute. Binary repesentation: 1111111 is default",
                        default="1111111")

    parser.add_argument('--matching', action="store", dest="matching_strategy",
                        help="Strategy for matching: sequential, exhaustive. Default = exhaustive_matcher",
                        default="exhaustive_matcher")

    datastore = DataStore()
    datastore.__dict__ = parser.parse_args().__dict__
    StartReconstruction(datastore)
