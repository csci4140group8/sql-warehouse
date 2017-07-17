from flask import Flask, jsonify, request, send_from_directory, send_file
import service

APP = Flask(__name__)

@APP.route('/')
def get_index():
    return send_file('static/index.html')

@APP.route('/<path:path>')
def static_pages(path):
    return send_from_directory('static', path)

@APP.route('/api/heatmap')
def get_heatmap():
    return jsonify(service.getHeatmap())

@APP.route('/api/projects')
def get_projects():
    return 'projects'

@APP.route('/api/platforms')
def get_platforms():
    return 'platforms'

if __name__ == '__main__':
    APP.run(debug=True)
