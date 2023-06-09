import wsgiref.simple_server
import urllib.parse
import sqlite3


def sanitize(input_string):
    output_string = ""
    for i in input_string:
        if i == ">":
            outchar = "&gt;"
        elif i == "<":
            outchar = "&lt;"
        else:
            outchar = i
        output_string += outchar
    return output_string


def get_sanitization_setting():
    with open("config.txt", "r") as file:
        sanitize = file.read().strip()
        return sanitize


sanitize_input_fields = get_sanitization_setting()

forms_data = []

conn = sqlite3.connect("feedback.db")
c = conn.cursor()


def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    content_type = "text/html"

    if path == "/":
        if method == "POST":
            input_obj = environ["wsgi.input"]

            input_length = int(environ["CONTENT_LENGTH"])

            body = input_obj.read(input_length).decode()

            data = urllib.parse.parse_qs(body, keep_blank_values=True)

            if sanitize_input_fields == "1":
                req = {
                    "name": sanitize(data["name"][0]),
                    "email": sanitize(data["email"][0]),
                    "type": sanitize(data["f-type"][0]),
                    "content": sanitize(data["feedback"][0]),
                }
            elif sanitize_input_fields == "0":
                req = {
                    "name": data["name"][0],
                    "email": data["email"][0],
                    "type": data["f-type"][0],
                    "content": data["feedback"][0],
                }

            # Insert the data into the SQLite database
            c.execute(
                """
                INSERT INTO feedback (name, email, type, content)
                VALUES (?, ?, ?, ?)
            """,
                (req["name"], req["email"], req["type"], req["content"]),
            )
            conn.commit()
            forms_data.append(req)

            response = b"Your feedback submitted successfully."
            status = "200 OK"
        else:
            with open("page.html", "r") as f:
                response = f.read().encode()
            status = "200 OK"

    elif path == "/feedback/":
        c.execute("SELECT * FROM feedback")
        data = c.fetchall()

        # Generate an HTML table with the data
        html = "<table>"
        html += "<tr><th>ID</th><th>Name</th><th>Email</th><th>Type</th><th>Content</th></tr>"
        for row in data:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
        html += "</table>"

        response = html.encode()
        status = "200 OK"
        content_type = "text/html"

    else:
        response = b"<h1>Not found</h1><p>Entered path not found</p>"
        status = "404 Not Found"

    headers = [("Content-Type", content_type), ("Content-Length", str(len(response)))]

    start_response(status, headers)
    return [response]


if __name__ == "__main__":
    try:
        w_s = wsgiref.simple_server.make_server(host="localhost", port=8021, app=application)
        w_s.serve_forever()
    except KeyboardInterrupt:
        conn.close()
