from fastapi import FastAPI, UploadFile, File, Request
from PIL import Image
import numpy as np
import io
import psutil
import time
from prometheus_client import Counter, Gauge, start_http_server
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

# Create and configure the FastAPI app
app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Prometheus Metrics Definitions
REQUEST_COUNTER = Counter('api_requests_total', 'Total number of API requests', ['client_ip'])
RUN_TIME_GAUGE = Gauge('api_run_time_seconds', 'Running time of the API')
TL_TIME_GAUGE = Gauge('api_tl_time_microseconds', 'Time per pixel in microseconds')
MEMORY_USAGE_GAUGE = Gauge('api_memory_usage', 'Memory usage of the API process in KB')
CPU_USAGE_GAUGE = Gauge('api_cpu_usage_percent', 'CPU usage percentage of the API process')
NETWORK_BYTES_SENT_GAUGE = Gauge('api_network_bytes_sent', 'Network bytes sent by the API process')
NETWORK_BYTES_RECV_GAUGE = Gauge('api_network_bytes_received', 'Network bytes received by the API process')

def process_memory_usage():
    """Returns the current memory usage of the process in kilobytes."""
    return psutil.virtual_memory().used / 1024

def format_and_process_image(image_bytes):
    """Process the uploaded image file and prepare it for digit prediction."""
    image = Image.open(io.BytesIO(image_bytes))
    resized_image = image.resize((28, 28)).convert("L")
    return np.array(resized_image).flatten()

@app.post("/predict/")
async def predict_image(request: Request, file: UploadFile = File(...)):
    """Endpoint to predict a digit from an uploaded image."""
    start_time = time.time()
    memory_usage_start = process_memory_usage()

    image_bytes = await file.read()
    image_data = format_and_process_image(image_bytes)
    predicted_digit = str(np.random.randint(0, 10))  # Placeholder for a model prediction

    run_time = time.time() - start_time
    memory_usage_end = process_memory_usage()

    # Update Prometheus metrics
    client_ip = request.client.host
    REQUEST_COUNTER.labels(client_ip=client_ip).inc()
    RUN_TIME_GAUGE.set(run_time)
    TL_TIME_GAUGE.set((run_time / len(image_bytes)) * 1e6)
    MEMORY_USAGE_GAUGE.set(np.abs(memory_usage_end - memory_usage_start))
    CPU_USAGE_GAUGE.set(psutil.cpu_percent(interval=None))
    net_io = psutil.net_io_counters()
    NETWORK_BYTES_SENT_GAUGE.set(net_io.bytes_sent)
    NETWORK_BYTES_RECV_GAUGE.set(net_io.bytes_recv)

    return {"predicted_digit": predicted_digit}

if __name__ == "__main__":
    start_http_server(8001)
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True, workers=1)
