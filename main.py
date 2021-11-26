import logging
import uvicorn

from server.rpc import RunRpc


def RunApi():
    uvicorn.run(
        "server.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )


if __name__ == "__main__":
    logging.basicConfig()
    RunApi()
    # RunRpc()
