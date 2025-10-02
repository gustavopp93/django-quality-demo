# Django Quality Demo

Este es un proyecto Django de demostración diseñado para mostrar cómo configurar y ejecutar pruebas con coverage para enviar reportes a SonarQube.


## Características

-  Django 5.2.6
-  Gestión de dependencias con `uv`
-  Tests con `pytest` y `pytest-django`
-  Coverage con `pytest-cov`
-  Configuración centralizada en `pyproject.toml`
-  Cobertura de pruebas ~75% (intencional)
-  Code smells incluidos para demostración

## Requisitos

- Python 3.12.11+
- `uv` (gestor de paquetes)

## Instalación

### 1. Instalar uv

Si no tienes `uv` instalado:

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clonar y configurar el proyecto

```bash
# Clonar el repositorio (o navegar al directorio)
cd django-quality-demo

# Instalar dependencias de producción
uv sync

# Instalar dependencias de desarrollo (pytest, ruff, etc.)
uv sync --group dev

# Aplicar migraciones
uv run python manage.py migrate
```

## Ejecución de Tests

### Ejecutar todas las pruebas

```bash
uv run pytest
```

### Ejecutar pruebas con coverage

```bash
uv run pytest --cov
```

### Generar reporte HTML de coverage

```bash
uv run pytest --cov --cov-report=html
```

Los reportes se generan en:
- **Terminal**: Reporte básico en consola
- **XML**: `coverage.xml` (para SonarQube)
- **HTML**: `htmlcov/index.html` (para visualización web)

## Estructura del Proyecto

```
django-quality-demo/
   products/                 # App principal
      models.py            # Modelos Product y Category
      views.py             # Vistas y API endpoints
      utils.py             # Utilidades y helpers
      helpers.py           # Code smells intencionales
      test_*.py            # Tests organizados por módulo
      urls.py              # URLs de la app
   qualitydemo/             # Configuración Django
      settings.py
      urls.py
   pyproject.toml           # Configuración central
   coverage.xml             # Reporte XML para SonarQube
   htmlcov/                 # Reportes HTML
   README.md
```

## APIs Disponibles

El proyecto incluye algunos endpoints de API para pruebas:

- `GET /api/products/{id}/` - Obtener producto por ID
- `GET /api/categories/count/` - Contador de productos por categoría

## Coverage Actual

El proyecto está diseñado para tener **~75% de cobertura** intencionalmente:

-  Modelos: ~97% de cobertura
-   Views: ~54% de cobertura (algunas vistas no testeadas)
-   Utils: ~66% de cobertura (algunas funciones sin tests)

## Code Smells Incluidos

Para demostración de análisis de calidad, se incluyen intencionalmente:

- Funciones complejas con anidamiento excesivo
- Funciones no utilizadas
- Código duplicado
- Métodos largos
- Condicionales complejas

## Integración con SonarQube

### Configuración Local de SonarQube

1. **Ejecutar SonarQube con Docker:**

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
```

2. **Generar reporte de coverage:**

```bash
uv run pytest --cov --cov-report=xml
```

3. **Configurar `sonar-project.properties`:**

```properties
sonar.projectKey=django-quality-demo
sonar.projectName=Django Quality Demo
sonar.projectVersion=1.0
sonar.sources=products,qualitydemo
sonar.exclusions=**/migrations/**,**/test_*.py
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=test-results.xml
```

4. **Ejecutar análisis:**

```bash
sonar-scanner
```

## Comandos Útiles

```bash
# Desarrollo
uv run python manage.py runserver

# Tests específicos
uv run pytest products/test_models.py
uv run pytest products/test_views.py -v

# Coverage con filtros
uv run pytest --cov=products --cov-report=term-missing

# Crear nuevas migraciones
uv run python manage.py makemigrations

# Shell de Django
uv run python manage.py shell
```

## Estructura de Tests

- `test_models.py`: Tests de modelos Django
- `test_views.py`: Tests de vistas y APIs
- `test_utils.py`: Tests de funciones utilitarias

## Notas para el Equipo

Este proyecto está configurado específicamente para:

1. **Demostrar integración con SonarQube**
2. **Mostrar métricas de calidad realistas** (~75% coverage)
3. **Incluir code smells para análisis**
4. **Usar herramientas modernas** (`uv`, `pytest`)

¡El objetivo es aprender y mejorar la calidad del código!