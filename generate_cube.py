import json
import os
import re
from jinja2 import Template
from playwright.sync_api import sync_playwright
from __init__ import __VERSION__


def markdown_to_html(text):
    """Convert simple markdown to HTML."""
    if not text:
        return text
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = text.replace('\n', '<br>')
    text = text.replace(' | ', ' &nbsp;|&nbsp; ')
    return text


def process_data(obj):
    """Recursively process all string values in the data structure."""
    if isinstance(obj, dict):
        return {k: process_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_data(item) for item in obj]
    elif isinstance(obj, str):
        return markdown_to_html(obj)
    return obj


def main():
    with open('reality_cube.json', 'r') as f:
        raw_data = json.load(f)

    data = process_data(raw_data)

    with open('template.html', 'r') as f:
        template = Template(f.read())

    html = template.render(data=data, version=__VERSION__)
    html_path = os.path.abspath('index.html')
    png_path = os.path.abspath('reality_cube.png')

    with open(html_path, 'w') as f:
        f.write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 720, 'height': 100}, device_scale_factor=2)
        page.goto(f'file://{html_path}')
        page.screenshot(path=png_path, full_page=True, scale='device')
        browser.close()

    print(f"Success! Generated {png_path}")


if __name__ == "__main__":
    main()
