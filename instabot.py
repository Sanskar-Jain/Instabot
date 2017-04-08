import requests

API_ACCESS_TOKEN = "3757590807.86dd109.a97ce7641dea40a4883ce2b22b9a0efd"
BASE_URL = "https://api.instagram.com/v1"


def check_status(data):
    if data['meta']['code'] == 200:
        return True
    else:
        return False


def print_info(data):
    if check_status(data):
        print("Details of owner in Json Format :")
        print(data)
        print("\nDetails of owner in Normal Form :")
        print("Name : ", data['data']['full_name'])
        print("Username : ", data['data']['username'])
        print("Link to Profile Picture : ", data['data']['profile_picture'])
        print("Media Shared : ", data['data']['counts']['media'])
        print("Followed By : ", data['data']['counts']['followed_by'])
        print("Followers : ", data['data']['counts']['follows'])
    else:
        print("Some error occurred. Try Again Later.")


def get_self_details():
    url = BASE_URL + "/users/self/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print_info(data)


def get_info(user_id):
    url = BASE_URL + "/users/" + user_id + "/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print_info(data)
    return data


def get_user_id(username):
    url = BASE_URL + "/users/search?q=" + username + "&access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    if check_status(data):
        if data['data'] == []:
            print("Sorry! User with the given username does not exists.")
            return False
        else:
            user_id = data['data'][0]['id']
            return user_id
    else:
        print("Some error occurred. Try Again Later.")
        return False


def recent_posts_self():
    url = BASE_URL + "/users/self/media/recent/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    if check_status(data):
        print(data)
    else:
        print("Some error occurred. Try Again Later.")


def no_of_posts(username):
    user_id = get_user_id(username)
    if user_id:
        data = get_info(user_id)
        if check_status(data):
            print(data)
            return data['data']['counts']['media']
        else:
            print("Some error occured. Try Again Later.")
            return False
    else:
        print("Some error occurred. Try Again Later.")
        return False


def user_recent_posts(username):
    user_id = get_user_id(username)
    url = BASE_URL + "/users/" + str(user_id) + "/media/recent/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    post_ids = []
    post_likes = []
    post_comments = []
    post_links = []
    for media in (data['data']):
        post_ids.append(media['id'])
        post_likes.append(media['likes']['count'])
        post_comments.append(media['comments']['count'])
        post_links.append(media['link'])
    print("Which Recent Post you wanna select ?")
    print("1. The one with maximum likes.")
    print("2. The one with maximum comments.")
    choice = input("Enter your choice (1 or 2) : ")
    if choice not in ['1', '2']:
        while choice not in ['1', '2']:
            print("You entered the wrong choice. Please choose from given options.")
            choice = input("Enter your choice (1 or 2) : ")
    if int(choice) == 1:
        max_likes = max(post_likes)
        pos = post_likes.index(max_likes)
        return post_ids[pos]
    elif int(choice) == 2:
        max_comments = max(post_comments)
        pos = post_comments.index(max_comments)
        return post_ids[pos]


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


def search_in_comment(username, word_to_be_searched='-1'):
    if word_to_be_searched == '-1':
        word_to_be_searched = input("Enter the word you want to search in comments of most popular post : ")
    post_id = user_recent_posts(username)
    url = BASE_URL + "/media/" + str(post_id) + "/comments/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    list_of_comments = []
    comments_id = []
    for comment in data['data']:
        list_of_comments.append(comment['text'])
        comments_id.append(comment['id'])
    comments_found = []
    comments_id_found = []
    for i in range(len(list_of_comments)):
        if word_to_be_searched in list_of_comments[i]:
            comments_found.append(list_of_comments[i])
            comments_id_found.append(comments_id[i])

    if len(comments_found) == 0:
        print("There is no comment having the word \'%s\'" % word_to_be_searched)
        return False, post_id, False
    else:
        print("Following comments contains the word \'%s\'" % word_to_be_searched)
        for i in range(len(comments_found)):
            print(str(i+1) + ". " + comments_found[i])
        return comments_id_found, post_id, comments_found


def delete_comment(username):
    word_to_be_searched = input("Enter the word you want to search and delete comment for in most popular post : ")
    comments_id_found, post_id, comments_found = search_in_comment(username, word_to_be_searched)
    if not comments_id_found:
        return False
    else:
        for i in range(len(comments_id_found)):
            url = BASE_URL + "/media/" + str(post_id) + "/comments/" + str(comments_id_found[i]) + "/?access_token=" + API_ACCESS_TOKEN
            data = requests.delete(url).json()
            if check_status(data):
                print("%s --> Deleted." % comments_found[i])
            elif data['meta']['error_message'] == "You cannot delete this comment":
                print(data['meta']['error_message'])
            else:
                print("Some error occurred. Try Again Later.")


def find_average_words_per_comment(post_id):
    url = BASE_URL + "/media/" + str(post_id) + "/comments/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    list_of_comments = []
    total_no_of_words = 0
    comments_id = []
    for comment in data['data']:
        list_of_comments.append(comment['text'])
        total_no_of_words += len(comment['text'].split())
        comments_id.append(comment['id'])
    average_words = total_no_of_words/len(list_of_comments)
    print(total_no_of_words)
    print(len(comments_id))
    print("Average no. of words per comment in most popular post = %d" % average_words)


def average_words_per_comment(username):
    post_id = user_recent_posts(username)
    find_average_words_per_comment(post_id)


user_name = "bot_demo"
# print(user_recent_posts(username))
# like_user_post(username)
# delete_comment(username)
average_words_per_comment(user_name)
# user_recent_posts(username)
# print(no_of_posts(username))
# comment_user_post(username)
# search_in_comment(username)
# get_self_details()
# print(get_user_id(username))
# user-id : bot_demo : 4990969427
# user-id : kamal_kashyap13 : 1379413795
# get_user_id("sanskar27jan_")
