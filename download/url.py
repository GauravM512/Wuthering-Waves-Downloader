import json
import urllib3
from urllib.parse import urljoin
import time
from .models.download_index import Model
from .models.resources import Model as ResourcesModel


INDEX="https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50009_ZXniDENS4vnMhNEhl7cLOQMojTLKLGgu/index.json"

LAUNCHER_INDEX="https://prod-volcdn-gamestarter.kurogame.net/pcstarter/prod/starter/50009_ZXniDENS4vnMhNEhl7cLOQMojTLKLGgu/G153/index.json"


http = urllib3.PoolManager()


def index():
    response = http.request('GET', INDEX)
    data = json.loads(response.data)
    data = Model(**data)
    return data

index_data = index()
cdn = "https://hw-pcdownload-aws.aki-game.net/"+index_data.default.resourcesBasePath

def resources():
    cdn = index_data.default.cdnList[0].url
    resources = urljoin(cdn, index_data.default.resources)
    response = http.request('GET', resources)
    data = json.loads(response.data.decode('utf-8'))
    data = ResourcesModel(**data)
    return data


if __name__ == "__main__":
    print(resources())