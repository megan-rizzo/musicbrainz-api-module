import requests
import time
import pandas as pd

class MusicBrainzAPI:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def __init__(self, user_agent, rate_limit):
        """
        Initialize the MusicBrainzAPI class.

        Args:
            user_agent (str): The User-Agent string to use for requests.
            rate_limit (int): The maximum number of requests per second.
        """
        self.user_agent = user_agent
        self.rate_limit = rate_limit  # Requests per second
        self.last_request_time = 0

    def _rate_limited_request(self, endpoint, params):
        """
        Perform a rate-limited request to the MusicBrainz API.
        Handles HTTP 503 errors with exponential backoff.

        Args:
            endpoint (str): API endpoint.
            params (dict): Query parameters.

        Returns:
            dict: JSON response from the API.
        """
        # Enforce rate-limiting
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < 1 / self.rate_limit:
            time.sleep(1 / self.rate_limit - elapsed_time)

        while True:
            try:
                response = requests.get(
                    endpoint,
                    params=params,
                    headers={"User-Agent": self.user_agent}
                )
                self.last_request_time = time.time()

                if response.status_code == 503:
                    # Exponential backoff for 503 errors
                    time.sleep(2)
                    continue
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                raise Exception(f"API Request Error: {e}")

    def fetch_all_places(self, query="*", limit=100):
        """
        Fetch all places from MusicBrainz using pagination.

        Args:
            query (str): Query string for searching places. Default is "*".
            limit (int): Number of results to fetch per page. Maximum is 100.

        Returns:
            pd.DataFrame: A DataFrame containing all places fetched from MusicBrainz.
        """
        endpoint = f"{self.BASE_URL}/place"
        all_places = []
        offset = 0

        while True:
            params = {"query": query, "fmt": "json", "limit": limit, "offset": offset}
            data = self._rate_limited_request(endpoint, params)

            # Append the results
            places = data.get("places", [])
            all_places.extend(places)

            # Break if there are no more results
            if len(places) < limit:
                break

            # Update offset for next page
            offset += limit

        # Convert to DataFrame
        df_places = pd.DataFrame(all_places)
        return df_places


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