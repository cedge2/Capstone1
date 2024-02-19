# Capstone1
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
