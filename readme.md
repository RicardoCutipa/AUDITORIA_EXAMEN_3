# INFORME FINAL DE AUDITORÍA DE SISTEMAS

## CARÁTULA

**Entidad Auditada:** CORPORATE EPIS PILOT  
**Ubicación:** Tacna, Perú (Despliegue Local / Sede Virtual)  
**Período auditado:** 19 de Noviembre de 2025  
**Equipo Auditor:** Ricardo Daniel Cutipa Gutierrez (Auditor Líder)  
**Fecha del informe:** 19/11/2025  
**Enlace al Repositorio:** https://github.com/RicardoCutipa/AUDITORIA_EXAMEN_3.git

---

## ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)  
2. [Antecedentes](#2-antecedentes)  
3. [Objetivos de la Auditoría](#3-objetivos-de-la-auditoría)  
4. [Alcance de la Auditoría](#4-alcance-de-la-auditoría)  
5. [Normativa y Criterios de Evaluación](#5-normativa-y-criterios-de-evaluación)  
6. [Metodología y Enfoque](#6-metodología-y-enfoque)  
7. [Hallazgos y Observaciones](#7-hallazgos-y-observaciones)  
8. [Análisis de Riesgos](#8-análisis-de-riesgos)  
9. [Recomendaciones](#9-recomendaciones)  
10. [Conclusiones](#10-conclusiones)  
11. [Plan de Acción y Seguimiento](#11-plan-de-acción-y-seguimiento)  
12. [Anexos](#12-anexos)  

---

## 1. RESUMEN EJECUTIVO

La presente auditoría técnica se realizó sobre el sistema de Mesa de Ayuda con IA de "Corporate EPIS Pilot". El propósito principal fue verificar la migración tecnológica del motor de inferencia hacia el modelo `smollm:360m` y validar la disponibilidad de los servicios.

**Conclusión Principal:** Se certifica que el sistema ha sido desplegado exitosamente y cumple con el requisito de utilizar el modelo `smollm:360m`, verificado a través de la interfaz de usuario. Sin embargo, se detectaron problemas de latencia (Timeouts) en consultas complejas debido a las limitaciones de hardware/modelo en la generación de respuestas extensas.

## 2. ANTECEDENTES

"Corporate EPIS Pilot" es un asistente de IA conversacional diseñado para entornos empresariales. Su arquitectura original incluye:
*   **RAG (Retrieval-Augmented Generation):** Uso de bases de conocimiento internas.
*   **Router de Intenciones:** Clasificación de solicitudes mediante LLM.
*   **Stack Tecnológico:** Frontend en React, Backend en FastAPI (Python) y orquestación mediante Docker.
*   **Cambio Solicitado:** Migración del modelo *Llama 3.1* al modelo ligero *smollm:360m* para entornos locales con recursos limitados.

## 3. OBJETIVOS DE LA AUDITORÍA

**Objetivo General:**
Auditar el código fuente y el funcionamiento en tiempo real del sistema para asegurar su operatividad bajo la nueva configuración del modelo `smollm:360m`.

**Objetivos Específicos:**
1.  Verificar el levantamiento exitoso de la arquitectura de microservicios (Docker).
2.  Validar que el sistema responde e identifica correctamente el modelo `smollm:360m`.
3.  Evaluar el rendimiento del sistema ante solicitudes de usuario.
4.  Comprobar la integridad de la interfaz gráfica y su conexión con el backend.

## 4. ALCANCE DE LA AUDITORÍA

*   **Ámbito Tecnológico:** Entorno de despliegue contenerizado (Docker Desktop sobre WSL 2).
*   **Sistemas:** Frontend (Puerto 5173), Backend (API Rest), Motor Ollama.
*   **Periodo:** Ejecución puntual el 19/11/2025.

## 5. NORMATIVA Y CRITERIOS DE EVALUACIÓN

*   **Requisitos del Proyecto:** Especificaciones técnicas de la migración a `smollm`.
*   **ISO/IEC 25010:** Criterios de calidad de software (Adecuación funcional y Eficiencia de desempeño).
*   **Buenas Prácticas DevOps:** Verificación de archivos `docker-compose.yml` y gestión de variables de entorno.

## 6. METODOLOGÍA Y ENFOQUE

Se utilizó un enfoque de **Caja Negra y Caja Gris**:
1.  **Revisión Estática:** Inspección del código fuente (`main.py`) y configuración de contenedores para confirmar el cambio de modelo.
2.  **Pruebas Dinámicas:** Interacción con el chatbot a través del navegador web.
3.  **Análisis de Logs:** Revisión de los registros del contenedor `backend` y `proxy` para evaluar el comportamiento interno.

## 7. HALLAZGOS Y OBSERVACIONES

### Hallazgo 01: Conformidad en el Despliegue y Modelo (Crítico)
*   **Descripción:** El sistema se levantó correctamente. Al realizar la prueba de conexión mediante el saludo "hola", el sistema respondió identificándose y confirmando el uso del motor `smollm:360m`.
*   **Evidencia:** Captura de pantalla `evidencia01.png` (Ver Anexos).
*   **Criterio:** Cumplimiento del requisito funcional del examen.
*   **Criticidad:** N/A (Hallazgo Positivo).

### Hallazgo 02: Latencia Excesiva y Timeouts en Consultas Complejas
*   **Descripción:** Durante pruebas de estrés con consultas como "tengo un problema", se observó un error `504 Gateway Time-out` en el Proxy (Nginx). Los logs del backend muestran tiempos de respuesta superiores a 400 segundos.
*   **Causa:** El modelo `smollm:360m`, al ser pequeño, entra en bucles de generación de texto repetitivo (alucinaciones), excediendo el tiempo de espera del servidor.
*   **Criticidad:** Alta (Afecta la disponibilidad).

## 8. ANÁLISIS DE RIESGOS

| Hallazgo | Riesgo asociado | Impacto | Probabilidad | Nivel de Riesgo |
|----------|-----------------|---------|--------------|-----------------|
| H-01 (Modelo) | N/A (Cumplimiento) | Positivo | N/A | N/A |
| H-02 (Timeout) | Denegación de servicio (DoS) por bloqueo de hilos en el backend. | Alto | Alta | **Alto** |

## 9. RECOMENDACIONES

**Para el Hallazgo 02 (Timeouts):**
1.  **Ajuste de Parámetros del Modelo:** Configurar el parámetro `stop` o `max_tokens` en la llamada a Ollama para evitar que el modelo genere texto infinitamente.
2.  **Optimización del Prompt:** Simplificar las instrucciones del "System Prompt" para que el modelo `smollm` (que es menos capaz) pueda entenderlas sin alucinar.
3.  **Aumentar Timeouts:** Aumentar los tiempos de espera en la configuración de Nginx (`proxy_read_timeout`), aunque esto es una solución paliativa.

## 10. CONCLUSIONES

1.  **Objetivo Cumplido:** Se ha verificado satisfactoriamente que "Corporate EPIS Pilot" ha migrado su infraestructura para operar con **smollm:360m**. La evidencia visual confirma la identidad del modelo en el entorno de producción local.
2.  **Estado del Sistema:** La arquitectura base (Frontend/Backend/DB) es sólida y despliega correctamente.
3.  **Observación de Auditoría:** Aunque el sistema funciona para interacciones cortas, se requiere optimización técnica para evitar los errores de tiempo de espera (`Timeout 504`) detectados en los logs durante consultas extensas.

## 11. PLAN DE ACCIÓN Y SEGUIMIENTO

| Hallazgo | Recomendación | Responsable | Fecha Comprometida |
|----------|----------------|-------------|---------------------|
| Latencia / Timeout | Configurar `max_tokens=150` en `main.py` | Desarrollo | Inmediato |
| Estabilidad Modelo | Refinar Prompts para modelos SLM | Arquitecto IA | Próximo Sprint |

---

## 12. ANEXOS

### Evidencia 01: Prueba de Funcionamiento y Verificación de Modelo
La siguiente captura demuestra:
1.  Interfaz de usuario operativa.
2.  Comunicación exitosa con el Backend.
3.  **Confirmación explícita del uso de `smollm:360m`** en la respuesta del asistente.

![Evidencia Principal](evidencias/evidencia01.png)

---
*Fin del Informe - Auditoría Corporate EPIS Pilot*