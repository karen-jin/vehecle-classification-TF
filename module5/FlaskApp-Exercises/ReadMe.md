*Python 3.8.5*

# Run the application with Flask

1. Create Python Virtual Environment
    ```
    python -m venv .
    ```
or
    ```
    virtualenv .
    ```

2. Activate Virtual Enviromment
    Linux
    ```
    source bin/activate
    ```

Windows
    ```
    source Scripts/activate
    ```

3. Install Dependencies 
    ```
    pip install -r requirements.txt
    ```

4. Run the app
    ```
    flask run
    ```

5. Go to http://localhost:5000/ to test the app

# Run the application with Docker
1. Install [Docker Desktop](https://www.docker.com/get-started)

2. Check Docker Installation
    ```
    docker run hello-world
    ```

3. Create the Docker image and build a container from the resulting image by executing the script:
    ```
    bash start.sh
    ```

4. To list all running Docker containers use the command:
    ```
    docker ps
    ```
    You will find that the `vehicles` container is now running. 

5. Go to http://localhost:56733/ to test the app

6. Useful commands:
- `docker start vehicles` - start the container
- `docker stop vehicles` - stop the container
- `docker restart vehicles`- restart the container
- `touch uwsgi.ini` - reload the app after making changes
