import os
from more_itertools import split_after
import fileinput

def read_comments_file():
    try:
        author_comment = {}
        with open(os.getenv("RW_DB_PATH"), "r") as file:
            for line in file:
                tmp = line.rstrip().split(" ")
                author_comment[tmp[0]] = tmp[1]
        return author_comment
    except:
        return {}

def remove_empty_lines():
    with open(os.getenv("RW_DB_PATH")) as reader, open(os.getenv("RW_DB_PATH"), 'r+') as writer:
        for line in reader:
            if line.strip():
                writer.write(line)
        writer.truncate()

def add_comment(author, id):
    with open(os.getenv("RW_DB_PATH"), "a+") as file:
        file.write(author + " " + id + "\n")
    remove_empty_lines()

def update_comment(author, id):
    for line in fileinput.input(os.getenv("RW_DB_PATH"), inplace=True):
        if author in line:
            print(author + " " + id + "\n")
        else:
            print(line)
    remove_empty_lines()

def get_latest_comment_by_author(author):
    tmp = read_comments_file()
    return tmp.get(author)

def get_filtered_comments(author, comments):
    id = get_latest_comment_by_author(author)
    if id == None:
        return comments
    size = len(comments)
    for i in range(size):
        if comments[i]["id"] == id: break
    if i == size - 1:
        return comments
    else:
        return comments[:i]

def save_latest_comment_for_author(author, comments):
    if not comments:
        return
    if author not in read_comments_file().keys():
        add_comment(author, comments[0]["id"])
    else:
        update_comment(author, comments[0]["id"])

