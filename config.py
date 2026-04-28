import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import config

class NanoEngine:
    def __init__(self):
        # Memuat tokenizer dan model ke CPU
        self.tokenizer = AutoTokenizer.from_pretrained(config.MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.MODEL_ID,
            torch_dtype=torch.float32,
            device_map="cpu",
            low_cpu_mem_usage=True
        )

    def generate(self, user_input):
        prompt = f"{config.get_system_prompt()}\nUser: {user_input}\nAssistant:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cpu")
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=config.MAX_NEW_TOKENS,
                temperature=config.TEMPERATURE,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs, skip_special_tokens=True).split("Assistant:")[-1].strip()

engine = NanoEngine()
