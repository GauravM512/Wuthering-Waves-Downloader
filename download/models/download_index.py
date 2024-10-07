from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CdnListItem(BaseModel):
    K1: int
    K2: int
    P: int
    url: str


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
    changelog: Dict[str, Any]
    changelogVisible: int
    resources: str
    resourcesBasePath: str
    resourcesDiff: ResourcesDiff
    resourcesExcludePath: List
    resourcesExcludePathNeedUpdate: List
    sampleHashSwitch: int
    version: str


class Text(BaseModel):
    de: Optional[str] = None
    zh_Hant: Optional[str] = Field(None, alias='zh-Hant')
    ko: Optional[str] = None
    ja: Optional[str] = None
    en: Optional[str] = None
    fr: Optional[str] = None
    es: Optional[str] = None


class RHIOptionListItem(BaseModel):
    cmdOption: str
    isShow: int
    text: Text


class ResourcesLogin(BaseModel):
    host: str
    loginSwitch: int


class Model(BaseModel):
    hashCacheCheckAccSwitch: int
    default: Default
    predownloadSwitch: int
    RHIOptionSwitch: int
    RHIOptionList: List[RHIOptionListItem]
    resourcesLogin: ResourcesLogin