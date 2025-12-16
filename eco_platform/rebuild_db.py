from app import app, db

def rebuild_db():
    with app.app_context():
        print("Dropping tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        print("Initializing data...")
        from app import init_db
        init_db()
        print("Database rebuilt successfully!")

if __name__ == "__main__":
    rebuild_db()
