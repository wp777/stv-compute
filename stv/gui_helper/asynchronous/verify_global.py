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
    
    result, time, states, strategy = global_model.verify_approximation(v != 1)
    
    if result:
        print(1)
    else:
        print(0)
    print(len(states))
    print(global_model.model.js_dump_strategy_objective(strategy))

if mode == "reduced":
    reduced_model = GlobalModelParser().parseBase64String(modelStr)
    reduced_model.generate(reduction=True)

    result, time, states, strategy = reduced_model.verify_approximation(v != 1)
    
    if result:
        print(1)
    else:
        print(0)
    print(len(states))
    print(reduced_model.model.js_dump_strategy_objective(strategy))
