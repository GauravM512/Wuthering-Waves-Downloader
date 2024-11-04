import json
import urllib3
from urllib.parse import urljoin
from typing import Optional
from .models.download_index import Model
from .models.resources import Model as ResourcesModel
from .config import GAME_INDICES, USER_AGENT

class URLHandler:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.http.headers["User-Agent"] = USER_AGENT

    def get_index(self, index_type: str) -> Optional[Model]:
        try:
            index_url = GAME_INDICES[index_type]
            response = self.http.request('GET', index_url)
            data = json.loads(response.data)
            return Model(**data)
        except Exception as e:
            print(f"Error fetching index: {e}")
            return None

    def get_resources(self, index_data: Model) -> Optional[ResourcesModel]:
        try:
            cdn = index_data.default.cdnList[0].url
            resources_url = urljoin(cdn, index_data.default.resources)
            response = self.http.request('GET', resources_url)
            data = json.loads(response.data.decode('utf-8'))
            return ResourcesModel(**data)
        except Exception as e:
            print(f"Error fetching resources: {e}")
            return None

if __name__ == "__main__":
    handler = URLHandler()
    index_data = handler.get_index("GP_INDEX")
    if index_data:
        resources_data = handler.get_resources(index_data)
        if resources_data:
            print(resources_data)