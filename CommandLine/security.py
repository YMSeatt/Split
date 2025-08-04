import hashlib
import os
from datetime import datetime
import portalocker

# --- Constants copied from other.py ---
APP_NAME = "BehaviorLogger"
MASTER_RECOVERY_PASSWORD_HASH = "5bf881cb69863167a3172fda5c552694a3328548a43c7ee258d6d7553fc0e1a1a8bad378fb131fbe10e37efbd9e285b22c29b75d27dcc2283d48d8edf8063292"
LOCK_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f"{APP_NAME}.lock"))

# --- File Lock Manager ---
class FileLockManager:
    def __init__(self, lock_file_path=LOCK_FILE_PATH):
        self.lock_file_path = lock_file_path
        self.lock = None

    def acquire_lock(self):
        try:
            self.lock = open(self.lock_file_path, 'w')
            portalocker.lock(self.lock, portalocker.LOCK_EX | portalocker.LOCK_NB)
            self.lock.write(str(os.getpid()))
            self.lock.flush()
            return True, ""
        except (IOError, portalocker.LockException) as e:
            error_message = f"Another instance of {APP_NAME} may already be running."
            return False, error_message

    def release_lock(self):
        if self.lock:
            try:
                portalocker.unlock(self.lock)
                self.lock.close()
            except Exception:
                pass
            finally:
                self.lock = None
                if os.path.exists(self.lock_file_path):
                    os.remove(self.lock_file_path)

# --- Password Management ---
class PasswordManager:
    def __init__(self, app_settings):
        self.app_settings = app_settings
        self.is_locked = False
        self.last_activity_time = datetime.now()

    def _hash_password(self, password):
        return hashlib.sha3_512(password.encode('utf-8')).hexdigest()

    def set_password(self, password):
        if not password:
            self.app_settings["app_password_hash"] = None
            return True
        self.app_settings["app_password_hash"] = self._hash_password(password)
        return True

    def check_password(self, password):
        stored_hash = self.app_settings.get("app_password_hash")
        if not stored_hash: return True
        return self._hash_password(password) == stored_hash

    def check_recovery_password(self, recovery_password):
        return self._hash_password(recovery_password) == MASTER_RECOVERY_PASSWORD_HASH

    def is_password_set(self):
        return bool(self.app_settings.get("app_password_hash"))

    def lock_application(self):
        if self.is_password_set():
            self.is_locked = True
            return True
        return False

    def unlock_application(self, password_attempt):
        if self.check_password(password_attempt) or self.check_recovery_password(password_attempt):
            self.is_locked = False
            self.last_activity_time = datetime.now()
            return True
        return False

    def check_auto_lock(self):
        if self.is_locked or not self.is_password_set() or not self.app_settings.get("password_auto_lock_enabled", False):
            return
        timeout_minutes = self.app_settings.get("password_auto_lock_timeout_minutes", 15)
        if timeout_minutes > 0:
            if (datetime.now() - self.last_activity_time).total_seconds() / 60 > timeout_minutes:
                self.lock_application()

    def record_activity(self):
        self.last_activity_time = datetime.now()
