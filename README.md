# Tarea 1 - Sistema Distribuido de Análisis de Preguntas y Respuestas

## Descripción del Proyecto
Sistema distribuido que compara y analiza la calidad de respuestas generadas por un LLM frente a respuestas humanas del dataset de Yahoo! Answers. La plataforma implementa un pipeline modular con cache, evaluación de calidad y almacenamiento persistente.

## Objetivos Cumplidos

### Requisitos Funcionales
- [x] **Dataset Yahoo! Answers**: 20,001 registros procesados
- [x] **Generador de Tráfico Sintético**: 2 distribuciones implementadas (Zipf y Poisson)
- [x] **Sistema de Cache**: Configurable con políticas LRU/FIFO
- [x] **Métrica de Calidad**: Similitud coseno con embeddings TF-IDF
- [x] **Almacenamiento Persistente**: SQLite
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

# Tecnologías Utilizadas

## Backend y APIs
- **Python 3.11** - Lenguaje de desarrollo
- **Flask** - Framework web para los microservicios
- **Requests** - Cliente HTTP para comunicación entre servicios
- **Scikit-learn** - Para cálculo de similitud coseno y TF-IDF

## Base de Datos y Almacenamiento
- **SQLite** - Base de datos
- **Pandas** - Procesamiento y carga de datasets

## Cache y Optimización
- **Collections.OrderedDict** - Implementación de cache en memoria
- **Políticas LRU/LFU** - Mecanismos de evicción configurables

## Modelo de Lenguaje
- **Ollama** - Plataforma para ejecución local de LLMs
- **TinyLLama** - Modelo de lenguaje

## Contenerización y Despliegue
- **Docker** - Contenerización de aplicaciones
- **Docker Compose** - Orquestación de múltiples servicios

## Desarrollo y Calidad de Código
- **JQ** - Procesamiento de JSON en línea de comandos
- **CURL** - Testing de endpoints HTTP

---


### 1. Clonar y Ejecutar
```bash
git clone <repositorio>
cd tareap2_sd
docker compose up -d --build
```

### 2. Inicializar base de datos
```bash
curl -X POST http://localhost:5004/init
```

### 3. Realizar consultas
```bash
curl "http://localhost:5004/consulta?dist=zipf&alpha=1.2" #para usar distribucion Zipf

curl "http://localhost:5000/consulta?dist=poisson&lambda=10" #para usar distribucion Poisson
```
### 4. Revisar estadísticas
```bash
curl -s http://localhost:5001/stats | jq
```
