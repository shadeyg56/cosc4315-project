import requests
import io

class OpenWebUI:
    def __init__(self, email: str, password: str, base_url: str = "http://localhost:3000/"):
        self.email = email
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self.user_token: str | None = self._login()

        self.session.headers.update({"Accept": "application/json"})

    def create_knowledge(self, name: str, desc: str):
        data = {
            "name": name,
            "description": desc,
            "data": {},
            "access_control": {}
        }
        knowledge = self._post("api/v1/knowledge/create", json=data)
        return knowledge
    
    def create_or_get_knowledge(self, name: str, desc: str):
        knowledge_list = self._get("api/v1/knowledge/")
        for knowledge in knowledge_list:
            if knowledge.get("name") == name:
                return knowledge
        knowledge = self.create_knowledge(name, desc)
        return knowledge
    
    def add_knowledge(self, knowledge_id: str, files: list[str]):
        file_ids = []
        file_json = []
        for i, file in enumerate(files):
            try:
                buffer = io.BytesIO(bytes(file, "ascii"))
                data = {
                    "file": (i, buffer, "text/plain")
                }
                resp = self._post("api/v1/files/?process=true", files=data)
                buffer.close()
                if resp.get("id"):
                    file_ids.append({"file_id": resp.get("id")})
                file_json.append(resp)
            except Exception as e:
                pass
        resp = self._post(f"api/v1/knowledge/{knowledge_id}/files/batch/add", json=file_ids)

    def download_model(self, model: str): 
        data = {
            "name": model
        }
        self._post("ollama/api/pull/0", json=data, should_return=False)

    def create_model_from(self, model: str, knowledge: list[dict]):
        for entry in knowledge:
            entry.update({"type": "collection"})
        data = {
            "id": "sysadmin",
            "base_model_id": model,
            "name": "SysAdmin Helper",
            "meta": {
                "profile_image_url": "/static/favicon.png",
                "knowledge": knowledge
            },
            "params": {},
            "access_control": {},
            "is_active": True
        }
        self._post("/api/v1/models/create", json=data)


    def _login(self) -> str | None:
        data = {
            "email": self.email,
            "password": self.password
        }
        resp = self._post("api/v1/auths/signin", json=data)
        return resp.get("token")

    def _get(self, endpoint: str, params=None):

        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def _post(self, endpoint, data=None, json=None, files=None, should_return=True):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=data, json=json, files=files)
        if should_return:
            return self._handle_response(response)
    
    def _handle_response(self, response):
        if response.status_code >= 400:
            raise requests.HTTPError(f"Error {response.status_code}: {response.text}")
        return response.json()