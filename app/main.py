from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel

app = FastAPI(
    title="API de Consulta de Dados Públicos",
    description="API para consulta de CEP, CNPJ e CPF simulado",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Endereco(BaseModel):
    cep: str
    logradouro: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    localidade: str | None = None
    uf: str | None = None

@app.get("/api/endereco/cep/{cep}", response_model=Endereco)
async def consultar_cep(cep: str):
    """
    Consulta um CEP no serviço ViaCEP
    """
    # vai só remover caracteres não numéricos do CEP
    cep = ''.join(filter(str.isdigit, cep))
    
    if len(cep) != 8:
        raise HTTPException(status_code=400, detail="CEP deve conter 8 dígitos")
    
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        response.raise_for_status()
        data = response.json()
        
        if "erro" in data:
            raise HTTPException(status_code=404, detail="CEP não encontrado")
            
        return Endereco(**data)
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Erro ao consultar o serviço ViaCEP") 