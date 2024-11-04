from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__, template_folder='wal')
url = "https://wallhaven.cc/api/v1/search"

@app.route('/')
def index():
    return render_template('wall.html')
@app.route('/api/wallpapers', methods=['GET'])
def get_wallpapers():
    device = request.args.get('device', default='desktop', type=str)
    resolution = '3840x2160' if device == 'desktop' else '1080x1920'
    query_terms = ['nature', 'abstract', 'city', 'animals', 'technology', 'art', 'anime', 'cars', 'space', 'fantasy']
    query = random.choice(query_terms)
    params = {
        'q': query,
        'categories': '111',
        'purity': '100',
        'page': 1,
        'sorting': 'random',
        'resolutions': resolution
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['data']:
        wallpapers = [{"url": item['path'], "id": item['id']} for item in data['data']]
        return jsonify(wallpapers)
    else:
        return jsonify({"message": "womp womp wallpapers not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
