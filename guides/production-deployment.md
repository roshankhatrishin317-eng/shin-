# 🚀 Production Deployment Guide

Complete guide for deploying Shin LiteLLM Gateway to production environments.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deployment Options](#deployment-options)
3. [VPS Deployment](#vps-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [HTTPS Setup](#https-setup)
7. [Process Management](#process-management)
8. [Backup and Recovery](#backup-and-recovery)
9. [Scaling](#scaling)

---

## Pre-Deployment Checklist

### Security

- [ ] Strong master key configured
- [ ] All secrets in environment variables
- [ ] `.env` file excluded from version control
- [ ] HTTPS configured
- [ ] Firewall rules set up
- [ ] Rate limiting enabled
- [ ] IP allowlist configured (if needed)
- [ ] Virtual keys created for users

### Configuration

- [ ] Production config tested
- [ ] All provider API keys verified
- [ ] Timeout values appropriate
- [ ] Logging configured
- [ ] Database configured
- [ ] CORS settings appropriate

### Testing

- [ ] All models tested
- [ ] Load testing completed
- [ ] Failover scenarios tested
- [ ] Monitoring set up
- [ ] Backup procedures tested

### Documentation

- [ ] Deployment runbook created
- [ ] Incident response plan documented
- [ ] Access credentials documented
- [ ] Recovery procedures documented

---

## Deployment Options

### Option 1: VPS/Cloud Server

**Best for:**
- Small to medium scale
- Full control needed
- Cost-effective

**Providers:**
- DigitalOcean
- Linode
- AWS EC2
- Google Cloud Compute
- Azure VMs

### Option 2: Docker Container

**Best for:**
- Consistent environments
- Easy scaling
- Microservices architecture

**Platforms:**
- Docker on VPS
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

### Option 3: Platform-as-a-Service

**Best for:**
- Quick deployment
- Minimal DevOps
- Auto-scaling

**Platforms:**
- Heroku
- Railway
- Render
- Fly.io

---

## VPS Deployment

### Step 1: Server Setup

#### Choose Server

Minimum requirements:
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 22.04 LTS

Recommended:
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB SSD

#### Provision Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git nginx certbot python3-certbot-nginx

# Create user
sudo useradd -m -s /bin/bash litellm
sudo su - litellm
```

### Step 2: Application Setup

```bash
# Clone repository
cd /home/litellm
git clone https://github.com/roshankhatrishin317-eng/shin-.git
cd shin-

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.template .env
nano .env  # Add your keys
```

### Step 3: Configure as Service

Create `/etc/systemd/system/litellm.service`:

```ini
[Unit]
Description=LiteLLM Gateway
After=network.target

[Service]
Type=simple
User=litellm
WorkingDirectory=/home/litellm/shin-
Environment="PATH=/home/litellm/shin-/venv/bin"
ExecStart=/home/litellm/shin-/venv/bin/python start_gateway.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable litellm
sudo systemctl start litellm
sudo systemctl status litellm
```

### Step 4: Set Up Nginx

Create `/etc/nginx/sites-available/litellm`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/litellm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: SSL Certificate

```bash
sudo certbot --nginx -d api.yourdomain.com
```

Test auto-renewal:

```bash
sudo certbot renew --dry-run
```

---

## Docker Deployment

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:4000/health || exit 1

# Run application
CMD ["python", "start_gateway.py"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  litellm:
    build: .
    ports:
      - "4000:4000"
    env_file:
      - .env
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./litellm.db:/app/litellm.db
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - litellm
    restart: unless-stopped
```

### Deploy with Docker

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# View logs
docker-compose logs -f litellm

# Stop
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. Launch Ubuntu 22.04 instance
2. Configure security group (ports 22, 80, 443)
3. Follow VPS deployment steps above

#### Using ECS/Fargate

1. Push Docker image to ECR
2. Create ECS cluster
3. Define task definition
4. Create service with load balancer

```bash
# Build and push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URL
docker build -t litellm .
docker tag litellm:latest YOUR_ECR_URL/litellm:latest
docker push YOUR_ECR_URL/litellm:latest
```

### Google Cloud Deployment

#### Using Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/litellm
gcloud run deploy litellm \
  --image gcr.io/PROJECT_ID/litellm \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 4000 \
  --set-env-vars "LITELLM_MASTER_KEY=your-key"
```

### Azure Deployment

#### Using Container Instances

```bash
# Create resource group
az group create --name litellm-rg --location eastus

# Create container
az container create \
  --resource-group litellm-rg \
  --name litellm \
  --image YOUR_IMAGE \
  --dns-name-label litellm-api \
  --ports 4000 \
  --environment-variables LITELLM_MASTER_KEY=your-key
```

---

## HTTPS Setup

### Option 1: Let's Encrypt (Certbot)

Already covered in VPS deployment.

### Option 2: Cloudflare

1. Add domain to Cloudflare
2. Set DNS A record to your server IP
3. Enable "Full (strict)" SSL mode
4. Gateway automatically gets HTTPS

### Option 3: Load Balancer SSL

AWS Application Load Balancer:

1. Create ALB
2. Add SSL certificate
3. Configure target group (port 4000)
4. Update security groups

---

## Process Management

### systemd (Linux)

Service file shown in VPS deployment.

**Commands:**

```bash
# Start
sudo systemctl start litellm

# Stop
sudo systemctl stop litellm

# Restart
sudo systemctl restart litellm

# Status
sudo systemctl status litellm

# Logs
sudo journalctl -u litellm -f
```

### PM2 (Node.js process manager)

```bash
# Install
npm install -g pm2

# Start
pm2 start start_gateway.py --name litellm --interpreter python3

# Monitor
pm2 monit

# Logs
pm2 logs litellm

# Restart
pm2 restart litellm

# Auto-start on boot
pm2 startup
pm2 save
```

### Supervisor

Install:

```bash
sudo apt install supervisor
```

Create `/etc/supervisor/conf.d/litellm.conf`:

```ini
[program:litellm]
directory=/home/litellm/shin-
command=/home/litellm/shin-/venv/bin/python start_gateway.py
user=litellm
autostart=true
autorestart=true
stderr_logfile=/var/log/litellm/err.log
stdout_logfile=/var/log/litellm/out.log
```

Commands:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start litellm
```

---

## Backup and Recovery

### Database Backup

```bash
# Create backup script
cat > /home/litellm/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/litellm/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp /home/litellm/shin-/litellm.db $BACKUP_DIR/litellm_$DATE.db

# Keep only last 7 days
find $BACKUP_DIR -name "litellm_*.db" -mtime +7 -delete
EOF

chmod +x /home/litellm/backup.sh
```

Add to crontab:

```bash
# Backup every 6 hours
0 */6 * * * /home/litellm/backup.sh
```

### Configuration Backup

```bash
# Backup config
tar -czf config_backup_$(date +%Y%m%d).tar.gz config.yaml .env

# Backup to S3 (AWS)
aws s3 cp config_backup_*.tar.gz s3://your-backup-bucket/
```

### Disaster Recovery

1. **Fresh server setup**
   ```bash
   sudo apt update && sudo apt install -y python3-pip git
   ```

2. **Restore application**
   ```bash
   git clone https://github.com/roshankhatrishin317-eng/shin-.git
   cd shin-
   pip install -r requirements.txt
   ```

3. **Restore configuration**
   ```bash
   # Restore from backup
   cp /backup/config.yaml .
   cp /backup/.env .
   ```

4. **Restore database**
   ```bash
   cp /backup/litellm.db .
   ```

5. **Start service**
   ```bash
   python start_gateway.py
   ```

---

## Scaling

### Vertical Scaling

Upgrade server resources:

```bash
# Monitor resource usage
htop
iotop
netstat -an | grep 4000 | wc -l
```

Indicators to scale up:
- CPU > 80% consistently
- Memory > 90%
- Slow response times

### Horizontal Scaling

#### Load Balancer Setup

```nginx
upstream litellm_backends {
    least_conn;
    server 10.0.0.1:4000;
    server 10.0.0.2:4000;
    server 10.0.0.3:4000;
}

server {
    listen 80;
    location / {
        proxy_pass http://litellm_backends;
    }
}
```

#### Shared Database

Use PostgreSQL for shared state:

```yaml
# config.yaml on all instances
general_settings:
  database_url: "postgresql://user:pass@db-host:5432/litellm"
```

### Auto-Scaling

#### AWS Auto Scaling Group

1. Create AMI with gateway
2. Create launch template
3. Configure auto-scaling group
4. Set scaling policies (CPU > 70%)

#### Kubernetes

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm
spec:
  replicas: 3
  selector:
    matchLabels:
      app: litellm
  template:
    metadata:
      labels:
        app: litellm
    spec:
      containers:
      - name: litellm
        image: your-image:latest
        ports:
        - containerPort: 4000
        envFrom:
        - secretRef:
            name: litellm-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: litellm
spec:
  selector:
    app: litellm
  ports:
  - port: 80
    targetPort: 4000
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

---

## Production Checklist

### Pre-Launch

- [ ] All tests passing
- [ ] Load testing completed
- [ ] Security audit done
- [ ] Monitoring configured
- [ ] Backups automated
- [ ] Documentation complete
- [ ] Team trained

### Launch

- [ ] DNS configured
- [ ] SSL certificate active
- [ ] Service running
- [ ] Health checks passing
- [ ] Monitoring active
- [ ] Alerts configured

### Post-Launch

- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Review logs
- [ ] Verify backups
- [ ] Test failover
- [ ] Document issues

---

## Next Steps

- **Monitor Performance**: [Monitoring Guide](monitoring-guide.md)
- **Handle Issues**: [Troubleshooting Guide](troubleshooting.md)
- **Secure Deployment**: [Security Guide](security-guide.md)

---

[⬅ Back to Guides](README.md) | [Next: Troubleshooting ➡](troubleshooting.md)

