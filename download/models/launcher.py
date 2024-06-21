from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class AnimateBackground(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class De(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class En(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class Es(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class Fr(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class Ja(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class Ko(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class ZhHant(BaseModel):
    url: str
    md5: str
    frameRate: int
    durationInSecond: int


class AnimateBackgroundLanguage(BaseModel):
    de: De
    en: En
    es: Es
    fr: Fr
    ja: Ja
    ko: Ko
    zh_Hant: ZhHant = Field(..., alias='zh-Hant')


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


class Default(BaseModel):
    cdnList: List[CdnListItem]
    changelog: Changelog
    installer: str
    installerMD5: str
    installerSize: int
    version: str


class NavigationBarLanguage(BaseModel):
    zh_Hans: str = Field(..., alias='zh-Hans')
    en: str
    ja: str
    ko: str
    zh_Hant: str = Field(..., alias='zh-Hant')
    fr: str
    de: str
    es: str
    ru: str
    pt: str
    id: str
    vi: str
    th: str


class Model(BaseModel):
    crashInitSwitch: int
    animateBgSwitch: int
    navigationBarSwitch: int
    animateBackground: AnimateBackground
    animateBackgroundLanguage: AnimateBackgroundLanguage
    default: Default
    navigationBarLanguage: NavigationBarLanguage
