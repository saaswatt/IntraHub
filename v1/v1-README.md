# PortalWiFi
### Windows-Based Wi-Fi Captive Portal & Internet Access Management System

**Project Version:** 0.1 — Initial Working Prototype  
**Development Status:** Active Development  
**Platform:** Windows 11  
**Primary Language:** Python  
**Backend Framework:** Flask  
**Development Environment:** Visual Studio Code  
**Documentation Date:** 31 October 2026

---

## 1. Project Overview

PortalWiFi is a Windows-based Wi-Fi captive portal management system designed to provide a customizable authentication interface for users connecting to a computer-hosted wireless network.

The primary objective is to transform an ordinary Wi-Fi hotspot into a managed network access environment where connecting users are presented with a customized welcome and authentication page before receiving internet access.

Instead of relying entirely on the default Wi-Fi connection experience, PortalWiFi aims to introduce a dedicated authentication layer that allows the hotspot administrator to customize the network's identity, display welcome messages, authenticate users and manage their internet access.

The software is being developed using Python and Windows networking capabilities, with Flask serving as the initial web server.

### 1.1 Problem Statement

Conventional Windows Wi-Fi hotspot functionality provides basic internet sharing. However, it does not offer the level of customization and authentication management required for a personalized captive portal experience.

For example, a person sharing their internet connection may want to:

- Display a customized welcome message.
- Present a branded login interface.
- Require a separate access password through a browser.
- Control which connected devices receive internet access.
- Monitor connected clients.
- Manage access without requiring users to install a separate application.

PortalWiFi aims to address these requirements through a locally hosted web interface and a network access management layer.

### 1.2 Project Objectives

The primary objectives are:

1. Create and manage a Wi-Fi hotspot from a Windows computer.
2. Host a custom captive portal locally.
3. Allow connected smartphones and other devices to access the portal through a browser.
4. Implement password-based authentication.
5. Associate authenticated users with their connecting network devices.
6. Restrict internet access for unauthenticated clients.
7. Provide an interface for managing hotspot settings and connected devices.
8. Maintain logs of authentication and network activity.

---

## 2. Current Development Status

PortalWiFi has successfully completed its initial proof-of-concept implementation.

The current prototype demonstrates that a Windows 11 computer can share an internet connection through its Wi-Fi adapter while simultaneously hosting a Flask-based authentication interface accessible from a separate smartphone.

### 2.1 Implemented and Tested Components

| Component | Status | Description |
|---|---|---|
| Windows Mobile Hotspot | Implemented and tested | Creates a wireless access point. |
| Internet Connection Sharing | Tested through Mobile Hotspot | Shares the laptop's existing internet connection. |
| Smartphone connectivity | Tested | External devices can connect to the hotspot. |
| Client IP identification | Tested | Windows displays connected clients and their IP addresses. |
| Client MAC identification | Tested | Windows displays the MAC address of connected clients. |
| Flask web server | Implemented and tested | Hosts the authentication interface. |
| Mobile login interface | Implemented and tested | Displays the portal on a smartphone. |
| Password validation | Implemented and tested | Compares submitted passwords against the configured password. |
| Windows Firewall configuration | Implemented and tested | Allows inbound TCP connections to port 8080 from the hotspot subnet. |

### 2.2 Features Not Yet Implemented

The following functionality remains under development:

- Automatic captive portal detection.
- Automatic opening of the login page after connecting.
- Network-level authentication.
- Blocking internet access for unauthenticated devices.
- Per-device authorization.
- Session management.
- Authentication event logging.
- Desktop management dashboard.
- Hotspot configuration through the application.

**Important:** The current prototype validates passwords at the application level only. Successfully entering the password does not currently grant or revoke actual internet access.

---

## 3. Development Environment

The initial implementation was developed and tested using the following environment.

### 3.1 Hardware

| Component | Specification |
|---|---|
| Computer | Windows 11 laptop |
| Wireless adapter | Qualcomm QCA9377 802.11ac Wireless Adapter |
| Wireless adapter manufacturer | Qualcomm Communications Inc. |
| Driver provider | Qualcomm Communications Inc. |
| Driver version | 12.0.0.1238 |
| Driver date | 22 November 2021 |
| Supported wireless bands | 2.4 GHz and 5 GHz |
| Wireless standards | 802.11a/b/g/n/ac |

### 3.2 Software

| Software | Purpose |
|---|---|
| Windows 11 | Host operating system |
| Python | Application development |
| Flask | Web application framework |
| PowerShell | Windows networking and firewall management |
| Visual Studio Code | Development environment |
| Python venv | Dependency isolation |

### 3.3 Python Dependencies

Currently, the prototype requires:

- Flask

The application runs inside a Python virtual environment to maintain dependency isolation.

---

## 4. Network Architecture

PortalWiFi currently relies on Windows Mobile Hotspot functionality.

Windows handles the wireless access point, IP address allocation and internet sharing. Flask independently hosts the web interface.

### 4.1 Current Network Architecture

```text
                 INTERNET
                    |
                    |
          Existing Wi-Fi Network
                    |
                    |
             WINDOWS 11 LAPTOP
                    |
          Qualcomm QCA9377 Adapter
                    |
                    |
          WINDOWS MOBILE HOTSPOT
                    |
                    |
          192.168.137.1
          Hotspot Gateway
                    |
                    |
             SMARTPHONE
          192.168.137.94
                    |
                    |
             WEB BROWSER
                    |
                    |
          HTTP PORTAL REQUEST
                    |
                    |
             FLASK SERVER
              PORT 8080
                    |
                    |
          PASSWORD VALIDATION
```

### 4.2 Network Interfaces Identified

The following IPv4 interfaces were identified during development.

| Interface | IPv4 Address | Purpose |
|---|---|---|
| Ethernet 4 | 192.168.56.1 | VirtualBox Host-Only network |
| Local Area Connection* 2 | 192.168.137.1 | Windows Wi-Fi Direct virtual interface used by the hotspot |
| Wi-Fi | 10.70.120.32 | Existing internet-facing Wi-Fi connection |

The hotspot gateway address was identified as:

**192.168.137.1**

The smartphone received the following address during testing:

**192.168.137.94**

The smartphone successfully accessed the Flask server through the hotspot gateway.

### 4.3 Understanding the Flask Binding Address

The Flask application is configured to listen on:

```python
app.run(
    host="0.0.0.0",
    port=8080,
    debug=False
)
```

The address `0.0.0.0` instructs Flask to listen on all available IPv4 network interfaces.

Consequently, the server can receive requests through the hotspot interface even though its startup output displays other interface addresses, such as:

```text
Running on http://127.0.0.1:8080
Running on http://10.70.120.32:8080
```

The smartphone accesses the application using:

```text
http://192.168.137.1:8080
```

This behavior was successfully tested.

---

## 5. Windows Hotspot Configuration

### 5.1 Initial Hardware Compatibility Test

The wireless adapter was inspected using:

```powershell
netsh wlan show drivers
```

The output identified:

```text
Interface name: Wi-Fi

Driver:
Qualcomm QCA9377 802.11ac Wireless Adapter

Hosted network supported: No
```

The adapter does not support the legacy Windows Hosted Network functionality.

The following command was also executed:

```powershell
netsh wlan show hostednetwork
```

The result showed:

```text
Hosted network settings

Mode: Allowed
Settings: <Not configured>

Hosted network status

Status: Not available
```

### 5.2 Selected Implementation

Instead of relying on the legacy Hosted Network functionality, Windows 11 Mobile Hotspot was used.

Configuration steps:

1. Open Windows Settings.
2. Navigate to Network & Internet.
3. Open Mobile Hotspot.
4. Select Wi-Fi as the internet connection source.
5. Select Wi-Fi as the sharing method.
6. Configure a temporary network name and password.
7. Enable Mobile Hotspot.

### 5.3 Successful Connectivity Test

The hotspot was successfully started.

A separate smartphone was able to:

- Discover the wireless network.
- Connect using the configured Wi-Fi password.
- Receive an IP address.
- Access the internet through the laptop.
- Appear in Windows Mobile Hotspot's connected-device list.

Windows displayed both the connected smartphone's IP address and MAC address.

This established that the host computer could successfully share its internet connection with an external device.

### 5.4 Important Architectural Limitation

Windows Mobile Hotspot currently uses its own Wi-Fi security configuration.

The desired final experience is:

```text
Discover Wi-Fi
      |
      v
Connect to open wireless network
      |
      v
Automatically open captive portal
      |
      v
Enter portal password
      |
      v
Authenticate
      |
      v
Receive internet access
```

However, the current Windows Mobile Hotspot configuration requires a Wi-Fi password before a device can join.

This means the existing implementation does not yet provide the exact desired user experience.

The feasibility of using a different access point implementation or a separate networking component must be investigated.

---

## 6. Project Structure

The current implementation is a proof of concept.

### 6.1 Current Project Structure

```text
IntraHub/
│
├── venv/
│
├── app.py
│
└── [other existing project files]
```

The current Flask implementation is contained in `app.py`.

The virtual environment contains the installed Python dependencies.

### 6.2 Planned Modular Architecture

The following structure is proposed for a future version. It has not yet been implemented.

```text
PortalWiFi/
│
├── main.py
├── requirements.txt
│
├── application/
│   ├── dashboard.py
│   ├── settings.py
│   └── client_manager.py
│
├── hotspot/
│   ├── controller.py
│   ├── adapter.py
│   └── connection.py
│
├── portal/
│   ├── server.py
│   ├── authentication.py
│   ├── redirect.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   └── success.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       ├── js/
│       │   └── portal.js
│       │
│       └── images/
│
├── network/
│   ├── dhcp.py
│   ├── dns.py
│   ├── firewall.py
│   └── traffic_filter.py
│
├── database/
│   ├── db.py
│   └── models.py
│
├── logs/
│
└── config/
    └── settings.json
```

The purpose of this architecture is to separate the user interface, authentication, hotspot management, network filtering and database functionality.

---

## 7. Flask Captive Portal Implementation

### 7.1 Application Overview

The initial Flask application provides a basic password-protected web interface.

The application:

1. Listens on all IPv4 interfaces.
2. Uses TCP port 8080.
3. Serves the login page through the root endpoint.
4. Accepts password submissions using HTTP POST.
5. Compares the submitted password with the configured environment variable.
6. Displays a success or failure message.

### 7.2 Application Configuration

The password is supplied through an environment variable.

PowerShell command:

```powershell
$env:PORTAL_PASSWORD='YourTemporaryPassword'
```

The application also contains a development fallback password if the environment variable is absent.

The fallback must be removed before any deployment beyond local testing.

### 7.3 Application Endpoint

The current application exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Display the login page |
| POST | `/` | Submit and validate the password |

### 7.4 Authentication Logic

The current authentication logic follows this structure:

```python
if request.method == "POST":

    password = request.form.get("password", "")

    if password == PORTAL_PASSWORD:
        message = "Authentication successful!"

    else:
        message = "Incorrect password. Try again."
```

This implementation performs a direct string comparison.

It is sufficient for demonstrating basic password validation but is not suitable as a production authentication mechanism.

### 7.5 Login Interface

The current login page uses HTML and embedded CSS.

Its interface contains:

- Wi-Fi symbol.
- Welcome heading.
- Custom welcome message.
- Network branding.
- Password input field.
- Authentication button.
- Success or failure message.
- Footer branding.

The page is responsive and was tested using a smartphone browser.

### 7.6 Current Authentication Limitation

The application currently displays an authentication success message but does not establish an authorized network session.

There is no connection between the Flask password-validation result and Windows' internet-sharing or firewall authorization mechanisms.

Therefore:

**A user can currently access the internet even without authenticating through the portal, provided they have already connected to the Windows hotspot.**

This is an expected limitation of the initial proof of concept.

---

## 8. Python Environment Setup

### 8.1 Create a Virtual Environment

From the project directory:

```powershell
python -m venv venv
```

### 8.2 Activate the Environment

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should display:

```text
(venv) PS G:\IntraHub>
```

### 8.3 Install Flask

```powershell
python -m pip install flask
```

### 8.4 Verify Installation

```powershell
python -m pip show flask
```

### 8.5 Dependency Management

Save the installed dependencies:

```powershell
pip freeze > requirements.txt
```

Install dependencies on another environment using:

```powershell
pip install -r requirements.txt
```

### 8.6 VS Code Interpreter Configuration

The Python interpreter must point to the project's virtual environment.

Expected interpreter path:

```text
G:\IntraHub\venv\Scripts\python.exe
```

In Visual Studio Code:

1. Press `Ctrl + Shift + P`.
2. Select Python: Select Interpreter.
3. Choose the project's virtual environment.
4. Reload the VS Code window if necessary.

This also resolves common Pylance import errors caused by interpreter mismatches.

---

## 9. Windows Firewall Configuration

The Flask server must accept inbound connections from devices connected to the hotspot.

A Windows Firewall inbound rule was created.

### 9.1 Firewall Rule

The following command was executed in an elevated PowerShell session:

```powershell
New-NetFirewallRule `
    -DisplayName "PortalWiFi Prototype" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 8080 `
    -Action Allow `
    -Profile Any `
    -RemoteAddress 192.168.137.0/24
```

### 9.2 Firewall Configuration Details

| Property | Value |
|---|---|
| Display Name | PortalWiFi Prototype |
| Direction | Inbound |
| Protocol | TCP |
| Local Port | 8080 |
| Action | Allow |
| Profile | Any |
| Remote Address | 192.168.137.0/24 |
| Enabled | True |

### 9.3 Verify Firewall Rule

```powershell
Get-NetFirewallRule -DisplayName "PortalWiFi Prototype"
```

The rule was successfully created and verified.

The returned status was:

```text
PrimaryStatus: OK

Status:
The rule was parsed successfully from the store.
```

### 9.4 Administrative Permissions

Creating Windows Firewall rules requires elevated permissions.

When the command was initially executed from a non-administrative VS Code terminal, Windows returned:

```text
New-NetFirewallRule : Access is denied.
```

The issue was resolved by launching VS Code with Administrator privileges.

Once the firewall rule was created, the Flask application could be run from a normal, non-elevated VS Code session.

**Security note:** The firewall rule allows connections to the portal server. It does not enforce authentication or restrict internet access for hotspot clients.

---

## 10. Running the Application

The current development workflow uses the integrated terminal in Visual Studio Code.

### 10.1 Open Project

Open the existing project directory:

```text
G:\IntraHub
```

### 10.2 Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 10.3 Configure Portal Password

```powershell
$env:PORTAL_PASSWORD='YourTemporaryPassword'
```

Single quotes are important in PowerShell when the password contains dollar signs.

For example, PowerShell interprets `$` as a variable prefix inside double-quoted strings. Single quotes preserve literal dollar signs.

### 10.4 Start Flask

```powershell
python app.py
```

### 10.5 Expected Output

```text
 * Serving Flask app 'app'
 * Debug mode: off

WARNING: This is a development server.
Do not use it in a production deployment.
Use a production WSGI server instead.

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.70.120.32:8080

Press CTRL+C to quit
```

### 10.6 Access the Portal

From the host computer:

```text
http://127.0.0.1:8080
```

From a smartphone connected to the Windows hotspot:

```text
http://192.168.137.1:8080
```

The smartphone must be connected to the hotspot before accessing the locally hosted portal.

### 10.7 Stop the Server

Use:

```text
CTRL + C
```

in the integrated terminal.

---

## 11. Testing and Verification

Testing was performed using a Windows 11 laptop and a separate smartphone.

### 11.1 Hotspot Connectivity Test

**Objective:** Verify that Windows Mobile Hotspot can broadcast a wireless network and share internet access.

Procedure:

1. Enable Windows Mobile Hotspot.
2. Connect a smartphone.
3. Verify that Windows lists the connected device.
4. Check the smartphone's IP and MAC addresses.
5. Verify internet connectivity.

**Result:** Successful.

### 11.2 Flask Server Accessibility Test

**Objective:** Verify that an external device can communicate with the Flask server.

Procedure:

1. Start the Flask application.
2. Connect the smartphone to the hotspot.
3. Open the smartphone browser.
4. Navigate to:

```text
http://192.168.137.1:8080
```

**Result:** Successful.

### 11.3 Server Request Logs

The following requests were recorded:

```text
192.168.137.94 - - [31/Oct/2026 04:08:22]
"GET / HTTP/1.1" 200 -

192.168.137.94 - - [31/Oct/2026 04:08:22]
"GET /favicon.ico HTTP/1.1" 404 -

192.168.137.94 - - [31/Oct/2026 04:08:37]
"POST / HTTP/1.1" 200 -
```

The logs establish that:

- The smartphone successfully reached the Flask server.
- The login page was requested.
- The password form was submitted.
- The Flask server processed the POST request.

The `favicon.ico` response returned HTTP 404 because a favicon has not yet been implemented. This does not affect the login functionality.

### 11.4 Password Authentication Test

**Objective:** Verify that the application accepts the configured password and rejects incorrect credentials.

Initial testing revealed a PowerShell variable expansion issue.

The password was initially assigned using double quotes:

```powershell
$env:PORTAL_PASSWORD="..."
```

Because `$` has special meaning in PowerShell double-quoted strings, this did not preserve the intended password literally.

The problem was corrected by using single quotes:

```powershell
$env:PORTAL_PASSWORD='YourTemporaryPassword'
```

The application was restarted and password validation was successfully tested.

**Result:** Successful.

### 11.5 Overall Test Results

| Test | Result |
|---|---|
| Windows hotspot creation | Passed |
| Smartphone discovery | Passed |
| Smartphone connection | Passed |
| IP address allocation | Passed |
| Internet connectivity | Passed |
| Windows client identification | Passed |
| Flask server startup | Passed |
| Smartphone portal access | Passed |
| HTTP GET request | Passed |
| HTTP POST request | Passed |
| Correct password validation | Passed |

---

## 12. Security Considerations

Security is an important aspect of PortalWiFi because the project is intended to control access to a shared network.

The current prototype is for local experimentation only.

### 12.1 Current Security Limitations

The current implementation has the following limitations:

1. Password comparison is performed directly against a configured string.
2. The application does not use password hashing.
3. Authentication is not maintained through secure sessions.
4. No CSRF protection is implemented.
5. No rate limiting is implemented.
6. No brute-force protection is implemented.
7. HTTP is used instead of HTTPS.
8. Successful authentication does not modify firewall permissions.
9. Unauthenticated users are not blocked from accessing the internet.
10. The Flask development server is being used.

### 12.2 Planned Security Improvements

The following improvements are intended for subsequent versions.

**Password security**
- Store password hashes instead of plaintext passwords.
- Use a suitable password-hashing algorithm such as Argon2id or scrypt.
- Remove hardcoded fallback credentials.

**Session management**
- Implement server-side authentication state.
- Use secure session cookies where the deployment architecture supports HTTPS.
- Introduce session expiration.
- Provide logout functionality.

**Request protection**
- Add CSRF protection.
- Implement login rate limiting.
- Record failed authentication attempts.
- Introduce protection against repeated password guessing.

**Network security**
- Block unauthenticated clients at the network layer.
- Authorize clients individually.
- Prevent unauthenticated devices from bypassing the portal.
- Investigate Windows Filtering Platform and other suitable packet-filtering mechanisms.

**Deployment security**
- Replace Flask's development server with a production-capable WSGI server.
- Restrict management interfaces.
- Protect configuration files.
- Avoid logging passwords or sensitive authentication data.

### 12.3 Responsible Usage

PortalWiFi is intended for networks that the administrator owns or is authorized to manage.

The software should not be used to intercept credentials, impersonate unrelated networks or collect private information without authorization.

---

## 13. Known Limitations

The following limitations have been identified during initial development.

### 13.1 Legacy Hosted Network Unsupported

The Qualcomm QCA9377 driver reports:

```text
Hosted network supported: No
```

Therefore, the legacy `netsh wlan hostednetwork` method is not being used.

Windows 11 Mobile Hotspot is the current access-point mechanism.

### 13.2 Wi-Fi Password Requirement

Windows Mobile Hotspot currently requires a wireless network password.

This differs from the intended final captive portal architecture, where users should be able to connect to an open wireless network and authenticate through the custom portal.

An alternative access-point architecture may be required to achieve that exact experience.

### 13.3 No Automatic Captive Portal Detection

Users currently need to manually navigate to:

```text
http://192.168.137.1:8080
```

The application does not yet register itself with the operating system's captive portal detection mechanisms.

### 13.4 No Network-Level Access Control

The current application only validates credentials within Flask.

It does not currently control Windows ICS or prevent unauthenticated clients from accessing the internet.

### 13.5 Development Server

The Flask development server is intended for development and testing.

It is not an appropriate production server.

---

## 14. Development Roadmap

Development will proceed incrementally, with each phase building upon a tested foundation.

### Phase 0 — Hardware and Network Compatibility

**Status: Completed**

Objectives:

- Inspect Windows networking interfaces.
- Identify wireless adapter capabilities.
- Verify Windows Mobile Hotspot support.
- Establish the hotspot gateway address.
- Verify external device connectivity.

Deliverable: A working Windows hotspot.

### Phase 1 — Initial Captive Portal

**Status: Completed**

Objectives:

- Install Python and Flask.
- Create the first Flask application.
- Develop a basic login interface.
- Configure password validation.
- Configure Windows Firewall.
- Test portal access from a smartphone.

Deliverable: A locally hosted mobile-accessible login page.

### Phase 2 — Modular Portal Architecture

**Status: Planned**

Objectives:

- Separate HTML templates from Python code.
- Introduce dedicated CSS and JavaScript files.
- Create a configuration system.
- Implement password hashing.
- Introduce session management.
- Implement authentication event logging.
- Add CSRF protection.
- Add login rate limiting.

Deliverable: A structured and maintainable authentication application.

### Phase 3 — Network-Level Authentication

**Status: Planned**

Objectives:

- Identify connecting clients.
- Associate authentication sessions with client IP addresses and MAC addresses.
- Implement per-device authorization.
- Investigate Windows Filtering Platform.
- Evaluate suitable packet-filtering approaches.
- Block unauthenticated internet traffic.
- Allow internet traffic after successful authorization.

Deliverable: Actual network-level authentication and access control.

### Phase 4 — Automatic Captive Portal Detection

**Status: Planned**

Objectives:

- Investigate captive portal detection mechanisms.
- Support appropriate connectivity checks.
- Implement suitable HTTP redirection.
- Test automatic portal opening on Android and iOS.
- Investigate operating-system-specific behavior.

Deliverable: A more seamless captive portal experience.

### Phase 5 — Desktop Management Interface

**Status: Planned**

Objectives:

- Develop a PySide6 desktop dashboard.
- Integrate hotspot management.
- Display connected devices.
- Manage authentication settings.
- Display connection history.
- Provide client disconnection controls.

Deliverable: A complete desktop management application.

---

## 15. Proposed Future Features

These features are potential extensions and are not part of the current prototype.

| Feature | Description |
|---|---|
| Custom SSID | Configure the wireless network name. |
| Custom branding | Upload a logo and customize portal appearance. |
| Welcome message | Configure the portal's welcome text. |
| Device management | View and manage connected clients. |
| Client disconnection | Disconnect individual devices. |
| Connection limits | Limit the number of connected clients. |
| Bandwidth monitoring | Monitor network consumption. |
| Connection history | Maintain connection records. |
| Authentication history | Record successful and failed login attempts. |
| Session expiration | Automatically revoke expired authorization. |
| QR code | Generate a QR code for network discovery. |
| Desktop dashboard | Manage the system through a graphical interface. |

---

## 16. Troubleshooting

### Problem 1: Flask import cannot be resolved

**Possible cause:** VS Code is using the wrong Python interpreter.

**Solution:**

Select:

```text
G:\IntraHub\venv\Scripts\python.exe
```

Then reload VS Code.

Verify Flask:

```powershell
python -m pip show flask
```

### Problem 2: Access is denied when creating a firewall rule

**Possible cause:** PowerShell is not running with Administrator privileges.

**Solution:**

Launch VS Code as Administrator and execute the firewall configuration command again.

### Problem 3: Smartphone cannot access the portal

Check:

1. Whether Mobile Hotspot is running.
2. Whether the smartphone is connected.
3. Whether the hotspot gateway is correct.
4. Whether Flask is running.
5. Whether Flask is listening on `0.0.0.0`.
6. Whether the firewall rule is enabled.

Check the firewall rule:

```powershell
Get-NetFirewallRule -DisplayName "PortalWiFi Prototype"
```

Check network addresses:

```powershell
Get-NetIPAddress -AddressFamily IPv4
```

### Problem 4: Incorrect password message despite entering the intended password

**Possible cause:** PowerShell variable expansion.

Use single quotes:

```powershell
$env:PORTAL_PASSWORD='YourTemporaryPassword'
```

Restart Flask after changing the environment variable.

### Problem 5: Favicon returns HTTP 404

**Possible cause:** No favicon has been configured.

This is harmless during the current prototype stage.

A favicon can be added when the frontend is modularized.

---

## 17. Current Development Commands — Quick Reference

| Operation | Command |
|---|---|
| Create virtual environment | `python -m venv venv` |
| Activate environment | `.\venv\Scripts\Activate.ps1` |
| Install Flask | `python -m pip install flask` |
| Check Flask | `python -m pip show flask` |
| Save dependencies | `pip freeze > requirements.txt` |
| Set portal password | `$env:PORTAL_PASSWORD='YourTemporaryPassword'` |
| Start application | `python app.py` |
| Stop application | `Ctrl + C` |
| Check Wi-Fi drivers | `netsh wlan show drivers` |
| Check Wi-Fi interfaces | `netsh wlan show interfaces` |
| Check IP configuration | `Get-NetIPAddress -AddressFamily IPv4` |
| Check network adapters | `Get-NetAdapter -IncludeHidden` |
| Check ICS service | `Get-Service SharedAccess` |
| Check firewall rule | `Get-NetFirewallRule -DisplayName "PortalWiFi Prototype"` |

---

## 18. Development Principles

The following principles will guide future development.

1. **Incremental development:** Implement and test one component at a time.
2. **Modular architecture:** Keep networking, authentication, frontend and application management separate.
3. **Security-first design:** Avoid insecure shortcuts in authentication and access control.
4. **Maintainability:** Prefer readable, documented and reusable code.
5. **Test-driven verification:** Verify network and authentication behavior before marking features complete.
6. **Compatibility:** Consider Windows networking limitations and different smartphone operating systems.
7. **Clear separation of responsibilities:** The portal interface must not be confused with actual network-level authorization.

---

## 19. Current Project Summary

As of 31 October 2026, PortalWiFi has successfully demonstrated its initial concept.

A Windows 11 laptop equipped with a Qualcomm QCA9377 wireless adapter is capable of sharing its internet connection through Windows Mobile Hotspot.

A separate smartphone can connect to the hotspot, receive an IP address and access the internet.

A Python Flask application running on the laptop can be accessed by the smartphone through the hotspot gateway at:

```text
http://192.168.137.1:8080
```

The application successfully displays a custom login page and validates submitted passwords.

The current implementation establishes the foundation for a more advanced captive portal management system.

However, automatic captive portal detection and actual network-level internet access control remain unimplemented.

**The next development milestone is PortalWiFi v0.2 — Modular Portal Architecture.**

---

## 20. Project Identity

**Project Name:** PortalWiFi

**Project Category:** Networking / Network Access Management

**Primary Platform:** Windows 11

**Backend:** Python + Flask

**Development Environment:** Visual Studio Code

**Current Version:** 0.1

**Current Status:** Initial Working Prototype

**Core Concept:**

A customizable, locally managed Wi-Fi captive portal that provides controlled internet access through a Windows-hosted wireless network.

---

*End of Documentation*

*PortalWiFi — Initial Working Prototype, Version 0.1.*