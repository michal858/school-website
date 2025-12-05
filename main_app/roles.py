from functools import wraps
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Musisz być zalogowany aby uzyskać dostęp.', 'error')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                return render_template('error.html', error=403)

            return func(*args, **kwargs)
        return decorated_view
    return wrapper
