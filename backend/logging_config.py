log_level = "DEBUG"
log_path = "logs"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "{asctime} {levelname} {name} {message}", "style": "{"}},
    "handlers": {
        "console": {"level": log_level, "class": "logging.StreamHandler", "formatter": "standard", "filters": []},
        "backend": {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": f"{log_path}/backend.log",
        },
    },
    "loggers": {
        "": {  # catch all. all logs go here
            "level": log_level,
            "handlers": ["backend"],
        },
    },
}
