import json
import os
from jinja2 import Template
from playwright.sync_api import sync_playwright
from __init__ import __VERSION__

def main():
    with open('reality_cube.json', 'r') as f:
        data = json.load(f)

    with open('template.html', 'r') as f:
        template = Template(f.read())

    html = template.render(data=data, version=__VERSION__)
    html_path = os.path.abspath('reality_cube_rendered.html')
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
