"""https://stackoverflow.com/questions/63853813/how-to-create-routes-with-fastapi-within-a-class"""
import typing as t
from abc import ABC, abstractmethod

from fastapi import FastAPI
from pydantic import BaseModel

_IAPIT = t.TypeVar("_IAPIT", bound="IAPI")

class IAPI(object):
    """Interface Class for custom ReST API"""

    @abstractmethod
    def __init__(self, app: FastAPI): ...

    #  @abstractmethod
    #  def get_index(self): ...
