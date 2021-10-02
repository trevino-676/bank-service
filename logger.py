import logging

logger = logging.getLogger("account-statments-service")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter(
        "[%(levelname)s] - %(asctime)s - %(message)s", datefmt="%d-%b_%y %H:%M:%S"
    )
)

logger.addHandler(console_handler)

