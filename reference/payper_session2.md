# Payper / Zendesk — SAGE Session 2
**Account:** Payper - Bagging & Palletizing Solutions
**Meeting Date:** April 16, 2026
**Plan:** Suite Professional + Sell
**Participants:** Manuel Méndez (Zendesk), Joan Feixas, Lara Offermann (Payper)

---

## Customer Goals Analysis

> **What's already working:** The SAT incident management operation is described as fairly unified, centralized, and standardized — they are not looking to redesign something that's broken.

---

### 1. Reporting que hoy sienten distorsionado

| Subgoal | Evidence from Transcript |
|---|---|
| Tener métricas de primera respuesta más fiables | "De aquí elimino de este análisis los que están marcados como voice… porque me desvirtúan el kpi" |
| Evitar que los tickets creados por ellos mismos distorsionen el tiempo de primera respuesta | "Cuando nosotros creamos un ticket de cero… según Zendesk hemos tardado tres días" |
| Medir mejor el tiempo de primera resolución para averías e incidencias | "He creado una vista nueva… que le llamo el tiempo de primera resolución" |
| Entender mejor cómo medir por grupo y categoría sin ajustes manuales | "Utilizo este efficiency y lo analizo por cada uno de los grupos" |

---

### 2. Conocimiento técnico disperso y poco reutilizable

| Subgoal | Evidence from Transcript |
|---|---|
| Tener una base de conocimiento estructurada para soporte técnico | "No tenemos una base de conocimiento donde tenemos nuestros documentos… no está estructurado ni organizado" |
| Poder consultar documentación técnica sin salir del ticket | "La inteligencia artificial me podría buscar de forma automática en una documentación que tengo en Sharepoint, en un servidor o donde sea" |
| Convertir soluciones repetidas en conocimiento reutilizable | "La solución que nosotros aplicamos… no la documentamos" |
| Preparar una base para usar IA con valor práctico | "La base de conocimiento es la cama de todo lo que viene ahora con ia" |

---

### 3. Procesos manuales que sienten básicos o arcaicos

| Subgoal | Evidence from Transcript |
|---|---|
| Identificar formas más directas o ágiles de trabajar en Zendesk | "Seguramente alguna cosa la estamos haciendo con algún proceso muy arcaico" |
| Revisar automatizaciones útiles sin perder la lógica operativa actual | "Lo estamos utilizando en lo básico, pero seguramente hay muchas cosas que no estamos aprovechando" |
| Encontrar mejoras concretas en eficiencia y productividad | "Traerles cuestiones que puedan eficientizar y sacarle partido a lo que tiene" |

---

### 4. Gestión multicanal con fricciones operativas concretas

| Subgoal | Evidence from Transcript |
|---|---|
| Reducir líos por tickets duplicados cuando el cliente abre un hilo nuevo | "Se nos crea otro ticket de lo mismo entonces tenemos que fusionar" |
| Entender si hay forma de reducir confusión por replies que Zendesk interpreta como comentario interno | "Detecta que debe ser un comentario interno… y claro al final también nos confunden un poco" |
| Mejorar la experiencia con adjuntos enviados como link | "Muchos clientes… nos responden no he recibido la oferta" |
| Mantener trazabilidad entre SAT y recambios sin perder contexto | "Utilizamos también la opción del link ticket" |

---

### 5. Uso más intencional de Sell para proactividad comercial

| Subgoal | Evidence from Transcript |
|---|---|
| Entender mejor cómo usar Sell para oportunidades | "Nos cuesta un poco entender cómo crear un link, un trick" |
| Pasar de un enfoque reactivo a uno más proactivo | "Somos un departamento de reactivo" |
| Incorporar recordatorios o alarmas para seguimiento comercial | "No sé… cómo está relacionado con alarmas" |

---

> **Key Insight:** Payper no está buscando rediseñar un proceso que hoy esté roto. Está buscando identificar dónde Zendesk ya puede reducir trabajo manual, ordenar el conocimiento técnico y dar métricas más limpias para operar mejor.

---

## Recommendations

### Reporting que hoy sienten distorsionado

| # | Recommendation | Why It Fits |
|---|---|---|
| 1 | Rediseñar los reportes de primera respuesta separando email de voice y excluyendo los tickets iniciados por agente | Hoy están corrigiendo el KPI manualmente porque voice y tickets creados por ellos distorsionan la lectura. En su caso, el canal importa mucho porque el volumen principal viene por email, llamadas y WhatsApp. |
| 2 | Crear un dashboard operativo por grupo y categoría, con vistas separadas para primera respuesta y primera resolución | Ya construyeron un cálculo propio para primera resolución, señal de que la necesidad existe. Tener ambos indicadores separados evita mezclar velocidad de contestación con tiempo real de resolución. |
| 3 | Revisar el uso del SLA como alarma operativa y acompañarlo con reporting de vencimientos | Ya usan SLA como recordatorio de respuesta en cuatro días. Tiene sentido mantenerlo, pero complementarlo con reporting para ver dónde se acumulan riesgos antes de vencer. |

### Conocimiento técnico disperso y poco reutilizable

| # | Recommendation | Why It Fits |
|---|---|---|
| 1 | Lanzar un primer Help Center con borradores generados desde el histórico reciente | Dijeron que hoy no documentan soluciones y que el conocimiento está disperso. Esto reduce el esfuerzo inicial y les da una base rápida para empezar. |
| 2 | Conectar sus fuentes existentes de conocimiento para que agentes consulten contenido desde el contexto del ticket | Joan describió justo la fricción de salir del ticket para buscar documentación. Esto ataca ese cambio de pantalla y mantiene al agente dentro del flujo de trabajo. |
| 3 | Activar un proceso ligero para convertir soluciones repetidas en artículos reutilizables | La conversación mostró que hoy resuelven pero no convierten esa resolución en conocimiento. Sin ese paso, ni agentes ni IA pueden reutilizar lo aprendido. |
| 4 | Preparar la base de conocimiento para IA agente, empezando por preguntas simples y repetitivas | Hoy ya tienen AI agent Essential disponible en su plan para consultas informativas basadas en conocimiento. Además, desde el 27 de abril empieza el despliegue de capacidades más avanzadas sin coste adicional, así que ordenar la base ahora les prepara para eso. |

### Procesos manuales que sienten básicos o arcaicos

| # | Recommendation | Why It Fits |
|---|---|---|
| 1 | Revisar automatizaciones pequeñas alrededor de clasificación, seguimiento y avisos, sin tocar la asignación manual | Ellos mismos dijeron que la asignación manual no les genera problema. La oportunidad no está en forzar routing automático, sino en quitar pasos manuales alrededor del trabajo. |
| 2 | Estandarizar el uso de macros para respuestas repetitivas y conectarlas al esfuerzo de conocimiento | En la llamada salió que hay respuestas repetitivas y macros posibles. Esto conecta eficiencia diaria con la futura base de conocimiento, en lugar de tratarlas como cosas separadas. |
| 3 | Activar sugerencias de tickets relacionados y revisión de duplicados | Hoy ya fusionan tickets cuando el cliente abre hilos nuevos. Esta recomendación encaja porque el problema no es el proceso de soporte, sino la duplicidad creada por el comportamiento del cliente. |

### Gestión multicanal con fricciones operativas concretas

| # | Recommendation | Why It Fits |
|---|---|---|
| 1 | Mantener side conversations para colaboración interna y formalizar cuándo usar child tickets entre SAT y recambios | Ya están usando ambos patrones de forma bastante correcta. La mejora aquí es consistencia operativa y trazabilidad, no cambiar de enfoque. |
| 2 | Revisar la configuración de linked work entre ticket principal y tickets hijos para asegurar visibilidad de estado | Comentaron que parte del valor está en ver el flujo ligado entre servicio y recambios. Esta recomendación refuerza esa trazabilidad entre áreas. |
| 3 | Evaluar una app de Marketplace para mejorar la visualización de adjuntos en emails salientes | La fricción con adjuntos salió de forma muy concreta y repetida. No hay una solución nativa clara, así que la mejor vía es validar app o alternativa técnica específica. |

### Uso más intencional de Sell para proactividad comercial

| # | Recommendation | Why It Fits |
|---|---|---|
| 1 | Tratar Sell como una línea de trabajo separada, con una sesión dedicada a pipeline, seguimiento y recordatorios | El propio cliente dijo que van "un poco flojitos" y que quieren hablar de proactividad comercial. Es una necesidad real, pero quedó fuera del foco principal de soporte en esta llamada. |
| 2 | Priorizar primero el vínculo operativo entre tickets y oportunidades antes de expandir procesos más amplios en Sell | En la conversación mencionaron relación ticket a Sell y dudas sobre alarmas y seguimiento. Tiene sentido empezar por ese punto concreto antes de abrir una transformación comercial mayor. |

---

### Gaps and Escalations

| Customer Need | Status | Suggested Path |
|---|---|---|
| Diseño detallado de reporting para voice y tickets creados por agente | Needs support | Validar con Advocacy o CX Analytics la lógica exacta del dataset y filtros |
| Solución para que los adjuntos no se envíen como link en email | Gap | Revisar Marketplace o alternativa técnica específica |
| Adopción y diseño de uso de Sell | Needs SA review | Tratarlo en sesión separada con especialista de Sell |

---

## Slide Guide

*Reference deck: Scaled CS 2025 Slides*

### Conocimiento técnico disperso y poco reutilizable

| Slide Title | Notes |
|---|---|
| Scaling Smarter with Zendesk Knowledge | Buena slide de apertura para aterrizar el problema actual: conocimiento existe, pero está disperso y no reutilizable. |
| Your Current Approach | Úsala para reflejar exactamente lo que dijeron: documentación en servidor, fuera de Zendesk, no estructurada. |
| Confidently scale self-service with Knowledge | Resume bien el cambio que quieren hacer, pasar de conocimiento disperso a conocimiento útil para agentes y clientes. |
| Skip the blank page, build articles instantly with AI | Muy relevante porque reduce el miedo al esfuerzo inicial de crear base de conocimiento. |
| Connect your external knowledge seamlessly with AI | Es la slide más ajustada a su caso si el conocimiento sigue viviendo fuera de Zendesk. |
| Empower the agents closest to customers | Conecta directamente con el dolor de no tener que salir del ticket para buscar información. |
| Leverage AI agents to boost automated resolutions | Úsala solo como visión de siguiente paso, después de explicar la base de conocimiento. |
| Turn insights into impact | Cierra bien el bloque mostrando que conocimiento también se puede medir. |

### Reporting que hoy sienten distorsionado

| Slide Title | Notes |
|---|---|
| Turn insights into impact | Es la mejor slide encontrada para conectar el problema de KPIs distorsionados con un enfoque más limpio de reporting. |
| Before we meet again | Puede servir para pedirles ejemplos concretos de métricas, categorías y excepciones que hoy ajustan manualmente. |

### Procesos manuales que sienten básicos o arcaicos

| Slide Title | Notes |
|---|---|
| Why Businesses Turn to Zendesk Guide for Smarter Self-Service | Funciona como slide de valor general si quieres hablar de eficiencia sin irte directo a detalle técnico. |
| Confidently scale self-service with Knowledge | Puede servir también para enmarcar quick wins operativos y reducir trabajo repetitivo. |

### Gestión multicanal con fricciones operativas concretas

| Slide Title | Notes |
|---|---|
| Your Current Approach | Te deja recoger las fricciones que mencionaron: duplicados, adjuntos por link, comentarios internos mal interpretados. No hay una slide específica mejor en los decks revisados para este tema. |

### Uso más intencional de Sell para proactividad comercial

| Slide Title | Notes |
|---|---|
| N/A | No se encontró una CTA deck específica de Sell. Tratar fuera de esta presentación o en una sesión separada. |

---

## Success Plan

**Objective:** Centralizar el conocimiento técnico, limpiar la lectura operativa de métricas y reducir trabajo manual en soporte, sin romper el modelo actual de operación entre SAT y recambios.

| Goals | Strategies | Resources | Outcomes & Timeline |
|---|---|---|---|
| Ordenar conocimiento | Lanzar borradores iniciales · Conectar contenido existente · Validar artículos más repetidos | Connecting external knowledge sources to your Zendesk account · Connecting Google Drive as an external knowledge source | Base útil en **30–45 días** |
| Ayudar al agente | Usar conocimiento en ticket · Consultar contexto lateral · Reutilizar respuestas frecuentes | Configuring the context panel in the Zendesk Agent Workspace · Using the context panel | Menos búsquedas fuera del ticket, **30 días** |
| Limpiar KPIs | Separar métricas por canal · Revisar primera respuesta · Crear dashboard operativo | Explore recipe: How to report on first reply time in Zendesk · Explore recipe: First reply time heatmap | KPIs más fiables, **30–45 días** |
| Reducir duplicados | Activar sugerencias de relación · Mejorar revisión de duplicados · Estandarizar fusión | Turning on merging suggestions for tickets · Merging related tickets based on suggestions · Merging tickets | Menos ruido operativo, **30 días** |
| Preparar IA | Empezar con FAQs simples · Probar respuestas automáticas informativas · Expandir tras rollout | Announcing expanded access to AI agent capabilities for all Zendesk customers · Using generative search to provide AI-powered answers to search queries | Primeros casos con IA, **45–60 días** |

### Additional Resources

- **Analyzing your help center knowledge base activity** — útil cuando quieran medir uso y evolución de conocimiento.
- **Using side conversation child tickets** — útil para afinar la trazabilidad entre SAT y recambios.

---

### Next Steps — What to Do First

| # | Action | Why First |
|---|---|---|
| 1 | Identificar dónde vive hoy el conocimiento técnico prioritario | Sin eso no conviene decidir entre Help Center nativo y conexión externa |
| 2 | Seleccionar 10 consultas repetitivas de SAT y recambios | Eso define el primer lote de artículos y casos de automatización |
| 3 | Revisar el dashboard actual de primera respuesta con exclusiones por canal | Es el ajuste más inmediato para limpiar lectura operativa |
| 4 | Activar y probar sugerencias de tickets relacionados | Ataca una fricción diaria sin cambiar el flujo principal |
| 5 | Elegir un caso simple de IA basado en conocimiento | Permite probar valor sin entrar aún en automatizaciones complejas |
