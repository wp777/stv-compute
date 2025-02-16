import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
from stv.comparing_strats import StrategyComparer
import base64
import subprocess
import os
import re

modelStr = sys.argv[3]

with open("stv_model_file.txt", "w") as file:
    dstr = base64.b64decode(modelStr).decode("UTF-8")
    dstr = dstr.replace("\r", "")
    print(dstr, file=file)
    formula = re.findall("^FORMULA: .*", dstr, re.MULTILINE)[0].lstrip("FORMULA:")

out_file = open("stv_output.txt", "w")
subprocess.call("../stv_v2/build/stv -f stv_model_file.txt -m 3 --OUTPUT_DOT_FILES --COUNTEREXAMPLE --NATURAL_STRATEGY", stdout=out_file, stderr=out_file, shell=True)
out_file.close()

global_model = {"nodes": [], "links": []}

counter_example_states = []
counter_example_links = []
with open("stv_output.txt") as file:
    states_line = False
    links_line = False
    for line in file:
        if len(line.strip()) == 0:
            states_line = False
            links_line = False
            continue
        if states_line and "(" in line:
            line = line.split("(")[-1]
            line = line.strip().rstrip(";)")
            for param in line.split(";"):
                counter_example_states[-1].append(param)
        elif "States:" in line:
            states_line = True
            counter_example_states.append([])
        elif links_line:
            links_line = False
            line = line.replace(";", ",")
            line = line.strip().rstrip(",")
            counter_example_links.append(line)
        elif "Decisions:" in line:
            links_line = True


with open("dot/stv_model_file-GlobalModel.dot") as file:
    data = file.read().split("\n")[14:-1]
    data = sorted(data, key=lambda x: (x.find('"->"'), x))
    states_ids = {}
    current_transition_id = 0
    current_id = 0
    for line in data:
        if line.find('"->"') == -1:
            elements = line.split('"')
            node_id = elements[1]
            node_id_value = int("1" + node_id.replace(";",""))
            node_label = elements[3]
            bgn = 1 if current_id == 0 else 0
            strat = 0
            for counter_ex in counter_example_states:
                strat = 0
                for param in counter_ex:
                    if param not in line:
                        strat = 0
                
            global_model["nodes"].append({"T": {"id": node_id}, "id": current_id, "bgn": bgn, "str": strat})
            states_ids[node_id] = current_id
            current_id += 1
        else:
            elements = line.split('"')
            transition_id = current_transition_id
            actions = elements[5]
            state_id = elements[1]
            target_id = elements[3]
            strat = 0
            for counter_ex in counter_example_links:
                if counter_ex in line:
                    strat = 1
            if len(elements) >= 8 and elements[7] == "red":
                strat = 1
            global_model["links"].append({"id": transition_id, "source": states_ids[state_id], "target": states_ids[target_id], "T": [actions],
                    "str": strat})
            current_transition_id += 1

for filename in os.listdir("dot"):
    f = os.path.join("dot", filename)
    if ".dot" in filename:
        os.remove(f)

natural_strategy = ""
complexity = ""
with open("stv_output.txt", "r") as file:
    output = file.read().split("\n")
    if "TRUE" in output[0]:
        print("1")
        natural_strategy = output[1:-3]
        complexity = output[-2].split(":")[1].strip()
    else:
        print("0")

print(json.dumps(global_model))
print(natural_strategy)
print(complexity)
