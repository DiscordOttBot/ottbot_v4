# TODO: Update typing when mypy get `ParamSpec` and `Concatenate`
import collections.abc as c
import typing as t

import tanjun

from ottbot.core.bot import OttBot
from ottbot.core.client import OttClient

R = t.TypeVar("R")  # return type

