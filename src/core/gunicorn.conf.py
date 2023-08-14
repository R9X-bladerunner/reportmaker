import os

workers = os.cpu_count() or 1
workers = workers * 2 + 1

worker_class = "uvicorn.workers.UvicornWorker"

# обязательный паараметр для корректной работы фонового процесса
# src/core/main.py::run_scheduled
preload_app = True
