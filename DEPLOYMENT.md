# 🚀 Deployment Guide - Diabetes Risk Predictor

This guide provides comprehensive instructions for deploying the Diabetes Risk Predictor to various platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you've completed these steps:

- [ ] Run health check: `python health_check.py`
- [ ] Test locally: `streamlit run app.py`
- [ ] Verify all pages work correctly
- [ ] Check model files exist (`logistic_model.pkl`, `scaler.pkl`)
- [ ] Validate dataset (`diabetes.csv`)
- [ ] Review requirements.txt
- [ ] Test on different screen sizes

## 🌐 Streamlit Cloud Deployment (Recommended)

### Step 1: Prepare Repository
```bash
# Ensure your code is in a GitHub repository
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Choose branch: `main`
6. Main file path: `app.py`
7. Click "Deploy!"

### Step 3: Configure Advanced Settings (Optional)
```toml
# .streamlit/config.toml is already configured
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
enableCORS = true
enableXsrfProtection = true
```

### Step 4: Monitor Deployment
- Check deployment logs for any errors
- Test all functionality in the deployed app
- Verify mobile responsiveness
- Test all navigation pages

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build the image
docker build -t diabetes-predictor .

# Run the container
docker run -p 8501:8501 diabetes-predictor

# Run with environment variables
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_HEADLESS=true \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  diabetes-predictor
```

### Docker Compose (Optional)
```yaml
# docker-compose.yml
version: '3.8'
services:
  diabetes-predictor:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    restart: unless-stopped
```

## ☁️ Heroku Deployment

### Step 1: Prepare Files
Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Step 2: Deploy
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-diabetes-predictor

# Set Python version (optional)
echo "python-3.9.16" > runtime.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open the app
heroku open
```

## 🔧 AWS EC2 Deployment

### Step 1: Launch EC2 Instance
- Choose Ubuntu 20.04 LTS
- Instance type: t2.micro (free tier) or t2.small
- Configure security group to allow HTTP (port 80) and HTTPS (port 443)
- Allow SSH (port 22) for your IP

### Step 2: Setup Server
```bash
# Connect to your instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install nginx (optional, for reverse proxy)
sudo apt install nginx -y

# Clone your repository
git clone https://github.com/your-username/diabetes-predictor.git
cd diabetes-predictor

# Install dependencies
pip3 install -r requirements.txt

# Run the app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Step 3: Setup as Service (Optional)
```bash
# Create systemd service
sudo nano /etc/systemd/system/diabetes-predictor.service
```

```ini
[Unit]
Description=Diabetes Risk Predictor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/diabetes-predictor
ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable diabetes-predictor
sudo systemctl start diabetes-predictor
sudo systemctl status diabetes-predictor
```

## 🌍 Google Cloud Platform (GCP)

### Using Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project-id/diabetes-predictor

# Deploy to Cloud Run
gcloud run deploy diabetes-predictor \
  --image gcr.io/your-project-id/diabetes-predictor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501
```

## 📊 Performance Optimization

### For Production Deployment
1. **Enable Caching**:
   ```python
   @st.cache_data
   def load_model():
       # Your model loading code
   ```

2. **Optimize Images**: Compress any images used in the app

3. **Minimize Dependencies**: Remove unused packages from requirements.txt

4. **Enable Compression**: Use gzip compression for static files

5. **Monitor Performance**: Set up logging and monitoring

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Validate all user inputs
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data
- [ ] Enable security headers
- [ ] Regular security audits

### Environment Variables
```bash
# For sensitive configuration
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_THEME_PRIMARY_COLOR="#1f77b4"
```

## 📈 Monitoring and Maintenance

### Health Monitoring
```bash
# Automated health checks
python health_check.py

# Monitor logs
tail -f app.log

# Check system resources
htop
df -h
```

### Maintenance Tasks
- Regular dependency updates
- Model retraining (if needed)
- Performance monitoring
- Security patches
- Backup important data

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Find process using port
lsof -i :8501
# Kill process
kill -9 <PID>
```

**Memory Issues**:
```bash
# Check memory usage
free -h
# Restart application
sudo systemctl restart diabetes-predictor
```

**Permission Errors**:
```bash
# Fix file permissions
chmod +x setup.sh
chown -R ubuntu:ubuntu /path/to/app
```

**Module Import Errors**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

### Getting Help
- Check application logs first
- Run health check script
- Review this deployment guide
- Check Streamlit documentation
- Open GitHub issue for bugs

### Useful Commands
```bash
# Check app status
curl -f http://localhost:8501/_stcore/health

# View logs
journalctl -u diabetes-predictor -f

# Restart service
sudo systemctl restart diabetes-predictor

# Update application
git pull origin main
sudo systemctl restart diabetes-predictor
```

## 🎯 Post-Deployment Checklist

After successful deployment:
- [ ] Test all functionality
- [ ] Verify mobile responsiveness
- [ ] Check page load times
- [ ] Test with different browsers
- [ ] Verify analytics tracking (if implemented)
- [ ] Set up monitoring alerts
- [ ] Document the deployment process
- [ ] Share the app URL with stakeholders

---

**🎉 Congratulations!** Your Diabetes Risk Predictor is now deployed and ready to help users assess their diabetes risk!

For any deployment issues, refer to the troubleshooting section or open an issue in the GitHub repository.