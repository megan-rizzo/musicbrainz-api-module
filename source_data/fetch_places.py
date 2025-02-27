from musicbrainz_api import MusicBrainzAPI

def main():
    """
    Main function to fetch all places from the MusicBrainz API and save them to a CSV file.
    """
    # Initialize the API with appropriate User-Agent and rate limit
    user_agent = "jihbr@umich.edu"  # User-Agent allowing 50 requests per second
    rate_limit = 50  # Adjust rate limit based on User-Agent

    api = MusicBrainzAPI(user_agent=user_agent, rate_limit=rate_limit)

    try:
        # Fetch all places
        print("Fetching all places from MusicBrainz...")
        df_places = api.fetch_all_places()
        
        # Display the total count of places fetched
        print(f"Fetched {len(df_places)} places.")

        # Save to a CSV file
        output_file = "places.csv"
        df_places.to_csv(output_file, index=False)
        print(f"Saved places to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
