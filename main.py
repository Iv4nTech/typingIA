from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

prompt = "Give me a four-line sentence in Spanish"
messages = [
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768
)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

# parsing thinking content
try:
    # rindex finding 151668 (</think>)
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0

thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
print('-----------------------------------')
print(f'Contenido generado: {content}')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/")
async def root():
  prompt = "Give me a four-line sentence in Spanish"
  messages = [
      {"role": "user", "content": prompt}
  ]

  text = tokenizer.apply_chat_template(
      messages,
      tokenize=False,
      add_generation_prompt=True,
      enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
  )
  model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

  generated_ids = model.generate(
      **model_inputs,
      max_new_tokens=32768
  )
  output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

  # parsing thinking content
  try:
      # rindex finding 151668 (</think>)
      index = len(output_ids) - output_ids[::-1].index(151668)
  except ValueError:
      index = 0

  thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
  content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

  return {
        "pensamiento": thinking_content,
        "respuesta": content
    }