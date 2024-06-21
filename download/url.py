import json
import urllib3
from .models.download_index import Model
from .models.resources import Model as ResourcesModel


INDEX="https://prod-alicdn-gamestarter.kurogame.com/pcstarter/prod/game/G153/50009_ZXniDENS4vnMhNEhl7cLOQMojTLKLGgu/index.json"

LAUNCHER_INDEX="https://prod-volcdn-gamestarter.kurogame.net/pcstarter/prod/starter/50009_ZXniDENS4vnMhNEhl7cLOQMojTLKLGgu/G153/index.json"

cdn=None

def index():
    http = urllib3.PoolManager()
    response = http.request('GET', INDEX)
    data = json.loads(response.data)
    data = Model(**data)
    return data

def resources():
    index_data = index()
    http = urllib3.PoolManager()
    global cdn
    cdn = [cdn.url for cdn in index_data.default.cdnList if cdn.P == min([cdn.P for cdn in index_data.default.cdnList])][0]
    resources = f"{cdn}{index_data.default.resources}"
    cdn = f"{cdn}{index_data.default.resourcesBasePath}"
    response = http.request('GET', resources)
    data = json.loads(response.data.decode('utf-8'))
    data = ResourcesModel(**data)
    return data


if __name__ == "__main__":
    print(resources())