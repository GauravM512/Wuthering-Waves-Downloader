from __future__ import annotations

from typing import List

from pydantic import BaseModel


class ResourceItem(BaseModel):
    dest: str
    md5: str
    sampleHash: str
    size: int


class SampleHashInfo(BaseModel):
    sampleNum: int
    sampleBlockMaxSize: int


class Model(BaseModel):
    resource: List[ResourceItem]
    sampleHashInfo: SampleHashInfo
