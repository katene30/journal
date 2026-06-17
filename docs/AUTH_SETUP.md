# Multi-User Authentication Setup

Add user registration, login, and password reset via API for the SvelteKit frontend.

## Stack

- **django-allauth** — Handles registration, email verification, password reset logic
- **dj-rest-auth** — Exposes allauth as REST API endpoints

## Installation

```bash
pip install dj-rest-auth[with-social] django-allauth
```

Add to `requirements.txt`:
```
dj-rest-auth[with-social]>=5.0
django-allauth>=0.61
```

## Django Configuration

### 1. Update settings.py

```python
INSTALLED_APPS = [
    # ... existing apps
    'django.contrib.sites',  # Required by allauth
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Optional: for social login later
    
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

MIDDLEWARE = [
    # ... existing middleware
    'allauth.account.middleware.AccountMiddleware',  # Add after AuthenticationMiddleware
]

# Site ID (required by allauth)
SITE_ID = 1

# REST Framework auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',  # Optional: for token auth
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory' for production

# Where to redirect after email confirmation (if using email verification)
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/app/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/app/'

# Login settings
LOGIN_URL = '/api/auth/login/'
LOGIN_REDIRECT_URL = '/app/'
```

### 2. Update urls.py

```python
urlpatterns = [
    # ... existing urls
    
    # Auth API
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
```

### 3. Run migrations

```bash
python manage.py migrate
```

## API Endpoints

After setup, these endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | Login with email/password |
| `/api/auth/logout/` | POST | Logout (clears session) |
| `/api/auth/user/` | GET | Get current user info |
| `/api/auth/user/` | PUT/PATCH | Update user info |
| `/api/auth/password/change/` | POST | Change password (logged in) |
| `/api/auth/password/reset/` | POST | Request password reset email |
| `/api/auth/password/reset/confirm/` | POST | Confirm password reset |
| `/api/auth/registration/` | POST | Register new user |
| `/api/auth/registration/verify-email/` | POST | Verify email address |

### Example: Register

```bash
curl -X POST http://localhost:8000/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password1": "securepass123", "password2": "securepass123"}'
```

### Example: Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

## Frontend Implementation

### 1. Add auth API functions

Create `frontend/src/lib/api/auth.ts`:

```typescript
import { api } from './client';

export interface User {
  pk: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password1: string;
  password2: string;
}

export const authApi = {
  login: (data: LoginData) => 
    api.post<{ key?: string }>('/auth/login/', data),
  
  logout: () => 
    api.post<void>('/auth/logout/', {}),
  
  register: (data: RegisterData) => 
    api.post<{ key?: string }>('/auth/registration/', data),
  
  getUser: () => 
    api.get<User>('/auth/user/'),
  
  resetPassword: (email: string) => 
    api.post<void>('/auth/password/reset/', { email }),
};
```

### 2. Create auth store

Create `frontend/src/lib/stores/auth.ts`:

```typescript
import { writable } from 'svelte/store';
import { authApi, type User } from '$lib/api/auth';

export const currentUser = writable<User | null>(null);
export const isAuthenticated = writable(false);

export const authActions = {
  login: async (email: string, password: string) => {
    await authApi.login({ email, password });
    const user = await authApi.getUser();
    currentUser.set(user);
    isAuthenticated.set(true);
  },
  
  logout: async () => {
    await authApi.logout();
    currentUser.set(null);
    isAuthenticated.set(false);
  },
  
  register: async (email: string, password: string) => {
    await authApi.register({ email, password1: password, password2: password });
    // Auto-login after registration
    await authActions.login(email, password);
  },
  
  checkAuth: async () => {
    try {
      const user = await authApi.getUser();
      currentUser.set(user);
      isAuthenticated.set(true);
    } catch {
      currentUser.set(null);
      isAuthenticated.set(false);
    }
  },
};
```

### 3. Create auth pages

Create these routes in SvelteKit:
- `/app/login` — Login form
- `/app/register` — Registration form
- `/app/forgot-password` — Password reset request

### 4. Protect routes

In `+layout.svelte` or individual pages:

```svelte
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { isAuthenticated, authActions } from '$lib/stores/auth';
  
  onMount(async () => {
    await authActions.checkAuth();
    if (!$isAuthenticated) {
      goto('/app/login');
    }
  });
</script>
```

## Email Configuration (Production)

For password reset emails to work, configure email in settings.py:

```python
# Development: Print emails to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: Use a real email service
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
# DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## Optional: Social Login (Google, GitHub)

Once basic auth works, you can add social login:

```python
INSTALLED_APPS = [
    # ... 
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
```

Then configure OAuth credentials in Django admin under "Social Applications".

## Checklist

- [ ] Install packages
- [ ] Update settings.py
- [ ] Update urls.py
- [ ] Run migrations
- [ ] Test registration endpoint
- [ ] Test login endpoint
- [ ] Create frontend auth API functions
- [ ] Create frontend auth store
- [ ] Create login page in Svelte
- [ ] Create registration page in Svelte
- [ ] Add route protection
- [ ] Configure email for production
- [ ] (Optional) Add social login
