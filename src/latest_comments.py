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

def add_comment(author, id):
    with open(os.getenv("RW_DB_PATH"), "a+") as file:
        file.write(author + " " + id + "\n")

def update_comment(author, id):
    for line in fileinput.input(os.getenv("RW_DB_PATH"), inplace=True):
        if author in line:
            print(author + " " + id)
        else:
            print(line)

def get_latest_comment_by_author(author):
    tmp = read_comments_file()
    return tmp.get(author)

def get_filtered_comments(author, comments):
    id = get_latest_comment_by_author(author)
    if id == None:
        return comments
    size = len(comments)
    idx_list = [idx + 1 for idx, val in
            enumerate(comments) if val["id"] == id]
    if len(idx_list) == 0:
        return []
    res = [comments[i: j] for i, j in
            zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    if len(res) == 1:
        return []
    else:
        return res[0][:-1]

def save_latest_comment_for_author(author, comments):
    if not comments:
        return
    if author not in read_comments_file().keys():
        add_comment(author, comments[0]["id"])
    else:
        update_comment(author, comments[0]["id"])

