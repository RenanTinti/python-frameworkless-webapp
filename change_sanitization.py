def toggle_sanitization():
    with open("config.txt", "r+") as file:
        sanitize = file.read().strip()
        if sanitize == "1":
            sanitize = "0"
        else:
            sanitize = "1"
        file.seek(0)
        file.write(sanitize)
        file.truncate()


if __name__ == "__main__":
    toggle_sanitization()
