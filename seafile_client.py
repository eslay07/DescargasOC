import os
import requests
import configurador


class SeafileClient:
    """Simple Seafile API client using token authentication."""

    def __init__(self, server_url: str, token: str):
        self.server_url = server_url.rstrip('/')
        self.token = token

    def _headers(self):
        return {
            'Authorization': f'Token {self.token}'
        }

    def _get_upload_link(self, repo_id: str, parent_dir: str = '/'):  # type: ignore
        """Return an upload link for the given repo and directory."""
        url = f"{self.server_url}/api2/repos/{repo_id}/upload-link/?p={parent_dir}"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        # API returns a quoted string, remove quotes
        return resp.text.strip('"')

    def upload_file(self, repo_id: str, file_path: str, parent_dir: str = '/'):  # type: ignore
        """Upload a file to Seafile."""
        upload_link = self._get_upload_link(repo_id, parent_dir)
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'parent_dir': parent_dir}
            resp = requests.post(upload_link, files=files, data=data,
                                 headers=self._headers(), timeout=60)
            resp.raise_for_status()
        return resp.json()


def get_client_from_config() -> SeafileClient:
    """Create a SeafileClient using values from configuracion."""
    config = configurador.cargar_config()
    url = config.get('seafile_url')
    token = config.get('seafile_token')
    if not url or not token:
        raise ValueError('Seafile URL y token deben estar configurados')
    return SeafileClient(url, token)
