import requests
import time

class MusicBrainzAPI:
    BASE_URL = "https://musicbrainz.org/ws/2"
    RATE_LIMIT_DELAY = 1  

    def __init__(self):
        self.last_request_time = 0

    def _rate_limited_request(self, endpoint, params):
        """
        Handles rate-limited API requests.
        """
        # Wait if the last request was less than the rate limit delay
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed_time)

        # Perform the API request
        response = requests.get(endpoint, params=params, headers={"User-Agent": "MusicBrainzAPI/1.0 (example@example.com)"})
        self.last_request_time = time.time()

        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        return response.json()

    def get_place(self, place_id):
        """
        Get information about a specific place by its MusicBrainz ID.
        """
        endpoint = f"{self.BASE_URL}/place/{place_id}"
        params = {"fmt": "json"}  # Return response in JSON format
        return self._rate_limited_request(endpoint, params)

    def search_place(self, query, limit=10):
        """
        Search for places matching a query.
        """
        endpoint = f"{self.BASE_URL}/place"
        params = {"query": query, "fmt": "json", "limit": limit}
        return self._rate_limited_request(endpoint, params)

    def get_work(self, work_id):
        """
        Get information about a specific work by its MusicBrainz ID.
        """
        endpoint = f"{self.BASE_URL}/work/{work_id}"
        params = {"fmt": "json"}  # Return response in JSON format
        return self._rate_limited_request(endpoint, params)

    def search_work(self, query, limit=10):
        """
        Search for works matching a query.
        """
        endpoint = f"{self.BASE_URL}/work"
        params = {"query": query, "fmt": "json", "limit": limit}
        return self._rate_limited_request(endpoint, params)

    def get_recording(self, recording_id):
        """
        Get information about a specific recording by its MusicBrainz ID.
        """
        endpoint = f"{self.BASE_URL}/recording/{recording_id}"
        params = {"fmt": "json"}  # Return response in JSON format
        return self._rate_limited_request(endpoint, params)

    def search_recording(self, query, limit=10):
        """
        Search for recordings matching a query.
        """
        endpoint = f"{self.BASE_URL}/recording"
        params = {"query": query, "fmt": "json", "limit": limit}
        return self._rate_limited_request(endpoint, params)