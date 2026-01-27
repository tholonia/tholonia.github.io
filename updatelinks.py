#!/usr/bin/env python3
"""
Update download links and version number in the_book_FRONT.html
Usage: ./updatelinks.py --pdf <url> --md <url> --html <url> --epub <url> --ver <version>
"""

import argparse
import re
from pathlib import Path

def update_links(file_path, pdf_url=None, md_url=None, html_url=None, epub_url=None, version=None):
    """Update download links and version in the HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = False
    
    # Update PDF link
    if pdf_url:
        content = re.sub(
            r'(<li>\s*<a\s+href=")[^"]+(">\s*<img alt="Download PDF")',
            rf'\g<1>{pdf_url}\g<2>',
            content
        )
        updated = True
        print(f"✅ Updated PDF link to: {pdf_url}")
    
    # Update MD link
    if md_url:
        content = re.sub(
            r'(<li>\s*<a\s+href=")[^"]+(">\s*<img alt="Download MD")',
            rf'\g<1>{md_url}\g<2>',
            content
        )
        updated = True
        print(f"✅ Updated MD link to: {md_url}")
    
    # Update HTML link
    if html_url:
        content = re.sub(
            r'(<a href=")[^"]+(">\s*<img alt="Download HTML")',
            rf'\g<1>{html_url}\g<2>',
            content
        )
        updated = True
        print(f"✅ Updated HTML link to: {html_url}")
    
    # Update ePub link
    if epub_url:
        content = re.sub(
            r'(<a href=")[^"]+(">\s*<img alt="Download ePub")',
            rf'\g<1>{epub_url}\g<2>',
            content
        )
        updated = True
        print(f"✅ Updated ePub link to: {epub_url}")
    
    # Update version number
    if version:
        content = re.sub(
            r'(<i>Current version )[^<]+(</i>)',
            rf'\g<1>{version}\g<2>',
            content
        )
        updated = True
        print(f"✅ Updated version to: {version}")
    
    if updated:
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n🎉 Successfully updated {file_path}")
    else:
        print("⚠️  No updates specified. Use --help for usage information.")

def main():
    parser = argparse.ArgumentParser(
        description='Update download links and version in the_book_FRONT.html',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update all links and version
  ./updatelinks.py --pdf "https://..." --md "https://..." --html "https://..." --epub "https://..." --ver "8.0.19, January 24, 2026"
  
  # Update only version
  ./updatelinks.py --ver "8.0.19, January 24, 2026"
  
  # Update only PDF and version
  ./updatelinks.py --pdf "https://..." --ver "8.0.19, January 24, 2026"
        """
    )
    
    parser.add_argument('--pdf', type=str, help='New PDF download URL')
    parser.add_argument('--md', type=str, help='New Markdown download URL')
    parser.add_argument('--html', type=str, help='New HTML download URL')
    parser.add_argument('--epub', type=str, help='New ePub download URL')
    parser.add_argument('--ver', type=str, help='New version string (e.g., "8.0.19, January 24, 2026")')
    parser.add_argument('--file', type=str, default='_layouts/the_book_FRONT.html',
                        help='Path to the HTML file (default: _layouts/the_book_FRONT.html)')
    
    args = parser.parse_args()
    
    # Check if at least one argument is provided
    if not any([args.pdf, args.md, args.html, args.epub, args.ver]):
        parser.print_help()
        return
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return
    
    update_links(
        file_path,
        pdf_url=args.pdf,
        md_url=args.md,
        html_url=args.html,
        epub_url=args.epub,
        version=args.ver
    )

if __name__ == '__main__':
    main()
