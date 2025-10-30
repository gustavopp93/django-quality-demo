#!/bin/bash

# Script simple para generar tráfico con curl

BASE_URL="http://localhost:8080"

# Array de endpoints
endpoints=(
    "/"
    "/product/1/"
    "/product/2/"
    "/product/3/"
    "/product/4/"
    "/product/5/"
    "/api/products/1/"
    "/api/products/2/"
    "/api/products/3/"
    "/api/products/4/"
    "/api/products/5/"
    "/api/categories/count/"
)

# Número de requests (default 1000)
NUM_REQUESTS=${1:-1000}

echo "Generando $NUM_REQUESTS requests..."

for i in $(seq 1 $NUM_REQUESTS); do
    # Seleccionar endpoint aleatorio
    endpoint=${endpoints[$RANDOM % ${#endpoints[@]}]}

    # Hacer request
    curl -s -o /dev/null -w "Request $i: %{url_effective} -> %{http_code}\n" "$BASE_URL$endpoint"

    # Pequeño delay opcional (descomentar si quieres)
    # sleep 0.01
done

echo "Completado: $NUM_REQUESTS requests enviados"
