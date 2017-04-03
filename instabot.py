import requests

API_ACCESS_TOKEN = "3757590807.86dd109.a97ce7641dea40a4883ce2b22b9a0efd"
BASE_URL = "https://api.instagram.com/v1"


def get_info(user_id):
    url = BASE_URL + "/users/" + user_id + "/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    return data


def get_user_id(user_name):
    url = BASE_URL + "/users/search?q=" + user_name + "&access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    return data['data'][0]['id']


def recent_posts_self():
    url = BASE_URL + "/users/self/media/recent/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print(data)


def no_of_posts(username):
    data = get_info(get_user_id(username))
    print(data)
    return data['data']['counts']['media']


def user_recent_posts(username):
    user_id = get_user_id(username)
    url = BASE_URL + "/users/" + user_id + "/media/recent/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print(data)
    id = []
    print(len(data['data']))
    for media in (data['data']):
        id.append(media['id'])
        print(media['link'])
    print(id)


def get_user_follows():
    url = BASE_URL + "/users/self/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print(data)




username = "bot_demo"
print(user_recent_posts(username))

# user-id : bot_demo : 4990969427
# user-id : kamal_kashyap13 : 1379413795
#get_user_id("sanskar27jain_")