"""Define the start up events and shut down events.

Please be aware that you can define multiple events and add them to the FastAPI
instance, and the adding order decides the executing order.
"""

import logging
from ..configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)
