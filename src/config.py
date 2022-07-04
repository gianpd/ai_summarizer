import os
import sys
import logging
logging.basicConfig(stream=sys.stdout, format='%(asctime)-15s %(message)s',
                level=logging.INFO, datefmt=None)
logger = logging.getLogger("Summarizer")

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    environment: os.getenv("ENVIRONMENT", "dev")
    hf_token: os.getenv("HF_TOKEN")

# save the settings to the cache in order to not reload it any time from disk
@lru_cache
def get_settings() -> BaseSettings:
    logger.info("Getting the settings ...")
    return Settings()
