import os
from typing import Dict, Optional

import tomli
from pydantic import BaseModel


class EnvConfig(BaseModel):
    secret_env: Dict[str, str] = {}
    config_env: Dict[str, str] = {}

    def __getattr__(self, name: str) -> Optional[str]:
        if name in self.secret_env:
            return self.secret_env[name]
        if name in self.config_env:
            return self.config_env[name]
        return os.environ.get(name)

    def __getitem__(self, name: str) -> Optional[str]:
        return self.__getattr__(name)

def load_env() -> EnvConfig:
    env_config = EnvConfig()

    # Load config from blaxel.toml
    try:
        with open('blaxel.toml', 'rb') as f:
            config_infos = tomli.load(f)
            if 'env' in config_infos:
                env_config.config_env.update(config_infos['env'])
    except Exception:
        pass

    # Load secrets from .env
    try:
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_config.secret_env[key] = value.replace('"', '')
    except Exception:
        pass

    return env_config

env = load_env()