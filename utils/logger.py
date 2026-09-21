import logging


def configurer_logging() -> None:
    # Configure le niveau et le format des logs de l'application
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
