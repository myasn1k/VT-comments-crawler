import requests

class VT():

    headers = {}
    url = ""

    def __init__(self, url: str, apikey: str):
        self.url = url
        self.headers = {"x-apikey": apikey, "accept": "application/json", "content-type": "application/json"}

    def do_patch(self, url, json):
        return requests.patch(self.url + url, headers=self.headers, json=json).status_code

    def do_delete(self, url):
        return requests.delete(self.url + url, headers=self.headers).status_code

    def do_get(self, url):
        return requests.get(self.url + url, headers=self.headers).json()
    
    def do_post(self, url, json):
        return requests.post(self.url + url, headers=self.headers, json=json).json()

    def get_item_given_comment_id(self, comment_id):
        return self.do_get(f"/api/v3/comments/{comment_id}/item")["data"]

    def get_user_comments(self, user):
        # Maybe here we could use the cursor (https://developers.virustotal.com/reference/users-relationships) to get all of them but i don't think it will be necessary
        return self.do_get(f"/api/v3/users/{user}/comments?limit=40")["data"]
