# Tarea 1 - Sistema Distribuido de Análisis de Preguntas y Respuestas

## Descripción del Proyecto
Sistema distribuido que compara y analiza la calidad de respuestas generadas por un LLM frente a respuestas humanas del dataset de Yahoo! Answers. La plataforma implementa un pipeline modular con cache, evaluación de calidad y almacenamiento persistente.

## Objetivos Cumplidos

### Requisitos Funcionales
- [x] **Dataset Yahoo! Answers**: 20,001 registros procesados
- [x] **Generador de Tráfico Sintético**: 3 distribuciones implementadas
- [x] **Sistema de Cache**: Configurable con políticas LRU/LFU
- [x] **Métrica de Calidad**: Similitud coseno con embeddings TF-IDF
- [x] **Almacenamiento Persistente**: SQLite con +20K registros
- [x] **Arquitectura en Contenedores**: Docker Compose

### Componentes del Sistema

| Servicio | Puerto | Descripción | Tecnología |
|----------|--------|-------------|------------|
| **g_trafico** | 5000 | Generador de tráfico y orquestador | Python/Flask |
| **cache** | 5001 | Sistema de cache en memoria | Python/Flask |
| **llm** | 5002 | Integración con modelo LLM | Python/Flask |
| **puntaje** | 5003 | Cálculo de similitud de respuestas | Python/Flask/sklearn |
| **almacenamiento** | 5004 | Base de datos y persistencia | Python/Flask/SQLite |
| **ollama** | 11434 | Servidor de modelos LLM | Ollama |

## Instalación y Despliegue Rápido

### Prerrequisitos
- Docker
- Docker Compose
- 4GB RAM mínimo (para Ollama)

### 1. Clonar y Ejecutar
```bash
git clone <repositorio>
cd tareap2_sd
docker-compose up --build
