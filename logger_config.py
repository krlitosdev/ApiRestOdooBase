import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("fastapi")