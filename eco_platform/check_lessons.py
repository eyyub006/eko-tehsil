from app import app, Lesson, db

def check_lessons():
    with app.app_context():
        lessons = Lesson.query.all()
        print(f"Total Lessons: {len(lessons)}")
        for l in lessons:
            print(f"ID: {l.id} | Title: {l.title}")

if __name__ == "__main__":
    check_lessons()
