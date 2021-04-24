import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser
from stv.comparing_strats import StrategyComparer

mode = sys.argv[3]  # "global" | "reduced"
modelStr = sys.argv[4]
heuristic = int(sys.argv[5])

if mode == "global":
    global_model = GlobalModelParser().parseBase64String(modelStr)
    global_model.generate(reduction=False)
    global_model.generate_local_models()
    winning_global = global_model.get_formula_winning_states()

    strategy_comparer_global = StrategyComparer(global_model.model, global_model.get_actions()[global_model.get_agent()])

    if heuristic == 0:
        (result, strategy) = strategy_comparer_global.domino_dfs(0, set(winning_global),
                                                                            [global_model.get_agent()],
                                                                            strategy_comparer_global.basic_h)
    elif heuristic == 1:
        (result, strategy) = strategy_comparer_global.domino_dfs(0, set(winning_global),
                                                                            [global_model.get_agent()],
                                                                            strategy_comparer_global.control_h)
    elif heuristic == 2:
        (result, strategy) = strategy_comparer_global.domino_dfs(0, set(winning_global),
                                                                            [global_model.get_agent()],
                                                                            strategy_comparer_global.epistemic_h)
    elif heuristic == 3:
        (result, strategy) = strategy_comparer_global.domino_dfs(0, set(winning_global),
                                                                            [global_model.get_agent()],
                                                                            strategy_comparer_global.visited_states_h)
    if result:
        print("1")
    else:
        print("0")
    print(global_model.model.js_dump_strategy_objective(strategy))

if mode == "reduced":
    reduced_model = GlobalModelParser().parseBase64String(modelStr)
    reduced_model.generate(reduction=True)
    winning_reduced = reduced_model.get_formula_winning_states()

    strategy_comparer_reduced = StrategyComparer(reduced_model.model,
                                                 reduced_model.get_actions()[reduced_model.get_agent()])

    if heuristic == 0:
        (result, strategy) = strategy_comparer_reduced.domino_dfs(0, set(winning_reduced),
                                                                                  [reduced_model.get_agent()],
                                                                                  strategy_comparer_reduced.basic_h)
    elif heuristic == 1:
        (result, strategy) = strategy_comparer_reduced.domino_dfs(0, set(winning_reduced),
                                                                                  [reduced_model.get_agent()],
                                                                                  strategy_comparer_reduced.control_h)
    elif heuristic == 2:
        (result, strategy) = strategy_comparer_reduced.domino_dfs(0, set(winning_reduced),
                                                                                  [reduced_model.get_agent()],
                                                                                  strategy_comparer_reduced.epistemic_h)
    elif heuristic == 3:
        (result, strategy) = strategy_comparer_reduced.domino_dfs(0, set(winning_reduced),
                                                                                  [reduced_model.get_agent()],
                                                                                  strategy_comparer_reduced.visited_states_h)
    if result:
        print("1")
    else:
        print("0")
    print(global_model.model.js_dump_strategy_objective(strategy))
