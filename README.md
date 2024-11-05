## Installation

The Code is written in Python 3.10.15. If you don't have Python installed you can find it here. If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip.

## Run Locally

### Step 1: Clone the repository to your local machine:
```bash
git clone https://github.com/jatin-12-2002/Interview_Question_Creator
```

### Step 2: Navigate to the project directory:
```bash
cd Interview_Question_Creator
```

### Step 3: Create a conda environment after opening the repository

```bash
conda create -p env python=3.10 -y
```

```bash
source activate ./env
```

### Step 4: Install the requirements
```bash
pip install -r requirements.txt
```

### Step 5: Set up environment variables:
- Create a .env file in the project directory.
- Define the necessary environment variables such as database connection strings, API keys, etc.
- Your .env file should should have these variables:
```bash
MISTRAL_API_KEY=""
HF_TOKEN=""
```
- My .env file is [here](https://drive.google.com/file/d/1D_7N8INSDax3oFKJIzbBNp2m8knhiTDV/view?usp=drive_link)


### Step 6: Install Redis
```bash
sudo apt-get update
```
```bash
sudo apt-get install redis-server
```

### Step 7: Start the Redis Server(usually done on port 6379 by default).
```bash
sudo service redis-server start
```

### Step 8: Check if Redis is running. It should return **PONG** if everything is working fine.
```bash
redis-cli ping
```

### Step 9: Start the Celery Worker. In a new terminal window, activate the environment then run:
```bash
celery -A app.celery worker --loglevel=info
```

### Step 10: Run the Flask application. In another terminal, start your Flask application with Gunicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --workers 2
```

### Step 11 - Prediction application
```bash
http://localhost:8080/

```

## Response Outputs
![image](assets/Output1.png)
![image](assets/Output2.png)
### You can download the sample output given by the model from [here](assets/QA.docx)


## AWS DEPLOYMENT
### Step 1: Push your entire code to github.
### Step 2: Login to your AWS account Link.
### Step 3: Launch your EC2 Instance.
### Step 4: Configure your EC2 Instance.
```bash
Use t2.large or greater size instances only as it is a GenerativeAI using LLMs project.
```

### Step 5: Command for configuring EC2 Instance.

### INFORMATION: sudo apt-get update and sudo apt update are used to update the package index on a Debian-based system like Ubuntu, but they are slightly different in terms of the tools they use and their functionality:

### Step 6: Connect your EC2 Instance and start typing the following commands

### Step 6.1: This command uses apt-get, the traditional package management tool.
```bash
sudo apt-get update
```

### Step 6.2: This command uses apt, a newer, more user-friendly command-line interface for the APT package management system.
```bash
sudo apt update -y
```

### Step 6.3: Install Nginx, Git and other tools
```bash
sudo apt install git nginx -y
```

### Step 6.3: Install required tools.
```bash
sudo apt install git curl unzip tar make sudo vim wget -y
```

### Step 6.4: Clone git repository.
```bash
git clone https://github.com/jatin-12-2002/Interview_Question_Creator
```

### Step 6.5: Navigate to the project directory:
```bash
cd Interview_Question_Creator
```

### Step 6.6: Create a .env file there.
```bash
touch .env
```

### Step 6.6: Open file in VI editor.
```bash
vi .env
```

### Step 6.7: Press insert and Mention .env variable then press esc for saving and write :wq for exit.
```bash
MISTRAL_API_KEY=""
HF_TOKEN=""
```

### Step 6.8: ### For checking the values of .env variables.
```bash
cat .env
```

### Step 6.9: For installing python and pip here is a command
```bash
sudo apt install python3-pip
```

### Step 6.10: install the requirements.txt. The --break-system-packages flag in pip allows to override the externally-managed-environment error and install Python packages system-wide.
```bash
pip3 install -r  requirements.txt
```
**OR**
```bash
pip3 install -r  requirements.txt --break-system-packages
```

### The --break-system-packages flag in pip allows to override the externally-managed-environment error and install Python packages system-wide. pip install package_name --break-system-packages

### Step 6.11: Test the Application with U. Verify the app is working by visiting **http://your-ec2-public-ip:8080**
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Step 6.12: Configure Nginx as a Reverse Proxy. Set up Nginx to forward requests to Uvicorn. Open the Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/default
```

### Step 6.13: Update the Nginx configuration as follows:
```bash
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
### Save and close the file

### Step 6.14: Then restart Nginx:
```bash
sudo systemctl restart nginx
```

### Step 6.15: Set Up Uvicorn as a Background Service. To keep Uvicorn as a systemd service, set up a systemd service file. Create a systemd  file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

### Step 6.16: Update the configuration as follows:
```bash
[Unit]
Description=Uvicorn instance to serve FastAPI app
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/your-repo-name
ExecStart=/usr/local/bin/uvicorn app:app --host 0.0.0.0 --port 8080

[Install]
WantedBy=multi-user.target
```
### Save and close the file

### Step 6.17: Start and enable the service:
```bash
sudo systemctl start uvicorn
```
```bash
sudo systemctl enable uvicorn
```

### Step 6.18: Install Redis
```bash
sudo apt-get update
```
```bash
sudo apt-get install redis-server
```

### Step 6.19: Start the Redis Server(usually done on port 6379 by default).
```bash
sudo service redis-server start
```

### Step 6.20: Check if Redis is running. It should return **PONG** if everything is working fine.
```bash
redis-cli ping
```

### Step 6.21: Start the Celery Worker. In a new terminal window, activate the environment then run:
```bash
celery -A app.celery worker --loglevel=info
```

### Step 7: Configure your inbound rule:
1. Go inside the security
2. Click on security group
3. Configure your inbound rule with certain values
4. Port 8080 0.0.0.0/0 for anywhere traffic TCP/IP protocol
5. Port 6379 (Redis) 0.0.0.0/0 for anywhere traffic TCP/IP protocol

### Step 8: Save it and now run your application.
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Step 9 - Run the Public Port of EC2 Instance
```bash
http://your-ec2-public-ip:8080
```

### If you encounter any error like code:400 while running "https:{Public_address}:5000" then just run it with 'http' instead of 'https'.


### Check that your app is accessible through http://your-ec2-public-ip. Nginx will handle incoming requests and proxy them to Uvicorn.


### This setup makes your app production-ready by using Nginx and Uvicorn for stability, performance, and scalability. You can continue to scale by increasing Uvicorn workers or adding load balancing if traffic grows.

## Conclusion 

