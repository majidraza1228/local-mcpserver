from fastmcp import FastMCP, tool
from markitdown import MarkItDown
app = FastMCP(name="markitdown", description="Convert files and URLs to Markdown")
mid = MarkItDown()
@tool(description="Convert a local file to Markdown")
def convert_file(path: str):
    return {"markdown": mid.convert(path).text()}
@tool(description="Convert a URL to Markdown")
def convert_url(url: str):
    return {"markdown": mid.convert(url).text()}
