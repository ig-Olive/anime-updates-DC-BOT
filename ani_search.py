import requests

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
    def search_anime(self, query):

        variables = {"search": query}

        response = requests.post(
            API_URL,
            json={"query": search_query, "variables": variables
            }
        )

        response.raise_for_status()

        data = response.json()
        if "errors" in data:
            raise Exception(data["errors"])

        data_list = []
        for items in data["data"]["Page"]["media"]:
            data_dict = {
                "title": items["title"]["english"],
                "episodes": items["episodes"],
                "id": items["id"],
                "status": items["status"],
            }
            data_list.append(data_dict)
        return data_list

    def get_shedule(self, query):
        variables = {"id": int(query)}

        response = requests.post(
            API_URL,
            json={"query": get_schedule, "variables": variables
            }
        )
        response.raise_for_status()

        data = response.json()
        if "errors" in data:
            raise Exception(data["errors"])

        return data["data"]

