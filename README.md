
# Monitoring FastAPI with Prometheus and Grafana

## Introduction
This document outlines the setup and monitoring of a FastAPI application using Prometheus for gathering metrics and Grafana for displaying those metrics.

## Installation Requirements
Ensure Docker and WSL are installed on your system.

Use the command `docker-compose up --build` to initiate both the FastAPI application and the Grafana dashboard.

## Application Structure and Metrics Collection
Find the FastAPI application code in `main.py` located at `root/src/app/`. Configure Prometheus using the `prometheus.yml` in `root/prometheus_data`. Place both `Dockerfile` and `requirements.txt` in the `src` directory, with `docker-compose.yml` at the root level.

### Metrics Tracked:
   - **Client IP Request Count:** Logs the number of requests from different IPs.
   - **Total API Response Time:** Records the duration to fulfill requests.
   - **Character Processing Time:** Measures the time taken to process each character.
   - **CPU Consumption:** Tracks CPU usage of the FastAPI app.
   - **Memory Usage:** Monitors the memory consumption.
   - **Data Transfer Volumes:** Logs the bytes sent and received.
   - **Data Transfer Speed:** Measures the rate of data transfer.

Use Grafana to visualize these metrics for better insights into application performance.

## Maintenance and Upgrades
Modify the code as necessary, updating the `requirements.txt` with new dependencies. To reflect these changes, rebuild your Docker environment using the command `docker-compose up --build`.

When finished, use `docker-compose down` to terminate the setup. If experiencing high memory or disk usage, consider using `wsl --shutdown` via an elevated command prompt to free up resources.

## Useful Resources
- [Introduction to Monitoring FastAPI with Grafana and Prometheus](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn)
- [Access FastAPI's Swagger UI at Multiple Ports](http://127.0.0.1:8002/docs)
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
