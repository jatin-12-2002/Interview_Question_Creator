# Interview Question Creator using Mistral and LangChain

# Introduction

**Interview Question Creator** is a powerful tool designed to streamline and enhance interview preparation by generating **domain-specific interview questions and answers**. This application leverages AI-powered models and custom processing techniques to create comprehensive question sets across technical, theoretical, and behavioral domains. Users can upload a PDF of relevant materials, from which tailored interview questions are **generated, refined, and formatted for download**.

## Model and Prompt Engineering
This tool utilizes the **Mistral large language model** via **LangChain**, a library that simplifies working with advanced language models. The LangChain integration enables efficient pipelines for both question generation and refinement. The generated questions undergo a **refinement process using prompt engineering** to ensure they cover diverse aspects of interview readiness, from **technical knowledge to problem-solving and interpersonal skills**. The **refining prompt** technique is especially valuable here: it helps identify and enhance questions for clarity and depth by iterating on the initial question set with additional context from the input material. This approach ensures the questions are well-rounded and relevant, addressing various dimensions of interview topics effectively.

## Formatting Output
Once questions and answers are generated, they are **formatted in a DOCX file with custom styling for readability and clarity**. This includes applying **Markdown-inspired styling**, such as bullet points, headers, and bold text, to create a professional and accessible document.

## Frontend and Interaction
On the frontend, a simple and intuitive **HTML**, **CSS**, and **JavaScript** interface allows users to upload PDFs, specify the number of questions, and download the final document. **JavaScript** manages user interactions, including file upload, server communication, status polling, and download link display, providing a smooth experience throughout.

## Handling Long Response Times with Redis and Celery and Deployment on AWS EC2
Since the **server has a 1-minute response timeout** and question generation can exceed this time limit, the app is designed to **handle tasks asynchronously using Celery and Redis**. **Redis** serves as both the task broker and results backend, while **Celery** enables background task management, allowing requests to be processed reliably and progress updates to be provided in real-time. Finally, the application is **deployed on an AWS EC2 instance**, providing flexibility, control, and scalability for end users who need on-demand access to the service.


## Tech Stack Used
- **Language**: Python
- **FrameWork**: LangChain
- **Backend**: FastAPI
- **Model**: Mistral Large Language Model (via LangChain)
- **Database**: FAISS (vector storage for embeddings)
- **Message Queue**: Redis
- **Task Management**: Celery
- **Frontend**: HTML, CSS, JavaScript

## Infrastructure
- **Deployment**: AWS EC2
- **Version Control**: GitHub


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
- My .env file is [here](https://drive.google.com/file/d/1JhzfK0ncRatvec8i5RUD6O5WgKissp3M/view?usp=drive_link)


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

### Step 6.7: Open file in VI editor.
```bash
vi .env
```

### Step 6.8: Press insert and Mention .env variable then press esc for saving and write :wq for exit.
```bash
MISTRAL_API_KEY=""
HF_TOKEN=""
```

### Step 6.9: ### For checking the values of .env variables.
```bash
cat .env
```

### Step 6.10: For installing python and pip here is a command
```bash
sudo apt install python3-pip
```

### Step 6.11: install the requirements.txt. The --break-system-packages flag in pip allows to override the externally-managed-environment error and install Python packages system-wide.
```bash
pip3 install -r  requirements.txt
```
**OR**
```bash
pip3 install -r  requirements.txt --break-system-packages
```

### The --break-system-packages flag in pip allows to override the externally-managed-environment error and install Python packages system-wide. pip install package_name --break-system-packages

### Step 6.12: Test the Application with Uvicorn. Verify the app is working by visiting **http://your-ec2-public-ip:8080**
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Step 6.13: Configure Nginx as a Reverse Proxy. Set up Nginx to forward requests to Uvicorn. Open the Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/default
```

### Step 6.14: Update the Nginx configuration as follows:
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

### Step 6.15: Then restart Nginx:
```bash
sudo systemctl restart nginx
```

### Step 6.16: Set Up Uvicorn as a Background Service. To keep Uvicorn as a systemd service, set up a systemd service file. Create a systemd  file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

### Step 6.17: Update the configuration as follows:
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

### Step 6.18: Start and enable the service:
```bash
sudo systemctl start uvicorn
```
```bash
sudo systemctl enable uvicorn
```

### Step 6.19: Connect to a new terminal of same EC2 Instance. Install Redis.
```bash
sudo apt-get update
```
```bash
sudo apt-get install redis-server
```

### Step 6.20: Start the Redis Server(usually done on port 6379 by default).
```bash
sudo service redis-server start
```

### Step 6.21: Check if Redis is running. It should return **PONG** if everything is working fine.
```bash
redis-cli ping
```

### Step 6.22: Start the Celery Worker.
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

### If you encounter any error like code:400 while running "https://{your-ec2-public-ip:8080}" then just run it with 'http' instead of 'https'.


### Check that your app is accessible through http://your-ec2-public-ip. Nginx will handle incoming requests and proxy them to Uvicorn.


### This setup makes your app production-ready by using Nginx and Uvicorn for stability, performance, and scalability. You can continue to scale by increasing Uvicorn workers or adding load balancing if traffic grows.

## Conclusion 

1. The **Interview Question Creator** uses a **RAG (Retrieval-Augmented Generation)** approach, combining retrieval-based techniques with **generative AI** to produce highly relevant, domain-specific questions and answers. By utilizing **FAISS** as the **vector database**, the app retrieves contextually similar information from user-uploaded documents, ensuring that generated questions are precise and tailored to specific topics, covering technical, behavioral, and theoretical aspects effectively.

2. The **Mistral model and its embeddings** play a crucial role in semantic understanding, creating embeddings that accurately capture the nuances of the uploaded content. This allows the app to build contextual embeddings, aligning the generated questions closely with the specific themes and topics of each document.

3. Integrating **LangChain** for **prompt engineering** and **question refinement** provides users with high-quality, diversified question sets. The iterative **refinement process** ensures each question is clear, focused, and balanced across multiple interview dimensions.

4. **Asynchronous task management with Celery and Redis** enables efficient handling of **longer processing times**, allowing the application to manage complex question generation tasks within real-world server constraints, providing status updates to users throughout the process.

5. **AWS EC2 deployment** ensures **scalability and stability**, giving users consistent, on-demand access to the service. Combined with an intuitive frontend interface, this solution offers a seamless, interactive experience for custom interview preparation.