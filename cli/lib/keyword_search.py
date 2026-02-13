from lib.search_utils import load_movies

# data = load_movies()
# print(data)
def search_command(query, n_results):
    movies = load_movies()
    res = []
    for movie in movies:
        if query in movie['title']:
            res.append(movie)
        if len(res) == n_results:
           break 
    return res




