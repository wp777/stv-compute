import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
import base64
import subprocess
import os
import re

mode = sys.argv[3]  # "global" | "reduced"
modelStr = sys.argv[4]

if mode != "reduced":
    with open("stv_model_file.txt", "w") as file:
        dstr = base64.b64decode(modelStr).decode("UTF-8")
        dstr = dstr.replace("\r", "")
        print(dstr, file=file)
        formula = re.findall("^FORMULA: .*", dstr, re.MULTILINE)[0].lstrip("FORMULA:")

    out_file = open("stv_output.txt", "w")
    #subprocess.call("pwd", stdout=out_file, stderr=out_file, shell=False)
    subprocess.call("../stv_v2/build/stv -f stv_model_file.txt -m 3 --OUTPUT_DOT_FILES", stdout=out_file, stderr=out_file, shell=True)
    out_file.close()

    localModels = []
    localModelNames = []
    global_model = {"nodes": [], "links": []}
    # formula = "text"

    with open("dot/stv_model_file-GlobalModel.dot") as file:
        data = file.read().split("\n")[14:-1]
        states_ids = {}
        current_transition_id = 0
        current_id = 0
        for line in data:
            if line.find('"->"') == -1:
                elements = line.split('"')
                node_id = elements[1]
                label_dict = {"id": node_id}
                node_label = elements[3][1:-1]
                for label in node_label.split("{"):
                    label = label.rstrip("|").rstrip("}")
                    for param in label.split("\\n")[1:]:
                        p_name, p_val = param.split("=")
                        label_dict[p_name] = p_val
                bgn = 1 if current_id == 0 else 0
                global_model["nodes"].append({"T": label_dict, "id": current_id, "bgn": bgn})
                states_ids[node_id] = current_id
                current_id += 1
            else:
                elements = line.split('"')
                transition_id = current_transition_id
                actions = elements[5]
                state_id = elements[1]
                target_id = elements[3]
                global_model["links"].append({"id": transition_id, "source": states_ids[state_id], "target": states_ids[target_id], "T": [actions],
                     "str": 0})
                current_transition_id += 1
    
    for filename in os.listdir("dot"):
        f = os.path.join("dot", filename)
        if os.path.isfile(f) and "LocalModel" in filename:
            agent_name = filename.split("-")[1].split("_")[1].split(".")[0]
            localModelNames.append(agent_name)
            with open(f, "r") as file:
                data = file.read().split("\n")[14:-1]
                current_transition_id = 0
                local_model = {"nodes": [], "links": []}
                for line in data:
                    line = line.strip()
                    if line.find('->') == -1:
                        elements = line.split('"')
                        node_id = int(elements[0].split("[")[0])
                        node_label = elements[1]
                        label_dict = {"id": node_id}
                        node_label = elements[1][1:-1].split("|")[-1]
                        for param in node_label.split("\\n"):
                            p_name, p_val = param.split("=")
                            label_dict[p_name] = p_val
                        bgn = 1 if node_id == 0 else 0
                        local_model["nodes"].append({"T": label_dict, "id": node_id, "bgn": bgn})
                    else:
                        elements = line.split('"')
                        transition_id = current_transition_id
                        actions = elements[1]
                        state_id, target_id = map(int, elements[0].split("[")[0].split("->"))
                        local_model["links"].append({"id": transition_id, "source": state_id, "target": target_id, "T": [actions],
                            "str": 0})
                        current_transition_id += 1
                localModels.append(json.dumps(local_model))
        if ".dot" in filename:
            os.remove(f)
    
    with open("stv_debug.txt", "w") as file:
        print(json.dumps({
            "localModels": localModels,
            "localModelNames": localModelNames,
            "globalModel": json.dumps(global_model),
            "reducedModel": None,
            "formula": formula
        }), file=file)
    
    print(json.dumps({
        "localModels": localModels,
        "localModelNames": localModelNames,
        "globalModel": json.dumps(global_model),
        "reducedModel": None,
        "formula": formula
    }))
    
    exit()

global_model = GlobalModelParser().parseBase64String(modelStr)
global_model.generate(reduction=False)
global_model.generate_local_models()

reduced_model = None
if mode == "reduced":
    reduced_model = GlobalModelParser().parseBase64String(modelStr)
    reduced_model.generate(reduction=True)
    winning_reduced = reduced_model.get_formula_winning_states()

winning_global = global_model.get_formula_winning_states()

# for state in global_model._states:
#     state.print()
# global_model.print()
localModels = []
localModelNames = []
for localModel in global_model._local_models:
    localModels.append(localModel._model.js_dump_model(winning=[], epistemic=False))
    localModelNames.append(localModel._agent_name)

print(json.dumps({
    "localModels": localModels,
    "localModelNames": localModelNames,
    "globalModel": global_model.model.js_dump_model(winning_global, global_model._show_epistemic, True, reduced_model.model if reduced_model else None),
    "reducedModel": reduced_model.model.js_dump_model(winning_reduced, global_model._show_epistemic, True) if reduced_model else None,
    "formula": global_model.formula
}))
