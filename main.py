from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import re

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen3-1.7B", 
    device_map="auto",
    torch_dtype="auto"
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
    if data.errors:
        letras = ",".join(data.errors)
        prompt = (
            f"letters:a,b,c|result:abc aac\n"
            f"letters:x,y|result:yyx xyx\n"
            f"letters:{letras}|result:"
        )
    else:
        prompt = "A random sentence in English: "


    result = pipe(
        prompt,
        max_new_tokens=25,       
        do_sample=True,          
        temperature=0.9,         
        top_k=50,                
        repetition_penalty=1.2,  
        return_full_text=False,
    )
    
    output = result[0]['generated_text'].strip()

  
    frase = output.split('\n')[0].strip()
    if ":" in frase:
        frase = frase.split(":")[-1].strip()

    final_content = re.sub(r'[^a-z\s]', '', frase.lower()).strip()

    return {
        "respuesta": final_content
    }