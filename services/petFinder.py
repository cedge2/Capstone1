import os
import requests

print("API Key:", os.environ.get("PETFINDER_API_KEY"))

class PetFinderAPI:
    BASE_URL = "https://api.petfinder.com/v2/"

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = requests.Session()
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        try:
            response = requests.post(
                f"{self.BASE_URL}oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.api_key,
                    "client_secret": self.secret_key
                }
            )
            print("Response Headers:", response.headers)
            print("Response Status Code:", response.status_code)
            print("Response Body:", response.text)

            response_data = response.json()
            return response_data["access_token"]
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except KeyError:
            print("Access token not found in the response.")
            return None

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def search_pets(self, animal_type=None, location=None, limit=20):
        """Search for pets based on type, location, and limit."""
        params = {
            "type": animal_type,
            "location": location,
            "limit": limit
        }
        try:
            response = self.session.get(
                f"{self.BASE_URL}animals",
                headers=self._headers(),
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to search pets: {e}")
            return None
