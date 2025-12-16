from app import app, db, Lesson

def populate_lessons():
    with app.app_context():
        # Clear existing if any (to avoid dups if check failed)
        # db.session.query(Lesson).delete()
        # db.session.commit()
        
        if Lesson.query.count() > 0:
            print("Lessons already exist.")
            return

        lessons = [
            Lesson(
                title="Zibil niyə çeşidlənməlidir?",
                description="Tullantıları düzgün ayırmağı öyrənək.",
                content="Zibilləri kağız, plastik və şüşə kimi ayıranda onları yenidən emal etmək olur. Bu təbiəti qoruyur!",
                question_text="Plastik butulkani hara atmalisan?",
                option_a="Adi zibil qutusuna",
                option_b="Plastik üçün xüsusi qutuya",
                correct_option="B",
                explanation="Afərin! Plastikləri ayrı toplasaq, onlardan yeni əşyalar düzəltmək olar."
            ),
            Lesson(
                title="Suyu qoruyaq",
                description="Su həyatdır, onu israf etməyək.",
                content="Dişlərimizi fırçalayarkən krantı açıq qoysaq, çoxlu su boşuna axar. Krantı bağlamağı unutma!",
                question_text="Diş fırçalayanda krantı nə etməlisən?",
                option_a="Bağlamalıyam",
                option_b="Açıq qoymalıyam",
                correct_option="A",
                explanation="Düzdür! Suyu qorumaq təbiəti qorumaqdır."
            ),
            Lesson(
                title="Hava Çirkliliyi",
                description="Təmiz hava üçün nə etməliyik?",
                content="Fabriklərdən və maşınlardan çıxan tüstü havanı çirkləndirir. Biz ağac əkərək və velosiped sürərək havanı təmiz saxlaya bilərik.",
                question_text="Həm idman edib, həm də havanı qorumaq üçün nə sürə bilərik?",
                option_a="Avtomobil",
                option_b="Velosiped",
                correct_option="B",
                explanation="Afərin! Velosiped tüstü buraxmır və sağlamlıq üçün faydalıdır."
            ),
            Lesson(
                title="Enerjiyə Qənaət",
                description="İşıqları boş yerə yandırma.",
                content="Otaqdan çıxanda işığı söndürmək lazımdır. Bu həm pulumuza, həm də təbiətə qənaət edir.",
                question_text="Otaqdan çıxanda nə etməlisən?",
                option_a="İşığı söndürməliyəm",
                option_b="İşığı yanılı qoymalıyam",
                correct_option="A",
                explanation="Düzdür! Enerjiyə qənaət etmək vacibdir."
            ),
            Lesson(
                title="Meşələrin Dostları",
                description="Ağaclar bizim dostumuzdur.",
                content="Ağaclar bizə oksigen verir. Onları qırmaq yox, qorumaq və yenilərini əkmək lazımdır.",
                question_text="Ağacları nə etməliyik?",
                option_a="Qırmalıyıq",
                option_b="Qorumalıyıq və suvarmalıyıq",
                correct_option="B",
                explanation="Əla! Ağaclar olmasa nəfəs ala bilmərik."
            )
        ]
        
        for l in lessons:
            db.session.add(l)
        
        db.session.commit()
        print(f"Added {len(lessons)} lessons.")

if __name__ == "__main__":
    populate_lessons()
