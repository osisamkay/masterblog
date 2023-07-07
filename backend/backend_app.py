from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all posts.

    Returns:
        A JSON response containing the list of posts, sorted based on the provided parameters if valid.
        If the sort parameters are invalid, returns a JSON response with an error message and a 400 status code.
    """
    sort_field = request.args.get('sort')
    sort_direction = request.args.get('direction')

    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. Allowed values: title, content"}), 400

    if sort_direction and sort_direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort direction. Allowed values: asc, desc"}), 400

    sorted_posts = POSTS.copy()

    if sort_field and sort_direction:
        sorted_posts.sort(key=lambda post: post[sort_field], reverse=(sort_direction == 'desc'))

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new post.

    Returns:
        If the post is successfully added, returns a JSON response with the newly created post and a 201 status code.
        If the request payload is missing or the required fields are not provided or empty, returns a JSON response with an error message and a 400 status code.
    """
    post = request.get_json()

    if not post:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['title', 'content']
    missing_fields = []

    for field in required_fields:
        if field not in post or not post[field]:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    new_post = {
        "id": POSTS[-1]['id'] + 1,
        "title": post['title'],
        "content": post['content']
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post by its ID.

    Args:
        post_id (int): The ID of the post to be deleted.

    Returns:
        If the post with the given ID exists, returns a JSON response with a success message and a 200 status code.
        If there is no post with the given ID, returns a JSON response with an error message and a 404 status code.
    """
    for index, post in enumerate(POSTS):
        if post['id'] == post_id:
            del POSTS[index]
            return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update a post by its ID.

    Args:
        post_id (int): The ID of the post to be updated.

    Returns:
        If the post with the given ID exists and the input is valid, returns a JSON response with the updated post and a 200 status code.
        If there is no post with the given ID, returns a JSON response with an error message and a 404 status code.
    """
    for post in POSTS:
        if post['id'] == post_id:
            new_title = request.json.get('title', post['title'])
            new_content = request.json.get('content', post['content'])

            post['title'] = new_title
            post['content'] = new_content

            updated_post = {
                "id": post['id'],
                "title": new_title,
                "content": new_content
            }
            POSTS.append(updated_post)
            return jsonify(updated_post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title or content.

    Returns:
        A JSON response containing the list of posts that match the search criteria.
        If no posts match the search criteria, an empty list is returned.
    """
    search_title = request.args.get('title')
    search_content = request.args.get('content')

    matching_posts = []

    for post in POSTS:
        if (search_title and search_title.lower() in post['title'].lower()) or \
           (search_content and search_content.lower() in post['content'].lower()):
            matching_posts.append(post)

    return jsonify(matching_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
