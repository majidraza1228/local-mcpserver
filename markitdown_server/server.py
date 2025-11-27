from fastmcp import FastMCP
from markitdown import MarkItDown
import os

app = FastMCP(name="markitdown", instructions="Convert files and URLs to Markdown format")
md = MarkItDown()

@app.tool(description="Convert a local file to Markdown")
def convert_file(path: str):
    """Convert a local file (PDF, DOCX, XLSX, PPTX, images, etc.) to Markdown."""
    try:
        if not os.path.exists(path):
            return {"error": f"File not found: {path}"}
        
        result = md.convert(path)
        return {
            "success": True,
            "markdown": result.text_content,
            "source": path,
            "title": result.title if hasattr(result, 'title') else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.tool(description="Convert a URL to Markdown")
def convert_url(url: str):
    """Convert web page content from a URL to Markdown."""
    try:
        result = md.convert(url)
        return {
            "success": True,
            "markdown": result.text_content,
            "source": url,
            "title": result.title if hasattr(result, 'title') else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.tool(description="Convert multiple files to Markdown")
def convert_batch(paths: list):
    """Convert multiple files to Markdown in batch."""
    results = []
    for path in paths:
        try:
            if os.path.exists(path):
                result = md.convert(path)
                results.append({
                    "success": True,
                    "path": path,
                    "markdown": result.text_content,
                    "title": result.title if hasattr(result, 'title') else None
                })
            else:
                results.append({
                    "success": False,
                    "path": path,
                    "error": "File not found"
                })
        except Exception as e:
            results.append({
                "success": False,
                "path": path,
                "error": str(e)
            })
    
    return {
        "total": len(paths),
        "successful": sum(1 for r in results if r.get("success")),
        "results": results
    }

@app.tool(description="Get supported file formats")
def get_supported_formats():
    """List all file formats supported by MarkItDown."""
    return {
        "formats": [
            {"extension": ".pdf", "description": "PDF documents"},
            {"extension": ".docx", "description": "Microsoft Word documents"},
            {"extension": ".xlsx", "description": "Microsoft Excel spreadsheets"},
            {"extension": ".pptx", "description": "Microsoft PowerPoint presentations"},
            {"extension": ".html", "description": "HTML files"},
            {"extension": ".txt", "description": "Plain text files"},
            {"extension": ".json", "description": "JSON files"},
            {"extension": ".xml", "description": "XML files"},
            {"extension": ".jpg", "description": "JPEG images (with OCR)"},
            {"extension": ".png", "description": "PNG images (with OCR)"},
            {"extension": ".gif", "description": "GIF images"},
            {"extension": ".wav", "description": "Audio files (with transcription)"}
        ],
        "url_support": True,
        "ocr_enabled": True,
        "audio_transcription": True
    }

if __name__ == "__main__":
    app.run()

