import sys
import json
from stv.models.asynchronous.parser import AssumptionParser

modelStr = sys.argv[3]

models, global_model = AssumptionParser().parseBase64String(modelStr)
formulas = []

for model in models:
    model.generate()
    formulas.append(model.formula)

global_model.generate()
formulas.append(global_model.formula)

print(json.dumps({
    "specs": [f"{model}" for model in models] + [f"{global_model}"],
    "localModels": [model.model.js_dump_model(model.get_formula_winning_states(), model._show_epistemic) for model in models],
    "localModelNames": [model.name for model in models],
    "globalModel": global_model.model.js_dump_model(global_model.get_formula_winning_states(), global_model._show_epistemic),
    "formulas": formulas
}))
