# Capstone1

Name: "PawtnerUp"

Link to Deployment: [PawtnerUp
](https://pawtnerup.onrender.com)

What it does: An adoption website that helps users find adoptable pets using the Petfinder API

Features implemented: Favorites list, search pets in your area, links to adoption websites

Updates/Extras: In the future, I would like to add maybe real-time chat, or a pending page so that users can know where their pet is in the adoption process, and communicate with the adoption organization in the same place, although this would be an extra and not fully necessary since the petfinder API leads you to the adoption websites anyways.

User flow: Users will either create an account or login, then can look up adoption agencies or animals in their area, and add them to their favorites list if they like.

API link: https://www.petfinder.com/developers/v2/docs/

Tools: Flask, Postgresql, Petfinder API, VSCode, GITHub

To run the app, first create a virtual environment, and download the requirements.txt file - 

    % python -m venv venv 
    % Source venv/bin/activate 
    % pip install -r requirements.txt 
    % deactivate

Make sure to set any environment variables, best practice is to store this separately from the main area for security, such as a .env file, making sure to include in the .gitignore, or wherever you are hosting the site

Create a database using postgresql, in this case it is named pawtnerup, but you can change it if needed -> Make sure to set your environment variable for your database url

    % psql -U postgres 
    postgres=# CREATE DATABASE pawtnerup; 
    \l

Once these steps are done, you can do:

    % flask run 
    deactivate
    
Credits for the png/jpgs for any photos or icons goes to: 

            <a target="_blank" href="https://icons8.com/icon/106513/pets">Pets</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
            <a target="_blank" href="https://icons8.com/icon/2TcinN40k0mq/dog-heart">Dog Heart</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
            <a target="_blank" href="https://icons8.com/icon/tCi-exGozYqD/heart-with-dog-paw">Heart with dog paw</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
            <a target="_blank" href="https://icons8.com/icon/3SEb6VCakmEV/no-image-gallery">No Image Gallery</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
