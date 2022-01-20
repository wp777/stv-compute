import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
from stv.models.asynchronous.parser import AssumptionParser

modelName = sys.argv[3]
modelStr = sys.argv[4]
v = int(sys.argv[5])

modelId = 0
count = 0

models, global_model = AssumptionParser().parseBase64String(modelStr)
formulas = []

modelId = len(models)

for model in models:
    model.generate()
    formulas.append(model.formula)
    if model.name == modelName:
        modelId = count

    count += 1

global_model.generate()
formulas.append(global_model.formula)

# print(json.dumps({
#     "specs": [f"{model}" for model in models],
#     "localModels": [model.model.js_dump_model(model.get_formula_winning_states(), model._show_epistemic) for model in models],
#     "localModelNames": [model.name for model in models],
#     "globalModel": global_model.model.js_dump_model(global_model.get_formula_winning_states(), global_model._show_epistemic),
#     "formulas": formulas
# }))

verifModel = None

if modelId == len(models):
    verifModel = global_model
else:
    verifModel = models[modelId]

result, time, states, strategy = verifModel.verify_approximation(v != 1)

if result:
    print(1)
else:
    print(0)

print(len(states))
print(verifModel.model.js_dump_strategy_objective(strategy))