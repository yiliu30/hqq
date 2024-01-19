#Settings
######################################################################################
hf_auth    = None #HuggingFace token
cache_path = ''   #cache directory to store data

#Chose a model
# model_id  = "meta-llama/Llama-2-7b-hf" 
model_id = (
    "/home/yliu7/workspace/gpt-fast/checkpoints/meta-llama/Llama-2-7b-chat-hf/tmp"
)
#model_id  = "meta-llama/Llama-2-13b-hf" 
#model_id  = "meta-llama/Llama-2-70b-hf" 

#Load model on the CPU
######################################################################################
from hqq.engine.hf import HQQModelForCausalLM, AutoTokenizer
model     = HQQModelForCausalLM.from_pretrained(model_id, use_auth_token=hf_auth, cache_dir=cache_path)
tokenizer = AutoTokenizer.from_pretrained(model_id,       use_auth_token=hf_auth, cache_dir=cache_path) 

#Quantize the model
######################################################################################
from hqq.core.quantize import *

#quant_config = BaseQuantizeConfig(nbits=8, group_size=128)
quant_config = BaseQuantizeConfig(nbits=4, group_size=64)
#quant_config = BaseQuantizeConfig(nbits=3, group_size=64)
#quant_config = BaseQuantizeConfig(nbits=2, group_size=16)
#quant_config = BaseQuantizeConfig(nbits=2, group_size=16, quant_scale=True) #scale is quantized to 8-bit/g=128

model.quantize_model(quant_config=quant_config)

#Optional: set the backend
#HQQLinear.set_backend(HQQBackend.PYTORCH_COMPILE)

# #Evaluate the quantized model 
######################################################################################
from eval_model import eval_wikitext2
eval_wikitext2(model, tokenizer, verbose=True) 

