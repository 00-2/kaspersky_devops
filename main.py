import datetime
import time

import yaml
import re
import os
import shutil
path_ = "./tests/"
dir_ = os.listdir(path_)


def handle_command(rule):
    exec_ = rule["exec"]
    if len(exec_.split(" ")) == 2:
        exec_exec_, exec_path_ = exec_.split(" ")
    else:
        exec_exec_ = exec_
        exec_path_ = ''
    if rule["active"]:
        # print(rule)
        # print(rule['title'])
        (size_rule, name_rule, date_rule) = (rule["size"], rule["name"], rule["date"])
        if name_rule:
            name_rule = name_rule.replace("\ ", "").replace(" ", "").replace('\n', "")
            for template in production_templates:
                temp_name_rule = name_rule.replace("production", ".*" + template + ".*/").replace("//", "\/")
                temp_temp_name_rule = temp_name_rule
                try:
                    for test_template in test_templates:
                        temp_temp_name_rule = temp_name_rule.replace("check", test_template + ".*/").replace("//", "\/")
                        for elem in dir_:
                            try:
                                path_to_assembly = path_ + elem
                                # print(temp_temp_name_rule)
                                # print(path_to_assembly)
                                m = re.search(temp_temp_name_rule, path_to_assembly)
                                if m:
                                    if exec_ == "DELETE":
                                        if exec_path_:
                                            shutil.rmtree(exec_path_)
                                        else:
                                            shutil.rmtree(path_to_assembly)
                                    break
                                for dir in os.listdir(path_to_assembly):
                                    full_file_path = path_to_assembly + "/" + dir
                                    # print(temp_temp_name_rule)
                                    # print(full_file_path)
                                    m = re.search(temp_temp_name_rule, full_file_path)
                                    if m:
                                        if exec_ == "DELETE":
                                            if exec_path_:
                                                shutil.rmtree(exec_path_)
                                            else:
                                                shutil.rmtree(full_file_path)
                            except FileNotFoundError:
                                pass
                except FileNotFoundError:
                    break

        if date_rule:
            command = date_rule['command']
            date_string = date_rule['time_string']
            date_format = date_rule['format']
            date_c = datetime.datetime.strptime(date_string, date_format).ctime()
            try:
                for elem in dir_:
                    path_to_assembly = path_ + elem
                    ti_c = os.path.getmtime(path_to_assembly)
                    c_ti = time.ctime(ti_c)
                    is_find = False
                    if (command == ">"):
                        if c_ti < date_c:
                            is_find = True
                    elif (command == "<"):
                        if c_ti > date_c:
                            is_find = True
                    elif (command == "=" or command == "=="):
                        if c_ti == date_c:
                            is_find = True
                    if is_find:
                        if exec_ == "DELETE":
                            if exec_path_:
                                shutil.rmtree(exec_path_)
                            else:
                                shutil.rmtree(path_to_assembly)
            except FileNotFoundError:
                pass

with open('config_file.yaml') as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
        production_templates = doc["patterns"]["production"]
        test_templates = doc["patterns"]["check"]
        for rule_name in doc["rules"]:
            rule = doc["rules"][rule_name]
            if 'rules' in rule:
                arr_of_rules = [ rule['rules']]
                for rule_ in arr_of_rules:
                    handle_command(rule_)
            else:
                handle_command(rule)

#


