import sys
import json
from stv.models.asynchronous.parser import AssumptionParser

modelStr = sys.argv[3]

global_models = AssumptionParser().parseBase64String(modelStr)

for model in global_models:
    model.generate()

print(json.dumps({
    "specs": [f"{model}" for model in global_models],
    "localModels": [model.model.js_dump_model(model.get_formula_winning_states(), model._show_epistemic) for model in global_models],
    "localModelNames": [model.name for model in global_models]
}))
