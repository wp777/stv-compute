import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
from stv.comparing_strats import StrategyComparer
from stv.models.asynchronous.parser import AssumptionParser

modelName = sys.argv[3]
modelStr = sys.argv[4]
heuristic = int(sys.argv[5])

models, global_model = AssumptionParser().parseBase64String(modelStr)
formulas = []

count = 0
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

winning = verifModel.get_formula_winning_states()

strategy_comparer = StrategyComparer(verifModel.model, verifModel.get_actions()[verifModel.get_agent()])

if heuristic == 0:
    (result, strategy) = strategy_comparer.domino_dfs(0, set(winning),
                                                                        [global_model.get_agent()],
                                                                        strategy_comparer.basic_h)
elif heuristic == 1:
    (result, strategy) = strategy_comparer.domino_dfs(0, set(winning),
                                                                        [global_model.get_agent()],
                                                                        strategy_comparer.control_h)
elif heuristic == 2:
    (result, strategy) = strategy_comparer.domino_dfs(0, set(winning),
                                                                        [global_model.get_agent()],
                                                                        strategy_comparer.epistemic_h)
elif heuristic == 3:
    (result, strategy) = strategy_comparer.domino_dfs(0, set(winning),
                                                                        [global_model.get_agent()],
                                                                        strategy_comparer.visited_states_h)
if result:
    print("1")
else:
    print("0")
print(verifModel.model.js_dump_strategy_objective(strategy))