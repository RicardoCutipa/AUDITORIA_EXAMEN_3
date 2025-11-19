# INFORME FINAL DE AUDITORÍA DE SISTEMAS

**Enlace al Repositorio:** https://github.com/RicardoCutipa/AUDITORIA_EXAMEN_3.git

---

## CARÁTULA

**Entidad Auditada:** CORPORATE EPIS PILOT (Sistema de Mesa de Ayuda con IA)  
**Ubicación:** Tacna, Perú (Despliegue en entorno local virtualizado)  
**Período auditado:** 19 de Noviembre de 2025  
**Equipo Auditor:** Ricardo Daniel Cutipa Gutierrez (Auditor Líder)  
**Fecha del informe:** 19/11/2025  

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

La presente auditoría técnica se realizó sobre el sistema "Corporate EPIS Pilot", una solución de Mesa de Ayuda basada en Inteligencia Artificial. El propósito principal fue verificar la operatividad del sistema tras la migración del motor de inferencia al modelo ligero **smollm:360m** ejecutado vía Ollama.

Tras la ejecución de pruebas funcionales y revisión de código, se certifica que el sistema ha sido desplegado exitosamente y **es funcional al 100%**. El chatbot responde coherentemente, identifica su modelo base y completa el flujo de creación de tickets de soporte, cumpliendo con los requisitos establecidos para el Examen de Auditoría.

## 2. ANTECEDENTES

La organización requiere implementar soluciones de IA generativa que puedan ejecutarse en entornos locales con recursos limitados. Previamente, el sistema operaba con modelos pesados (Llama 3) que dificultaban su despliegue en equipos estándar.
Para este examen, se solicitó la clonación, configuración y puesta en marcha del sistema utilizando específicamente el modelo `smollm:360m`, asegurando la integración entre el Frontend (React), Backend (FastAPI) y el gestor de modelos (Ollama).

## 3. OBJETIVOS DE LA AUDITORÍA

**Objetivo General:**
Auditar el despliegue técnico, la integridad del código fuente y la funcionalidad operativa del sistema "Corporate EPIS Pilot" para garantizar su correcto funcionamiento bajo la arquitectura de microservicios con el modelo `smollm:360m`.

**Objetivos Específicos:**
1.  **Verificar la Disponibilidad:** Comprobar que los contenedores Docker (Frontend, Backend, Ollama) se levanten correctamente y expongan los puertos esperados.
2.  **Validar el Modelo de IA:** Confirmar mediante pruebas de interacción que el sistema está utilizando efectivamente el modelo `smollm:360m` y no otro.
3.  **Evaluar el Flujo de Negocio:** Verificar que el sistema sea capaz de procesar una solicitud de usuario compleja y generar un ticket de soporte simulado sin errores.
4.  **Revisión de Código y Configuración:** Analizar el archivo `docker-compose.yml` y el código backend para asegurar que las variables de entorno apuntan a los servicios correctos.

## 4. ALCANCE DE LA AUDITORÍA

*   **Ámbito Tecnológico:** Entorno de ejecución local sobre Docker.
*   **Sistemas Evaluados:**
    *   Interfaz de Usuario (Frontend React).
    *   API de Procesamiento (Backend FastAPI/Python).
    *   Motor de Inferencia (Servicio Ollama).
*   **Procesos:** Chat interactivo y generación de tickets.
*   **Periodo:** Ejecución puntual el 19/11/2025.

## 5. NORMATIVA Y CRITERIOS DE EVALUACIÓN

*   **Requisitos del Examen:** Uso obligatorio de `smollm:360m` y funcionalidad al 100%.
*   **ISO/IEC 25010:** Estándar de calidad de software (Adecuación funcional y Eficiencia).
*   **Buenas Prácticas DevOps:** Correcta orquestación de contenedores y manejo de logs.

## 6. METODOLOGÍA Y ENFOQUE

Se utilizó un enfoque mixto (Caja Negra y Caja Blanca):
1.  **Pruebas Funcionales (Caja Negra):** Interacción directa con el Chatbot simulando ser un usuario final para validar respuestas y tiempos de latencia.
2.  **Revisión de Código (Caja Blanca):** Inspección de los archivos de configuración y logs del sistema para validar la carga del modelo.
3.  **Captura de Evidencias:** Documentación visual de los hitos clave del funcionamiento.

## 7. HALLAZGOS Y OBSERVACIONES

### Hallazgo 01: Correcta Integración del Modelo smollm:360m
*   **Descripción:** Al iniciar la conversación con el saludo "hola", el agente virtual respondió identificándose explícitamente como potenciado por `smollm:360m`.
*   **Evidencia:** Ver Anexo (Evidencia 01).
*   **Criterio:** Cumplimiento del requisito técnico principal.
*   **Criticidad:** Informativo (Positivo).

### Hallazgo 02: Funcionalidad Completa en Creación de Tickets
*   **Descripción:** Se simuló un reporte de incidente ("tengo un problema"). El sistema fue capaz de entender la intención, solicitar detalles y confirmar la creación del ticket de soporte sin errores de conexión.
*   **Evidencia:** Ver Anexo (Evidencia 02).
*   **Criterio:** Adecuación funcional del sistema.
*   **Criticidad:** Informativo (Positivo).

### Hallazgo 03: Latencia en Respuestas Generativas
*   **Descripción:** Se observó que, dependiendo de los recursos del host, el modelo puede tardar entre 5 a 10 segundos en generar respuestas largas, aunque no llega a fallar (timeout).
*   **Causa:** Ejecución de inferencia en CPU.
*   **Criticidad:** Medio (Afecta experiencia de usuario).

## 8. ANÁLISIS DE RIESGOS

| Hallazgo | Riesgo asociado | Impacto | Probabilidad | Nivel de Riesgo |
|----------|-----------------|---------|--------------|-----------------|
| H-03 (Latencia) | Abandono del usuario por tiempos de espera prolongados. | Medio | Media | Medio |
| Configuración Docker | Si el servicio Ollama no tiene persistencia, el modelo debe descargarse en cada reinicio. | Alto | Baja | Bajo |

## 9. RECOMENDACIONES

1.  **Optimización de Recursos:** Asignar más recursos de CPU/RAM al contenedor de Docker o habilitar soporte GPU (Nvidia Container Toolkit) si el hardware lo permite.
2.  **Feedback de Usuario:** Implementar indicadores de "Escribiendo..." más visibles en el Frontend para mitigar la percepción de latencia.
3.  **Persistencia:** Asegurar que el volumen de Docker para Ollama (`/root/.ollama`) esté correctamente mapeado para evitar descargas recurrentes del modelo `smollm`.

## 10. CONCLUSIONES

1.  **Sistema Operativo:** El sistema "Corporate EPIS Pilot" se ha levantado y configurado correctamente. Es funcional al 100%.
2.  **Cumplimiento de Requisitos:** Se ha verificado el uso del modelo **smollm:360m** según lo solicitado en el examen.
3.  **Integridad:** La comunicación entre el Frontend y el Backend es estable, permitiendo completar flujos de conversación complejos como la gestión de tickets.

## 11. PLAN DE ACCIÓN Y SEGUIMIENTO

| Hallazgo | Recomendación | Responsable | Fecha Comprometida |
|----------|----------------|-------------|---------------------|
| Latencia Inferencia | Evaluar implementación de soporte GPU en Docker | DevOps | 20/11/2025 |
| UX/UI Feedback | Mejorar loader en interfaz de chat | Desarrollo Frontend | 21/11/2025 |

---

## 12. ANEXOS

### Evidencia 01: Verificación de Identidad del Modelo
Captura de pantalla demostrando el saludo inicial donde el sistema confirma el uso de `smollm:360m`.

![Saludo Inicial y Modelo](/evidencias/evidencia01.png)

### Evidencia 02: Flujo de Creación de Ticket Exitoso
Captura de pantalla que valida la capacidad del sistema para procesar intenciones de usuario, mantener el contexto de la conversación y confirmar la acción de soporte (creación de ticket).

![Creación de Ticket](/evidencias/evidencia02.png)
