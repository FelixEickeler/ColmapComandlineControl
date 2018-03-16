from subprocess import call
import os
import sys
from os import path
from types import *
import re
from string import Template
import json



#stuff
skip_folder = []
root_dir = sys.argv[1] if 1 in sys.argv and path.exists(sys.argv[1]) else "./"
ini_dir = sys.argv[2] if 2 in sys.argv and path.exists(sys.argv[2]) else path.join(root_dir, "project.ini")


def main():
    rec = Reconstructor()
    rec.project_ini = rec.load_project_ini(ini_dir)




        #PRE CONDITIONS
        current_project_path = path.join(root_dir, project_folder)
        rec.root_dir = current_project_path

        print("currently working on " + current_project_path)

        # ext_conf["database_path"] = path.join(current_project_path,database_name)
        # ext_conf["image_path"] = path.join(current_project_path,image_folder_name)
        #rec.execute_step("feature_extractor")
        #rec.execute_step("exhaustive_matcher")
        #rec.execute_step("mapper")
        #rec.execute_step("image_undistorter")
        rec.execute_step("dense_stereo")
        rec.execute_step("dense_fuser")
        rec.create_statistics()





class Reconstructor:

    def __init__(self):
        self.project_ini = {}
        self.root_dir = "./"
        self.name = ""

    @property
    def logging_path(self):
        return self.project_ini[no_category]["log_path"] if "log_path" in self.project_ini["no_category"] else path.join(root_dir, "log")

    @logging_path.setter
    def logging_path(self, path):
        self.project_ini[no_category]["log_path"] = path

    def build_options(self, step):
        print(step)
        tconfig = {}

        if step == "feature_extractor":
            tconfig.update(self.project_ini["SiftExtraction"])
            tconfig.update(self.project_ini["ImageReader"])
            tconfig["database_path"] = Template(self.project_ini["no_category"]["no_category.database_path"]).safe_substitute(project=self.root_dir)
            tconfig["image_path"] = Template(self.project_ini["no_category"]["no_category.image_path"]).safe_substitute(project=self.root_dir)

        elif step == "exhaustive_matcher":
            tconfig.update(self.project_ini["SiftMatching"])
            tconfig.update(self.project_ini["ExhaustiveMatching"])
            tconfig["database_path"] = Template(self.project_ini["no_category"]["no_category.database_path"]).safe_substitute(project=self.root_dir)

        elif step == "mapper":
            tconfig.update(self.project_ini["Mapper"])
            tconfig["export_path"] = Template(self.project_ini["no_category"]["no_category.export_path"]).safe_substitute(project=self.root_dir)
            tconfig["database_path"] = Template(self.project_ini["no_category"]["no_category.database_path"]).safe_substitute(project=self.root_dir)
            tconfig["image_path"] = Template(self.project_ini["no_category"]["no_category.image_path"]).safe_substitute(project=self.root_dir)
            call(["mkdir", tconfig["export_path"]])

        elif step == "image_undistorter":#
            tconfig["input_path"] = Template(self.project_ini["no_category"]["no_category.export_path"]).safe_substitute(project=self.root_dir)
            tconfig["input_path"] = path.join(tconfig["input_path"], "0")
            tconfig["output_path"] = Template(self.project_ini["no_category"]["no_category.output_path"]).safe_substitute(project=self.root_dir)
            tconfig["image_path"] = Template(self.project_ini["no_category"]["no_category.image_path"]).safe_substitute(project=self.root_dir)
            call(["mkdir", tconfig["output_path"]])

        elif step == "dense_stereo":  #
            tconfig.update(self.project_ini["DenseStereo"])
            tconfig["workspace_path"] = Template(self.project_ini["no_category"]["no_category.output_path"]).safe_substitute(project=self.root_dir)
            #tconfig["output_path"] = path.join( tconfig["output_path"] ,"0")root_dir

        elif step == "dense_fuser":  #
            tconfig.update(self.project_ini["DenseFusion"])
            tconfig["workspace_path"] = Template(self.project_ini["no_category"]["no_category.output_path"]).safe_substitute(project=self.root_dir)
            tconfig["output_path"] = path.join(Template(self.project_ini["no_category"]["no_category.output_path"]).safe_substitute(project=self.root_dir), "fused.ply")
        else:
            return None

        #add path because will only read if valid
        options = ["colmap", step]
        for key, arg in tconfig.items():
            options +=["--" + key, str(arg)]
        return options

    def execute_step(self, step):
        options = self.build_options(step)
        if options:
            logging_path = self.logging_path
            if not path.exists(logging_path):
                call(["mkdir", logging_path])

            # print ("\n\n\n##################################")
            # for i in range(0, len(options),2):
            #     print(options[i] + " = " + options[i+1])
            #
            # print ("##################################\n\n\n")
            with open(path.join(logging_path, step), "wb") as log:
                call(options, stdout=log)
        else:
            raise Exception("Wrong Argument!")

    def create_statistics(self):
        with open(path.join(self.root_dir, 'project_configuration.json'), 'w') as outfile:
            json.dump(data, outfile,  ensure_ascii=False)
        if path.exists(path.join(self.root_dir, "sparse", "0")):
            with open(path.join(self.root_dir, self.name + "_" + "statistics.json"), 'w') as outfile:
                call(["colmap", "model_analyzer", "project_path", path.join(self.root_dir, "sparse", "0")], stdout=outfile)

    @staticmethod
    def load_project_ini(file_path):
        #regex = r"^\[\w+[\],\s]$"
        regex = r"\[(\w+)\]"
        config = {"no_category":{}}
        current = "no_category"

        with open(file_path,"r") as project_ini:
            for line in project_ini:
                matches = re.search(regex, line)
                if matches:
                    current = matches.groups()[0]
                    config[current] = {}
                else:
                    arg, value = line.replace(" ", "").rstrip().split("=",1)
                    if value == "true":
                        value = "1"
                    elif value == "false":
                        value = "0"
                    elif value == "":
                        continue

                    config[current][current + "." + arg] = value
            return config


if __name__ == "__main__": main()
