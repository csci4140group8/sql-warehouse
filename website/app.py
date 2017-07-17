from flask import Flask, jsonify, request, send_from_directory

APP = Flask(__name__)

@APP.route('/<path:path>', methods=['GET'])
def static_pages(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    APP.run(debug=True)
