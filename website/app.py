from flask import Flask, jsonify, request, send_from_directory, send_file
import service

APP = Flask(__name__)

# Static Files

@APP.route('/')
def get_index():
    return send_file('static/index.html')

@APP.route('/<path:path>')
def static_pages(path):
    return send_from_directory('static', path)

# Utility endpoints, for determining the interactive bits

@APP.route('/api/timesteps/<scale>')
def get_timesteps(scale):
    return jsonify(service.getTimeSteps(scale))

@APP.route('/api/project_ids')
def get_project_ids():
    return jsonify(service.getProjects())

# Visualizations

@APP.route('/api/heatmap')
def get_heatmap():
    scale = request.args.get('scale')
    value = request.args.get('value')
    return jsonify(service.getHeatmap(scale, value))

@APP.route('/api/projects')
def get_projects():
    project_id = request.args.get('project_id')
    return jsonify(service.getProjectBoundaries(project_id))

@APP.route('/api/platforms')
def get_platforms():
    project_id = request.args.get('project_id')
    return jsonify(service.getPlatforms(project_id))

if __name__ == '__main__':
    APP.run(debug=True)
