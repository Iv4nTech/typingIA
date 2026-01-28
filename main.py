from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-1.7B"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ErrorKeys(BaseModel):
    errors: list[str]

@app.post("/")
async def root(data: ErrorKeys):


    print(f'DATOS DE ENTRADA A LA IA: {data.errors}')
    task = f"Use-only:{','.join(data.errors)}|Nonsense sentences only characters" if data.errors else "coherent English sentence"

    prompt = f"[TASK]: {task}\n[RULES]: lowercase,no-symbols, no letters space between, lyrics only in english\nRESULT:"
        
    messages = [{"role": "user", "content": prompt}]

    text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False 
        )
        
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=30,
        do_sample=True,        
        temperature=0.8,       
        top_p=0.9,            
        repetition_penalty=1.2
    )
    

    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):]
    full_output = tokenizer.decode(output_ids, skip_special_tokens=True)

    thinking_content = ""
    final_content = full_output

    if "</think>" in full_output:
        parts = full_output.split("</think>")
        thinking_content = parts[0].replace("<think>", "").strip()
        final_content = parts[1].strip()
    elif "<think>" in full_output:
        parts = full_output.split("<think>")
        final_content = parts[-1].strip()

    return {
        "pensamiento": thinking_content,
        "respuesta": final_content
    }