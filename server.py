from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/web/', defaults={'path': ''})
@app.route('/web/<path:path>')

def serve(path):
    # Default file
    if path == "":
        path = "index.html"

    file_path = f"web/{path}"

    # If file exists, serve it
    if not os.path.isfile(file_path):
        return f"Invalid Path {file_path}"

    if path.endswith(".html"):
        resp = open(file_path).read()
        size = len(resp) 
        print(f" > Loaded {file_path} | {size:,} bytes")

        return resp

    print(f" > Sending {file_path} ")

    return send_file(file_path) 


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
