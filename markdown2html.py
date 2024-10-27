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
    - The script parses headings in Markdown format and converts them to HTML.

Markdown Syntax Supported:
    - # Heading level 1 converts to <h1>Heading level 1</h1>
    - ## Heading level 2 converts to <h2>Heading level 2</h2>
    - ### Heading level 3 converts to <h3>Heading level 3</h3>
    - #### Heading level 4 converts to <h4>Heading level 4</h4>
    - ##### Heading level 5 converts to <h5>Heading level 5</h5>
    - ###### Heading level 6 converts to <h6>Heading level 6</h6>
    - Unordered lists with '-' convert to <ul><li>...</li></ul>
    - Ordered lists with '*' convert to <ol><li>...</li></ol>

Exit codes:
    - 0: Success
    - 1: Error (wrong number of arguments or missing file)

Example:
    ./markdown2html.py README.md README.html

"""


import sys
import os

if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
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

            for line in infile:
                # Strip leading and trailing spaces/newlines
                line = line.strip()

                # Check for headings (Markdown syntax)
                if line.startswith('#'):
                    # Count the number of '#' to determine
                    # the heading level
                    heading_level = len(line.split(' ')[0])
                    if 1 <= heading_level <= 6:
                        # Extract the heading content after the '#' symbols
                        heading_content = line[heading_level:].strip()
                        # Write the corresponding HTML tag
                        # to the output file
                        outfile.write(
                                f"<h{heading_level}>"
                                f"{heading_content}"
                                f"</h{heading_level}>\n"
                                )
                    continue  # Skip to the next line

                # Check for unordered lists
                if line.startswith('- '):
                    if not in_unordered_list:
                        outfile.write("<ul>\n")
                        in_unordered_list = True
                    # Extract the list item content
                    list_item = line[2:].strip()
                    outfile.write(f"<li>{list_item}</li>\n")
                    continue

                # Check for ordered lists
                if line.startswith('* '):
                    if not in_ordered_list:
                        outfile.write("<ol>\n")
                        in_ordered_list = True
                    # Extract the list item content
                    list_item = line[2:].strip()
                    outfile.write(f"<li>{list_item}</li>\n")
                    continue

                # Close any open lists if the line is empty or doesn't match
                if in_unordered_list:
                    outfile.write("</ul>\n")
                    in_unordered_list = False
                if in_ordered_list:
                    outfile.write("</ol>\n")
                    in_ordered_list = False

            # Close any open lists at the end of the file
            if in_unordered_list:
                outfile.write("</ul>\n")
            if in_ordered_list:
                outfile.write("</ol>\n")

        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
