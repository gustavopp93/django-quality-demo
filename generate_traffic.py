#!/usr/bin/env python3
"""
Script para generar tráfico HTTP a la aplicación Django
y visualizar métricas en Grafana
"""

import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
import argparse


BASE_URL = "http://localhost:8080"

# Endpoints disponibles
ENDPOINTS = [
    "/",
    "/product/1/",
    "/product/2/",
    "/product/3/",
    "/product/4/",
    "/product/5/",
    "/api/products/1/",
    "/api/products/2/",
    "/api/products/3/",
    "/api/products/4/",
    "/api/products/5/",
    "/api/categories/count/",
]


def make_request(endpoint):
    """Realiza una petición HTTP al endpoint especificado"""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, timeout=10)
        status = response.status_code
        print(f"✓ {endpoint:40} -> {status}")
        return status
    except requests.exceptions.RequestException as e:
        print(f"✗ {endpoint:40} -> ERROR: {str(e)[:50]}")
        return None


def generate_traffic(num_requests=100, concurrent=5, delay=0.1):
    """
    Genera tráfico HTTP a la aplicación

    Args:
        num_requests: Número total de requests a realizar
        concurrent: Número de requests concurrentes
        delay: Delay entre requests en segundos
    """
    print(f"\n{'='*70}")
    print(f"Generando {num_requests} requests con {concurrent} workers concurrentes")
    print(f"{'='*70}\n")

    requests_made = 0
    success_count = 0
    error_count = 0

    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        for i in range(num_requests):
            # Seleccionar un endpoint aleatorio
            endpoint = random.choice(ENDPOINTS)

            # Enviar request
            future = executor.submit(make_request, endpoint)
            result = future.result()

            requests_made += 1
            if result and 200 <= result < 400:
                success_count += 1
            else:
                error_count += 1

            # Pequeño delay entre requests
            if delay > 0:
                time.sleep(delay)

            # Mostrar progreso cada 10 requests
            if (i + 1) % 10 == 0:
                print(f"\n--- Progreso: {i+1}/{num_requests} requests completados ---\n")

    # Resumen final
    print(f"\n{'='*70}")
    print(f"RESUMEN")
    print(f"{'='*70}")
    print(f"Total de requests:  {requests_made}")
    print(f"Exitosos:          {success_count}")
    print(f"Errores:           {error_count}")
    print(f"Tasa de éxito:     {(success_count/requests_made*100):.2f}%")
    print(f"{'='*70}\n")


def continuous_traffic(duration_minutes=5, requests_per_minute=60):
    """
    Genera tráfico continuo durante un período de tiempo

    Args:
        duration_minutes: Duración en minutos
        requests_per_minute: Número de requests por minuto
    """
    total_seconds = duration_minutes * 60
    delay = 60 / requests_per_minute
    num_requests = duration_minutes * requests_per_minute

    print(f"\n{'='*70}")
    print(f"Generando tráfico continuo por {duration_minutes} minutos")
    print(f"Rate: {requests_per_minute} requests/minuto")
    print(f"Total requests esperados: {num_requests}")
    print(f"{'='*70}\n")

    start_time = time.time()
    requests_made = 0

    while time.time() - start_time < total_seconds:
        endpoint = random.choice(ENDPOINTS)
        make_request(endpoint)
        requests_made += 1
        time.sleep(delay)

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"Tráfico continuo completado")
    print(f"Tiempo transcurrido: {elapsed:.2f} segundos")
    print(f"Requests realizados: {requests_made}")
    print(f"Rate real: {requests_made/(elapsed/60):.2f} requests/minuto")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generar tráfico HTTP a la aplicación Django"
    )
    parser.add_argument(
        "-n", "--num-requests",
        type=int,
        default=100,
        help="Número total de requests (default: 100)"
    )
    parser.add_argument(
        "-c", "--concurrent",
        type=int,
        default=5,
        help="Número de requests concurrentes (default: 5)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0.1,
        help="Delay entre requests en segundos (default: 0.1)"
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Modo continuo en lugar de batch"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Duración en minutos para modo continuo (default: 5)"
    )
    parser.add_argument(
        "--rpm",
        type=int,
        default=60,
        help="Requests por minuto en modo continuo (default: 60)"
    )

    args = parser.parse_args()

    if args.continuous:
        continuous_traffic(args.duration, args.rpm)
    else:
        generate_traffic(args.num_requests, args.concurrent, args.delay)
