from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class CdnListItem(BaseModel):
    K1: int
    K2: int
    P: int
    url: str


class Changelog(BaseModel):
    zh_Hans: str = Field(..., alias='zh-Hans')
    de: str
    zh_Hant: str = Field(..., alias='zh-Hant')
    ko: str
    ja: str
    en: str
    fr: str
    es: str


class CurrentGameInfo(BaseModel):
    fileName: str
    md5: str
    version: str


class PreviousGameInfo(BaseModel):
    fileName: str
    md5: str
    version: str


class ResourcesDiff(BaseModel):
    currentGameInfo: CurrentGameInfo
    previousGameInfo: PreviousGameInfo


class Default(BaseModel):
    cdnList: List[CdnListItem]
    changelog: Changelog
    resources: str
    resourcesBasePath: str
    resourcesDiff: ResourcesDiff
    resourcesExcludePath: List
    resourcesExcludePathNeedUpdate: List
    sampleHashSwitch: int
    version: str


class Model(BaseModel):
    hashCacheCheckAccSwitch: int
    default: Default
