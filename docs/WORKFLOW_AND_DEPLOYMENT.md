# SurveyJS Project Workflow and Deployment Guide

## Project Overview
SurveyJS is a FastAPI-based backend application that provides RESTful API endpoints for handling survey-related operations. The application uses MongoDB as its database and includes CORS middleware for cross-origin resource sharing.

## Project Structure
```
.
├── main.py              # Main application entry point
├── requirements.txt     # Project dependencies
├── app/
│   ├── __init__.py
│   ├── database.py     # Database connection and configuration
│   ├── model.py        # Data models and schemas
│   ├── routers.py      # API route definitions
│   └── services.py     # Business logic and services
└── docs/               # Project documentation
```

## Development Workflow

### 1. Setting Up Development Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   MONGODB_URL=your_mongodb_connection_string
   DATABASE_NAME=your_database_name
   ```

### 2. Running the Application Locally
1. Activate the virtual environment if not already activated
2. Start the application:
   ```bash
   uvicorn main:app --reload
   ```
3. Access the API documentation at `http://localhost:8000/docs`

## Deployment Guide (Ubuntu)

### 1. Server Prerequisites
1. Update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install required packages:
   ```bash
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

### 2. Project Setup
1. Create a directory for the application:
   ```bash
   sudo mkdir /opt/surveyjs
   sudo chown $USER:$USER /opt/surveyjs
   ```

2. Clone the repository:
   ```bash
   cd /opt/surveyjs
   git clone <repository-url> .
   ```

3. Set up Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   nano .env
   ```
   Add your configuration:
   ```
   MONGODB_URL=your_mongodb_connection_string
   DATABASE_NAME=your_database_name
   ```

### 3. Setting up Systemd Service
1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/surveyjs.service
   ```

2. Add the following configuration:
   ```ini
   [Unit]
   Description=SurveyJS FastAPI Application
   After=network.target

   [Service]
   User=your_username
   Group=your_username
   WorkingDirectory=/opt/surveyjs
   Environment="PATH=/opt/surveyjs/venv/bin"
   EnvironmentFile=/opt/surveyjs/.env
   ExecStart=/opt/surveyjs/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable surveyjs
   sudo systemctl start surveyjs
   ```

### 4. Nginx Configuration
1. Create Nginx configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/surveyjs
   ```

2. Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/surveyjs /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### 5. SSL Configuration (Optional but Recommended)
1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your_domain.com
   ```

## Monitoring and Maintenance

### Checking Application Status
```bash
sudo systemctl status surveyjs
```

### Viewing Application Logs
```bash
sudo journalctl -u surveyjs -f
```

### Updating the Application
1. Navigate to the application directory:
   ```bash
   cd /opt/surveyjs
   ```

2. Pull latest changes:
   ```bash
   git pull origin master
   ```

3. Activate virtual environment and update dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Restart the service:
   ```bash
   sudo systemctl restart surveyjs
   ```

## Troubleshooting
- Check application logs: `sudo journalctl -u surveyjs -f`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Verify MongoDB connection: `mongo your_mongodb_url`
- Check firewall settings: `sudo ufw status`

## Security Considerations
1. Always use strong passwords and keep them secure
2. Regularly update system packages and dependencies
3. Configure firewall rules appropriately
4. Use SSL/TLS for all production deployments
5. Follow the principle of least privilege for service accounts
6. Regularly backup your MongoDB database
