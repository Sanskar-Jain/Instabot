# --------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------ INSTABOT ----------------------------------------------------------#
# --------------------------------------------------------------------------------------------------------------------#


# Imports requests library for handling HTTP requests.
import requests


# Access Token generated from Instabot servers.
API_ACCESS_TOKEN = "3757590807.86dd109.a97ce7641dea40a4883ce2b22b9a0efd"

# Base URL for every URL used in the file.
BASE_URL = "https://api.instagram.com/v1"


# Function to check if the request is performed Successfully or not.
def check_status(data):
    if data['meta']['code'] == 200:
        return True
    else:
        return False


# Function to print Sorry Message if the username does not exists.
def sorry_message():
    print("\n____________________________________________________ User Information _____________________________________________________\n")
    print("Sorry! User with the given username does not exists.")
    print("\n___________________________________________________________________________________________________________________________\n")


# Function to print User/Self Information.
def print_info(data, self='self'):
    if check_status(data):
        if self == 'self':
            print("\n____________________________________________________ Owner Information ____________________________________________________\n")
        else:
            print("\n____________________________________________________ User Information _____________________________________________________\n")
        print("Name                    : ", data['data']['full_name'])
        print("Username                : ", data['data']['username'])
        print("Link to Profile Picture : ", data['data']['profile_picture'])
        print("Media Shared            : ", data['data']['counts']['media'])
        print("Followed By             : ", data['data']['counts']['followed_by'])
        print("Followers               : ", data['data']['counts']['follows'])
        if data['data']['website'] != '':
            print("Website                 : ", data['data']['website'])
        else:
            print("Website                 :  No Website Available")
        if data['data']['bio'] != '':
            print("Bio                     : ", data['data']['bio'])
        else:
            print("Bio                     :  No Info Available")
        print("\n___________________________________________________________________________________________________________________________\n")
    else:
        print("\nSome error occurred. Try Again Later.")


# Function to get the Details of the Owner.
def get_self_details():
    url = BASE_URL + "/users/self/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    print_info(data)


# Function to get UserName using UserId.
def get_user_name(user_id):
    url = BASE_URL + "/users/" + user_id + "/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    return data['data']['username']


# Function to get UseerId by UserName.
def get_user_id(username):
    url = BASE_URL + "/users/search?q=" + username + "&access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    if check_status(data):
        if data['data'] == []:
            sorry_message()
            return False
        else:
            user_id = data['data'][0]['id']
            return user_id
    else:
        return False


# Function to get the Details of the User.
def get_info(user_id):
    if user_id:
        url = BASE_URL + "/users/" + user_id + "/?access_token=" + API_ACCESS_TOKEN
        data = requests.get(url).json()
        print_info(data, 'user')
    else:
        return False


# Function to find the no. of posts by a User. Helper Function to handle the case of No Posts.
def get_users_recent_post(username):
    user_id = get_user_id(username)
    if user_id:
        url = BASE_URL + "/users/" + str(user_id) + "/media/recent/?access_token=" + API_ACCESS_TOKEN
        data = requests.get(url).json()
        if len(data['data']) == 0:
            print("\n__________________ Post Status __________________")
            print("\nNo Posts Found for this User !")
            print("\n_________________________________________________")
        return len(data['data'])

# Function to find the Most Popular Post of a User depending upon the criteria given.
def user_popular_posts(username):
    user_id = get_user_id(username)
    if user_id:
        if get_users_recent_post(username):
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
            print("\nWhich Recent Post you wanna select ?")
            print("1. The one with maximum likes.")
            print("2. The one with maximum comments.")
            choice = input("\nEnter your choice (1 or 2) : ")
            if choice not in ['1', '2']:
                while choice not in ['1', '2']:
                    print("You entered the wrong choice. Please choose from given options.")
                    choice = input("Enter your choice (1 or 2) : ")
            if int(choice) == 1:
                max_likes = max(post_likes)
                pos = post_likes.index(max_likes)
                return post_ids[pos], post_links[pos]
            elif int(choice) == 2:
                max_comments = max(post_comments)
                pos = post_comments.index(max_comments)
                return post_ids[pos], post_links[pos]
        else:
            return False, False
    else:
        return False, False


# Function to like the Most Popular Post of a user.
def like_user_post(username):
    post_id, post_link = user_popular_posts(username)
    if post_id and post_link:
        url = BASE_URL + "/media/" + str(post_id) + "/likes"
        payload = {'access_token': API_ACCESS_TOKEN}
        data = requests.post(url, payload).json()
        if data['meta']['code'] == 200:
            print("The post has been liked.")
        else:
            print("Some error occurred! Try Again.")


# Function to comment on Most Popular Post of the User.
def comment_user_post(username):
    post_id, post_link = user_popular_posts(username)
    if post_id and post_link:
        url = BASE_URL + "/media/" + str(post_id) + "/comments"
        text = input("\nEnter the comment you wanna post : ")
        payload = {'access_token': API_ACCESS_TOKEN, 'text': text}
        data = requests.post(url, payload).json()
        if data['meta']['code'] == 200:
            print("\nYour comment has been Posted.")
        else:
            print("\nSome error occurred! Try Again.")


# Function to find the Comments in Most Popular Post having a Particular Word.
def search_in_comment(username, word_to_be_searched='-1'):
    post_id, post_link = user_popular_posts(username)
    if word_to_be_searched == '-1':
        word_to_be_searched = input("Enter the word you want to search in comments of most interesting post : ")
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
        print("\nDeleting.....\n")
        return comments_id_found, post_id, comments_found


# Function to Delete the comment on Most Popular Post of User having a Particular Word.
def delete_comment(username):
    user_id = get_user_id(username)
    if user_id:
        if get_users_recent_post(username):
            word_to_be_searched = input("Enter the word you want to search and delete comment for in most interesting post : ")
            comments_id_found, post_id, comments_found = search_in_comment(username, word_to_be_searched)
            if not comments_id_found:
                return False
            else:
                for i in range(len(comments_id_found)):
                    url = BASE_URL + "/media/" + str(post_id) + "/comments/" + str(comments_id_found[i]) + "/?access_token=" + API_ACCESS_TOKEN
                    data = requests.delete(url).json()
                    if check_status(data):
                        print("%s --> Deleted." % comments_found[i])
                        break
                    elif data['meta']['error_message'] == "You cannot delete this comment":
                        print("%s --> %s as it is made by another user." % (bot_comments_found[i], data['meta']['error_message']))
                    else:
                        print("Some error occurred. Try Again Later.")


# Function to find Average Number of Words per Comment.
def find_average_words_per_comment(post_id):
    url = BASE_URL + "/media/" + str(post_id) + "/comments/?access_token=" + API_ACCESS_TOKEN
    data = requests.get(url).json()
    if len(data['data']) == 0:
        print("There are no comments on this post...")
    else:
        list_of_comments = []
        total_no_of_words = 0
        comments_id = []
        for comment in data['data']:
            list_of_comments.append(comment['text'])
            total_no_of_words += len(comment['text'].split())
            comments_id.append(comment['id'])
        average_words = float(total_no_of_words)/len(list_of_comments)
        print("\nAverage no. of words per comment in most interesting post = %.2f" % average_words)


# Helper Function to find Average Number of Words per Comment. Made to complete the Need of Objective.
def average_words_per_comment(username):
    user_id = get_user_id(username)
    if user_id:
        if get_users_recent_post(username):
            post_id, post_link = user_popular_posts(username)
            find_average_words_per_comment(post_id)


# Menu for the User to interact with the Instabot.
print("\nHello User! Welcome to the Instabot Environment.")
choice = '1'
while choice != '9':
    print("\nWhat do you want to do using the bot?")
    print("1. Get the Details of the owner.")
    print("2. Get the UserId of the User.")
    print("3. Get Information about the User.")
    print("4. Get the most popular post of the User.")
    print("5. Like a post of the User.")
    print("6. Comment on post of the User.")
    print("7. Delete the comment containing a particular word.")
    print("8. Get the average no. of words per comment in most insteresting post.")
    print("9. Exit.\n\n")

    choice = input("Enter Your Choice(1-9) : ")

# Perform Actions Depending on the User's Choice. Runs Until User wishes to Exit.
    if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
        if int(choice) == 1:
            get_self_details()
        else:
            user_name = input("\nEnter the Username of the User : ")
            if int(choice) == 2:
                user_id = get_user_id(user_name)
                if user_id:
                    print("\n__________ UserId __________")
                    print("\nUsername : %s" % get_user_name(user_id))
                    print("UserId   : %s" % user_id)
                    print("\n____________________________")
            elif int(choice) == 3:
                user_id = get_user_id(user_name)
                if user_id:
                    get_info(user_id)
            elif int(choice) == 4:
                post_id, post_link = user_popular_posts(user_name)
                if post_link and post_id:
                    print("\n\n_________________________ Most Popular Post _________________________")
                    print("\nPost Id : %s" % post_id)
                    print("Post Link : %s" % post_link)
                    print("\n_____________________________________________________________________")
            elif int(choice) == 5:
                like_user_post(user_name)
            elif int(choice) == 6:
                comment_user_post(user_name)
            elif int(choice) == 7:
                delete_comment(user_name)
            elif int(choice) == 8:
                average_words_per_comment(user_name)
        print("\nWant to do more using Instabot?")
        ch = 'P'
        flag = 0
        while ch not in ['Y','N']:
            if flag != 0:
                print("Wrong Choice Entered. Try Again...")
            ch = input("\nEnter your choice (Y/N) :").upper()
            flag = 1
            if ch == 'N':
                break
        if ch == 'N':
            break
    elif choice == '9':
        pass
    else:
        print("\nWrong choice entered.... Try Again.")

# Terminates the Program by Printing a Message.
print(" _/\_ Thanks for using Instabot Service. _/\_ ")