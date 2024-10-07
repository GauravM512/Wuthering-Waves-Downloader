import json
import urllib3
from urllib.parse import urljoin
from .models.download_index import Model
from .models.resources import Model as ResourcesModel

GAME =dict(
    GP_INDEX="https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50009_ZXniDENS4vnMhNEhl7cLOQMojTLKLGgu/index.json",
    OS_INDEX="https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json"
    )
http = urllib3.PoolManager()
http.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


def index(index_url):
    response = http.request('GET', index_url)
    data = json.loads(response.data)
    data = Model(**data)
    return data


def resources(index_data):
    cdn = index_data.default.cdnList[0].url
    resources = urljoin(cdn, index_data.default.resources)
    response = http.request('GET', resources)
    data = json.loads(response.data.decode('utf-8'))
    data = ResourcesModel(**data)
    return data


if __name__ == "__main__":
    print(resources(index(GAME["GP_INDEX"])))