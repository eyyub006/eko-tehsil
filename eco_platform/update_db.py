from app import app, db, Lesson

def update_db():
    with app.app_context():
        # New Lessons Data
        new_lessons = [
            {
                "title": "Hava Çirkliliyi",
                "description": "Təmiz hava üçün nə etməliyik?",
                "content": "Fabriklərdən və maşınlardan çıxan tüstü havanı çirkləndirir. Biz ağac əkərək və velosiped sürərək havanı təmiz saxlaya bilərik.",
                "question_text": "Həm idman edib, həm də havanı qorumaq üçün nə sürə bilərik?",
                "option_a": "Avtomobil",
                "option_b": "Velosiped",
                "correct_option": "B",
                "explanation": "Afərin! Velosiped tüstü buraxmır və sağlamlıq üçün faydalıdır."
            },
            {
                "title": "Enerjiyə Qənaət",
                "description": "İşıqları boş yerə yandırma.",
                "content": "Otaqdan çıxanda işığı söndürmək lazımdır. Bu həm pulumuza, həm də təbiətə qənaət edir.",
                "question_text": "Otaqdan çıxanda nə etməlisən?",
                "option_a": "İşığı söndürməliyəm",
                "option_b": "İşığı yanılı qoymalıyam",
                "correct_option": "A",
                "explanation": "Düzdür! Enerjiyə qənaət etmək vacibdir."
            },
            {
                "title": "Meşələrin Dostları",
                "description": "Ağaclar bizim dostumuzdur.",
                "content": "Ağaclar bizə oksigen verir. Onları qırmaq yox, qorumaq və yenilərini əkmək lazımdır.",
                "question_text": "Ağacları nə etməliyik?",
                "option_a": "Qırmalıyıq",
                "option_b": "Qorumalıyıq və suvarmalıyıq",
                "correct_option": "B",
                "explanation": "Əla! Ağaclar olmasa nəfəs ala bilmərik."
            }
        ]

        for ld in new_lessons:
            exists = Lesson.query.filter_by(title=ld['title']).first()
            if not exists:
                l = Lesson(**ld)
                db.session.add(l)
                print(f"Added: {ld['title']}")
            else:
                print(f"Skipped (exists): {ld['title']}")
        
        db.session.commit()
        print("Database updated successfully!")

if __name__ == "__main__":
    update_db()
