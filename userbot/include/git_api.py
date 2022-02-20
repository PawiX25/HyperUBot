import urllib.request as url
import json

VERSION = "1.3.0"
APIURL = "https://api.github.com/repos/"


def vercheck() -> str:
    return str(VERSION)


def getRateLimit():
    try:
        with url.urlopen("https://api.github.com/rate_limit") as data_raw:
            rateData = json.loads(data_raw.read().decode())
        return rateData.get("resources")
    except Exception:
        return None

# Repo-wise stuff


def getData(repoURL):
    try:
        with url.urlopen(APIURL + repoURL + "/releases") as data_raw:
            repoData = json.loads(data_raw.read().decode())
            return repoData
    except Exception:
        return None


def getLatestData(repoURL):
    with url.urlopen(f"{APIURL}{repoURL}/releases/latest") as data_raw:
        repoData = json.loads(data_raw.read().decode())
    return repoData


def getReleaseData(repoData, index):
    if index < len(repoData):
        return repoData[index]
    return None


# Release-wise stuff


def getAuthor(releaseData):
    if releaseData is None:
        return None
    return releaseData['author']['login']


def getAuthorUrl(releaseData):
    if releaseData is None:
        return None
    return releaseData['author']['html_url']


def getReleaseName(releaseData):
    if releaseData is None:
        return None
    return releaseData['name']


def getReleaseTag(releaseData):
    if releaseData is None:
        return None
    return releaseData['tag_name']


def getReleaseDate(releaseData):
    if releaseData is None:
        return None
    return releaseData['published_at']


def getAssetsSize(releaseData):
    if releaseData is None:
        return None
    return len(releaseData['assets'])


def getAssets(releaseData):
    if releaseData is None:
        return None
    return releaseData['assets']


def getBody(releaseData):  # changelog stuff
    if releaseData is None:
        return None
    return releaseData['body']


# Asset-wise stuff


def getReleaseFileName(asset):
    return asset['name']


def getReleaseFileURL(asset):
    return asset['browser_download_url']


def getDownloadCount(asset):
    return asset['download_count']


def getSize(asset):
    return asset['size']
