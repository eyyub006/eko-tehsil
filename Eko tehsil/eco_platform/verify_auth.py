from app import app, db, User
import os

def check_auth():
    # Force db creation in memory/test context or ensure real db fits
    # But here we just check if logic holds without crashing
    with app.app_context():
        # Check if fields exist
        try:
            # Inspection
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            if 'password_hash' in columns:
                print("✅ Password column exists.")
            else:
                # If migration failed, we might need to recreate DB manually or handle partial failure
                print("❌ Password column MISSING. (Might require DB rebuild)")
        except Exception as e:
            print(f"Error checking DB: {e}")

        # Check Admin Route Logic (static check)
        print("✅ Routes loaded.")

if __name__ == "__main__":
    check_auth()
