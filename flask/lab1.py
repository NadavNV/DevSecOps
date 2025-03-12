import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)
index = 0
posts = []


@app.get('/posts')
def get_all_posts():
    return jsonify({'success': True, 'posts': posts})


@app.get('/posts/<post_id>')
def get_post_by_id(post_id):
    for post in posts:
        if post['id'] == int(post_id):
            return jsonify({'success': True, 'post': post})
    return "Post not found", 404


def validate_post(post: dict) -> bool:
    return 'title' in post and 'content' in post and 'author' in post


@app.post('/posts')
def add_post():
    global index
    new_post = request.json
    if validate_post(new_post):
        index += 1
        # I'm creating the new post like this instead of just appending
        # new_post directly because new_post might have additional fields
        # that I do not want to keep.
        new_post = {
            'id': index,
            'title': new_post['title'],
            'content': new_post['content'],
            'author': new_post['author'],
            'date_posted': datetime.datetime.now().replace(microsecond=0).isoformat(),
        }
        posts.append(new_post)
        return jsonify({'success': True, 'post': new_post}), 201
    else:
        return 'invalid data', 400


if __name__ == "__main__":
    app.run(port=5000)
