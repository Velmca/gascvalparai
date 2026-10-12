import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import mimetypes

st.set_page_config(
    page_title="Government Arts and Science College, Valparai",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent

def file_to_data_uri(file_path):
    """Convert a local image into a browser-safe data URI."""
    path = BASE_DIR / file_path
    if not path.exists():
        return ""
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"

def load_css():
    css_path = BASE_DIR / "css" / "style.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""

def build_home_page():
    # Read the existing HTML page.
    html_path = BASE_DIR / "index.html"
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
    else:
        html = """
        <h1>Government Arts and Science College, Valparai</h1>
        <p>index.html was not found in the repository.</p>
        """

    # Replace Windows absolute image paths with repository-relative paths.
    windows_path_pattern = r'C:\\Users\\GASC3\\Desktop\\COLLEGE-WEBSITE\\GASC_Valparai_College_Website\\'
    html = html.replace(windows_path_pattern, "")

    # Convert image references to data URIs so they work on Streamlit Cloud.
    image_names = re.findall(r'(?:src=["\'])([^"\']+\.(?:png|jpg|jpeg|webp|gif))', html, re.I)
    for image_name in set(image_names):
        image_uri = file_to_data_uri(image_name)
        if image_uri:
            html = html.replace(image_name, image_uri)

    # Remove external CSS link because we inject CSS below.
    html = re.sub(
        r'<link[^>]+href=["\']css/style\.css["\'][^>]*>',
        "",
        html,
        flags=re.I
    )

    # Prevent the old HTML page from trying to load its own full document.
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.I | re.S)
    if body_match:
        body = body_match.group(1)
    else:
        body = html

    css = load_css()

    # Streamlit Cloud-safe HTML document.
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                background: transparent;
            }}
            {css}
        </style>
    </head>
    <body>
        {body}
    </body>
    </html>
    """

    components.html(
        page,
        height=1500,
        scrolling=True
    )

build_home_page()
