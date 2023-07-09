# run.py

from app import create_app

app = create_app()

# This will print all the routes
# for rule in app.url_map.iter_rules():
#     print(rule)

if __name__ == "__main__":
    app.run(debug=True, port=4444)

