import sys
import json
from stv.models.asynchronous.parser import GlobalModelParser

model1Str = sys.argv[3]
model2Str = sys.argv[4]

global_model1 = GlobalModelParser().parseBase64String(model1Str)
global_model1.generate(reduction=False)
global_model1.generate_local_models()

global_model2 = GlobalModelParser().parseBase64String(model2Str)
global_model2.generate(reduction=False)
global_model2.generate_local_models()

winning = []

print(json.dumps({
    "model1": global_model1.model.js_dump_model(winning),
    "model2": global_model2.model.js_dump_model(winning),
}))
