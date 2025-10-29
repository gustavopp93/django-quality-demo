# Nginx + Gunicorn + Prometheus Exporter Setup

## Arquitectura

```
Cliente → Nginx (puerto 8080) → Gunicorn (puerto 8000) → Django App
                ↓
        Nginx Prometheus Exporter (puerto 9113) → Prometheus (localhost:9090)
```

## Componentes

### 1. Gunicorn
- Servidor WSGI para Django
- Configurado en `gunicorn.conf.py`
- Corre en el puerto 8000 (interno al contenedor)

### 2. Nginx
- Proxy reverso que recibe las peticiones del cliente
- Sirve archivos estáticos y media
- Expone el endpoint `/metrics` para stub_status
- Corre en el puerto 8080 (mapeado al puerto 80 interno del contenedor)

### 3. Nginx Prometheus Exporter
- Consume las métricas de nginx desde `/metrics`
- Exporta las métricas en formato Prometheus
- Corre en el puerto 9113

## Configuración de Prometheus

Para que Prometheus pueda scrapear las métricas del nginx-exporter, necesitas agregar el siguiente job a tu archivo de configuración de Prometheus:

```yaml
scrape_configs:
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
        labels:
          service: 'qualitydemo-nginx'
          environment: 'development'
```

### Si Prometheus está en tu máquina local

Agrega el contenido del archivo `prometheus.yml` a tu configuración de Prometheus en `localhost:9090`.

### Si Prometheus está en Docker

Modifica el archivo `docker-compose.yml` para agregar Prometheus como servicio y usa `nginx-exporter:9113` como target en lugar de `localhost:9113`.

## Uso

### 1. Instalar dependencias
```bash
uv sync
```

### 2. Levantar los servicios
```bash
docker-compose up --build
```

### 3. Verificar que todo funciona

- **Aplicación Django**: http://localhost:8080
- **Nginx health check**: http://localhost:8080/health
- **Nginx stub_status**: http://localhost:8080/metrics
- **Nginx Prometheus metrics**: http://localhost:9113/metrics
- **Prometheus UI**: http://localhost:9090

### 4. Consultar métricas en Prometheus

Ve a http://localhost:9090 y prueba las siguientes queries:

```promql
# Conexiones activas de nginx
nginx_connections_active

# Peticiones totales
nginx_http_requests_total

# Tasa de peticiones por segundo
rate(nginx_http_requests_total[5m])

# Conexiones aceptadas
nginx_connections_accepted
```

## Métricas disponibles

El nginx-prometheus-exporter expone las siguientes métricas:

- `nginx_connections_active` - Número de conexiones activas
- `nginx_connections_accepted` - Total de conexiones aceptadas
- `nginx_connections_handled` - Total de conexiones manejadas
- `nginx_http_requests_total` - Total de peticiones HTTP
- `nginx_connections_reading` - Conexiones leyendo headers
- `nginx_connections_writing` - Conexiones escribiendo respuestas
- `nginx_connections_waiting` - Conexiones en espera (keepalive)

## Troubleshooting

### El exporter no puede conectarse a nginx
Verifica que nginx esté exponiendo el endpoint `/metrics`:
```bash
docker exec -it qualitydemo-nginx curl http://localhost:80/metrics
```

O desde tu máquina local:
```bash
curl http://localhost:8080/metrics
```

### Prometheus no puede scrapear las métricas
1. Verifica que el exporter esté corriendo: `docker ps | grep nginx-exporter`
2. Verifica que el exporter exponga métricas: `curl http://localhost:9113/metrics`
3. Revisa los logs de Prometheus para ver errores de scraping
