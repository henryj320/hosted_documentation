# hosted_documentation

Last update: 2023-06-07 23:53
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
