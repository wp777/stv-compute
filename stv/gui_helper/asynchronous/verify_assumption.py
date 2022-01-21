import sys
from stv.models.asynchronous.parser import AssumptionParser

modelName = sys.argv[3]
modelStr = sys.argv[4]
v = int(sys.argv[5])

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