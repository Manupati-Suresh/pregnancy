# 🚀 Deployment Guide - Diabetes Risk Predictor

This guide provides step-by-step instructions for deploying the Diabetes Risk Predictor to various platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you've completed these steps:

- [ ] Run health check: `python health_check.py`
- [ ] Test locally: `streamlit run app.py`
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Check that model files exist (`logistic_model.pkl`, `scaler.pkl`)
- [ ] Validate dataset (`diabetes.csv`)
- [ ] Review configuration files

## 🌐 Streamlit Cloud Deployment (Recommended)

### Prerequisites
- GitHub account with the repository
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps
1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/your-username/diabetes-risk-predictor.git
   ```

2. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Deploy App**
   - Click "New app"
   - Select your repository
   - Choose branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

4. **Configuration**
   - App will automatically use `.streamlit/config.toml`
   - No additional configuration needed

### Expected Deployment Time
- Initial deployment: 2-5 minutes
- Subsequent updates: 30-60 seconds

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build image
docker build -t diabetes-predictor .

# Run container
docker run -p 8501:8501 diabetes-predictor

# Run with environment variables
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_HEADLESS=true \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  diabetes-predictor
```

### Docker Compose
```yaml
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

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

1. **Create Procfile**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create setup.sh**
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

3. **Make setup.sh executable**
   ```bash
   chmod +x setup.sh
   ```

### Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

## 🔧 AWS EC2 Deployment

### Launch EC2 Instance
1. Choose Amazon Linux 2 AMI
2. Select t2.micro (free tier eligible)
3. Configure security group (port 8501)
4. Launch with key pair

### Setup on EC2
```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install Python 3.9
sudo amazon-linux-extras install python3.8

# Install git
sudo yum install git -y

# Clone repository
git clone https://github.com/your-username/diabetes-risk-predictor.git
cd diabetes-risk-predictor

# Install dependencies
pip3 install -r requirements.txt

# Run app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Setup as Service (Optional)
```bash
# Create service file
sudo nano /etc/systemd/system/diabetes-predictor.service

# Add content:
[Unit]
Description=Diabetes Risk Predictor
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/diabetes-risk-predictor
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable diabetes-predictor
sudo systemctl start diabetes-predictor
```

## 🌊 DigitalOcean App Platform

### Deploy via GitHub
1. Connect GitHub account
2. Select repository
3. Configure build settings:
   - Build command: `pip install -r requirements.txt`
   - Run command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Set environment variables:
   - `STREAMLIT_SERVER_HEADLESS=true`
   - `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

## 🔍 Post-Deployment Verification

### Health Checks
1. **App Accessibility**
   ```bash
   curl -I https://your-app-url.com
   ```

2. **API Endpoints**
   ```bash
   curl https://your-app-url.com/_stcore/health
   ```

3. **Functionality Test**
   - Navigate to app URL
   - Test prediction with sample data
   - Verify all pages load correctly
   - Check visualizations render properly

### Performance Monitoring
- Monitor response times
- Check memory usage
- Verify model loading times
- Test concurrent user handling

## 🔧 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   # Check Python version
   python --version
   
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

2. **Model File Not Found**
   ```bash
   # Retrain model
   python train_model.py
   
   # Verify files exist
   ls -la *.pkl
   ```

3. **Port Issues**
   ```bash
   # Check if port is in use
   netstat -tulpn | grep 8501
   
   # Use different port
   streamlit run app.py --server.port 8502
   ```

4. **Memory Issues**
   ```bash
   # Check memory usage
   free -h
   
   # Optimize model loading
   # Use @st.cache_data decorator
   ```

### Logs and Debugging
```bash
# View Streamlit logs
streamlit run app.py --logger.level debug

# Check system logs (Linux)
journalctl -u diabetes-predictor -f

# Docker logs
docker logs container-name -f
```

## 🔒 Security Considerations

### Production Security
- Use HTTPS in production
- Set secure headers
- Implement rate limiting
- Monitor for unusual activity
- Regular security updates

### Environment Variables
```bash
# Set in production
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

## 📊 Monitoring and Analytics

### Application Monitoring
- Set up uptime monitoring
- Track response times
- Monitor error rates
- Log prediction requests

### User Analytics
- Track page views
- Monitor user interactions
- Analyze prediction patterns
- Gather user feedback

## 🔄 Continuous Deployment

### GitHub Actions (Example)
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run health check
      run: |
        python health_check.py
    
    - name: Deploy to Streamlit Cloud
      # Streamlit Cloud auto-deploys on push to main
      run: echo "Deployment triggered"
```

## 📞 Support

### Deployment Issues
- Check deployment logs
- Verify all files are committed
- Ensure requirements.txt is up to date
- Test locally before deploying

### Getting Help
- GitHub Issues: Report deployment problems
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Documentation: [docs.streamlit.io](https://docs.streamlit.io)

---

**Happy Deploying! 🚀**

For additional support, please open an issue on GitHub or contact the development team.