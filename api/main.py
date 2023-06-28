"""Main script to convert Markdown files into HTML files."""
from glob import glob

website_location = "/usr/share/nginx/html/"

def run_all(parent_directory_path: str) -> bool:

    # Finds all MarkDown files within the directory.
    all_files = glob(f"{parent_directory_path}/**/*.md", recursive=True)

    for filename in all_files:

        # shortened_filename = filename.replace(f"{parent_directory_path}/", "")

        create_single_file(filename)

        print(filename)



    print(all_files)
    pass

def create_single_file(md_path: str) -> bool:
    """Converts a single .md file into a .html page.

    Args:
        md_path (str): Path to the Markdown file being converted.

    Returns:
        bool: T/F whether the file was converted successfully or not
    """

    if not isinstance(md_path, str):
        return False
    

    given_file = open(md_path, 'r')
    given_lines = given_file.readlines()
    given_file.close()


    # Stores each line from the input .md in an array.
    count = 0
    given_array = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "</head>",
        "<body>"
        ]
    
    # Adds each line from the MarkDown into the array.
    for line in given_lines:
        count += 1

        # Removes the newline from the end of each line.
        line = line.split("\n")[0]

        given_array.append(line)


    given_array.append("</body>")
    given_array.append("</html>")


    # Finds the path that the HTML page will be
    HTML_path = md_path.split(".md")[0].replace(" ", "_") + ".html"

    HTML_path_split = HTML_path.split("/")
    HTML_path = HTML_path_split[len(HTML_path_split)-1]
    HTML_path = website_location + HTML_path
    

    # Outputs each line of the array into a HTML file
    output_file = open(HTML_path, "w")
    for line in given_array:
        output_file.write(line)
    output_file.close()

    # Creates a new file in the given path.
    # file = open(HTML_path, "x")
    # file.close()

    # file = open(HTML_path, "w")http://192.168.1.113:1008/Test.html
    # file.write("Hey there!")
    # file.close()

    return True



if __name__ == "__main__":
    print("Yep")

    # create_single_file("/Vault/" + "Test.md")http://192.168.1.113:1008/Test.html

    run_all("Vault")

