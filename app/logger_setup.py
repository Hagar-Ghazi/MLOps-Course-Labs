"""
Logging configuration.
"""

import logging


def setup_logging():
    # Set up basic logging with level INFO using logging.basicConfig()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Create a named logger using logging.getLogger() and return it
    logger = logging.getLogger("churn_api")
    return logger


# ====================================================
# HyperDX
# ====================================================

# import logging
# import os

# def setup_logging():
#     logging.basicConfig(
#         level  = logging.INFO,
#         format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#     )

#     # HyperDX integration via OpenTelemetry
#     try:
#         from opentelemetry._logs import set_logger_provider
#         from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
#         from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
#         from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

#         provider = LoggerProvider()
#         exporter = OTLPLogExporter(
#             endpoint = "https://in-otel.hyperdx.io",
#             headers = {"authorization": os.environ.get("HYPERDX_API_KEY", "")}
#         )
#         provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
#         set_logger_provider(provider)

#         handler = LoggingHandler(logger_provider=provider)
#         logging.getLogger().addHandler(handler)
#     except Exception:
#         pass  # Gracefully degrade if HyperDX isn't configured

#     return logging.getLogger("churn_api")
