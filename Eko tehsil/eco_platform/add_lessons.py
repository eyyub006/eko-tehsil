from app import app, db, Lesson

def add_more_lessons():
    with app.app_context():
        new_lessons = [
            Lesson(
                title="Plastik Tullantılar",
                description="Plastik təbiətdə neçə il qalır?",
                content="Plastik butulkaların təbiətdə yox olması üçün 450 il lazımdır! Buna görə də plastikdən az istifadə etməliyik və onları təkrar emala göndərməliyik.",
                question_text="Plastik butulka təbiətdə neçə ilə yox olur?",
                option_a="10 ilə",
                option_b="450 ilə",
                correct_option="B",
                explanation="Dəhşətlidir, elə deyilmi? 450 il!"
            ),
            Lesson(
                title="Günəş Enerjisi",
                description="Tükənməyən enerji mənbəyi.",
                content="Günəş panelləri günəş işığını elektrikə çevirir. Bu təmiz enerjidir və təbiəti çirkləndirmir.",
                question_text="Günəş enerjisi necə enerjidir?",
                option_a="Təmiz və tükənməz",
                option_b="Çirkli və zərərli",
                correct_option="A",
                explanation="Günəş bizə həm istilik, həm də təmiz enerji verir."
            ),
            Lesson(
                title="Heyvanları Qoruyaq",
                description="Nəsli kəsilməkdə olan növlər.",
                content="Bəzi heyvanlar (məsələn, Ceyranlar) azalır. Biz onların yaşadığı yerləri qorumalıyıq ki, onlar çoxala bilsinlər.",
                question_text="Nəsli kəsilən heyvanlar üçün nə etməliyik?",
                option_a="Onları ovlamalıyıq",
                option_b="Qorumalıyıq",
                correct_option="B",
                explanation="Təbiət bütün canlıların evidir."
            )
        ]
        
        count = 0
        for l in new_lessons:
            # Check duplicates by title
            if not Lesson.query.filter_by(title=l.title).first():
                db.session.add(l)
                count += 1
        
        db.session.commit()
        print(f"Added {count} new lessons.")

if __name__ == "__main__":
    add_more_lessons()
