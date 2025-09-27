# Vercel Deployment Guide for Solar System Django App

## Prerequisites
1. Vercel CLI installed (`npm i -g vercel`)
2. Git repository with your code
3. Database (PostgreSQL recommended)

## Step-by-Step Deployment

### 1. Environment Variables Setup
Before deploying, you need to set up environment variables in Vercel:

```bash
# Set these in Vercel dashboard or via CLI
vercel env add SECRET_KEY
vercel env add DEBUG
vercel env add DATABASE_URL
vercel env add ALLOWED_HOSTS
```

**Environment Variables to Set:**
- `SECRET_KEY`: A secure Django secret key (generate one using Django's built-in generator)
- `DEBUG`: Set to "False" for production
- `DATABASE_URL`: Your PostgreSQL database connection string
- `ALLOWED_HOSTS`: Set to ".vercel.app"

### 2. Database Setup
For production, you'll need a PostgreSQL database. Recommended options:
- **Neon** (Free tier available): https://neon.tech/
- **Supabase** (Free tier available): https://supabase.com/
- **Railway** (Free tier available): https://railway.app/

### 3. Deploy to Vercel

#### Option A: Deploy via Vercel CLI
```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name: solar-system-django (or your preferred name)
# - Directory: ./
# - Override settings? N
```

#### Option B: Deploy via GitHub Integration
1. Push your code to GitHub
2. Go to https://vercel.com/dashboard
3. Click "New Project"
4. Import your GitHub repository
5. Configure environment variables
6. Deploy

### 4. Run Database Migrations
After deployment, you need to run migrations:

```bash
# Connect to your Vercel function
vercel env pull .env.local

# Run migrations locally with production database
python manage.py migrate --settings=solar_system_drf.settings
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser --settings=solar_system_drf.settings
```

## Configuration Files

### vercel.json
The `vercel.json` file has been configured to:
- Use Python 3.11 runtime
- Route all requests to `/api/index.py`
- Serve static files from `/staticfiles/`
- Serve media files from `/media/`

### api/index.py
This file serves as the entry point for Vercel:
- Sets up Django WSGI application
- Configures proper Python path
- Handles requests through the `handler` function

### requirements.txt
All dependencies are pinned to specific versions for stability.

## Troubleshooting

### Common Issues:

1. **"Command exited with 127"**
   - This usually means Python/pip command not found
   - Solution: The configuration has been updated to use proper Python runtime

2. **Static files not loading**
   - Make sure `python manage.py collectstatic --noinput` runs successfully
   - Check that static files are in the `staticfiles/` directory

3. **Database connection issues**
   - Verify `DATABASE_URL` environment variable is set correctly
   - Ensure database is accessible from Vercel's servers

4. **CSRF token errors**
   - Check that `CSRF_TRUSTED_ORIGINS` includes your Vercel domain
   - Ensure `SECURE_SSL_REDIRECT` is properly configured

### Debug Steps:
1. Check Vercel function logs in the dashboard
2. Verify all environment variables are set
3. Test database connection locally with production settings
4. Check static file collection locally

## Post-Deployment

1. **Verify Deployment**: Visit your Vercel URL
2. **Check Admin Panel**: Visit `/admin/` to ensure it's accessible
3. **Test API Endpoints**: If you have API endpoints, test them
4. **Monitor Logs**: Keep an eye on Vercel function logs for any errors

## Additional Notes

- The app is configured to work with Vercel's serverless functions
- Static files are served efficiently using Vercel's CDN
- Database migrations need to be run manually after deployment
- The app uses WhiteNoise for static file serving in production

## Support

If you encounter issues:
1. Check the Vercel deployment logs
2. Verify all environment variables are correctly set
3. Ensure your database is accessible
4. Test locally with production settings first
