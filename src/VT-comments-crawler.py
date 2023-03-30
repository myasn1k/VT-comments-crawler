import logging
import traceback
from config import Config
from vt import VT
import sys
from elasticsearch import Elasticsearch, helpers

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
        Config["elastic"]["port"]], http_compress=True, verify_certs=False, timeout=60)

    comments = {}
    comment_authors = Config["vt"]["comment_authors"]
    logging.info(f"Found {len(comment_authors)} comment authors")
    for author in comment_authors:
        comments[author] = vt.get_user_comments(author)
        logging.info(f"Found {len(comments[author])} comments for author {author}")
        for comment in comments[author]:
            comment["item_related"] = vt.get_item_given_comment_id(comment["id"])
        logging.info(f"Retrieved all items related to author {author} comments")

    logging.info("Finished")

if __name__ == "__main__":
    try:
        main(sys.argv)
    except:
        logging.error(f"Got a fatal error")
        logging.error(traceback.format_exc().strip())
