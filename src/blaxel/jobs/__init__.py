import argparse
import os
import sys
import asyncio
from typing import Any, Dict, Callable
import requests

class BlJob:
    def get_arguments(self) -> Dict[str, Any]:
        if not os.getenv('BL_EXECUTION_DATA_URL'):
            parser = argparse.ArgumentParser()
            # Parse known args, ignore unknown
            args, unknown = parser.parse_known_args()
            # Convert to dict and include unknown args
            args_dict = vars(args)
            # Add unknown args to dict
            for i in range(0, len(unknown), 2):
                if i + 1 < len(unknown):
                    key = unknown[i].lstrip('-')
                    args_dict[key] = unknown[i + 1]
            return args_dict

        response = requests.get(os.getenv('BL_EXECUTION_DATA_URL'))
        data = response.json()
        tasks = data.get('tasks', [])
        return tasks[self.index] if self.index < len(tasks) else {}

    @property
    def index_key(self) -> str:
        return os.getenv('BL_EXECUTION_INDEX_KEY', 'TASK_INDEX')

    @property
    def index(self) -> int:
        index_value = os.getenv(self.index_key)
        return int(index_value) if index_value else 0

    def start(self, func: Callable):
        """
        Run a job defined in a function, it's run in the current process.
        Handles both async and sync functions.
        Arguments are passed as keyword arguments to the function.
        """
        try:
            parsed_args = self.get_arguments()
            if asyncio.iscoroutinefunction(func):
                asyncio.run(func(**parsed_args))
            else:
                func(**parsed_args)
            sys.exit(0)
        except Exception as error:
            print('Job execution failed:', error, file=sys.stderr)
            sys.exit(1)

# Create a singleton instance
bl_job = BlJob()