# 👨‍🎓 Mentoring Management System

A comprehensive mentoring management system built with PHP and MySQL. Manages mentoring relationships, schedules, progress tracking, and mentor-mentee communications in one centralized platform.

![PHP](https://img.shields.io/badge/PHP-7.4+-blue?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 👥 **User Management** - Mentors, mentees, admins
- 📅 **Scheduling System** - Schedule mentoring sessions
- 💬 **Messaging** - Direct communication between mentees and mentors
- 📊 **Progress Tracking** - Monitor mentee progress and goals
- 📝 **Documentation** - Notes and session records
- 📊 **Analytics Dashboard** - Performance metrics
- 🔐 **Role-Based Access** - Different permissions for users
- 📱 **Responsive Design** - Works on mobile and desktop

---

## 🛠️ Technologies Used

- **PHP 7.4+** - Server-side scripting
- **MySQL 5.7+** - Database management
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript** - Client-side functionality
- **Bootstrap** - Responsive framework
- **AJAX** - Asynchronous requests
- **jQuery** - JavaScript library

---

## 🚀 Quick Start

### Prerequisites

- Web server (Apache/Nginx)
- PHP 7.4+
- MySQL 5.7+
- Browser with JavaScript enabled

### Installation

#### Option 1: XAMPP/WAMP/LAMP Setup

```bash
# 1. Extract project to webroot
# For XAMPP: C:\xampp\htdocs\mentoring-system
# For WAMP: C:\wamp\www\mentoring-system
# For Linux: /var/www/html/mentoring-system

# 2. Create database
mysql -u root -p
CREATE DATABASE mentoring_system;
USE mentoring_system;
SOURCE database.sql;

# 3. Update config
# Edit config.php with your database credentials
DB_HOST = localhost
DB_USER = root
DB_PASS = your_password
DB_NAME = mentoring_system

# 4. Access in browser
http://localhost/mentoring-system
```

#### Option 2: Docker Setup

```bash
docker-compose up -d
# Automatically sets up PHP, MySQL, and database
```

---

## 📖 User Guide

### For Admins

1. **Manage Users**
   - Create mentor/mentee accounts
   - Assign roles and permissions
   - Monitor activity

2. **View Analytics**
   - Overall platform statistics
   - User engagement metrics
   - Session completion rates

3. **System Configuration**
   - Set mentoring goals
   - Configure email notifications
   - Manage system settings

### For Mentors

1. **View Mentees**
   - List of assigned mentees
   - Mentee progress overview
   - Contact information

2. **Schedule Sessions**
   - Create session schedule
   - Send invitations
   - Track attendance

3. **Provide Feedback**
   - Give progress feedback
   - Set goals
   - Document achievements

### For Mentees

1. **Find Mentors**
   - Browse available mentors
   - View mentor profiles
   - Send connection requests

2. **Attend Sessions**
   - View scheduled sessions
   - Join virtual meetings
   - Download session notes

3. **Track Progress**
   - View goals
   - Check feedback
   - View recommendations

---

## 📁 Project Structure

```
Mentoring-Management-System/
├── config.php                  # Database configuration
├── index.php                   # Home page
├── login.php                   # Login page
├── logout.php                  # Logout functionality
│
├── dashboard/
│   ├── admin_dashboard.php    # Admin panel
│   ├── mentor_dashboard.php   # Mentor dashboard
│   └── mentee_dashboard.php   # Mentee dashboard
│
├── users/
│   ├── profile.php            # User profile
│   ├── edit_profile.php       # Edit profile
│   └── manage_users.php       # User management (admin)
│
├── mentoring/
│   ├── sessions.php           # Session management
│   ├── schedule.php           # Scheduling
│   ├── progress.php           # Progress tracking
│   └── goals.php              # Goal management
│
├── messaging/
│   ├── messages.php           # Message list
│   ├── compose.php            # Send message
│   └── notifications.php      # Notifications
│
├── reports/
│   ├── progress_report.php    # Progress reports
│   ├── attendance_report.php  # Attendance records
│   └── analytics.php          # Analytics dashboard
│
├── css/
│   ├── style.css              # Main stylesheet
│   └── responsive.css         # Mobile styles
│
├── js/
│   ├── app.js                 # Main JavaScript
│   ├── dashboard.js           # Dashboard logic
│   └── messaging.js           # Messaging logic
│
├── includes/
│   ├── header.php             # Header template
│   ├── footer.php             # Footer template
│   └── functions.php          # Helper functions
│
├── database.sql               # Database schema
└── README.md                  # Documentation
```

---

## 🗄️ Database Schema

### Key Tables

```sql
-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('admin', 'mentor', 'mentee'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mentoring Relationships
CREATE TABLE mentoring_pairs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mentor_id INT,
    mentee_id INT,
    start_date DATE,
    status ENUM('active', 'completed'),
    FOREIGN KEY (mentor_id) REFERENCES users(id),
    FOREIGN KEY (mentee_id) REFERENCES users(id)
);

-- Sessions
CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mentoring_pair_id INT,
    session_date DATETIME,
    duration INT,
    notes TEXT,
    FOREIGN KEY (mentoring_pair_id) REFERENCES mentoring_pairs(id)
);

-- Messages
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT,
    receiver_id INT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

-- Goals
CREATE TABLE goals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mentee_id INT,
    goal_text TEXT,
    target_date DATE,
    status ENUM('pending', 'in_progress', 'completed'),
    FOREIGN KEY (mentee_id) REFERENCES users(id)
);
```

---

## 🔐 Security Features

- ✅ Password hashing (bcrypt)
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CSRF tokens
- ✅ Session management
- ✅ Role-based access control
- ✅ Email verification

---

## 🎯 Key Functionalities

| Feature | Description |
|---------|-------------|
| **User Authentication** | Secure login/registration |
| **Role Management** | Admin, Mentor, Mentee roles |
| **Scheduling** | Calendar-based session scheduling |
| **Messaging** | Real-time messaging system |
| **Progress Tracking** | Goal and achievement tracking |
| **Reporting** | Generate progress and attendance reports |
| **Notifications** | Email and in-app notifications |

---

## ⚙️ Configuration

Edit `config.php`:

```php
<?php
// Database Configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'password');
define('DB_NAME', 'mentoring_system');

// Application Settings
define('APP_NAME', 'Mentoring Management System');
define('APP_URL', 'http://localhost/mentoring-system');

// Email Configuration
define('MAIL_HOST', 'smtp.gmail.com');
define('MAIL_USER', 'your-email@gmail.com');
define('MAIL_PASS', 'your-password');
?>
```

---

## 🚀 Deployment

### Deploying to Server

```bash
# 1. Upload files via FTP
ftp -u your_server.com

# 2. Create database on server
mysql -h host -u user -p < database.sql

# 3. Update config.php
# Set correct database credentials

# 4. Set permissions
chmod 755 /var/www/html/mentoring-system
chmod 644 /var/www/html/mentoring-system/*.php
```

---

## 🐛 Troubleshooting

### Database Connection Error
```php
// Check config.php credentials
// Verify MySQL is running
// Check user permissions
```

### Emails Not Sending
- Configure SMTP settings
- Check email credentials
- Verify firewall rules
- Enable "Less secure apps" (Gmail)

### Session Issues
- Clear browser cookies
- Check PHP session directory permissions
- Verify session timeout settings

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Video conferencing integration
- Mobile app version
- API development
- Advanced analytics

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 📞 Support

For issues and questions:
- GitHub Issues: [Report here](https://github.com/NISARGAGOWDRU/Mentoring-Management-System/issues)
- Email: support@mentoringsystem.com

---

**Made with ❤️ by NISARGA GOWDRU**
