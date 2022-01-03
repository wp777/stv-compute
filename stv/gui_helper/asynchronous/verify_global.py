import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser

mode = sys.argv[3]  # "global" | "reduced"
modelStr = sys.argv[4]
v = int(sys.argv[5])

if mode == "global":
    global_model = GlobalModelParser().parseBase64String(modelStr)
    global_model.generate(reduction=False)
    global_model.generate_local_models()
    
    if v == 1:
        atl_model_global = global_model.model.to_atl_imperfect()
    else:
        atl_model_global = global_model.model.to_atl_perfect()
    
    winning = global_model.get_formula_winning_states()
    result = atl_model_global.minimum_formula_many_agents([global_model.get_agent()], winning)
    
    if 0 in result:
        print(1)
    else:
        print(0)
    print(len(result))
    print(global_model.model.js_dump_strategy_objective(atl_model_global.strategy))

if mode == "reduced":
    reduced_model = GlobalModelParser().parseBase64String(modelStr)
    reduced_model.generate(reduction=True)
    
    if v == 1:
        atl_model_reduced = reduced_model.model.to_atl_imperfect()
    else:
        atl_model_reduced = reduced_model.model.to_atl_perfect()
    
    winning = reduced_model.get_formula_winning_states()
    result = atl_model_reduced.minimum_formula_many_agents([reduced_model.get_agent()], winning)
    
    if 0 in result:
        print(1)
    else:
        print(0)
    print(len(result))
    print(reduced_model.model.js_dump_strategy_objective(atl_model_reduced.strategy))
