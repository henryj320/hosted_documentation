# hosted_documentation

Last update: 2023-06-30 15:44
<br><br>

## Development Notes for hosted_documentation

1. Set up the repository
    - Added a README.md, development_notes.md and LICENSE file.
    - Linked the Project table to the repository.
    - Created a "sprint 1" label for the issues.
    - Created a .gitignore file.
    - Created a "Vault" directory.
2. Creating the initial Docker container
    - Goal is to make it take the required files and allow them to be seen.
    - ` sudo docker build --tag hosted-documentation-image . `
    - ` sudo docker run --publish 1008:80 --name hosted-documentation-container -d hosted-documentation-image `
    - http://localhost:1008/Vault/Example.md **OR** http://localhost:1008/Example.md
        - That worked. It actually downloaded *Example.md* instead of showing it, but it worked.
            - That's not an issue, as I will be converting it to HTML anyway.
3. Trying the docker container with ` -v ` instead
    - So that the user can choose the location of the Markdown files.
    - Removing the COPY command
    - ` sudo docker build --tag hosted-documentation-image --no-cache . `
    - ` sudo docker remove --force hosted-documentation-container `
    - ` sudo docker run --publish 1008:80 --name hosted-documentation-container -v Vault:/usr/share/nginx/html -d hosted-documentation-image `
    - Going to the URL failed
    - ` sudo docker exec -it hosted-documentation-container sh `
        - Not there
        - I'll look into it in the future.
4. Creating the initial Python file.
    - Added a line in Dockerfile to create a directory - ` RUN mkdir -p /Pages `.
        - Checking it worked
            - Yep. Worked fine
    - Wrote some code to create the file
    - Testing it
        - Nope, going to need two containers linked with a volume.
        - That's the next step.
5. Making a docker-compose.yml file.
    ` docker compose up -d `
    - Accessible at http://192.168.1.102:1008/
6. Creating a volume
    - Adding a line to the *docker-compose.yml*
    - Checking that files persist
    - ` sudo docker exec -it hosted-documentation-container sh `
    - ` cd volume `
    - ` touch test.txt `
    - Restarted the container
    - Checked it was there
        - Yep, *test.txt* was there!
    - Deleting the old volume
        - ` docker volume rm hosted-documentation-volume `
    - Making the volume link to the "/usr/share/nginx/html" directory
    - ` docker compose up -d `
    - ` sudo docker exec -it hosted-documentation-nginx sh `
    - Making a test file called *test.html*
        - ` echo Does this work? > test.html `
        - Go to it at http://192.168.1.102:1008/test.html
    - Checking that it still exists after a restart
        - ` docker compose down `
        - ` docker compose up -d `
        - Yep, the file is still there!
    - Does it survive a rebuild?
        - ` docker compose down `
        - ` docker compose up -d --build `
        - Yep, the file is still there because the volume was not recreated
        - Perfect.
    - Next step is to create another Dockerfile to run the main.py script and create a HTML file inside of the volume.
7. Making the Dockerfile for the API
    - Split the Python into its own folder
    - Make the api.Dockerfile
    - Added it to docker-compose.yml
    - ` docker compose up -d `
    - Checking that the main.py script was run
        - Changed the location that the main.py outputs to
        - ` sudo docker exec -it hosted-documentation-nginx sh `
        - ` cd /usr/share/nginx/html/ `
        - ` cat ExamplePython.html `
            - Yep, its there!
8. Making a real HTML file from it
    - Adapting main.py
    - Trying to make it read the correct file
    - Doesnt seem to be copying "Vault" into the right location.
    - Changed it to have two volumes - one for the vault and another for the HTML
    - The python script still isn't outputting into the right place
    - Got it working. The HTML_path was not correct.
9. Been a while. Trying to run it.
    - ` docker compose up -d `
    - Looking inside of the nginx container
        - ` docker exec -it hosted-documentation-nginx sh `
        - Looks like the Example.md file is converted
            - http://192.168.1.113:1008/Example.html
    - Making a *Test.md* file inside of "Vault" to see if it is converted
        - Changed the file referenced in *main.py* to be Test.md instead
        - Added the *Test.md* file
        - ` docker compose down `
        - ` docker compose up -d `
        - ` docker exec -it hosted-documentation-nginx sh `
        - ` cd /usr/share/nginx/html `
        - Nope, it isnt there
        - ` cd ./Vault `
            - Nope, it isnt in there
            - So the volume needs to be recreated
        - ` docker compose down `
        - ` docker compose up --force-recreate -d `
            - Nope, the file still isnt in the vault
    - ` docker volume ls `
        - Both the html and vault volumes show up
    - Maybe it just needs to be rebuild
        - ` docker compose down `
        - ` docker compose up --build -d `
        - Nope
    - So why is the content of Vault not being copied into the volume?
    - ` docker compose rm -f `
    - ` docker compose build --no-cache `
    - ` docker compose up -d `
    - Nope, Test.md still isnt inside of Vault
    - ` docker compose down -v `
    - ` docker compose build --no-cache `
    - ` docker compose up -d `
    - ` docker exec -it hosted-documentation-nginx sh `
        - The Test.md file is there!
        - http://192.168.1.113:1008/Test.html
            - It shows the file!
    - So, in summary: The volume needs to be recreated to work.
10. Making it so that all Markdown files inside of "Vault" are converted into .html, not just specific ones
    - Changing the code
    - It now makes all of the files, but doesn't retain the subdirectories
        - That's a good start. I'll make it retain the subdirectories at a later point
        - Added a TODO on line 73 for where to do it.
    - Testing it worked
        - ` docker compose down -v `
        - ` docker compose build --no-cache `
        - ` docker compose up -d `
        - ` docker exec -it hosted-documentation-nginx sh `
        - The code isnt in there
        - ` docker logs hosted-documentation-api `
            - FileNotFoundError: [Errno 2] No such file or directory: 'usr/share/nginx/html/Vault/Example.html'
            - Removed this line: ` # directories_to_add += "Output/" `
                - Didnt change anything
        - ` directories_to_add = website_location `
            - So that it starts at "/usr/share/nginx/html" instead of "/"
                - That worked
            - http://192.168.1.113:1008/Vault/Example.html
            - http://192.168.1.113:1008/Vault/Testing_Subdirectories/TEstingSubSub/Subsub.html
            - All are working
11. Adding CSS
    - Added a config file
        - ` hosted-documentation-volume-config:/Config `
        - Nevermind, just copying it into the nginx folder.
    - Added lots of customisation.
12. Converting Markdown to HTML
    - Added conversion for Headers.
    - Converted "***" into ` <b><i>Text</i></b>.
    - Got Bold and Italic working again.
    - Converting code blocks.
