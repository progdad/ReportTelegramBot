from __future__ import annotations
import logging
import os


async def set_logger(namespace: str, uid: int) -> logging.Logger:
    logger = logging.getLogger(namespace)
    logger.setLevel(logging.DEBUG)

    fmt = f"%(asctime)s :: %(name)s :: %(levelname)s :: UI:{uid} :: %(message)s"
    _format = logging.Formatter(
        fmt=fmt,
        datefmt="%Y-%m-%d,%H:%M:%S"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_format)
    stream_handler.setLevel(logging.DEBUG)

    file_handler = await setup_file_handler(uid)
    file_handler.setFormatter(_format)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


async def setup_file_handler(uid: int) -> logging.FileHandler:
    _scripts_starts = os.getcwd().find("scripts")
    user_logs_path = os.getcwd()[:_scripts_starts] + "logs/"

    file_handler = logging.FileHandler(filename=f"{user_logs_path}/{uid}.log")
    file_handler.setLevel(logging.INFO)
    return file_handler

