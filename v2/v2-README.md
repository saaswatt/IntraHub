# PortalWiFi v0.2 — Modular Captive Portal Application

**Project:** IntraHub  
**Component:** PortalWiFi  
**Version:** 0.2.0  
**Development platform:** Windows 11  
**Programming language:** Python 3.12  
**Web framework:** Flask 3.1  
**Status:** Application-layer prototype completed; ready for version freeze  
**Last updated:** 31 October 2026

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Background](#2-project-background)
3. [Purpose of Version 0.2](#3-purpose-of-version-02)
4. [Version History](#4-version-history)
5. [System Architecture](#5-system-architecture)
6. [Development Environment](#6-development-environment)
7. [Technology Stack](#7-technology-stack)
8. [Project Directory Structure](#8-project-directory-structure)
9. [Application Components](#9-application-components)
10. [Authentication Architecture](#10-authentication-architecture)
11. [Session Management](#11-session-management)
12. [Security Implementation](#12-security-implementation)
13. [Logging and Monitoring](#13-logging-and-monitoring)
14. [Configuration Management](#14-configuration-management)
15. [Application Execution](#15-application-execution)
16. [Installation and Setup](#16-installation-and-setup)
17. [Application Workflow](#17-application-workflow)
18. [Testing and Validation](#18-testing-and-validation)
19. [Network Environment](#19-network-environment)
20. [What Works and What Does Not](#20-what-works-and-what-does-not)
21. [Known Limitations](#21-known-limitations)
22. [Security Considerations](#22-security-considerations)
23. [Important Architectural Decisions](#23-important-architectural-decisions)
24. [Version 0.1 vs Version 0.2](#24-version-01-vs-version-02)
25. [Version 0.3 Development Plan](#25-version-03-development-plan)
26. [Long-Term Roadmap](#26-long-term-roadmap)
27. [Git and Version Control](#27-git-and-version-control)
28. [Troubleshooting](#28-troubleshooting)
29. [Final Project Status](#29-final-project-status)
30. [Development Notes and Lessons Learned](#30-development-notes-and-lessons-learned)

---

# 1. Project Overview

PortalWiFi is a captive portal component being developed as part of the IntraHub project.

The objective is to create a Wi-Fi access management system in which users connecting to a designated wireless network are presented with an authentication portal before receiving permission to access the internet.

The intended system has three major responsibilities:

1. Provide a web-based authentication interface.
2. Authenticate wireless clients and maintain their authorization state.
3. Enforce network access restrictions based on authentication status.

Version 0.2 focuses exclusively on the first responsibility and the application-level foundations of the second.

It introduces a modular Flask application with password hashing, session management, CSRF protection, rate limiting, authentication logging and a responsive interface.

**Important:** PortalWiFi v0.2 is not yet a complete network-enforced captive portal. Successful authentication changes the Flask application's session state. It does not currently modify Windows network forwarding rules or grant actual internet access through a network filtering mechanism.

That distinction is fundamental to understanding the current implementation.

## 1.1 Primary Objective

The long-term objective is to build a system with the following behaviour:

- A wireless client connects to the IntraHub hotspot.
- The client attempts to access a website.
- The client is redirected or otherwise directed to the captive portal.
- The client authenticates.
- The system records the client's authorization.
- The network enforcement component permits the authenticated client's traffic.
- Unauthenticated clients remain restricted.
- Authorization can subsequently be revoked.

Version 0.2 establishes the application foundation required for this workflow.

## 1.2 Current Development Scope

| Area | Version 0.2 scope |
|---|---|
| Web application | Implemented |
| Authentication interface | Implemented |
| Password verification | Implemented |
| Session management | Implemented |
| Application security | Implemented |
| Authentication logging | Implemented |
| Mobile accessibility | Tested |
| Wi-Fi hotspot integration | Tested manually |
| Network traffic enforcement | Not implemented |
| Automatic captive portal detection | Not implemented |
| Client authorization management | Not implemented |

---

# 2. Project Background

The development of PortalWiFi began with a simple objective: create a Wi-Fi network where users must authenticate before being allowed to use the internet.

The initial proof of concept was developed using Flask.

The first version demonstrated that a laptop running Windows 11 could host a Flask application while simultaneously operating a Windows Mobile Hotspot. Another device could connect to that hotspot and access the Flask application through the laptop's hotspot gateway address.

This proved that the basic connectivity and web application components could work together.

However, the first implementation had architectural and security limitations:

- The application was contained in a single Python file.
- Authentication relied on a comparatively basic password comparison.
- There was no proper session-based authorization state.
- There was no CSRF protection.
- There was no authentication rate limiting.
- There was no structured authentication event logging.
- The application was not organized for future expansion.

Version 0.2 was therefore developed as a separate implementation rather than modifying the original prototype.

This allowed the first version to remain available as a working reference.

---

# 3. Purpose of Version 0.2

Version 0.2 is named:

**Modular Portal Architecture**

Its primary objective is to convert the original proof of concept into a maintainable and more secure Flask application.

The development priorities were:

1. Separate application logic from presentation.
2. Introduce centralized configuration management.
3. Replace plaintext password verification with password hashing.
4. Introduce session-based authentication.
5. Implement CSRF protection.
6. Implement login rate limiting.
7. Introduce authentication event logging.
8. Improve the user interface.
9. Test accessibility from an actual wireless client.
10. Establish a foundation for future network enforcement.

The version was deliberately kept independent of Windows Filtering Platform (WFP).

This was an important scope decision.

Network-level enforcement introduces a different set of technical requirements, including privileged Windows APIs, packet filtering, interface identification and authorization synchronization.

Combining that work with the initial modularization effort would have made debugging and testing considerably more difficult.

Version 0.2 therefore concentrates on making the web application reliable before integrating it with a network enforcement component.

---

# 4. Version History

## 4.1 Version 0.1 — Initial Proof of Concept

Version 0.1 established basic communication between the laptop and a wireless client.

Implemented capabilities included:

- A Flask web server.
- A basic login page.
- Password-based authentication.
- Access to the application through the laptop's hotspot gateway.
- Basic mobile-device testing.

The implementation was intentionally simple.

Its purpose was to establish whether the basic concept was technically feasible.

### Limitations of v0.1

- Monolithic application structure.
- Limited security controls.
- No proper authentication session lifecycle.
- No CSRF protection.
- No login rate limiting.
- Limited logging.
- No actual network-level access enforcement.

## 4.2 Version 0.2 — Modular Portal Architecture

Version 0.2 introduced a more structured implementation.

The application was separated into configuration, extensions, routes, templates, static resources and runtime initialization.

Security controls were added to the authentication workflow.

The application was also tested from a smartphone connected to the Windows Mobile Hotspot.

**Version 0.2 is the current stable application-layer baseline.**

---

# 5. System Architecture

Version 0.2 follows a modular Flask application architecture.

The application is divided into several logical components.

## 5.1 High-Level Architecture

```text
                  Wireless Client
                         |
                         |
                  Windows Mobile
                      Hotspot
                         |
                         |
                  Laptop Gateway
                  192.168.137.1
                         |
                         |
                  Flask Application
                    Port 8080
                         |
             +-----------+-----------+
             |                       |
             |                       |
        Application              Static Assets
          Routes                 CSS / JavaScript
             |
             |
        Authentication
             |
       +-----+------+
       |            |
       |            |
   Password      Session
   Verification  Management
       |            |
       +-----+------+
             |
             |
       Security Controls
       - CSRF Protection
       - Rate Limiting
       - Password Hashing
             |
             |
       Authentication Logs
```

This diagram represents the application architecture, not the complete future network architecture.

## 5.2 Logical Components

| Component | Responsibility |
|---|---|
| Flask application factory | Initializes the application |
| Configuration module | Loads application settings |
| Extensions module | Initializes security extensions |
| Routes module | Handles HTTP requests |
| Template layer | Renders the portal interface |
| CSS | Controls presentation and responsiveness |
| JavaScript | Implements client-side interactions |
| Environment file | Stores deployment-specific configuration |
| Logging subsystem | Records authentication events |

## 5.3 Request Lifecycle

When a client accesses the portal:

1. The browser sends an HTTP request.
2. Flask receives the request.
3. The appropriate route is selected.
4. The route retrieves the necessary configuration and session information.
5. Flask renders the login template.
6. The browser receives the HTML document.
7. The browser loads the CSS and JavaScript resources.
8. The user can submit the authentication form.

For a login request:

1. The browser submits the password using HTTP POST.
2. Flask-WTF validates the CSRF token.
3. Flask-Limiter evaluates the request limit.
4. The route retrieves the submitted password.
5. Werkzeug verifies the password against the stored password hash.
6. The application updates the session according to the result.
7. An authentication event is written to the application log.
8. The application redirects the browser to the portal page.

---

# 6. Development Environment

The development environment used for version 0.2 is Windows-based.

## 6.1 Operating System

- Windows 11
- Windows PowerShell
- Windows Mobile Hotspot

The application was developed and tested on the laptop rather than inside a Linux virtual machine.

## 6.2 Programming Environment

| Component | Version / Configuration |
|---|---|
| Python | 3.12.9 |
| Flask | 3.1.3 |
| Flask-WTF | 1.3.0 |
| Flask-Limiter | 4.1.1 |
| python-dotenv | 1.2.4 |
| Werkzeug | 3.1.9 |
| Editor | Visual Studio Code |
| Terminal | Windows PowerShell |
| Virtual environment | Python venv |
| Docker | Not required |

The project uses a shared virtual environment located at the IntraHub repository root.

## 6.3 Virtual Environment

The virtual environment is located at:

```text
G:\IntraHub\venv
```

It is shared by the IntraHub development environment.

Activation command:

```powershell
cd G:\IntraHub
.\venv\Scripts\Activate.ps1
```

After activation, PowerShell should display the environment name:

```text
(venv) PS G:\IntraHub>
```

The virtual environment isolates the project's Python dependencies from the system Python installation.

---

# 7. Technology Stack

## 7.1 Python

Python is the primary programming language.

It is responsible for:

- Application initialization.
- HTTP request handling.
- Authentication logic.
- Session handling.
- Configuration loading.
- Logging.
- Integration with security libraries.

## 7.2 Flask

Flask is the web framework used to implement the portal.

It provides:

- Routing.
- HTTP request handling.
- Template rendering.
- Session management.
- Application configuration.
- Flash messages.
- Integration with extensions.

Flask was selected because it is lightweight and allows the application to be structured without introducing unnecessary framework complexity.

## 7.3 Flask-WTF

Flask-WTF provides CSRF protection.

It protects state-changing form submissions by requiring a valid CSRF token.

Version 0.2 applies CSRF protection to the application.

The login and logout forms include CSRF tokens.

## 7.4 Flask-Limiter

Flask-Limiter provides request rate limiting.

It is used to restrict the number of login attempts originating from a particular client IP address.

The login route currently uses:

```python
@limiter.limit("5 per minute")
```

The purpose is to reduce automated password guessing and repeated login attempts.

The current storage backend is:

```text
memory://
```

This is suitable for the current single-process prototype, but it is not a persistent or shared production rate-limit store.

## 7.5 Werkzeug

Werkzeug is used for secure password hash verification.

The application uses:

```python
from werkzeug.security import check_password_hash
```

Instead of storing and comparing the original password, the application verifies the submitted password against a stored hash.

## 7.6 python-dotenv

python-dotenv loads environment variables from the project's root `.env` file.

This allows configuration and secret values to remain outside the application source code.

## 7.7 HTML, CSS and JavaScript

The frontend is separated into three parts:

- HTML defines the structure.
- CSS controls appearance and responsiveness.
- JavaScript provides interactive behaviour.

This separation makes the interface easier to maintain and modify.

---

# 8. Project Directory Structure

The IntraHub repository is organized as follows:

```text
G:\IntraHub\
│
├── .git\
├── .gitignore
├── .vscode\
├── .env
├── venv\
│
├── v1\
│   ├── app.py
│   ├── requirements.txt
│   └── v1-README.md
│
└── v2\
    │
    ├── .env.example
    ├── requirements.txt
    ├── run.py
    │
    ├── app\
    │   ├── __init__.py
    │   ├── config.py
    │   ├── extensions.py
    │   ├── routes.py
    │   │
    │   ├── templates\
    │   │   └── login.html
    │   │
    │   └── static\
    │       ├── css\
    │       │   └── style.css
    │       │
    │       └── js\
    │           └── portal.js
    │
    └── logs\
        └── auth.log
```

The `auth.log` file is generated when the application runs and records authentication events.

It may not exist before the first application launch.

The `__pycache__` directory may also appear automatically after Python executes the modules. It contains generated bytecode and is not part of the source architecture.

## 8.1 Root-Level Files

### `.gitignore`

The repository uses `.gitignore` to prevent unnecessary or sensitive files from being committed.

Important exclusions include:

```gitignore
venv/
.venv/
__pycache__/
*.py[cod]
.env
.env.*
.vscode/
*.log
.DS_Store
Thumbs.db
```

The environment example file should be explicitly allowed if the `.env.*` pattern is retained:

```gitignore
!.env.example
```

This ensures that the example configuration can be committed without exposing the actual `.env` file.

### `.env`

The root `.env` file contains deployment-specific configuration and secrets.

It is not intended to be committed to Git.

### `v1/`

Contains the original proof-of-concept implementation.

Version 0.1 is preserved as a reference and should not be modified as part of the v0.2 freeze.

### `v2/`

Contains the modular implementation.

This directory is the primary source directory for PortalWiFi v0.2.

---

# 9. Application Components

This section explains the responsibility of every major Python and frontend file.

## 9.1 `run.py`

Location:

```text
G:\IntraHub\v2\run.py
```

Purpose:

This is the application's runtime entry point.

Current implementation:

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
```

### Explanation

`from app import create_app`

Imports the application factory.

`app = create_app()`

Creates and configures the Flask application.

`host="0.0.0.0"`

Makes Flask listen on all available IPv4 interfaces.

This is necessary because the wireless client accesses the application through the laptop's hotspot interface rather than only through localhost.

`port=8080`

Runs the application on TCP port 8080.

`debug=False`

Disables Flask debug mode.

Debug mode should not be enabled when the portal is accessible to other devices.

### Important distinction

Listening on `0.0.0.0` does not automatically make the application secure or publicly accessible.

The actual reachable interfaces depend on the operating system, firewall and network configuration.

---

## 9.2 `app/__init__.py`

Location:

```text
G:\IntraHub\v2\app\__init__.py
```

Purpose:

This file contains the Flask application factory.

The application factory is responsible for initializing the application and its extensions.

The current implementation performs the following operations:

1. Imports the required Flask components.
2. Creates a Flask application instance.
3. Loads configuration.
4. Checks that critical secrets are configured.
5. Creates the logging directory if necessary.
6. Initializes the authentication log handler.
7. Initializes CSRF protection.
8. Initializes rate limiting.
9. Registers the application blueprint.
10. Returns the configured Flask application.

### Application factory pattern

The application factory pattern separates application creation from application execution.

Instead of constructing the Flask application directly inside the routes module, the factory initializes the application centrally.

This becomes useful when introducing:

- Automated testing.
- Different configurations.
- Additional blueprints.
- Database extensions.
- Additional security components.
- Separate development and deployment environments.

### Configuration validation

The application explicitly checks for:

```python
SECRET_KEY
PORTAL_PASSWORD_HASH
```

If either value is missing, application startup is stopped with an error.

This prevents the application from silently running with an insecure default secret or missing authentication configuration.

### Logging implementation

The application uses:

```python
RotatingFileHandler
```

Current configuration:

| Parameter | Value |
|---|---|
| Log file | `logs/auth.log` |
| Maximum file size | 1,000,000 bytes |
| Backup files | 3 |
| Encoding | UTF-8 |
| Log level | INFO |

When the log file reaches its configured size, it is rotated and older log files are retained according to the backup count.

This prevents the authentication log from growing indefinitely.

---

## 9.3 `app/config.py`

Location:

```text
G:\IntraHub\v2\app\config.py
```

Purpose:

Centralizes application configuration.

It loads the root `.env` file and exposes the settings through a configuration class.

Current configuration fields:

| Setting | Purpose |
|---|---|
| `SECRET_KEY` | Signs Flask session data |
| `PORTAL_NAME` | Name displayed by the portal |
| `WELCOME_MESSAGE` | Welcome text displayed to users |
| `PORTAL_SSID` | Configured wireless network name |
| `PORTAL_PASSWORD_HASH` | Stored authentication password hash |
| `SESSION_COOKIE_HTTPONLY` | Restricts JavaScript access to the session cookie |
| `SESSION_COOKIE_SAMESITE` | Controls cross-site cookie behaviour |
| `SESSION_COOKIE_SECURE` | Controls whether cookies require HTTPS |
| `PERMANENT_SESSION_LIFETIME` | Sets the permanent session lifetime |
| `RATELIMIT_STORAGE_URI` | Configures rate-limit storage |
| `RATELIMIT_DEFAULT` | Defines a configured default rate-limit value |

### Session configuration

Current values:

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = 1800
```

The session lifetime is 1,800 seconds, or 30 minutes, for permanent sessions.

`HTTPONLY` helps prevent client-side JavaScript from reading the session cookie.

`SAMESITE=Lax` provides a baseline restriction on cross-site cookie transmission.

`SESSION_COOKIE_SECURE=False` is currently used because the prototype is accessed over local HTTP.

This is a development compromise, not a production recommendation.

For an HTTPS deployment, the secure cookie setting should be enabled.

---

## 9.4 `app/extensions.py`

Location:

```text
G:\IntraHub\v2\app\extensions.py
```

Purpose:

Defines the Flask extensions used by the application.

Current implementation:

```python
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)
```

### CSRFProtect

Initializes CSRF protection.

It is attached to the Flask application during application creation.

### Limiter

Creates the rate-limiting extension.

The key function is:

```python
get_remote_address
```

This identifies a client using its remote IP address.

The current rate-limiting storage is in-memory.

The extension is initialized centrally so that other routes can use the same limiter instance.

---

## 9.5 `app/routes.py`

Location:

```text
G:\IntraHub\v2\app\routes.py
```

Purpose:

Contains the portal's HTTP routes and authentication logic.

The application uses a Flask Blueprint named:

```python
portal_bp
```

A blueprint organizes related routes into a logical module.

### Route 1: `/`

Method:

```text
GET
```

Purpose:

Displays the portal interface.

The route retrieves:

- Portal name.
- Welcome message.
- Current authentication state.

It then renders:

```text
login.html
```

The authentication state is obtained from:

```python
session.get("authenticated", False)
```

This determines whether the portal should display the login interface or the authenticated-state interface.

### Route 2: `/login`

Method:

```text
POST
```

Purpose:

Processes login submissions.

The route is protected by:

```python
@limiter.limit("5 per minute")
```

The current authentication process is:

1. Retrieve the submitted password.
2. Retrieve the configured password hash.
3. Verify the submitted password using Werkzeug.
4. If verification succeeds, clear the previous session.
5. Set the authenticated session flag.
6. Mark the session as permanent.
7. Record a successful authentication event.
8. Display a success message.
9. Redirect to the portal page.

If verification fails:

1. Record an authentication failure.
2. Display an error message.
3. Redirect to the portal page.

The application does not store the original submitted password in the authentication log.

### Route 3: `/logout`

Method:

```text
POST
```

Purpose:

Terminates the current Flask session.

The route:

1. Clears the session.
2. Records a logout event.
3. Displays a disconnection message.
4. Redirects to the portal page.

Logout is implemented as a POST request and is protected by the application's CSRF middleware.

### Important implementation limitation

The `authenticated` session value is currently an application-level state.

It is not yet synchronized with a Windows network filtering rule.

Consequently, logging in or logging out does not currently change the client's actual internet forwarding permissions.

---

## 9.6 `app/templates/login.html`

Location:

```text
G:\IntraHub\v2\app\templates\login.html
```

Purpose:

Contains the HTML structure of the captive portal interface.

The template is responsible for rendering the portal based on the application state.

Its main responsibilities include:

- Displaying the portal name.
- Displaying the welcome message.
- Showing the login form.
- Showing the authenticated state.
- Displaying success and error notifications.
- Providing the logout form.
- Including CSRF tokens in POST forms.
- Loading the external CSS and JavaScript files.

### CSRF integration

The forms include CSRF tokens generated by Flask-WTF.

The token is submitted with the form and validated by the server.

This prevents the application from accepting state-changing form submissions without a valid CSRF token.

### Flash messages

The template displays application messages using Flask's flash-message mechanism.

These messages communicate outcomes such as:

- Successful authentication.
- Incorrect password.
- Successful disconnection.

---

## 9.7 `app/static/css/style.css`

Location:

```text
G:\IntraHub\v2\app\static\css\style.css
```

Purpose:

Controls the visual appearance of the portal.

The stylesheet provides:

- Dark blue visual styling.
- Login card layout.
- Form styling.
- Notification styling.
- Responsive layout behaviour.
- Mobile-friendly spacing and presentation.

Keeping CSS separate from the HTML allows the interface to evolve without modifying authentication logic.

---

## 9.8 `app/static/js/portal.js`

Location:

```text
G:\IntraHub\v2\app\static\js\portal.js
```

Purpose:

Implements client-side interactions.

The current JavaScript functionality includes:

- Password visibility toggle.
- Login form loading state.

JavaScript improves usability but does not replace server-side authentication.

The server remains responsible for validating credentials.

---

## 9.9 `requirements.txt`

Location:

```text
G:\IntraHub\v2\requirements.txt
```

Current contents:

```text
Flask>=3.1,<4.0
Flask-WTF>=1.2,<2.0
Flask-Limiter>=3.12,<5.0
python-dotenv>=1.1,<2.0
```

These entries specify the application's direct dependency requirements.

The actual installed environment also contains transitive dependencies such as Werkzeug, Jinja2, Click, itsdangerous and other packages.

The version ranges allow compatible updates within the specified major-version boundaries.

For reproducible deployments, a future release should consider maintaining a fully pinned dependency lock or requirements file.

---

# 10. Authentication Architecture

Authentication is one of the most important components of v0.2.

The original prototype used a comparatively basic password comparison.

Version 0.2 replaces that approach with password-hash verification.

## 10.1 Password Storage

The application does not need to store the original password.

Instead, it stores a password hash in the environment configuration.

The hash is generated using Werkzeug's password hashing utilities.

During login, the application uses:

```python
check_password_hash(password_hash, password)
```

The function checks whether the submitted password matches the stored hash.

### Why hashing matters

If an attacker obtains a properly generated password hash, the original password is not immediately exposed as plaintext.

However, password hashing does not make a weak password strong.

A sufficiently weak password may still be guessed or cracked offline.

The password must therefore be strong, and the hash must be protected.

## 10.2 Authentication Decision

The current authentication decision is based on a single configured portal password.

Conceptually:

```text
Submitted Password
        |
        v
Retrieve Stored Hash
        |
        v
Verify Password
        |
   +----+----+
   |         |
 Valid     Invalid
   |         |
   v         v
Set        Log Failure
Session       |
   |          |
   v          v
Success     Error
Message     Message
```

## 10.3 Current Authentication Model

The current implementation is a shared-password authentication model.

It does not yet provide:

- Individual user accounts.
- Usernames.
- Role-based access control.
- Per-device authorization records.
- Authentication history by user identity.
- Persistent device authorization.
- Device registration.

These features may be considered in later versions if required by the project scope.

---

# 11. Session Management

Version 0.2 uses Flask's session mechanism.

The session is used to remember whether the current browser has successfully authenticated.

## 11.1 Session State

The application uses the following session value:

```python
session["authenticated"] = True
```

The portal checks this value when rendering the main page.

If the value is missing or false, the application treats the browser as unauthenticated.

## 11.2 Successful Authentication

After a successful password check:

```python
session.clear()
session["authenticated"] = True
session.permanent = True
```

The existing session is cleared before the new authenticated state is created.

This helps avoid carrying forward unexpected previous session values.

## 11.3 Session Lifetime

The configured permanent session lifetime is:

```text
1800 seconds
```

Equivalent to:

```text
30 minutes
```

## 11.4 Logout

Logout clears the session:

```python
session.clear()
```

The browser is then returned to the unauthenticated portal interface.

## 11.5 What the Session Does Not Do

The Flask session is not a network authorization mechanism.

It does not:

- Change Windows Firewall rules.
- Add WFP filters.
- Modify Windows routing.
- Control NAT forwarding.
- Authorize a wireless adapter.
- Automatically identify a particular physical device.

This is one of the most important limitations to remember when moving to v0.3.

---

# 12. Security Implementation

Security was a major focus of version 0.2.

The application introduces several baseline controls.

## 12.1 Password Hashing

**Status: Implemented**

Passwords are verified against a stored hash using Werkzeug.

The original password is not intentionally stored in the authentication log.

## 12.2 CSRF Protection

**Status: Implemented**

Flask-WTF CSRF protection is initialized globally.

The login and logout forms include CSRF tokens.

The middleware validates state-changing requests.

## 12.3 Login Rate Limiting

**Status: Implemented**

The login route is restricted to:

```text
5 requests per minute
```

The rate limit is based on the remote IP address.

This helps reduce rapid automated login attempts.

The current implementation uses in-memory storage.

Therefore:

- Rate-limit state is not persistent.
- State is not shared across multiple application processes.
- Restarting the application resets the stored counters.

A shared storage backend should be considered before multi-worker deployment.

## 12.4 Secure Session Cookie Settings

**Status: Implemented**

Current settings include:

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
```

The secure-cookie option is currently disabled for the local HTTP prototype.

HTTPS should be introduced before using the application in a deployment where credentials and sessions are exposed to untrusted networks.

## 12.5 Secret Management

**Status: Implemented**

The application uses environment variables for:

- Flask's secret key.
- Portal password hash.
- Portal configuration.

The actual `.env` file is excluded from Git.

There are no hardcoded fallback secrets in the application factory.

## 12.6 Authentication Logging

**Status: Implemented**

The application records:

- Successful authentication.
- Failed authentication.
- Logout events.

The logs contain event information and the remote IP address.

They should not contain submitted passwords or secret keys.

## 12.7 Debug Mode

**Status: Disabled**

The runtime entry point uses:

```python
debug=False
```

This avoids exposing the Flask interactive debugger to connected devices.

## 12.8 Security Controls Summary

| Security control | Implementation |
|---|---|
| Password hashing | Werkzeug |
| Session management | Flask sessions |
| CSRF protection | Flask-WTF |
| Login rate limiting | Flask-Limiter |
| Secret configuration | Environment variables |
| Session cookie HttpOnly | Enabled |
| SameSite cookie policy | Lax |
| HTTPS-only cookie | Disabled for local HTTP |
| Authentication logging | Rotating file handler |
| Debug mode | Disabled |

---

# 13. Logging and Monitoring

Version 0.2 introduces authentication event logging.

## 13.1 Log Location

```text
G:\IntraHub\v2\logs\auth.log
```

## 13.2 Logged Events

The current application records three primary event categories.

| Event | Meaning |
|---|---|
| `authentication_success` | Password verification succeeded |
| `authentication_failure` | Password verification failed |
| `session_logout` | Browser session was cleared |

The records include the client's remote IP address.

## 13.3 Log Rotation

The application uses a rotating file handler.

Configuration:

```text
Maximum file size: 1 MB
Backup count: 3
Encoding: UTF-8
```

This prevents unlimited growth of a single log file.

## 13.4 Why Logging Matters

Authentication logs are useful for:

- Troubleshooting login problems.
- Identifying repeated authentication failures.
- Observing authentication activity.
- Understanding application behaviour.
- Supporting future security auditing.

## 13.5 Current Logging Limitations

The application does not yet maintain a structured database of clients or authentication sessions.

The log is not currently a complete security audit system.

It does not establish:

- A persistent device identity.
- A unique authorization record.
- A MAC-to-IP mapping.
- A network access grant.
- A complete session history.

These capabilities belong to future development.

---

# 14. Configuration Management

Version 0.2 uses a root-level `.env` file.

Location:

```text
G:\IntraHub\.env
```

The application configuration module resolves the project root and loads this file.

This is important because the application is launched from the `v2` directory but the configuration file is stored at the repository root.

## 14.1 Environment Variables

The current configuration includes:

```dotenv
SECRET_KEY=<generated-secret>
PORTAL_NAME=IntraHub
PORTAL_SSID=IntraHub-WiFi
WELCOME_MESSAGE=Welcome to IntraHub. Authenticate to continue.
PORTAL_PASSWORD_HASH=<generated-password-hash>
SESSION_COOKIE_SECURE=false
```

Replace the placeholders with actual values.

Do not copy real secret values into documentation, source control or public screenshots.

## 14.2 SECRET_KEY

The Flask secret key is used to sign session data and support other security-related Flask functionality.

It should be randomly generated.

It should not be committed to Git.

Changing this key invalidates existing signed session cookies.

## 14.3 PORTAL_NAME

Controls the name displayed in the portal interface.

## 14.4 PORTAL_SSID

Stores the intended wireless network name.

At this stage, this is configuration metadata.

It does not configure Windows Mobile Hotspot or change the actual wireless SSID.

## 14.5 WELCOME_MESSAGE

Controls the welcome text displayed on the portal.

## 14.6 PORTAL_PASSWORD_HASH

Contains the stored hash used for password verification.

The original password should not be stored in this variable.

## 14.7 SESSION_COOKIE_SECURE

Currently set to:

```dotenv
SESSION_COOKIE_SECURE=false
```

This is required for the present local HTTP testing arrangement.

For an HTTPS deployment, it should be set to:

```dotenv
SESSION_COOKIE_SECURE=true
```

The application must actually be served over HTTPS before enabling this setting.

## 14.8 `.env.example`

The repository includes:

```text
G:\IntraHub\v2\.env.example
```

This file serves as a configuration reference.

It should contain placeholder values, not real secrets.

Note that the application's current configuration loader reads the repository-root `.env`, not `v2/.env`.

The example file is documentation for the expected settings, not the active runtime configuration.

---

# 15. Application Execution

## 15.1 Starting the Application

Open Windows PowerShell.

Navigate to the project root:

```powershell
cd G:\IntraHub
```

Activate the shared virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Navigate to the v2 directory:

```powershell
cd .\v2
```

Start the application:

```powershell
python .\run.py
```

The application listens on:

```text
Port: 8080
Host: 0.0.0.0
```

## 15.2 Local Access

On the laptop, open:

```text
http://127.0.0.1:8080
```

## 15.3 Wireless Client Access

A wireless client can access the portal using the laptop's hotspot gateway address.

During the recorded test, the gateway was:

```text
192.168.137.1
```

Therefore, the portal URL was:

```text
http://192.168.137.1:8080
```

The address is specific to the tested Windows Mobile Hotspot configuration.

It should not be assumed to remain the same on every Windows installation.

## 15.4 Stopping the Application

Return to the PowerShell window running Flask.

Press:

```text
Ctrl + C
```

This stops the development server.

---

# 16. Installation and Setup

This section describes how to reproduce the v0.2 environment on the existing development machine.

## 16.1 Prerequisites

- Windows 11.
- Python 3.12 or a compatible supported version.
- Visual Studio Code or another editor.
- PowerShell.
- Git.
- Access to the IntraHub repository.

## 16.2 Install Dependencies

From the project root:

```powershell
cd G:\IntraHub
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the v2 dependencies:

```powershell
python -m pip install -r .\v2\requirements.txt
```

## 16.3 Verify Installation

Run:

```powershell
python --version
```

Then:

```powershell
python -m pip show Flask Flask-WTF Flask-Limiter python-dotenv Werkzeug
```

## 16.4 Configure Environment Variables

Ensure that the repository-root `.env` file exists.

It must contain valid values for:

- `SECRET_KEY`
- `PORTAL_PASSWORD_HASH`

It should also contain the portal display settings.

Never publish the actual secret values.

## 16.5 Start the Application

```powershell
cd G:\IntraHub\v2
python .\run.py
```

## 16.6 Verify Local Access

Open:

```text
http://127.0.0.1:8080
```

Confirm that:

- The page loads.
- CSS is applied.
- JavaScript loads.
- The login interface is visible.

## 16.7 Verify Wireless Access

Enable Windows Mobile Hotspot.

Connect a smartphone to the hotspot.

Determine the current hotspot gateway address and open:

```text
http://<HOTSPOT_GATEWAY_IP>:8080
```

---

# 17. Application Workflow

This section describes the actual application workflow in more detail.

## 17.1 Initial Page Load

The client requests:

```http
GET /
```

Flask invokes the `index()` route.

The route reads:

- `PORTAL_NAME`
- `WELCOME_MESSAGE`
- `session["authenticated"]`

It passes the resulting values to the HTML template.

The browser receives the portal interface.

## 17.2 Authentication Submission

The user enters a password and submits the login form.

The browser sends:

```http
POST /login
```

The form includes the CSRF token.

The request passes through the configured middleware and route-level rate limiter.

The application then checks the password against the stored hash.

## 17.3 Successful Authentication

When the password is correct:

```text
Password verification: SUCCESS
Session: Cleared and updated
Authenticated flag: True
Log event: authentication_success
Response: Redirect to /
```

The browser is then shown the authenticated-state interface.

## 17.4 Failed Authentication

When the password is incorrect:

```text
Password verification: FAILED
Log event: authentication_failure
Response: Redirect to /
```

The application displays an error notification.

## 17.5 Logout

The user submits the logout form.

The browser sends:

```http
POST /logout
```

The application clears the session and records the logout event.

The user returns to the unauthenticated interface.

## 17.6 Important Network Behaviour

Even after successful authentication, the smartphone's internet access is not currently controlled by the Flask session.

The authentication state only affects the web application.

This is expected behaviour in v0.2.

---

# 18. Testing and Validation

Testing was performed on the Windows 11 development machine.

The application was tested locally and through a smartphone connected to the laptop's Windows Mobile Hotspot.

## 18.1 Python Compilation

The application source was checked using:

```powershell
python -m compileall .\v2
```

The compilation check completed successfully.

This verifies that Python could compile the source files without syntax errors.

It does not prove that every runtime path or security control is correct.

## 18.2 Local HTTP Test

The application was started on port 8080.

The local portal was accessed through:

```text
http://127.0.0.1:8080
```

The application returned a successful HTTP response.

## 18.3 Static Resource Test

The browser successfully loaded:

- CSS stylesheet.
- JavaScript file.

A missing favicon request was observed during testing.

The favicon 404 was harmless and did not affect portal operation.

## 18.4 Authentication Tests

The following scenarios were tested:

| Test | Observed result |
|---|---|
| Open portal | Successful |
| Submit valid password | Successful |
| Submit incorrect password | Error notification |
| Logout | Successful |
| Access portal from smartphone | Successful |
| Load CSS on smartphone | Successful |
| Load JavaScript on smartphone | Successful |
| Submit login from smartphone | Successful |
| Submit logout from smartphone | Successful |

## 18.5 Mobile Hotspot Test

The laptop operated as a Windows Mobile Hotspot.

The smartphone connected to it and accessed the Flask application.

Recorded network information:

| Item | Recorded value |
|---|---|
| Hotspot gateway | `192.168.137.1` |
| Smartphone IP | `192.168.137.94` |
| Flask port | `8080` |
| Flask bind address | `0.0.0.0` |

These values represent the test environment at the time of testing, not permanent configuration.

## 18.6 Internet Access Test

An important test was performed to establish whether the Flask authentication state controlled actual internet access.

The following were observed:

- The smartphone could access external websites while connected to the hotspot.
- Logging out of the portal did not remove internet connectivity.
- Stopping the Flask application did not remove internet connectivity.

External connectivity was tested using services including Google, Wikipedia and Cloudflare.

This demonstrated that Windows Mobile Hotspot internet forwarding was operating independently of the Flask application.

**Conclusion:** The web portal was operational, but network-level access control had not yet been implemented.

This is not a failed authentication test. It identifies the boundary between the application layer and the network layer.

---

# 19. Network Environment

The initial prototype uses Windows 11 Mobile Hotspot.

## 19.1 Wireless Adapter

The development laptop uses:

- Qualcomm QCA9377 802.11ac wireless adapter.
- Recorded driver version: 12.0.0.1238.
- Driver date: 22 November 2021.

The adapter supports 2.4 GHz and 5 GHz wireless operation.

The legacy Windows Hosted Network feature was reported as unsupported.

## 19.2 Windows Mobile Hotspot

Because the legacy Hosted Network functionality was unavailable, Windows 11 Mobile Hotspot was used.

Windows Mobile Hotspot creates a Wi-Fi Direct virtual network interface.

Windows Internet Connection Sharing (ICS) provides the internet-sharing functionality.

## 19.3 Recorded Interface Information

During the initial network investigation:

| Interface | Recorded information |
|---|---|
| Upstream Wi-Fi | `10.70.120.32` |
| Hotspot gateway | `192.168.137.1` |
| Hotspot interface alias | `Local Area Connection* 2` |
| Smartphone client | `192.168.137.94` |
| VirtualBox Host-Only | `192.168.56.1` |

These values may change after network reconfiguration or restarting Mobile Hotspot.

The actual adapter interface index must be discovered dynamically rather than hardcoded.

## 19.4 Firewall Configuration

An inbound Windows Firewall rule was created for the Flask prototype.

The rule allowed:

```text
Direction: Inbound
Protocol: TCP
Local port: 8080
Action: Allow
Profile: Any
Remote address: 192.168.137.0/24
```

Its purpose was to allow wireless clients on the hotspot subnet to reach the portal application.

This rule does not block or control internet forwarding.

It only permits access to the specified application port under the configured conditions.

---

# 20. What Works and What Does Not

This is the most important operational summary of version 0.2.

## 20.1 Confirmed Functionality

- Flask application starts successfully.
- The application loads configuration from the root `.env`.
- Missing critical configuration causes startup failure.
- The application renders the portal interface.
- CSS and JavaScript load.
- Password verification uses a stored hash.
- Valid credentials update the Flask session.
- Invalid credentials produce an error message.
- Logout clears the session.
- CSRF protection is enabled.
- Login rate limiting is configured.
- Authentication events are logged.
- Logs use rotating file storage.
- The portal can be accessed from a smartphone connected to the laptop hotspot.

## 20.2 Functionality Not Yet Implemented

- Internet access blocking for unauthenticated devices.
- Internet access granting after successful authentication.
- Automatic captive portal detection.
- Automatic browser redirection.
- Device registration.
- Persistent client authorization records.
- IP-to-device authorization mapping.
- WFP integration.
- IPv4 network enforcement.
- IPv6 network enforcement.
- Dynamic network filter creation.
- Dynamic network filter removal.

## 20.3 Why This Distinction Matters

A conventional login application and a captive network access-control system are not the same thing.

A login application can identify whether a browser has authenticated.

A network enforcement system must independently determine whether packets from a particular wireless client should be forwarded.

The two systems must eventually communicate with each other.

Version 0.2 implements the application side.

Version 0.3 will begin implementing the network enforcement side.

---

# 21. Known Limitations

The following limitations are known and should remain documented.

## 21.1 No Network-Level Enforcement

The biggest limitation is that authentication does not control the actual network forwarding path.

The Windows Mobile Hotspot and ICS continue to forward traffic independently of the Flask session.

## 21.2 No Automatic Captive Portal Detection

Users currently need to open the portal URL manually.

The application does not yet implement the mechanisms required for automatic captive portal detection by operating systems.

## 21.3 Application-Level Sessions Only

Authentication is stored in a Flask browser session.

The application does not yet maintain a separate authorization record for each wireless client.

## 21.4 In-Memory Rate Limiting

The current rate limiter uses memory storage.

This is adequate for the present single-process prototype, but it is not suitable for reliable shared rate limiting across multiple application workers.

## 21.5 HTTP Deployment

The prototype is accessed through HTTP.

Credentials and session-related traffic are therefore not protected by TLS in the current test arrangement.

This must be addressed before exposing the system to an untrusted production environment.

## 21.6 Shared Password Model

The current implementation uses a shared portal password.

There is no individual identity or per-user account management.

## 21.7 Windows-Specific Network Integration Not Implemented

The application does not yet interact with:

- Windows Filtering Platform.
- Windows Base Filtering Engine.
- Windows network forwarding APIs.
- Windows service management.
- Network interface authorization policies.

These are future integration responsibilities.

---

# 22. Security Considerations

Version 0.2 introduces several security controls, but it should still be treated as a development prototype.

## 22.1 Do Not Commit Secrets

Never commit:

- `.env`
- Actual Flask secret keys.
- Actual password hashes.
- Credentials.
- Private deployment configuration.

A password hash is not the original password, but it is still sensitive authentication material.

## 22.2 Do Not Use the Development Server in Production

Flask's built-in development server is being used for the prototype.

The warning displayed by Flask is expected.

A production deployment requires an appropriate production WSGI server and deployment configuration.

## 22.3 Use HTTPS

Before production use:

- Configure HTTPS.
- Enable secure session cookies.
- Protect credentials in transit.
- Review certificate management.
- Review trusted proxy configuration if a reverse proxy is introduced.

## 22.4 Review Rate-Limit Storage

The in-memory rate-limit backend must be replaced with a suitable shared backend if the application is deployed using multiple processes or workers.

## 22.5 Do Not Run Flask as Administrator

The Flask application should remain an unprivileged process.

Future Windows network enforcement will require privileged operations.

Those operations should be separated into a dedicated controller or service.

Running the entire web application with administrative privileges would unnecessarily increase the impact of an application compromise.

## 22.6 Protect Authentication Logs

Authentication logs can contain IP addresses and information about user activity.

They should be protected from unauthorized access.

They should not contain passwords, secret keys or other sensitive authentication material.

## 22.7 IPv6 Must Be Considered

Future network restrictions must account for IPv6.

Implementing only IPv4 blocking could leave an alternative network path available if IPv6 forwarding is enabled.

---

# 23. Important Architectural Decisions

Several decisions made during v0.2 will influence future versions.

## 23.1 Preserve v0.1

The original implementation remains untouched.

This preserves a working proof of concept and allows comparison between versions.

## 23.2 Use a Modular Flask Architecture

Application initialization, configuration, routes, templates and static assets are separated.

This improves maintainability and makes it easier to add future components.

## 23.3 Use an Application Factory

The application factory centralizes initialization.

It also provides a useful foundation for future automated testing.

## 23.4 Separate Web Authentication from Network Enforcement

The Flask application is responsible for authentication and application state.

A separate network enforcement component will be responsible for controlling packet forwarding.

This separation avoids giving the web application unnecessary operating-system privileges.

## 23.5 Use Windows Filtering Platform for Future Enforcement

The planned network enforcement mechanism is Windows Filtering Platform (WFP).

WFP provides Windows APIs for managing packet filtering policies.

The proposed implementation will use the user-mode WFP management APIs for basic filtering.

A custom kernel callout driver is not currently required for the intended initial prototype.

## 23.6 Use a Dynamic WFP Session

The proposed first WFP prototype will use a dynamic filtering session.

WFP objects associated with a dynamic session are automatically removed when that session ends.

This is useful during development because an unexpected controller shutdown should not leave permanent filtering rules behind.

## 23.7 Keep the Network Controller Separate

The intended future design is:

```text
                  Wireless Client
                         |
                         v
                  Windows Hotspot
                         |
                         v
                 Windows Network Stack
                         |
                         v
                    WFP Filters
                         |
                         v
                   Internet Access


                 Flask Portal
                      |
                      v
               Authentication
                      |
                      v
              Authorization State
                      |
                      v
              Restricted Local IPC
                      |
                      v
              WFP Controller
                      |
                      v
                WFP Management API
```

This is a planned architecture, not a feature implemented in v0.2.

---

# 24. Version 0.1 vs Version 0.2

| Feature | v0.1 | v0.2 |
|---|---|---|
| Flask application | Yes | Yes |
| Modular structure | No | Yes |
| Dedicated templates | No | Yes |
| Dedicated CSS | No | Yes |
| Dedicated JavaScript | No | Yes |
| Environment configuration | Basic | Centralized |
| Password verification | Basic comparison | Password hash verification |
| Session management | No proper session workflow | Yes |
| CSRF protection | No | Yes |
| Login rate limiting | No | Yes |
| Authentication logging | Limited | Yes |
| Log rotation | No | Yes |
| Mobile interface | Basic | Improved |
| Smartphone testing | Yes | Yes |
| Network enforcement | No | No |

Version 0.2 is an architectural and security improvement over v0.1.

It is not yet a network access-control release.

---

# 25. Version 0.3 Development Plan

**Proposed version name: Network Enforcement Layer**

Version 0.3 will focus on integrating the application with Windows network filtering.

This is the next major engineering challenge.

## 25.1 Primary Objective

When a wireless client connects to the hotspot:

- Unauthenticated client traffic should be blocked from reaching external networks.
- The client should retain access to the portal hosted on the laptop.
- Successful authentication should authorize the appropriate client.
- The WFP controller should apply the required network filtering policy.
- Logout or revocation should remove the client's authorization.

## 25.2 Why Windows Filtering Platform?

The current network-sharing implementation uses Windows Mobile Hotspot and ICS.

The application must therefore control the forwarding path rather than simply control its own HTTP routes.

WFP provides filtering capabilities within the Windows networking stack.

The planned prototype will investigate the IPv4 forwarding layer:

```text
FWPM_LAYER_IPFORWARD_V4
```

This layer is relevant because the initial target is traffic being forwarded through the laptop.

## 25.3 Proposed v0.3 Architecture

The future design will contain two independently running components.

### Component A: Flask Portal

Responsibilities:

- Display the portal.
- Receive authentication requests.
- Verify credentials.
- Maintain application sessions.
- Determine whether a client should be authorized.
- Send authorization changes to the controller.

### Component B: WFP Controller

Responsibilities:

- Open a WFP engine session.
- Identify the hotspot interface.
- Install filtering rules.
- Block unauthorized forwarded traffic.
- Permit authorized client traffic.
- Revoke authorization.
- Report controller status.
- Clean up dynamic filters when the controller exits.

The controller will require elevated privileges.

The Flask process will not.

## 25.4 Initial WFP Prototype Scope

The first WFP prototype should be deliberately small.

It should provide commands or operations equivalent to:

```text
block
allow-client
revoke-client
status
clear
```

These are conceptual operations for the controller.

They are not currently implemented commands in the v0.2 application.

The first tests should use the actual hotspot interface and a known test client.

## 25.5 Interface Identification

The controller must identify the correct network interface dynamically.

It must not assume that:

```text
Local Area Connection* 2
```

will always be the hotspot interface.

Interface names and indexes may change.

The controller should inspect:

- Interface index.
- Interface description.
- Interface state.
- IPv4 address.
- IPv6 addresses.
- Forwarding configuration.

## 25.6 Filtering Strategy

The initial design will investigate:

1. Identifying forwarded traffic received from the hotspot interface.
2. Applying a default block policy to unauthorized hotspot clients.
3. Adding a more specific permit policy for authorized client addresses.
4. Ensuring the laptop's own host-bound portal traffic remains accessible.
5. Testing the actual interaction with ICS and NAT.

Filter precedence and WFP arbitration must be implemented and verified carefully.

The system must not accidentally block:

- The laptop's own internet traffic.
- Traffic required for the portal.
- The upstream network interface.
- Other unrelated network adapters.

## 25.7 IPv4 and IPv6

The first enforcement prototype may begin with IPv4.

However, IPv6 must be inspected and accounted for before claiming complete access control.

An IPv4-only policy must not be presented as complete network isolation if IPv6 forwarding remains possible.

## 25.8 Communication Between Flask and WFP

The proposed integration will use a restricted local communication mechanism, likely a Windows named pipe.

The purpose is to allow the Flask application to request authorization changes without running Flask as Administrator.

The communication mechanism must authenticate or restrict its client and validate requests.

## 25.9 Testing Requirements

Version 0.3 should not be considered complete until the following behaviours are demonstrated:

| Test | Expected behaviour |
|---|---|
| Unauthenticated client | External forwarding blocked |
| Portal access | Still available |
| Successful login | Client becomes authorized |
| Authorized client | External forwarding permitted |
| Logout | Authorization revoked |
| Controller shutdown | Dynamic WFP rules cleaned up |
| Unrelated host traffic | Unaffected |
| Upstream connection | Unaffected |
| IPv6 | No unintended bypass |
| Hotspot restart | Interface and filtering state handled correctly |

---

# 26. Long-Term Roadmap

The following roadmap is a planning reference. It does not mean these features are already implemented.

| Version | Name | Main objective |
|---|---|---|
| v0.1 | Initial Prototype | Prove basic portal connectivity |
| v0.2 | Modular Portal Architecture | Secure and organize the web application |
| v0.3 | Network Enforcement | Integrate WFP |
| v0.4 | Captive Portal Integration | Improve client detection and onboarding |
| v0.5 | Client Management | Maintain device authorization records |
| v0.6 | Administrative Interface | Manage clients and portal configuration |
| v0.7 | Monitoring and Audit | Improve network and security visibility |
| v1.0 | Integrated Prototype | Deliver an integrated captive network access-control system |

The final scope should be determined by actual requirements and testing rather than by version numbers alone.

---

# 27. Git and Version Control

The project is maintained in the GitHub repository:

```text
https://github.com/saaswatt/IntraHub.git
```

The repository contains the IntraHub project, including the preserved v1 and the newer v2 implementation.

## 27.1 Important Git Practices

Before committing:

- Verify that `.env` is ignored.
- Verify that the virtual environment is ignored.
- Verify that logs are ignored.
- Verify that generated Python bytecode is ignored.
- Ensure `.env.example` remains trackable.
- Do not commit credentials or private configuration.

## 27.2 Check Git Status

From the repository root:

```powershell
cd G:\IntraHub
git status
```

## 27.3 Review Files Before Committing

```powershell
git diff --stat
git diff -- .gitignore
```

Review the staged files as well before committing.

## 27.4 Commit v0.2

After the README and source files have been reviewed:

```powershell
git add .gitignore v2
git status
```

Check that no secret files or runtime logs are staged.

Then:

```powershell
git commit -m "Finalize PortalWiFi v0.2 modular portal"
```

## 27.5 Create a Version Tag

After verifying the commit:

```powershell
git tag -a v0.2.0 -m "PortalWiFi v0.2 - Modular Portal Architecture"
```

Verify:

```powershell
git tag
```

## 27.6 Push the Version

```powershell
git push origin main
git push origin v0.2.0
```

Use the repository's actual current branch if it is not named `main`.

## 27.7 Freeze v0.2

After tagging:

- Treat v0.2 as the stable application-layer baseline.
- Do not introduce new network enforcement features into v0.2.
- Develop WFP integration independently for v0.3.
- Preserve the ability to return to the tagged release.

---

# 28. Troubleshooting

## 28.1 Application Fails to Start

Possible cause:

Missing environment configuration.

Check:

```text
G:\IntraHub\.env
```

Ensure that both `SECRET_KEY` and `PORTAL_PASSWORD_HASH` are configured.

## 28.2 Flask Cannot Import a Package

Possible cause:

The virtual environment is not active or the required package is missing.

Activate the environment:

```powershell
cd G:\IntraHub
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r .\v2\requirements.txt
```

## 28.3 Smartphone Cannot Access the Portal

Check:

1. Is Windows Mobile Hotspot enabled?
2. Is the smartphone connected to the hotspot?
3. Is Flask running?
4. Is Flask listening on `0.0.0.0`?
5. Is the smartphone using the correct gateway address?
6. Is the Windows Firewall rule allowing TCP port 8080?
7. Is the laptop and smartphone still using the expected hotspot subnet?

The hotspot gateway address may change.

Do not assume it is always `192.168.137.1`.

## 28.4 Portal Loads Without Styling

Check that the browser can retrieve the CSS file.

Inspect the browser's developer tools and Flask request logs.

Verify:

```text
app/static/css/style.css
```

## 28.5 Login Always Fails

Possible causes:

- Incorrect password.
- Wrong stored password hash.
- Incorrect `.env` file.
- Application started with unexpected configuration.
- Hash value was copied incorrectly.

The active configuration is loaded from the repository-root `.env`.

Do not paste actual secrets into public troubleshooting messages.

## 28.6 CSRF Error

Check:

- The form contains the CSRF token.
- The request is submitted using POST.
- The browser is retaining the required session cookie.
- The session secret is correctly configured.

## 28.7 Rate Limit Reached

The login route currently allows five requests per minute per remote IP address.

If the limit is reached, the request may be rejected until the rate-limit window permits further attempts.

The current in-memory rate-limit state resets when the application process restarts.

Restarting should not be treated as a production security workaround.

## 28.8 Internet Still Works After Logout

This is expected in v0.2.

The application does not yet control network forwarding.

Windows Mobile Hotspot and ICS continue to provide internet connectivity independently of the Flask session.

Network enforcement is planned for v0.3.

---

# 29. Final Project Status

## 29.1 Version 0.2 Completion Summary

PortalWiFi v0.2 successfully establishes a modular, security-conscious Flask application that can be accessed from both the development laptop and a smartphone connected to the laptop's Windows Mobile Hotspot.

It introduces:

- Modular Flask architecture.
- Centralized configuration.
- Environment-based secret management.
- Password hash verification.
- Flask session management.
- CSRF protection.
- Login rate limiting.
- Rotating authentication logs.
- Responsive frontend resources.
- Successful local and wireless-client testing.

## 29.2 What Has Been Proven

The following technical points have been demonstrated:

1. A Windows 11 laptop can host the Flask portal.
2. The portal can listen on the laptop's wireless hotspot interface.
3. A connected smartphone can access the portal.
4. The authentication application can process valid and invalid submissions.
5. Flask sessions can represent browser authentication state.
6. The application can record authentication events.
7. The portal remains operational independently of the laptop's normal upstream Wi-Fi interface.

## 29.3 What Has Not Been Proven

The following are not yet demonstrated:

1. Unauthenticated wireless clients can be prevented from accessing the internet.
2. Authenticated clients can be selectively permitted through the Windows forwarding path.
3. Logout can revoke network access.
4. Automatic captive portal detection works.
5. IPv4 and IPv6 forwarding are both correctly controlled.
6. The application and a privileged network controller can communicate securely.

These are the central engineering objectives of the next phase.

## 29.4 Release Decision

**PortalWiFi v0.2 — Modular Portal Architecture**

Status: Ready for final documentation, Git review and version freeze.

Recommended release tag:

```text
v0.2.0
```

The next development milestone is:

```text
PortalWiFi v0.3 — Network Enforcement Layer
```

---

# 30. Development Notes and Lessons Learned

This section records the most important engineering lessons from the development of v0.2.

## 30.1 A Web Login Is Not Network Authentication

The most important discovery was that successful web authentication does not automatically change the network permissions of the device.

The application and the operating system's network forwarding mechanism operate at different layers.

They must be integrated explicitly.

## 30.2 Windows Mobile Hotspot Uses a Separate Networking Mechanism

The Flask application can communicate with devices connected to the hotspot, but Windows Mobile Hotspot and ICS independently manage internet sharing.

Stopping Flask does not stop the hotspot's forwarding behaviour.

## 30.3 Application Architecture Should Be Modular Before It Becomes Complex

The transition from a single-file prototype to a modular application made it easier to reason about configuration, authentication, presentation and security independently.

This will be particularly valuable when the network enforcement component is introduced.

## 30.4 Privileges Should Be Separated

The Flask application should not need administrator privileges just because the future network controller does.

Keeping privileged network operations in a separate component reduces the attack surface and makes the system easier to manage.

## 30.5 Network Interface Details Must Be Discovered, Not Assumed

Windows interface names and indexes may change.

Future enforcement code must identify the correct hotspot interface at runtime.

## 30.6 Security Must Be Evaluated at Multiple Layers

Password hashing, CSRF protection, session security and rate limiting protect the application.

They do not automatically protect the network forwarding path.

A complete captive access-control system needs both application security and network enforcement.

---

# End of PortalWiFi v0.2 Documentation

**Project:** IntraHub  
**Component:** PortalWiFi  
**Version:** 0.2.0  
**Release milestone:** Modular Portal Architecture  
**Next milestone:** v0.3 — Network Enforcement Layer

This document describes the implementation and observed behaviour of PortalWiFi v0.2 as of 31 October 2026. Planned features are explicitly identified as future work and should not be interpreted as existing functionality.