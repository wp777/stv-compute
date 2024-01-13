import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
import base64
import subprocess

mode = sys.argv[3]  # "global" | "reduced"
modelStr = sys.argv[4]

if mode != "reduced":
    with open("stv_model_file.txt", "w") as file:
        dstr = base64.b64decode(modelStr).decode("UTF-8")
        dstr = dstr.replace("\r", "")
        print(dstr, file=file)

    out_file = open("stv_output.txt", "w")
    subprocess.call("../stv_v2/build/stv.exe -f stv_model_file.txt -m 3 --OUTPUT_DOT_FILES", stdout=out_file, stderr=out_file, shell=False)
    out_file.close()

    localModels = [json.dumps({"nodes": [{"T": {"j": "j"}, "id": 0, "bgn": 0, "win": 0, "str": 0}], "links": [{"id": 0, "source": 0, "target": 0, "T": "", "str": 0}]})]
    localModelNames = ["Hello"]
    global_model = {"nodes": [], "links": []}
    formula = "text"

    with open("dot/stv_model_file-GlobalModel.dot") as file:
        data = file.read().split("\n")[14:-1]
        for line in data:
            if line.find('"->"') == -1:
                elements = line.split('"')
                node_id = elements[1]
                node_label = elements[3]
                global_model["nodes"].append({"T": node_label, "id": node_id, "bgn": 0})
            else:
                elements = line.split('"')
                transition_id = elements[5]
                actions = elements[5]
                state_id = elements[1]
                target_id = elements[3]
                global_model["links"].append({"id": transition_id, "source": state_id, "target": target_id, "T": actions,
                     "str": 0})
    
    # global_model = {"nodes": [{"T": {"j": "j"}, "id": 0, "bgn": 0, "win": 0, "str": 0}], "links": [{"id": 0, "source": 0, "target": 0, "T": "", "str": 0}]}
    # global_model = {}
    localModels = [json.dumps(global_model)]
    # localModelNames = {}
    
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

    # print(json.dumps({
    #     # "localModels": localModels,
    #     # "localModelNames": localModelNames,
    #     "globalModel": json.dumps({"nodes": [], "links": []}),
    #     # "reducedModel": None,
    #     # "formula": formula
    # }))
    
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
