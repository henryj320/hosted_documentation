# hosted_documentation

Last update: 2023-04-30 23:34
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
