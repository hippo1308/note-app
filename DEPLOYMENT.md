# 🚀 PythonAnywhere Deployment Guide

## Step-by-Step Instructions

### 1. **Create PythonAnywhere Account**
- Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for a free account
- Verify your email

### 2. **Upload Your Files**
- **Option A: Upload via Web Interface**
  1. Go to the "Files" tab in PythonAnywhere
  2. Create a new directory (e.g., `noteapp`)
  3. Upload all your files:
     - `app.py`
     - `requirements.txt`
     - `templates/` folder (upload as zip, then extract)
     - `static/` folder (if you have one)

- **Option B: Git Clone (Recommended)**
  1. Push your code to GitHub first
  2. In PythonAnywhere, go to "Consoles" → "Bash"
  3. Run: `git clone https://github.com/yourusername/your-repo.git`
  4. Navigate to your project: `cd your-repo`

### 3. **Set Up Virtual Environment**
```bash
# In PythonAnywhere Bash console
cd your-project-directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. **Create Web App**
1. Go to "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.10
5. Set the path to your app: `/home/yourusername/your-project-directory/app.py`

### 5. **Configure WSGI File**
1. Click on the WSGI configuration file link
2. Replace the content with:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/your-project-directory'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application

# Optional: Set environment variables
os.environ['SECRET_KEY'] = 'your-super-secret-key-here'
```

### 6. **Set Up Database**
1. In your PythonAnywhere Bash console:
```bash
cd your-project-directory
source venv/bin/activate
python3
```

2. In Python console:
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database created successfully!")
```

### 7. **Configure Static Files**
1. In the "Web" tab, scroll to "Static files"
2. Add:
   - URL: `/static/`
   - Directory: `/home/yourusername/your-project-directory/static`

### 8. **Reload Your Web App**
- Click the "Reload" button in the "Web" tab

### 9. **Test Your App**
- Your app will be available at: `yourusername.pythonanywhere.com`

## 🔧 **Troubleshooting**

### Common Issues:

1. **Import Errors**
   - Make sure you're in the virtual environment
   - Check that all requirements are installed

2. **Database Issues**
   - Ensure the database file has write permissions
   - Check the database path in your app configuration

3. **Static Files Not Loading**
   - Verify static file configuration in Web tab
   - Check file paths are correct

4. **500 Internal Server Error**
   - Check the error logs in the "Web" tab
   - Look for specific error messages

### **Security Notes:**
- Change the SECRET_KEY in production
- Use environment variables for sensitive data
- Consider using a proper database (MySQL/PostgreSQL) for production

## 📝 **Hackathon Tips:**

1. **Demo Preparation:**
   - Create a test account for judges
   - Prepare a demo script
   - Test all features before presentation

2. **Documentation:**
   - Update your README with the live URL
   - Include screenshots of your app
   - Document any special features

3. **Backup:**
   - Keep a local copy of your code
   - Use version control (Git)
   - Document your deployment process

## 🎯 **Your Live URL:**
Once deployed, your app will be available at:
`https://yourusername.pythonanywhere.com`

## 📞 **Need Help?**
- PythonAnywhere has excellent documentation
- Check their forums for common issues
- Most hackathon organizers can help with deployment issues 