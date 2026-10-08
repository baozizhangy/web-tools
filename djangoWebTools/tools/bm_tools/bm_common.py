import json
from typing import Callable, Optional

from utils.logger_util import web_logger
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger


def _log_step(steps: list, message: str, progress_callback: Optional[Callable[[str], None]] = None):
    web_logger.info(f"[QUERY_ORDER_STEP] {message}")
    steps.append(message)
    if progress_callback:
        progress_callback(message)


def _trigger_repay_sync_job(env):
    return xxl_job_trigger('107', env=env)


def _to_dict_response(response):
    if isinstance(response, dict):
        return response
    if isinstance(response, str):
        return json.loads(response)
    return response
