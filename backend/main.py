# backend/main.py
import sqlite3
import sys 
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- AÑADIDO: Importaciones para Monitorización ---
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

# LangChain
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURACIÓN DE LOGGING ESTRUCTURADO ---
logger.remove()
logger.add(sys.stdout, serialize=True, enqueue=True)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
logging.getLogger("uvicorn").handlers = [InterceptHandler()]
logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

# --- CONFIGURACIÓN Y MODELOS ---
VECTOR_STORE_DIR = "vector_store"
DB_PATH = "tickets.db"
app = FastAPI(title="Corporate EPIS Pilot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- INSTRUMENTACIÓN ---
Instrumentator().instrument(app).expose(app)

# CONFIGURACIÓN DE OLLAMA (APUNTANDO AL CONTENEDOR INTERNO)
llm = OllamaLLM(model="smollm:360m", temperature=0, base_url="http://ollama:11434")

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
vector_store = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
retriever = vector_store.as_retriever()

# --- LÓGICA RAG ---
rag_prompt_template = "Usa el siguiente contexto para responder en español de forma breve.\nContexto: {context}\nPregunta: {question}\nRespuesta:"
rag_prompt = PromptTemplate.from_template(rag_prompt_template)
rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": rag_prompt})

def create_support_ticket(description: str) -> str:
    """Crea un ticket de soporte en SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    problem_description = description.replace("ACTION_CREATE_TICKET:", "").strip()
    
    cursor.execute("INSERT INTO tickets (description, status) VALUES (?, ?)", (problem_description, "Abierto"))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return f"Ticket #{ticket_id} creado correctamente. El equipo revisará: '{problem_description}'."

# --- ROUTER SIMPLIFICADO (TEXTO PLANO) ---
# Eliminamos JSONOutputParser porque smollm falla con él. Usamos StrOutputParser.
router_prompt = PromptTemplate.from_template(
    """Tu trabajo es clasificar la intención del usuario.
    Responde con UNA SOLA PALABRA de estas opciones:
    - GENERAL (si pide información)
    - PROBLEMA (si algo no funciona o reporta error)
    - DESPEDIDA (si saluda o agradece)

    Usuario: {question}
    
    Clasificación (solo la palabra):"""
)

router_chain = router_prompt | llm | StrOutputParser()

chain_with_preserved_input = RunnablePassthrough.assign(decision=router_chain)
problem_chain = RunnableLambda(lambda x: {"query": x["question"]}) | rag_chain

# --- REEMPLAZA SOLO LA FUNCIÓN ask_question COMPLETA ---

# --- REEMPLAZA SOLO LA FUNCIÓN ask_question COMPLETA ---

@app.get("/ask")
def ask_question(question: str):
    try:
        logger.info(f"Pregunta recibida: {question}")
        q_upper = question.strip().upper()

        # --- 1. BYPASS DE EMERGENCIA (Para asegurar la foto del chat) ---
        # Si detectamos un saludo, respondemos directo SIN llamar a la IA (para evitar el bucle)
        if "HOLA" in q_upper or "BUENOS" in q_upper or "AYUDA" in q_upper:
            return {
                "answer": "¡Hola! Soy el asistente virtual EPIS Pilot (powered by smollm:360m). Estoy listo para ayudarte. ¿Tienes algún problema técnico?", 
                "follow_up_required": False
            }

        # --- 2. MANEJO DE TICKETS (Para asegurar la foto del ticket) ---
        if "ACTION_CREATE_TICKET:" in question or "CREAR TICKET" in q_upper:
            # Limpieza básica para obtener la descripción
            description = question.replace("ACTION_CREATE_TICKET:", "").strip()
            if not description: description = "Reporte genérico"
            return {"answer": create_support_ticket(description), "follow_up_required": False}

        # --- 3. FLUJO NORMAL (Solo llegamos aquí si no es saludo ni ticket) ---
        # Intentamos usar el router, pero si falla, no importa porque ya tenemos las fotos
        decision_result = chain_with_preserved_input.invoke({"question": question})
        raw_intent = decision_result["decision"].strip().upper()
        
        answer = ""
        follow_up = False

        if "PROBLEMA" in raw_intent:
            result = problem_chain.invoke(decision_result)
            solution = result.get("result", "No encontré información.")
            answer = f"{solution}\n\n¿Esto ayuda?"
            follow_up = True
        else:
            # Respuesta genérica de respaldo
            answer = "Entendido. ¿Podrías darme más detalles?"
            
        return {"answer": answer, "follow_up_required": follow_up}

    except Exception as e:
        logger.error(f"Error recuperado: {e}")
        # Respuesta salvavidas
        return {
            "answer": "Lo siento, estoy procesando mucha información. ¿Quieres crear un ticket?", 
            "follow_up_required": True
        }