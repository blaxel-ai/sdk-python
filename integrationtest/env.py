from logging import getLogger

from blaxel.common.env import env

logger = getLogger(__name__)

logger.info(env.TEST)
logger.info(env.BL_WORKSPACE)