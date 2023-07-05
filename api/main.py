"""Main script to convert Markdown files into HTML files."""
from glob import glob
import os
from pathlib import Path

website_location = "/usr/share/nginx/html/"
# Testing: website_location = "Output/"

def run_all(parent_directory_path: str) -> bool:
    # Finds all MarkDown files within the directory.
    all_files = glob(f"{parent_directory_path}/**/*.md", recursive=True)

    # Converts all .md files into .html.
    for filename in all_files:
        create_single_file(filename)


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


    HTML_path_split = HTML_path.split("/")

    directories = HTML_path_split
    directories.pop()  # Removes the file from directories array.

    # Creates a path of all directories (e.g. First_Dir/Sec_Dir).
    directories_to_add = website_location

    # Replaces " " with "_" to create a full path of directories to add.
    for index, directory in enumerate(directories):
        directory = directory.replace(" ", "_")
        directories_to_add = directories_to_add + directory

        if index != len(directories) - 1:
            directories_to_add = directories_to_add + "/"

    # Makes each directory recursively.
    path = Path(directories_to_add)
    os.makedirs(directories_to_add, exist_ok=True)


    # Removes everything except the filename.html.
    HTML_path = website_location + HTML_path
    
    # Reads the .md file and stores it as an array.
    given_file = open(md_path, 'r')
    given_lines = given_file.readlines()
    given_file.close()


    # Stores each line from the input .md in an array.
    count = 0
    given_array = [
        "<html>",
        "<head>",
        "<link rel='stylesheet' href='/Config/master.css'>",
        "</head>",
        "<body>"
        ]
    
    code_block_entered = False

    # Adds each line from the .md into the array.
    for line in given_lines:
        count += 1

        # Removes the newline from the end of each line.
        line = line.split("\n")[0]        

        image_present = False
        image_extensions = [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".eps", ".raw"]

        # Converts images to HTML format
        for ext in image_extensions:
            if ext in line and "![" in line:

                image_present = True

                url_split = line.split("(")[1]  # Removes "![](".
                url_split = url_split.split(")")[0]  # Removes ")".

                url_split = url_split.split("/")

                # If image is not in a subfolder.
                if len(url_split) == 1:
                    line = f"<img src='{url_split[0]}'>"
                    image_present = True

                else:

                    filename = url_split.pop()  # Takes the filename and removes the end ")".

                    url_split.pop(0) # Removes the "![](".

                    full_path = "./Vault/"
                    for directory in url_split:
                        full_path += directory + "/"
                
                    full_path += filename

                    line = f"<img src='{full_path}'>"

                    image_present = True
            
        
        # Stop converting if line is an image.
        if not image_present:

            # Converting headers.
            if "######" in line:
                line_split = line.split("###### ")[1]
                line = f"<h6>{line_split}</h6>"
            elif "#####" in line:
                line_split = line.split("##### ")[1]
                line = f"<h5>{line_split}</h5>"
            elif "####" in line:
                line_split = line.split("#### ")[1]
                line = f"<h4>{line_split}</h4>"
            elif "###" in line:
                line_split = line.split("### ")[1]
                line = f"<h3>{line_split}</h3>"
            elif "##" in line:
                line_split = line.split("## ")[1]
                line = f"<h2>{line_split}</h2>"
            elif "#" in line:
                line_split = line.split("# ")[1]
                line = f"<h1>{line_split}</h1>"

            elif "---" in line:
                line = "<hr>"


            # Converts all other lines into paragraphs.
            elif line != "":
                line = f"<p>{line}</p>"
        

            # Converting bold & italic, bold and italic instances.
            if "***" in line:
                location = line.find("***")  # Finds where the next "***" is.
                opened_tag = True
                new_line = line[:location] + "<b><i>"

                line = line[(location + 3):]  # Removes the beginning of line.
                location = line.find("***")  

                # Loop until no more "***"
                while location != -1:

                    if not opened_tag:
                        new_line = f"{new_line}{line[:location]}<b><i>"
                        opened_tag = True
                    else:
                        new_line = f"{new_line}{line[:location]}</i></b>"
                        opened_tag = False

                    # Removes the beginning of the line.
                    line = line[(location + 3):]

                    # Finds the next instance of "***"
                    location = line.find("***")

                # Adds the final to the line after no more "***" is found.
                new_line += line
                line = new_line


            # Converting Bold to HTML
            elif "**" in line:
                location = line.find("**")  # Finds where the next "***" is.
                opened_tag = True
                new_line = line[:location] + "<b>"

                line = line[(location + 2):]  # Removes the beginning of line.
                location = line.find("**")  

                # Loop until no more "***"
                while location != -1:

                    if not opened_tag:
                        new_line = f"{new_line}{line[:location]}<b>"
                        opened_tag = True
                    else:
                        new_line = f"{new_line}{line[:location]}</b>"
                        opened_tag = False


                    # Removes the beginning of the line.
                    line = line[(location + 2):]

                    # Finds the next instance of "***"
                    location = line.find("**")

                # Adds the final to the line after no more "***" is found.
                new_line += line
                line = new_line
            

            # Converting Italic to HTML
            elif "*" in line:
                location = line.find("*")  # Finds where the next "***" is.
                opened_tag = True
                new_line = line[:location] + "<i>"

                line = line[(location + 1):]  # Removes the beginning of line.
                location = line.find("*")  

                # Loop until no more "***"
                while location != -1:

                    if not opened_tag:
                        new_line = f"{new_line}{line[:location]}<i>"
                        opened_tag = True
                    else:
                        new_line = f"{new_line}{line[:location]}</i>"
                        opened_tag = False


                    # Removes the beginning of the line.
                    line = line[(location + 1):]

                    # Finds the next instance of "***"
                    location = line.find("*")

                # Adds the final to the line after no more "***" is found.
                new_line += line
                line = new_line
            

            # Coverting code blocks to HTML
            if "```" in line:
                # Opening a code block
                if not code_block_entered:
                    line = "<div class='codeBlock'>"
                    code_block_entered = True

                else:
                    line = "</div>"
                    code_block_entered = False


        given_array.append(line)

    # Close the body and HTML tags at the end.
    given_array.append("</body>")
    given_array.append("</html>")
    

    # Outputs each line of the array into a HTML file
    output_file = open(HTML_path, "w")
    for line in given_array:
        output_file.write(line)
    output_file.close()

    return True



if __name__ == "__main__":
    print("Yep")

    # create_single_file("/Vault/" + "Test.md")http://192.168.1.113:1008/Test.html

    run_all("Vault")

