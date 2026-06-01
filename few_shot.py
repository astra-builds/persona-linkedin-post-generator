import json

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.file_path = file_path
        self.posts = []
        self.load_posts()

    def load_posts(self):
        with open(self.file_path, encoding='utf-8') as f:
            self.posts = json.load(f)

    def get_filtered_posts(self, length=None, language=None, tag=None):
        filtered = self.posts[:]

        if length and length != "any":
            if length == "short":
                filtered = [p for p in filtered if p["line_count"] <= 5]
            elif length == "medium":
                filtered = [p for p in filtered if 6 <= p["line_count"] <= 10]
            elif length == "long":
                filtered = [p for p in filtered if p["line_count"] >= 11]

        if language and language != "any":
            filtered = [p for p in filtered if p["language"].lower() == language.lower()]

        if tag and tag != "any":
            filtered = [p for p in filtered if tag.lower() in [t.lower() for t in p["tags"]]]

        return filtered

    def get_few_shots(self, length=None, language=None, tag=None, count=3):
        filtered = self.get_filtered_posts(length, language, tag)
        filtered.sort(key=lambda p: p["engagement"], reverse=True)
        return [p["text"] for p in filtered[:count]]
