import os
import traceback
from enum import Enum


https = "https"
http = "http"
d = {}


def get_caller_name():
    caller = traceback.extract_stack()[0][0]
    caller_name = os.path.splitext(os.path.basename(caller))[0]
    return caller_name


def set_env(env):
    caller_name = get_caller_name()
    d[caller_name] = env


class Host(Enum):
    fun = '{}://fun.fanli.com'

    def __str__(self):
        return self.value.format(d.get(get_caller_name(), https))

    def reset_env(self, env):
        return self.value, format(env)
