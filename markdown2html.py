#!/usr/bin/python3
"""
markdown2html.py: A script to convert a Markdown file to an HTML file.

Usage:
    ./markdown2html.py <input_markdown_file> <output_html_file>

    - The script takes two arguments:
        1. The name of the Markdown file to read (input).
        2. The name of the output HTML file to write to (output).

    - If the number of arguments is less than 2,
    it prints an error message and exits.
    - If the Markdown file doesn’t exist,
    it prints an error message and exits.
    - The script parses headings, unordered lists, ordered lists, paragraphs,
      and bold/emphasized text in Markdown format and converts them to HTML.

Markdown Syntax Supported:
    - # Heading level 1 converts to <h1>Heading level 1</h1>
    - ## Heading level 2 converts to <h2>Heading level 2</h2>
    - ### Heading level 3 converts to <h3>Heading level 3</h3>
    - #### Heading level 4 converts to <h4>Heading level 4</h4>
    - ##### Heading level 5 converts to <h5>Heading level 5</h5>
    - ###### Heading level 6 converts to <h6>Heading level 6</h6>
    - Unordered lists with '-' convert to <ul><li>...</li></ul>
    - Ordered lists with '*' convert to <ol><li>...</li></ol>
    - Paragraphs convert to <p>...</p>
    - Bold text with '**' converts to <b>...</b>
    - Emphasized text with '__' converts to <em>...</em>

Exit codes:
    - 0: Success
    - 1: Error (wrong number of arguments or missing file)

Example:
    ./markdown2html.py README.md README.html
"""

import sys
import os
import re

def convert_line_to_html(line):
    """Convert a single line of markdown to HTML."""
    # Match bold text between ** and capture everything inside
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    # Match emphasized text between __ and capture everything inside
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)

    return line


if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Get the input and output file names
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r') as infile, \
        open(output_file, 'w') as outfile:
            in_unordered_list = False
            in_ordered_list = False
            paragraph_content = []

            for line in infile:
                # Strip leading and trailing spaces/newlines
                line = line.strip()

                # Handle empty lines for paragraphs
                if not line:
                    if paragraph_content:
                        # Join paragraph content and write it as a <p> element
                        paragraph_text = ' '.join(paragraph_content).strip()
                        outfile.write(f"<p>{paragraph_text}</p>\n")
                        paragraph_content = []  # Reset for next paragraph
                    if in_unordered_list:
                        outfile.write("</ul>\n")
                        in_unordered_list = False
                    if in_ordered_list:
                        outfile.write("</ol>\n")
                        in_ordered_list = False
                    continue

                # Check for headings
                if line.startswith('#'):
                    heading_level = len(line.split(' ')[0])
                    if 1 <= heading_level <= 6:
                        heading_content = line[heading_level:].strip()
                        outfile.write(f"<h{heading_level}>{heading_content}</h{heading_level}>\n")
                    continue  # Skip to the next line

                # Handle unordered lists
                if line.startswith('- '):
                    if not in_unordered_list:
                        outfile.write("<ul>\n")
                        in_unordered_list = True
                    list_item = line[2:].strip()
                    list_item_html = convert_line_to_html(list_item)
                    outfile.write(f"<li>{list_item_html}</li>\n")
                    continue

                # Handle ordered lists
                if line.startswith('* '):
                    if not in_ordered_list:
                        outfile.write("<ol>\n")
                        in_ordered_list = True
                    list_item = line[2:].strip()
                    list_item_html = convert_line_to_html(list_item)
                    outfile.write(f"<li>{list_item_html}</li>\n")
                    continue

                # Handle paragraph content (including bold and emphasis)
                line = line.replace('**', '<b>', 1).replace('__', '<em>', 1)
                line = line.replace('**', '</b>', 1).replace('__', '</em>', 1)
                if paragraph_content:
                    # If there is already paragraph content, we append a line break
                    paragraph_content.append(f"<br/>{line}")
                else:
                    paragraph_content.append(line)  # Add line to paragraph content

            # Close any remaining paragraph at the end of the file
            if paragraph_content:
                paragraph_text = ' '.join(paragraph_content).strip()
                outfile.write(f"<p>{paragraph_text}</p>\n")

            if in_unordered_list:
                outfile.write("</ul>\n")
            if in_ordered_list:
                outfile.write("</ol>\n")

        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
