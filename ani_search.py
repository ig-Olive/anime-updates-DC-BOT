import aiohttp

API_URL = "https://graphql.anilist.co"

search_query = '''
query ($search: String) {
  Page(page: 1, perPage: 5) {
    media(search: $search, type: ANIME) {
      title {
        romaji
        english
      }
      id
      status
      episodes
    }
  }
}
'''

get_schedule = '''query ($id: Int){ 
  Media (id: $id, type: ANIME) { 
    id
    title {
      romaji
      english
      native
      }
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
      }
    airingSchedule {
      nodes {
        episode
        airingAt
      }
    }
  }
  }
'''


class AnimeSearch():
    def __init__(self):
        pass
    async def search_anime(self, query):
        variables = {"search": query}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        API_URL,
                        json={"query": search_query, "variables": variables},
                        timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
        except aiohttp.ClientResponseError:
            return None
        except aiohttp.ClientError:
            return None

        data_list = []
        for items in data["data"]["Page"]["media"]:
            data_dict = {
                "title": items["title"]["english"] or items["title"]["romaji"] or items["title"]["native"] or "Unknown Anime",
                "episodes": items["episodes"],
                "id": items["id"],
                "status": items["status"],
            }
            data_list.append(data_dict)
        return data_list

    async def get_schedule(self, query):
        variables = {"id": int(query)}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    API_URL,
                    json={"query": get_schedule, "variables": variables},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
        except aiohttp.ClientResponseError:
            return None
        except aiohttp.ClientError:
            return None
        if "errors" in data:
            raise Exception(data["errors"])

        return data["data"]


