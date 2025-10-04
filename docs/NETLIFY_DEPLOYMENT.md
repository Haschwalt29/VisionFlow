# Netlify Deployment Guide

This guide covers deploying the VisionFlow frontend to Netlify.

## Prerequisites

1. **Backend deployed on Render** (required for API connection)
2. **GitHub repository** with frontend code
3. **Netlify account** (free tier available)

## Deployment Steps

### 1. Connect Repository to Netlify

1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"New site from Git"**
3. Choose **GitHub** as provider
4. Select your **VisionFlow** repository
5. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

### 2. Environment Variables

Set the backend API URL in Netlify:

1. Go to **Site settings** → **Environment variables**
2. Add variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-render-app.onrender.com`

Replace `your-render-app` with your actual Render service name.

**Note**: Environment variables must be set through the Netlify UI, NOT in the `netlify.toml` file to avoid triggering secrets scanning during deployment.

### 3. Build Configuration

The `netlify.toml` file already configures:
- ✅ Build command and publish directory
- ✅ SPA redirects (for React routing)
- ✅ Security headers
- ✅ Caching for static assets

### 4. Deploy

1. Click **"Deploy site"**
2. Netlify will automatically:
   - Install dependencies (`npm install`)
   - Build the React app (`npm run build`)
   - Deploy to CDN

## Post-Deployment

### Custom Domain (Optional)

1. **Go to**: Site settings → Domain management
2. **Add custom domain**: Input your domain name
3. **Configure DNS**: Follow Netlify's DNS instructions

### Environment Variables Override

You can override environment variables directly in Netlify:
- Go to **Site settings** → **Environment variables**
- Add production URL for `REACT_APP_API_URL`

## Troubleshooting

### Build Failures

- **Check**: Node.js version compatibility
- **Verify**: All dependencies install correctly
- **Review**: Build logs for specific errors

### API Connection Issues

- **Verify**: Backend URL is correct and accessible
- **Check**: CORS settings in backend
- **Confirm**: Environment variable is set correctly

### Routing Issues

The SPA redirect rule should handle client-side routing:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Automatic Deployments

With GitHub integration, Netlify will automatically redeploy when you push to your main branch.

## Performance Optimization

Configured optimizations:
- ✅ Static asset caching (1 year)
- ✅ Security headers
- ✅ Gzip compression (automatic)
- ✅ CDN distribution (automatic)

## Monitoring

Track your deployment:
- **Deploy logs**: Available in Netlify dashboard
- **Analytics**: Available on paid plans
- **Function logs**: For serverless functions (if used)

## Backup

Always maintain your source code on GitHub for backup and disaster recovery.
