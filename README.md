# trekking-management-application
Trekking Management Application

## Project Structure
 
```
trekking_management_application/
├── app.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── trek.py
│   ├── booking.py
│   └── trek_image.py
├── blueprints/
│   ├── authentication.py
│   ├── admin.py
│   ├── staff.py
│   └── user.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── authentication/
│   │   ├── login.html
│   │   ├── user_registration.html
│   │   └── staff_registration.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── staff.html
│   │   ├── staff_approvals.html
│   │   ├── treks.html
│   │   ├── create_trek.html
│   │   ├── edit_trek.html
│   │   └── bookings.html
│   ├── staff/
│   │   ├── dashboard.html
│   │   ├── treks.html
│   │   ├── edit_trek.html
│   │   ├── participants.html
│   │   └── profile.html
│   └── user/
│       ├── dashboard.html
│       ├── treks.html
│       ├── bookings.html
│       └── profile.html
└── static/
    └── style.css
```