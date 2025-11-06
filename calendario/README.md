# Calendario App - Interrogazioni Programmate

This app manages scheduled interrogations with student notification capabilities.

## Features

- **Per-Subject Calendars**: Each subject has its own calendar of scheduled interrogations
- **Unified Calendar View**: See all scheduled interrogations across all subjects
- **Student Management**: Assign dates to students, with support for multiple interrogations
- **Date Manipulation** (Admin only):
  - Shift students up/down in the schedule
  - Swap dates between two students
  - Insert new dates and automatically shift subsequent events
- **Browser Push Notifications**: Students can subscribe to receive notifications 1 week and 2 days before their interrogation

## Usage

### For Admins

1. Navigate to **Calendari** in the main navigation
2. Select a subject to manage its calendar
3. Use the **+** floating button to add new scheduled interrogations
4. Use the action buttons in each event card to:
   - **Sposta su/giù**: Move a student earlier/later in the schedule
   - **Modifica**: Edit the date or notes
   - **Elimina**: Delete a scheduled interrogation
   - **Scambia date**: Swap dates between two students

### For Students

1. Navigate to the calendar for your subject
2. Find your scheduled interrogation
3. Click on it to expand details
4. Click the **"Notificami"** button to enable notifications
5. Grant notification permissions when prompted
6. You'll receive two notifications:
   - One week before your interrogation
   - Two days before your interrogation

## Setting Up Notifications

### 1. VAPID Keys

VAPID keys are already configured in `settings.py`. If you need to regenerate them:

```bash
python -c "
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key = private_key.public_key()
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)
public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')

print('VAPID_PRIVATE_KEY =')
print(private_bytes.decode('utf-8'))
print()
print('VAPID_PUBLIC_KEY =', repr(public_key_b64))
"
```

### 2. Cron Job for Sending Notifications

To automatically send notifications, set up a cron job to run daily:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9:00 AM
0 9 * * * cd /path/to/domanitiinterrogo && source venv/bin/activate && python manage.py send_notifications
```

Or manually run the command:

```bash
python manage.py send_notifications
```

### 3. HTTPS Requirement

Push notifications require HTTPS in production. Make sure your site is served over HTTPS (already configured with Traefik in your Docker setup).

## Models

### InterrogazioneProgrammata

- `studente`: Foreign key to Student
- `materia`: Foreign key to Subject
- `data`: Date of the scheduled interrogation
- `note`: Optional notes
- `created_at`, `updated_at`: Timestamps

### NotificationSubscription

- `studente`: Foreign key to Student
- `evento`: Foreign key to InterrogazioneProgrammata
- `subscription_endpoint`: Browser push subscription endpoint
- `subscription_p256dh`: Encryption key
- `subscription_auth`: Authentication secret
- `notified_one_week`: Boolean flag for 1-week notification
- `notified_two_days`: Boolean flag for 2-day notification
- `created_at`: Timestamp

## API Endpoints

- `GET /calendario/` - List all subjects
- `GET /calendario/unificato/` - Unified calendar view
- `GET /calendario/materia/<id>/` - Subject-specific calendar
- `POST /calendario/add/` - Add new event (staff only)
- `POST /calendario/delete/<id>/` - Delete event (staff only)
- `POST /calendario/update/<id>/` - Update event (staff only)
- `POST /calendario/materia/<id>/shift-up/<event_id>/` - Shift student up (staff only)
- `POST /calendario/materia/<id>/shift-down/<event_id>/` - Shift student down (staff only)
- `POST /calendario/materia/<id>/swap/` - Swap two students (staff only)
- `POST /calendario/subscribe/` - Subscribe to notifications
- `POST /calendario/unsubscribe/` - Unsubscribe from notifications

## Technical Details

### Service Worker

The service worker (`/static/sw.js`) handles push notifications in the browser. It must be served from the root path for proper scope.

### Browser Compatibility

Push notifications are supported in:
- Chrome/Edge 42+
- Firefox 44+
- Safari 16+ (macOS 13+)

### Security

- All admin operations require staff permissions (`@staff_member_required`)
- CSRF protection on all POST endpoints
- VAPID authentication for push notifications
- Service worker requires HTTPS in production

## Troubleshooting

### Notifications not working

1. Check browser console for errors
2. Ensure HTTPS is enabled in production
3. Verify VAPID keys are correctly configured
4. Check that the service worker is registered: `navigator.serviceWorker.ready`
5. Verify notification permissions: `Notification.permission`

### Cron job not running

1. Check cron logs: `grep CRON /var/log/syslog`
2. Ensure the Python environment is activated in the cron command
3. Use absolute paths in the cron command
4. Check that the Django project path is correct

### Database issues

Run migrations if you encounter database errors:

```bash
python manage.py makemigrations calendario
python manage.py migrate calendario
```
