#using uv so this is only required to pass the cli tests
python3 src/main.py
cd public && python3 -m http.server 8888