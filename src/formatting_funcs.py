def pop_id_set_author_reformat_comment(comment, author):
    attributes = comment.pop("attributes")
    comment["date"] = attributes["date"]
    comment["tags"] = attributes["tags"]
    comment["text"] = attributes["text"]
    comment["votes"] = attributes["votes"]
    del comment["type"]
    comment["url"] = comment.pop("links")["self"]
    comment["author"] = author
    return comment.pop("id")

def get_filtered_file(file):
    return {"md5": file["attributes"].get("md5"),
            "sha1": file["attributes"].get("sha1"),
            "sha256": file["attributes"].get("sha256")}

def get_filtered_domain(domain):
    return {"domain": domain["id"]}

def get_filtered_url(url):
    return {"url": url["attributes"]["url"]}

def get_filtered_ip_address(ip_address):
    return {"ip_address": ip_address["id"]}

def get_filtered_item_related(item_related):
    if item_related["type"] == "file":
        return get_filtered_file(item_related)
    elif item_related["type"] == "domain":
        return get_filtered_domain(item_related)
    elif item_related["type"] == "url":
        return get_filtered_url(item_related)
    elif item_related["type"] == "ip_address":
        return get_filtered_ip_address(item_related)
    else:
        raise NotImplementedError(f"Item related type {item_related['type']} doesn't exist")

