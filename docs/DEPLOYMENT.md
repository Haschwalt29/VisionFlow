# Render Deployment Guide

## Overview

VisionFlow backend can be deployed on Render using the provided configuration.

## Deployment Steps

### 1. Prepare Repository

Ensure your repository includes:
- `render.yaml` (render configuration)
- `backend/requirements.txt` (python dependencies)
- `backend/app.py` (main application)
- `backend/wsgi.py` (WSGI entry point)

### 2. Create Render Web Service

1. **Log into Render Dashboard**
   - Visit [render.com](https://render.com)
   - Connect your GitHub repository

2. **Create New Web Service**
   - Choose "Web Service"
   - Connect your VisionFlow repository
   - Select branch: `main` or `master`

3. **Configure Service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app`
   - **Python Version**: 3.10+

### 3. Environment Variables

Set these in Render dashboard:

```
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
FLASK_ENV=production
PORT=10000
```

### 4. Automatic Deployment

Once configured:
- Render automatically deploys on git push
- Check deployment logs for issues
- Service URL will be provided after deployment

## Configuration Files

### render.yaml
```yaml
services:
  - type: web
    name: visionflow-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: GOOGLE_AI_API_KEY
        sync: false
      - key: FLASK_ENV
        value: production
```

### wsgi.py
Provides WSGI entry point for production servers.

## Monitoring

- Check Render dashboard for service health
- Monitor logs for application errors
- Track CPU/Memory usage
- Set up alerts for downtime

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt

2. **Runtime Errors**
   - Check environment variables are set
   - Review application logs in Render

3. **Database Issues**
   - SQLite file location
   - File system permissions

### Debugging

- Enable debug logs by setting `FLASK_ENV=development`
- Check Render service logs
- Test endpoints manually

## Scaling

For high traffic:
- Upgrade to paid Render plan
- Add redis for session storage
- Consider database migration to PostgreSQL

## Security

- Keep API keys secure in environment variables
- Enable HTTPS (automatic with Render)
- Regular security updates for dependencies
