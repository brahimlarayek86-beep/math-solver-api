from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY", "")

@app.post("/api/v1/solve/text")
async def solve_text(problem: str):
    if not openai.api_key:
        return {"error": "API key missing"}
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "كن مدرس رياضيات عربي."},
            {"role": "user", "content": problem}
        ]
    )
    
    return {"solution": response.choices[0].message.content}

@app.get("/health")
async def health():
    return {"status": "ok", "api_key_set": bool(openai.api_key)}

@app.get("/")
async def root():
    return {"message": "Math Solver API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
