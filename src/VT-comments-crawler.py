import urllib3
urllib3.disable_warnings()
import logging
import traceback
from config import Config
from vt import VT
import sys
from elasticsearch import Elasticsearch, helpers
import formatting_funcs as ff
import latest_comments as lc

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y/%m/%d %H:%M:%S",
    handlers=[
        logging.StreamHandler()
    ]
)

def main(argv):
    vt = VT(url="https://www.virustotal.com", apikey=Config["vt"]["key"])
    es = Elasticsearch(hosts=[Config["elastic"]["proto"] + "://" + 
        Config["elastic"]["username"] + ":" +
        Config["elastic"]["password"] + "@" + 
        Config["elastic"]["host"] + ":" +
        str(Config["elastic"]["port"])], http_compress=True, verify_certs=False, request_timeout=60)

    comments = {}
    comment_authors = Config["vt"]["comment_authors"]
    logging.info(f"Found {len(comment_authors)} comment authors")
    for author in comment_authors:
        comments[author] = lc.get_filtered_comments(author, vt.get_user_comments(author))
        logging.info(f"Found {len(comments[author])} comments for author {author}")
        for comment in comments[author]:
            comment["item_related"] = vt.get_item_given_comment_id(comment["id"])
        logging.info(f"Retrieved all items related to author {author} comments")
        lc.save_latest_comment_for_author(author, comments[author])

    for author, author_comments in comments.items():
        logging.info(f"Pushing comments found for the author {author} to elastic")
        for comment in author_comments:
            if comment["item_related"]["type"] == "graph":
                continue
            index = Config["elastic"]["indexes"][comment["item_related"]["type"]]
            id = ff.pop_id_set_author_reformat_comment(comment, author)
            comment["item_related"] = ff.get_filtered_item_related(comment["item_related"])
            es.index(index=index, id=id, document=comment)
    logging.info("Pushed all comments to elastic")
    for k, index in Config["elastic"]["indexes"].items():
        es.indices.refresh(index=index)
    logging.info("Refreshed all elastic indexes")

    logging.info("Finished")

if __name__ == "__main__":
    try:
        main(sys.argv)
    except:
        logging.error(f"Got a fatal error")
        logging.error(traceback.format_exc().strip())
