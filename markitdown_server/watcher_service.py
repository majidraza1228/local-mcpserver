#!/usr/bin/env python3
"""
MarkItDown File Watcher Service

Monitors a directory for new documents and automatically converts them to Markdown.
Converted files are saved with .md extension in an output directory.
"""

import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from markitdown import MarkItDown
from datetime import datetime

# Configuration
WATCH_DIR = Path("/Users/syedraza/Documents/markitdown")
OUTPUT_DIR = Path("/Users/syedraza/Documents/markitdown/converted")
PROCESSED_DIR = Path("/Users/syedraza/Documents/markitdown/processed")

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.xlsx', '.pptx', 
    '.html', '.txt', '.json', '.xml',
    '.jpg', '.jpeg', '.png', '.gif', '.wav'
}

class MarkItDownHandler(FileSystemEventHandler):
    """Handles file system events and converts documents to Markdown."""
    
    def __init__(self):
        self.md = MarkItDown()
        self.processing = set()  # Track files currently being processed
        
        # Create directories if they don't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        WATCH_DIR.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Watching: {WATCH_DIR}")
        print(f"📄 Output: {OUTPUT_DIR}")
        print(f"✅ Processed: {PROCESSED_DIR}")
        print(f"🔄 Ready to convert documents...\n")
    
    def on_created(self, event):
        """Handle new file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip if file is in output or processed directory
        if OUTPUT_DIR in file_path.parents or PROCESSED_DIR in file_path.parents:
            return
        
        # Check if file extension is supported
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return
        
        # Avoid processing the same file twice
        if file_path in self.processing:
            return
        
        # Wait a moment for file to be fully written
        time.sleep(1)
        
        self.convert_document(file_path)
    
    def convert_document(self, file_path: Path):
        """Convert a document to Markdown."""
        self.processing.add(file_path)
        
        try:
            print(f"🔄 Processing: {file_path.name}")
            
            # Convert to markdown
            result = self.md.convert(str(file_path))
            
            # Generate output filename
            output_filename = file_path.stem + ".md"
            output_path = OUTPUT_DIR / output_filename
            
            # Handle duplicate filenames
            counter = 1
            while output_path.exists():
                output_filename = f"{file_path.stem}_{counter}.md"
                output_path = OUTPUT_DIR / output_filename
                counter += 1
            
            # Write markdown content
            with open(output_path, 'w', encoding='utf-8') as f:
                # Add metadata header
                f.write(f"<!-- \n")
                f.write(f"Source: {file_path.name}\n")
                f.write(f"Converted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if hasattr(result, 'title') and result.title:
                    f.write(f"Title: {result.title}\n")
                f.write(f"-->\n\n")
                
                # Write content
                f.write(result.text_content)
            
            print(f"✅ Converted: {output_filename}")
            print(f"   Saved to: {output_path}\n")
            
            # Move original file to processed directory
            processed_path = PROCESSED_DIR / file_path.name
            
            # Handle duplicate filenames in processed directory
            counter = 1
            while processed_path.exists():
                processed_path = PROCESSED_DIR / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            
            file_path.rename(processed_path)
            print(f"📦 Moved to: {processed_path}\n")
            
        except Exception as e:
            print(f"❌ Error converting {file_path.name}: {str(e)}\n")
        
        finally:
            self.processing.discard(file_path)

def main():
    """Run the file watcher service."""
    print("=" * 60)
    print("MarkItDown File Watcher Service")
    print("=" * 60)
    print()
    
    # Create event handler and observer
    event_handler = MarkItDownHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    
    # Start watching
    observer.start()
    
    print(f"✨ Service started successfully!")
    print(f"📥 Drop files into: {WATCH_DIR}")
    print(f"📤 Get markdown from: {OUTPUT_DIR}")
    print(f"🛑 Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping service...")
        observer.stop()
    
    observer.join()
    print("✅ Service stopped.")

if __name__ == "__main__":
    main()
