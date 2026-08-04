from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai", temperature=0)

class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(description="The vulnerabilities in the code", default=None)
    riskLevel: str = Field(description="The risk level of the vulnerabilities", default=None)
    suggestions: list[str] = Field(description="The suggestions for fixing the vulnerabilities", default=None)


class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(description="The concerns about the code", default=None)
    qualityScore: int = Field(description="The quality score of the code from 1 to 10", default=None, ge=1, le=10)
    recommendations: list[str] = Field(description="The recommendations for improving the code", default=None)

class PerformanceReview(BaseModel):
    time_complexity: list[str] = Field(description="The time complexity of the code", default=None)    
    spatial_complexity: list[str] = Field(description="The spatial complexity of the code", default=None)    
    bottlenecks_detected: list[str] = Field(description="The bottlenecks detected in the code", default=None)
    justification: list[str] = Field(description="Justification for the performance review", default=None)



class State(TypedDict):
    code: str
    security_review: SecurityReview
    maintainability_review: MaintainabilityReview
    performance_review: PerformanceReview
    final_review: str

def security_review(state: State):
    code = state['code']
    messages = [
        ("system", "You are an expert in code security. Focus on identifying security vulnerabilities, injection risks, and authentication issues."),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'security_review': schema
    }


def maintainability_review(state: State):
    code = state['code']
    messages = [
        ("system", "You are an expert in code quality. Focus on code structure, readability, and adherence to best practices."),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(MaintainabilityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'maintainability_review': schema
    }

def performance_review(state: State):
    code = state['code']
    messages = [
        ("system", '''# ROL Y OBJETIVO
Eres un Ingeniero Especialista en Optimización de Código y Rendimiento de Software (Performance Engineer). Tu objetivo es analizar, refactorizar y maximizar la eficiencia funcional, de memoria y de tiempo de ejecución del código proporcionado.

# TAREAS PRINCIPALES
1. Identificar cuellos de botella (operaciones I/O costosas, algoritmos ineficientes, iteraciones innecesarias, fugas de memoria o uso excesivo de recursos).
2. Refactorizar el código para minimizar la complejidad temporal y espacial (Notación Big-O).
3. Asegurar que la lógica de negocio y el comportamiento esperado se mantengan 100% idénticos al original.

# REGLAS DE EJECUCIÓN
- Mantén el mismo lenguaje de programación y paradigma del código original a menos que se solicite lo contrario.
- Prioriza soluciones nativas del lenguaje antes de sugerir librerías externas.
- Si hay un compromiso (trade-off) entre legibilidad y rendimiento extremo, acláralo explícitamente en la explicación.

# FORMATO DE SALIDA OBLIGATORIO
Estructura siempre tu respuesta con el siguiente formato:

## 1. Diagnóstico Inicial
- Complejidad Temporal Actual: O(...)
- Complejidad Espacial Actual: O(...)
- Cuellos de Botella Detectados: [Lista breve de los puntos críticos de ineficiencia]
'''),
        ("user", f"Review this code: {code}")
    ]
    llm_with_structured_output = llm.with_structured_output(PerformanceReview)
    schema = llm_with_structured_output.invoke(messages)
    return {
        'performance_review': schema
    }


def aggregator(state: State):
    security_review = state['security_review']
    maintainability_review = state['maintainability_review']
    performance_review = state['performance_review']
    messages = [
        ("system", "You are a technical lead summarizing multiple code reviews"),
        ("user", f"Synthesize these code review results into a concise summary with key actions: Security review: {security_review} and Maintainability review: {maintainability_review} and Performance review: {performance_review}")
    ]
    response = llm.invoke(messages)
    return {
        'final_review': response.text
    }


builder = StateGraph(State)

builder.add_node('security_review', security_review)
builder.add_node('maintainability_review', maintainability_review)
builder.add_node('performance_review', performance_review)
builder.add_node('aggregator', aggregator)

builder.add_edge(START, 'security_review')
builder.add_edge(START, 'maintainability_review')
builder.add_edge(START, 'performance_review')
builder.add_edge("security_review", "aggregator")
builder.add_edge("maintainability_review", "aggregator")
builder.add_edge("performance_review", "aggregator")
builder.add_edge('aggregator', END)
agent = builder.compile()