from ytmusicapi import YTMusic

ytmusic = YTMusic("oauth.json")

#playlistId = ytmusic.create_playlist("test_api", "test description")
#ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

search_results = ytmusic.search("Oasis Wonderwall")
print(search_results[0])