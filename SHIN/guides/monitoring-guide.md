# 📊 Monitoring Guide

Learn how to monitor, track, and analyze your Shin LiteLLM Gateway performance, usage, and costs.

## 📋 Table of Contents

1. [Monitoring Overview](#monitoring-overview)
2. [Admin Dashboard](#admin-dashboard)
3. [Logging](#logging)
4. [Usage Tracking](#usage-tracking)
5. [Cost Analysis](#cost-analysis)
6. [Performance Metrics](#performance-metrics)
7. [Alerts and Notifications](#alerts-and-notifications)
8. [Database Queries](#database-queries)

---

## Monitoring Overview

### What to Monitor

```
┌─────────────────────────────────────┐
│  Request Volume & Response Times    │
├─────────────────────────────────────┤
│  Token Usage & Costs                │
├─────────────────────────────────────┤
│  Error Rates & Types                │
├─────────────────────────────────────┤
│  Model Performance                  │
├─────────────────────────────────────┤
│  API Key Usage                      │
└─────────────────────────────────────┘
```

### Built-in Monitoring Tools

1. **Admin Dashboard** - Web UI at `/ui`
2. **Request Logs** - SQLite database
3. **Log Files** - `gateway.log`, `litellm.log`
4. **Health Endpoint** - `/health`
5. **Metrics API** - `/metrics`

---

## Admin Dashboard

### Accessing the Dashboard

```
http://localhost:4000/ui
```

Or with authentication:

```yaml
# In config.yaml
general_settings:
  ui_username: "admin"
  ui_password: os.environ/UI_PASSWORD
```

### Dashboard Features

#### 1. **Overview**
- Total requests
- Active models
- Current usage
- Recent errors

#### 2. **Models**
- List all models
- Test models
- View model stats
- Enable/disable models

#### 3. **API Keys**
- Create virtual keys
- View key usage
- Revoke keys
- Set budgets

#### 4. **Usage**
- Requests per model
- Token consumption
- Cost breakdown
- Usage trends

#### 5. **Logs**
- Recent requests
- Error logs
- Search and filter
- Export logs

---

## Logging

### Log Files

```bash
# Gateway logs
tail -f gateway.log

# LiteLLM logs
tail -f litellm.log

# Tunnel logs (if using Cloudflare)
tail -f tunnel.log
```

### Log Configuration

```yaml
# In config.yaml
general_settings:
  log_level: "INFO"        # DEBUG, INFO, WARNING, ERROR
  json_logs: true          # JSON format logs
  log_file: "gateway.log"  # Log file path

litellm_settings:
  set_verbose: true        # Verbose logging
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| DEBUG | Development | Detailed debugging info |
| INFO | Production | Normal operations |
| WARNING | Production | Potential issues |
| ERROR | Production | Errors only |

### Viewing Logs

```bash
# All logs
tail -f gateway.log

# Errors only
tail -f gateway.log | grep ERROR

# Specific model
tail -f gateway.log | grep "model=gpt-4"

# Authentication failures
tail -f gateway.log | grep "auth.*failed"

# Last 100 lines
tail -n 100 gateway.log
```

### Log Rotation

```bash
# Install logrotate
sudo apt install logrotate

# Create /etc/logrotate.d/litellm
sudo nano /etc/logrotate.d/litellm
```

Add:
```
/path/to/gateway.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 user user
}
```

---

## Usage Tracking

### Database Schema

```sql
-- Requests table
CREATE TABLE request_log (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    user_id TEXT,
    model TEXT,
    messages TEXT,
    response TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    cost REAL,
    latency REAL,
    status_code INTEGER
);
```

### Query Recent Requests

```python
import sqlite3

conn = sqlite3.connect('litellm.db')
cursor = conn.cursor()

# Last 10 requests
cursor.execute("""
    SELECT timestamp, model, total_tokens, cost
    FROM request_log
    ORDER BY timestamp DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} | {row[2]} tokens | ${row[3]}")
```

### Track Usage by Model

```python
cursor.execute("""
    SELECT model, 
           COUNT(*) as requests,
           SUM(total_tokens) as total_tokens,
           SUM(cost) as total_cost
    FROM request_log
    WHERE timestamp > datetime('now', '-7 days')
    GROUP BY model
    ORDER BY total_cost DESC
""")

print("Model Usage (Last 7 Days)")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:30} | {row[1]:6} reqs | {row[2]:8} tokens | ${row[3]:.2f}")
```

### Track Usage by User

```python
cursor.execute("""
    SELECT user_id,
           COUNT(*) as requests,
           SUM(cost) as total_cost
    FROM request_log
    WHERE timestamp > datetime('now', '-30 days')
    GROUP BY user_id
    ORDER BY total_cost DESC
""")

print("User Usage (Last 30 Days)")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]:20} | {row[1]:6} reqs | ${row[2]:.2f}")
```

---

## Cost Analysis

### Real-Time Cost Tracking

```bash
curl http://localhost:4000/spend/info \
  -H "Authorization: Bearer YOUR_MASTER_KEY"
```

Response:
```json
{
  "total_spend": 123.45,
  "daily_spend": 12.34,
  "monthly_spend": 98.76,
  "by_model": {
    "gpt-4": 45.67,
    "gpt-3.5-turbo": 23.45
  }
}
```

### Cost by Model

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('litellm.db')

# Last 30 days cost by model
query = """
    SELECT 
        model,
        COUNT(*) as requests,
        SUM(prompt_tokens) as prompt_tokens,
        SUM(completion_tokens) as completion_tokens,
        SUM(cost) as total_cost,
        AVG(cost) as avg_cost
    FROM request_log
    WHERE timestamp > datetime('now', '-30 days')
    GROUP BY model
    ORDER BY total_cost DESC
"""

df = pd.read_sql_query(query, conn)
print(df)
```

### Daily Cost Trend

```python
query = """
    SELECT 
        DATE(timestamp) as date,
        COUNT(*) as requests,
        SUM(cost) as daily_cost
    FROM request_log
    WHERE timestamp > datetime('now', '-30 days')
    GROUP BY DATE(timestamp)
    ORDER BY date
"""

df = pd.read_sql_query(query, conn)

# Plot with matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['daily_cost'])
plt.xlabel('Date')
plt.ylabel('Cost ($)')
plt.title('Daily API Costs')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cost_trend.png')
```

### Budget Alerts

```yaml
# In config.yaml
litellm_settings:
  max_budget: 100.00       # USD per month
  budget_duration: "30d"
```

Or per-key:
```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "max_budget": 50.0,
    "budget_duration": "7d"
  }'
```

---

## Performance Metrics

### Response Time

```python
# Average response time by model
cursor.execute("""
    SELECT 
        model,
        AVG(latency) as avg_latency,
        MIN(latency) as min_latency,
        MAX(latency) as max_latency
    FROM request_log
    WHERE timestamp > datetime('now', '-7 days')
    GROUP BY model
    ORDER BY avg_latency
""")

print("Model Performance (Last 7 Days)")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:30} | Avg: {row[1]:.2f}s | Min: {row[2]:.2f}s | Max: {row[3]:.2f}s")
```

### Error Rate

```python
cursor.execute("""
    SELECT 
        model,
        COUNT(*) as total_requests,
        SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as errors,
        ROUND(100.0 * SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) / COUNT(*), 2) as error_rate
    FROM request_log
    WHERE timestamp > datetime('now', '-7 days')
    GROUP BY model
    ORDER BY error_rate DESC
""")

print("Model Error Rates (Last 7 Days)")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:30} | {row[1]:6} reqs | {row[2]:5} errors | {row[3]:5}%")
```

### Throughput

```python
cursor.execute("""
    SELECT 
        strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
        COUNT(*) as requests_per_hour
    FROM request_log
    WHERE timestamp > datetime('now', '-24 hours')
    GROUP BY hour
    ORDER BY hour
""")

print("Hourly Throughput (Last 24 Hours)")
print("-" * 40)
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]:5} requests")
```

---

## Alerts and Notifications

### Health Check Endpoint

```bash
curl http://localhost:4000/health
```

Response:
```json
{
  "status": "healthy",
  "uptime": 123456,
  "version": "1.44.0"
}
```

### Monitoring Script

Create `monitor.sh`:

```bash
#!/bin/bash

GATEWAY_URL="http://localhost:4000"
MASTER_KEY="your-master-key"
ALERT_EMAIL="admin@example.com"

# Check health
health=$(curl -s "$GATEWAY_URL/health" | jq -r '.status')

if [ "$health" != "healthy" ]; then
    echo "Gateway unhealthy!" | mail -s "Gateway Alert" $ALERT_EMAIL
fi

# Check error rate
errors=$(sqlite3 litellm.db "SELECT COUNT(*) FROM request_log WHERE timestamp > datetime('now', '-1 hour') AND status_code >= 400")

if [ "$errors" -gt 100 ]; then
    echo "High error rate: $errors errors in last hour" | mail -s "Gateway Alert" $ALERT_EMAIL
fi
```

Run every 5 minutes:
```bash
*/5 * * * * /path/to/monitor.sh
```

### Slack Notifications

```yaml
# In config.yaml
litellm_settings:
  success_callback: []
  failure_callback: ["slack"]

environment_variables:
  SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Email Alerts

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'gateway@example.com'
    msg['To'] = 'admin@example.com'
    
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)

# Check for high costs
cursor.execute("SELECT SUM(cost) FROM request_log WHERE DATE(timestamp) = DATE('now')")
daily_cost = cursor.fetchone()[0] or 0

if daily_cost > 100:
    send_alert(
        "High Daily Cost Alert",
        f"Daily cost has reached ${daily_cost:.2f}"
    )
```

---

## Database Queries

### Useful Queries

#### Top Users by Cost

```sql
SELECT 
    user_id,
    COUNT(*) as requests,
    SUM(total_tokens) as tokens,
    SUM(cost) as total_cost
FROM request_log
WHERE timestamp > datetime('now', '-30 days')
GROUP BY user_id
ORDER BY total_cost DESC
LIMIT 10;
```

#### Most Expensive Requests

```sql
SELECT 
    timestamp,
    model,
    total_tokens,
    cost,
    substr(messages, 1, 100) as request_preview
FROM request_log
ORDER BY cost DESC
LIMIT 20;
```

#### Request Volume by Hour

```sql
SELECT 
    strftime('%H', timestamp) as hour,
    COUNT(*) as requests
FROM request_log
WHERE DATE(timestamp) = DATE('now')
GROUP BY hour
ORDER BY hour;
```

#### Failed Requests

```sql
SELECT 
    timestamp,
    model,
    status_code,
    substr(response, 1, 200) as error_message
FROM request_log
WHERE status_code >= 400
ORDER BY timestamp DESC
LIMIT 50;
```

#### Token Efficiency

```sql
SELECT 
    model,
    AVG(prompt_tokens) as avg_input,
    AVG(completion_tokens) as avg_output,
    AVG(total_tokens) as avg_total
FROM request_log
WHERE timestamp > datetime('now', '-7 days')
GROUP BY model;
```

---

## Monitoring Dashboard Script

Create `dashboard.py`:

```python
import sqlite3
from datetime import datetime, timedelta

def generate_dashboard():
    conn = sqlite3.connect('litellm.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("LITELLM GATEWAY DASHBOARD")
    print("=" * 80)
    print()
    
    # Today's stats
    cursor.execute("""
        SELECT 
            COUNT(*) as requests,
            SUM(total_tokens) as tokens,
            SUM(cost) as cost
        FROM request_log
        WHERE DATE(timestamp) = DATE('now')
    """)
    
    row = cursor.fetchone()
    print(f"TODAY'S STATS")
    print(f"  Requests: {row[0]:,}")
    print(f"  Tokens: {row[1]:,}")
    print(f"  Cost: ${row[2]:.2f}")
    print()
    
    # Top models
    cursor.execute("""
        SELECT 
            model,
            COUNT(*) as requests,
            SUM(cost) as cost
        FROM request_log
        WHERE DATE(timestamp) = DATE('now')
        GROUP BY model
        ORDER BY requests DESC
        LIMIT 5
    """)
    
    print("TOP MODELS TODAY")
    for row in cursor.fetchall():
        print(f"  {row[0]:30} | {row[1]:5} reqs | ${row[2]:.2f}")
    print()
    
    # Recent errors
    cursor.execute("""
        SELECT COUNT(*)
        FROM request_log
        WHERE DATE(timestamp) = DATE('now')
        AND status_code >= 400
    """)
    
    errors = cursor.fetchone()[0]
    print(f"ERRORS TODAY: {errors}")
    print()
    print("=" * 80)

if __name__ == "__main__":
    generate_dashboard()
```

Run it:
```bash
python dashboard.py
```

---

## Monitoring Best Practices

### 1. Set Up Alerts

- Monitor error rates
- Track unusual cost spikes
- Alert on gateway downtime
- Watch for authentication failures

### 2. Regular Reviews

- Daily: Check error logs
- Weekly: Review cost trends
- Monthly: Analyze usage patterns
- Quarterly: Optimize model selection

### 3. Keep Historical Data

```bash
# Backup database weekly
0 0 * * 0 cp litellm.db backups/litellm-$(date +\%Y\%m\%d).db
```

### 4. Monitor External Services

- Provider API status pages
- Third-party monitoring (UptimeRobot, Pingdom)
- Infrastructure monitoring (if self-hosted)

---

## Next Steps

- **Deploy to Production**: [Production Deployment](production-deployment.md)
- **Troubleshoot Issues**: [Troubleshooting Guide](troubleshooting.md)
- **Secure Gateway**: [Security Guide](security-guide.md)

---

[⬅ Back to Guides](README.md) | [Next: Production Deployment ➡](production-deployment.md)

