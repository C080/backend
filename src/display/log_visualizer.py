from io import StringIO
from pathlib import Path

from bs4 import BeautifulSoup
from rich.console import Console
from rich.syntax import Syntax

from src.display.css_html_js import style_content
from src.envs import NUM_LINES_VISUALIZE
from src.logging import log_file

proj_dir = Path(__name__).parent


def log_file_to_html_string():
    with open(log_file, "rt") as f:
        # Seek to the end of the file minus 300 lines
        # Read the last 300 lines of the file
        lines = f.readlines()
        lines = lines[-NUM_LINES_VISUALIZE:]

        # Syntax-highlight the last 300 lines of the file using the Python lexer and Monokai style
        output = "".join(reversed(lines))
        syntax = Syntax(output, "python", theme="monokai", word_wrap=True)

    console = Console(record=True, width=150, style="#272822", file=StringIO())
    console.print(syntax)
    html_content = console.export_html(inline_styles=True)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # Modify the <pre> tag
    pre_tag = soup.pre
    pre_tag['class'] = 'scrollable'
    del pre_tag['style']

    # Add your custom styles and the .scrollable CSS to the <style> tag
    style_tag = soup.style
    style_tag.append(style_content)

    return soup.prettify()
