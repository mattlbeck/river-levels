"""Entry point for the streamlit data visualisation app"""
import sys
from src.streamlit.multipage import MultiPage
from src.streamlit.pages import stations, river_levels

# Add pages to PYTHONPATH, which allows streamlit to watch
# them for changes
sys.path.append("src/streamlit/pages")

app = MultiPage()

# Add pages
for page in (stations, river_levels):
    app.add_page(page.PAGE_NAME, page.app)

app.run()
