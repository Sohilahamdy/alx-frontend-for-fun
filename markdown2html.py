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
    - If the Markdown file doesn’t exist, it prints an error message and exits.

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

        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
