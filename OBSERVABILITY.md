# Observability Stack Setup

Este proyecto está configurado con **Grafana Alloy** y **OpenTelemetry** para una observabilidad completa.

## Arquitectura

```
Django App (OpenTelemetry SDK)
           ↓
    Grafana Alloy (Collector)
           ↓
    ┌──────┼────────┐
    ↓      ↓        ↓
  Loki   Tempo   Prometheus
 (Logs) (Traces) (Metrics)
    ↓      ↓        ↓
       Grafana
```

## Componentes

### 1. OpenTelemetry en Django
- **SDK**: Instrumentación automática de Django y PostgreSQL
- **Exportador OTLP**: Envía traces, logs y métricas a Alloy
- **Configuración**: `qualitydemo/otel_config.py`

### 2. Grafana Alloy
- **Puerto 4318**: OTLP HTTP receiver
- **Puerto 12345**: Alloy UI
- **Configuración**: `alloy-config.alloy`

### 3. Datos recolectados

#### Traces (Tempo)
- Peticiones HTTP a Django
- Queries a PostgreSQL
- Middleware execution
- View processing time

#### Logs (Loki)
- Logs estructurados de Django (JSON)
- Logs de nginx (access y error)
- Logs de contenedores Docker

#### Metrics (Prometheus)
- Métricas HTTP (latencia, status codes)
- Métricas de base de datos
- Métricas de OpenTelemetry

## Inicio rápido

### 1. Instalar dependencias

```bash
uv sync
```

### 2. Levantar servicios

```bash
docker compose up -d
```

### 3. Verificar servicios

- **Django**: http://localhost:8080
- **Alloy UI**: http://localhost:12345
- **Grafana**: http://localhost:3000 (en grafana-demo)

### 4. Generar tráfico

```bash
# Genera peticiones para ver traces y logs
./generate_traffic.sh
```

## Variables de entorno

```bash
ENABLE_OTEL=true                                    # Habilitar OpenTelemetry
OTEL_SERVICE_NAME=django-quality-demo              # Nombre del servicio
OTEL_SERVICE_VERSION=0.1.0                         # Versión del servicio
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4318     # Endpoint de Alloy (HTTP)
OTEL_ENVIRONMENT=development                       # Entorno
```

## Visualización en Grafana

### Ver Traces
1. Ve a Grafana → Explore
2. Selecciona datasource **Tempo**
3. Busca traces por:
   - Service name: `django-quality-demo`
   - Operation: `GET /products/`
   - Duration: `> 100ms`

### Ver Logs
1. Ve a Grafana → Explore
2. Selecciona datasource **Loki**
3. Query ejemplo:
   ```logql
   {job="django"} | json | level="info"
   ```

### Correlación Traces + Logs
Los traces incluyen `trace_id` que permite correlacionar con logs automáticamente en Grafana.

## Troubleshooting

### Ver logs de Alloy
```bash
docker compose logs alloy -f
```

### Verificar que Django envía datos
```bash
docker compose logs web | grep "OpenTelemetry configured"
```

### Verificar conectividad con Loki/Tempo
```bash
# Desde el contenedor de Alloy
docker compose exec alloy wget -O- http://loki:3100/ready
docker compose exec alloy wget -O- http://tempo:3200/ready
```

## Stack de Observabilidad

Este proyecto usa **solo OpenTelemetry + Alloy**:

| Componente | Protocolo | Puerto |
|-----------|----------|--------|
| Django → Alloy | OTLP HTTP | 4318 |
| Alloy → Tempo | OTLP HTTP | 4318 |
| Alloy → Loki | HTTP | 3100 |
| Alloy → Prometheus | HTTP | 9090 |

**Nota**: No usamos gRPC ni Zipkin, solo OTLP HTTP nativo.

## Referencias

- [Grafana Alloy Docs](https://grafana.com/docs/alloy/latest/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [OpenTelemetry Django](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html)
