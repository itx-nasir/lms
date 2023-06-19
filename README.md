# Lab Management System

A comprehensive lab management system built with FastAPI, Jinja2, Bootstrap, and SQLite.

## Features

✅ **Authentication**
- Single admin account with secure password hashing
- Session-based authentication with JWT tokens
- Default credentials: `admin` / `admin123`

✅ **Patient Management**
- Add, edit, delete patients
- Search functionality
- Patient demographics tracking

✅ **Test Management**
- Manage test categories
- Add/edit tests with pricing, units, and reference ranges
- Organize tests by categories

✅ **Order Management**
- Create test orders for patients
- Add multiple tests to orders
- Automatic total calculation
- Order status tracking (pending/completed)

✅ **Reports & Results**
- Enter test results for completed orders
- Generate professional PDF reports
- Print-friendly layouts
- Export to PDF using WeasyPrint

✅ **Modern UI/UX**
- Bootstrap 5 responsive design
- Clean and intuitive interface
- HTMX for enhanced interactivity
- Mobile-friendly design

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the System**
   - Open: http://localhost:8000
   - Login: `admin` / `admin123`

## Project Structure

```
lms/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration
├── crud.py              # Database operations
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication logic
├── utils.py             # PDF generation utilities
├── requirements.txt     # Python dependencies
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── patients.html
│   ├── tests.html
│   ├── orders.html
│   └── reports.html
└── static/             # CSS, JS, and assets
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Database Schema

- **patients**: id, name, age, gender, phone, created_at
- **test_categories**: id, name
- **tests**: id, name, price, unit, reference_range, category_id
- **test_orders**: id, patient_id, ordered_at, total_amount, status
- **test_order_items**: id, order_id, test_id, result_value, result_notes
- **admin_users**: id, username, hashed_password, created_at

## API Endpoints

- `GET /` - Home (redirects to dashboard)
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /dashboard` - Dashboard with stats
- `GET /patients` - Patient management
- `GET /tests` - Test management
- `GET /orders` - Order management
- `GET /reports` - Reports and results
- `GET /docs` - Auto-generated API documentation

## Features in Detail

### Dashboard
- Real-time statistics
- Quick action buttons
- Overview of system status

### Patient Management
- Complete patient registration
- Search and filter patients
- Edit patient information

### Test Management
- Create test categories
- Add tests with detailed information
- Manage pricing and reference ranges

### Order Processing
- Create orders for patients
- Select multiple tests
- Automatic total calculation
- Status tracking

### Report Generation
- Enter test results
- Generate professional reports
- PDF export functionality
- Print-friendly layouts

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates + Bootstrap 5
- **Authentication**: JWT with secure password hashing
- **PDF Generation**: WeasyPrint
- **Interactivity**: HTMX for dynamic features

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Session management
- CSRF protection
- Input validation and sanitization

## Development

The system is designed to be:
- **Simple**: Minimal setup, no complex dependencies
- **Secure**: Proper authentication and data validation
- **Fast**: SQLite for quick operations
- **Offline**: Works completely offline
- **Extensible**: Clean architecture for easy modifications

## Production Deployment

For production use:
1. Change the SECRET_KEY in `auth.py`
2. Update default admin credentials
3. Configure proper logging
4. Set up SSL/HTTPS
5. Use a production WSGI server

## License

This project is open source and available under the MIT License.