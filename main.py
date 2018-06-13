from filemanager import FileManager
from reconstructor import Reconstructor
import sys
from os import path

#stuff
skip_folder = []

root_dir = sys.argv[1] if len(sys.argv) >= 1 and path.exists(sys.argv[1]) else "./"
ini_dir = sys.argv[2] if len(sys.argv) >= 2 and path.exists(sys.argv[2]) else path.join(root_dir, "project.ini")
project_folder = "./"
print(root_dir)

def main():
    rec = Reconstructor()
    # fm  = FileManager()

    rec.project_ini = rec.load_project_ini(ini_dir)

    ##load all stuff...



    #PRE CONDITIONS
    current_project_path = path.join(root_dir, project_folder)
    rec.root_dir = current_project_path

    print("currently working on " + current_project_path)

    # ext_conf["database_path"] = path.join(current_project_path,database_name)
    # ext_conf["image_path"] = path.join(current_project_path,image_folder_name)
    rec.execute_step("feature_extractor")
    rec.execute_step("exhaustive_matcher")
    rec.execute_step("mapper")
    rec.execute_step("image_undistorter")
    rec.execute_step("dense_stereo")
    rec.execute_step("dense_fuser")
    rec.create_statistics()



if __name__ == "__main__": main()
