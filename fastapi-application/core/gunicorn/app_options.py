from typing import Any


def get_app_options(
        host:str,
        port:int,
        workers:int,
        timeout:int,
) -> dict[str, Any]:
    return {
        "bind": f"{host}:{port}",
        "timeout": timeout,
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "access_log":"-",
        "error_log":"-",
    }