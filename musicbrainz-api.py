import requests
import time

class MusicBrainzAPI:
    BASE_URL = "https://musicbrainz.org/ws/2/"
    HEADERS = {"User-Agent": "MusicApp/1.0 (your-email@example.com)"}
    RATE_LIMIT_SECONDS = 1  # 1 second for anonymous users

    def __init__(self):
        self.last_request_time = 0

    def _rate_limit(self):
        """
        Ensures that requests comply with the API's rate limit.
        """
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.RATE_LIMIT_SECONDS:
            time.sleep(self.RATE_LIMIT_SECONDS - elapsed_time)
        self.last_request_time = time.time()

    def search_artist(self, artist_name, limit=5):
        """
        Search for an artist by name.
        """
        self._rate_limit()
        url = f"{self.BASE_URL}artist/"
        params = {"query": artist_name, "fmt": "json", "limit": limit}
        response = requests.get(url, headers=self.HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    def get_artist_releases(self, artist_id, limit=5):
        """
        Get releases (albums) for a specific artist.
        """
        self._rate_limit()
        url = f"{self.BASE_URL}release/"
        params = {"artist": artist_id, "fmt": "json", "limit": limit}
        response = requests.get(url, headers=self.HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    def get_recording_details(self, recording_id):
        """
        Get details of a specific recording (track).
        """
        self._rate_limit()
        url = f"{self.BASE_URL}recording/{recording_id}"
        params = {"fmt": "json"}
        response = requests.get(url, headers=self.HEADERS, params=params)
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    musicbrainz = MusicBrainzAPI()

    # Search for an artist
    artist_name = "Radiohead"
    artists = musicbrainz.search_artist(artist_name)
    print("Artists found:")
    for artist in artists["artists"]:
        print(f"Name: {artist['name']}, ID: {artist['id']}")

    # Get releases for the first artist found
    if artists["artists"]:
        artist_id = artists["artists"][0]["id"]
        releases = musicbrainz.get_artist_releases(artist_id)
        print("\nReleases:")
        for release in releases["releases"]:
            print(f"Title: {release['title']}, Date: {release.get('date', 'Unknown')}")

    # Get details of a specific recording
    if releases["releases"]:
        recording_id = releases["releases"][0]["id"]
        recording_details = musicbrainz.get_recording_details(recording_id)
        print("\nRecording Details:")
        print(recording_details)