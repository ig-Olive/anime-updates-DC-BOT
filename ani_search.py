import requests

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

shedule_query = '''query ($id: Int){ 
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

        variables = {"search": str(query)}

        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": search_query, "variables": variables}
        )

        data = response.json()
        print(data)
    def get_shedule(self, query):
        variables = {"id": int(query)}
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": shedule_query, "variables": variables}
        )
        data = response.json()
        print(data)

