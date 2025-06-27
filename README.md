# NoteApp - Advanced Note Taking Application

A feature-rich Flask-based note-taking application with user authentication, note editing, reminders, and pinning functionality.

## 🚀 **Live Demo**
**Deployed on PythonAnywhere:** [Your URL will be here after deployment]

**Demo Account:**
- Username: `demo`
- Password: `demo123`

## 🏆 **Hackathon Project**

This project was built for [Your Hackathon Name] with the following goals:
- **Problem Solved**: Digital note-taking with advanced organization features
- **Target Users**: Students, professionals, and anyone who needs to organize information
- **Key Innovation**: Real-time pinning and intelligent reminder system

## Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Note Management**: Create, read, update, and delete notes
- **Note Editing**: Full editing capabilities for existing notes
- **Note Pinning**: Pin important notes to keep them at the top
- **Reminders**: Set custom reminders for notes with date and time
- **Responsive Design**: Modern, mobile-friendly interface

### Advanced Features
- **Real-time Pinning**: Toggle pin status without page refresh
- **Reminder Management**: Dedicated page for viewing upcoming and overdue reminders
- **Visual Indicators**: Color-coded reminders and pinned notes
- **Auto-save**: Automatic saving of note modifications
- **Search & Organization**: Notes organized by pin status and creation date

## Installation

### Local Development
1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:5000`

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed PythonAnywhere deployment instructions.

## Usage

### Getting Started
1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Create Notes**: Use the form on the dashboard to add new notes

### Note Features
- **Title & Content**: Add descriptive titles and detailed content
- **Reminders**: Set optional reminders with date and time
- **Pinning**: Click the pin icon to pin/unpin important notes
- **Editing**: Click the edit button to modify existing notes
- **Deletion**: Remove notes you no longer need

### Reminder System
- **Set Reminders**: Add date/time reminders when creating or editing notes
- **View Reminders**: Visit the Reminders page to see upcoming and overdue reminders
- **Overdue Alerts**: Overdue reminders are highlighted in red
- **Upcoming Reminders**: Future reminders are shown in blue

### Navigation
- **Dashboard**: Main page with all your notes
- **Reminders**: Dedicated page for reminder management
- **Logout**: Secure logout functionality

## File Structure

```
website!!/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── DEPLOYMENT.md         # Deployment instructions
├── setup_pythonanywhere.py # Database setup script
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # Main dashboard
│   ├── edit_note.html    # Note editing form
│   └── reminders.html    # Reminders page
└── instance/             # Database files (auto-generated)
    └── notes.db          # SQLite database
```

## Technical Details

### Backend
- **Framework**: Flask
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Security**: Password hashing with Werkzeug

### Frontend
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS for interactive features

### Database Schema
- **Users**: username, email, password_hash
- **Notes**: title, content, created_at, updated_at, is_pinned, reminder_date, user_id

## Security Features
- Password hashing and salting
- User session management
- CSRF protection
- Input validation
- User authorization (users can only access their own notes)

## 🎯 **Hackathon Features**

### What Makes This Special:
1. **Real-time Pinning**: Instant visual feedback without page refresh
2. **Smart Reminders**: Intelligent organization of upcoming vs overdue reminders
3. **User Experience**: Clean, intuitive interface with smooth interactions
4. **Mobile Responsive**: Works perfectly on all devices
5. **Production Ready**: Proper error handling and security measures

### Technical Achievements:
- **AJAX Integration**: Real-time pin toggling
- **Database Design**: Efficient schema with proper relationships
- **Security Implementation**: Proper authentication and authorization
- **Responsive Design**: Mobile-first approach with Bootstrap 5

## Customization

### Adding New Features
1. **Database**: Add new fields to the Note model in `app.py`
2. **Routes**: Create new Flask routes for functionality
3. **Templates**: Add corresponding HTML templates
4. **Styling**: Modify CSS in `base.html` or add new stylesheets

### Styling
- Modify the CSS in `templates/base.html`
- Add custom Bootstrap classes
- Include additional CSS frameworks as needed

## Troubleshooting

### Common Issues
1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **Database Issues**: Delete `instance/notes.db` and restart the application
3. **Port Conflicts**: Change the port in `app.py` if 5000 is already in use

### Development
- Set `debug=True` in `app.py` for development mode
- Check the console for error messages
- Use browser developer tools for frontend debugging

## Future Enhancements

Potential features to add:
- **Note Categories/Tags**: Organize notes by categories
- **Search Functionality**: Search through note content
- **Export/Import**: Backup and restore notes
- **Collaboration**: Share notes with other users
- **Rich Text Editor**: Enhanced text formatting
- **File Attachments**: Add images and documents to notes
- **Email Notifications**: Send reminder emails
- **Mobile App**: Native mobile application

## 🏅 **Hackathon Submission**

### Demo Instructions:
1. **Visit the live URL**: [Your deployed URL]
2. **Use demo account**: username=`demo`, password=`demo123`
3. **Show key features**:
   - Create a new note with reminder
   - Pin an important note
   - Edit an existing note
   - View reminders page
   - Demonstrate mobile responsiveness

### Technical Stack:
- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (production-ready for MySQL/PostgreSQL)
- **Deployment**: PythonAnywhere

## License

This project is open source and available under the MIT License. 