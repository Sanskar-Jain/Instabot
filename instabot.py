import requests

API_ACCESS_TOKEN = "3757590807.86dd109.a97ce7641dea40a4883ce2b22b9a0efd"
BASE_URL = "https://api.instagram.com/v1"


def get_self_details():
    url = BASE_URL + "/users/self/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print("Details of owner in Json Format :")
    print(data)
    print("\nDetails of owner in Normal Form :")
    print("Name : ", data['data']['full_name'])
    print("Username : ", data['data']['username'])
    print("Link to Profile Picture : ", data['data']['profile_picture'])
    print("Media Shared : ", data['data']['counts']['media'])
    print("Followed By : ", data['data']['counts']['followed_by'])
    print("Followers : ", data['data']['counts']['follows'])


def get_info(user_id):
    url = BASE_URL + "/users/" + user_id + "/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    return data


def get_user_id(user_name):
    url = BASE_URL + "/users/search?q=" + user_name + "&access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print(data)
    if data['data'] == []:
        print("Sorry! User with the given username does not exists.")
    else:
        user_id = data['data'][0]['id']
        return user_id


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
    url = BASE_URL + "/users/" + str(user_id) + "/media/recent/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    id = []
    likes = []
    comments = []
    links = []
    for media in (data['data']):
        id.append(media['id'])
        likes.append(media['likes']['count'])
        comments.append(media['comments']['count'])
        links.append(media['link'])
    print("Which Recent Post you wanna select ?")
    print("1. The one with maximum likes.")
    print("2. The one with maximum comments.")
    choice = input("Enter your choice (1 or 2) : ")
    if choice not in ['1', '2']:
        while choice not in ['1', '2']:
            print("You entered the wrong choice. Please choose from given options.")
            choice = input("Enter your choice (1 or 2) : ")
    if int(choice) == 1:
        max_likes = max(likes)
        pos = likes.index(max_likes)
        return id[pos]
    elif int(choice) == 2:
        max_comments = max(comments)
        pos = comments.index(max_comments)
        return id[pos]


def like_user_post(username):
    post_id = user_recent_posts(username)
    url = BASE_URL + "/media/" + str(post_id) + "/likes"
    payload = {'access_token': API_ACCESS_TOKEN}
    data = requests.post(url, payload).json()
    if data['meta']['code'] == 200:
        print("The post has been liked.")
    else:
        print("Some error occurred! Try Again.")


def comment_user_post(username):
    post_id = user_recent_posts(username)
    url = BASE_URL + "/media/" + str(post_id) + "/comments"
    text = input("Enter the comment you wanna post : ")
    payload = {'access_token': API_ACCESS_TOKEN, 'text': text}
    data = requests.post(url, payload).json()
    if data['meta']['code'] == 200:
        print("Your comment has been Posted.")
    else:
        print("Some error occurred! Try Again.")


def search_in_comment(username):
    word_to_be_searched = input("Enter the word you want to search in comments of most popular post : ")
    post_id = user_recent_posts(username)
    print(post_id)
    url = BASE_URL + "/media/" + str(post_id) + "/comments/?access_token=" + API_ACCESS_TOKEN
    print(url)
    data = requests.get(url).json()
    print(data)
    list_of_comments = []
    for comment in data['data']:
        list_of_comments.append(comment['text'])
    print(list_of_comments)


def get_user_follows():
    url = BASE_URL + "/users/self/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print(data)


username = "bot_demo"
# print(user_recent_posts(username))
# like_user_post(username)
# comment_user_post(username)
search_in_comment(username)
# get_self_details()
# print(get_user_id(username))
# user-id : bot_demo : 4990969427
# user-id : kamal_kashyap13 : 1379413795
# get_user_id("sanskar27jain_")
