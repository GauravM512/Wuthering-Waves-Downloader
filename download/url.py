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
    print(resources())