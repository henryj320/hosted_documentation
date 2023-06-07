"""Main script to convert Markdown files into HTML files."""

def create_single_file(md_path: str) -> bool:
    """Converts a single .md file into a .html page.

    Args:
        md_path (str): Path to the Markdown file being converted.

    Returns:
        bool: T/F whether the file was converted successfully or not
    """

    if not isinstance(md_path, str):
        return False

    # Finds the path that the HTML page will be
    HTML_path = md_path.split(".md")[0].replace(" ", "_") + ".html"

    # Creates a new file in the given path.
    file = open(HTML_path, "x")
    file.close()

    file = open(HTML_path, "w")
    file.write("Hey there!")
    file.close()

    return True



if __name__ == "__main__":
    print("Yep")

    create_single_file("Vault/Example.md")