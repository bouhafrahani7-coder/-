from flet import *
import sqlite3

# -------- DATABASE --------
conn = sqlite3.connect("lessons.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    level TEXT,
    phone TEXT
)
""")
conn.commit()

# -------- APP --------
def main(page: Page):
    page.title = "إدارة الدروس الخاصة"
    page.theme_mode = ThemeMode.LIGHT
    page.window.width = 500
    page.window.height = 600
    page.padding = 20

    name = TextField(label="اسم التلميذ")
    level = TextField(label="المستوى")
    phone = TextField(label="رقم الهاتف")

    students_column = Column(scroll="auto")

    def load_students():
        students_column.controls.clear()
        cur.execute("SELECT name, level, phone FROM students")
        for s in cur.fetchall():
            students_column.controls.append(
                Container(
                    content=Text(f"👤 {s[0]} | 🎓 {s[1]} | 📞 {s[2]}"),
                    padding=10,
                    border_radius=10,
                    bgcolor=Colors.BLUE_50
                )
            )
        page.update()

    def add_student(e):
        if not name.value or not level.value:
            return
        cur.execute(
            "INSERT INTO students VALUES (NULL, ?, ?, ?)",
            (name.value, level.value, phone.value)
        )
        conn.commit()
        name.value = ""
        level.value = ""
        phone.value = ""
        load_students()

    add_btn = ElevatedButton(
        "➕ إضافة تلميذ",
        on_click=add_student,
        bgcolor=Colors.BLUE,
        color=Colors.WHITE
    )

    page.add(
        Text("📚 إدارة الدروس الخاصة", size=22, weight="bold"),
        Divider(),
        name,
        level,
        phone,
        add_btn,
        Divider(),
        Text("📋 قائمة التلاميذ", size=18),
        students_column
    )

    load_students()

app(target=main)
