import mysql.connector
import datetime
import sys

# ─────────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────────
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uomnewsportaldbtest"
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    print(f"[ERROR] Could not connect to database: {e}")
    sys.exit(1)


# ─────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────
def execute(query, params=()):
    try:
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"  [DB Error] {e}")
        return False


def generate_id(table, column, prefix):
    cursor.execute(f"SELECT MAX({column}) FROM {table}")
    result = cursor.fetchone()[0]
    if result is None:
        return prefix + "001"
    num = int(result[len(prefix):])
    return prefix + str(num + 1).zfill(3)


def generate_log_id():
    cursor.execute("SELECT MAX(Log_id) FROM search_log")
    result = cursor.fetchone()[0]
    if not result:
        return "L001"
    prefix = ''.join([c for c in result if not c.isdigit()])
    number = ''.join([c for c in result if c.isdigit()])
    return prefix + str(int(number) + 1).zfill(len(number))


def load_map(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return {r[1]: r[0] for r in rows}


def print_table(headers, rows, col_width=22):
    """Pretty-print a table to the terminal."""
    if not rows:
        print("  (no records found)")
        return
    sep = "+" + "+".join(["-" * (col_width + 2) for _ in headers]) + "+"
    header_row = "| " + " | ".join(str(h).ljust(col_width) for h in headers) + " |"
    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        line = "| " + " | ".join(str(v if v is not None else "")[:col_width].ljust(col_width) for v in row) + " |"
        print(line)
    print(sep)
    print(f"  {len(rows)} record(s) shown.\n")


def input_prompt(label, default=""):
    val = input(f"  {label}{' [' + default + ']' if default else ''}: ").strip()
    return val if val else default


def pick_from_map(label, mapping):
    """Let user choose a key from a name→id mapping. Returns the ID."""
    items = list(mapping.items())
    if not items:
        print(f"  [Warning] No {label} available.")
        return None
    print(f"\n  Available {label}s:")
    for i, (name, _) in enumerate(items, 1):
        print(f"    {i}. {name}")
    while True:
        choice = input(f"  Choose {label} number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            name, id_ = items[int(choice) - 1]
            return id_
        print("  Invalid choice. Try again.")


def menu(title, options):
    """Display a numbered menu and return the chosen option number (int)."""
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    print(f"  0. Back / Exit")
    while True:
        choice = input("\n  Enter choice: ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(options):
            return int(choice)
        print("  Invalid choice. Try again.")


# ─────────────────────────────────────────────
#  USER PORTAL
# ─────────────────────────────────────────────
def user_portal():
    while True:
        choice = menu("👤  USER PORTAL", [
            "Register New User",
            "View All Users",
            "View Articles",
            "Post a Comment",
            "View Comments",
            "View Tags",
            "View Categories",
            "Search Articles (Search Log)",
        ])
        if choice == 0:
            break
        elif choice == 1:
            user_register()
        elif choice == 2:
            user_list()
        elif choice == 3:
            view_articles()
        elif choice == 4:
            post_comment()
        elif choice == 5:
            view_comments()
        elif choice == 6:
            view_tags()
        elif choice == 7:
            view_categories()
        elif choice == 8:
            search_articles()


def user_register():
    print("\n  ── Register New User ──")
    new_id = generate_id("user", "User_id", "U")
    print(f"  Auto-generated User ID: {new_id}")
    name  = input_prompt("Name")
    email = input_prompt("Email")
    dob   = input_prompt("DOB (YYYY-MM-DD)")
    if not name:
        print("  [Error] Name is required.")
        return
    if not dob:
        print("  [Error] Date of Birth is required.")
        return
    if execute("INSERT INTO `user`(User_id, Name, Email, DOB) VALUES (%s,%s,%s,%s)",
               (new_id, name, email, dob)):
        print(f"  ✓ User registered successfully! ID: {new_id}")


def user_list():
    print("\n  ── Registered Users ──")
    cursor.execute("SELECT User_id, Name, Email, DOB FROM `user`")
    print_table(["User_id", "Name", "Email", "DOB"], cursor.fetchall())


def view_articles(filter_text=None):
    print("\n  ── View Articles ──")
    if filter_text is None:
        filter_text = input_prompt("Search keyword (leave blank for all)", "")
    if filter_text:
        cursor.execute("""
            SELECT a.Article_id, a.Title, a.Content, a.Published_Date, au.Name
            FROM `article` a JOIN `author` au ON a.Author_id = au.Author_Id
            WHERE a.Title LIKE %s OR a.Content LIKE %s
        """, ('%' + filter_text + '%', '%' + filter_text + '%'))
    else:
        cursor.execute("""
            SELECT a.Article_id, a.Title, a.Content, a.Published_Date, au.Name
            FROM `article` a JOIN `author` au ON a.Author_id = au.Author_Id
        """)
    print_table(["Article_id", "Title", "Content", "Published_Date", "Author"], cursor.fetchall(), col_width=30)


def post_comment():
    print("\n  ── Post a Comment ──")
    u_user_map    = load_map("SELECT User_id, Name FROM `user`")
    u_article_map = load_map("SELECT Article_id, Title FROM `article`")
    if not u_user_map:
        print("  No users found. Please register first.")
        return
    if not u_article_map:
        print("  No articles found.")
        return
    new_id = generate_id("comment", "Comment_id", "C")
    print(f"  Auto-generated Comment ID: {new_id}")
    user_id    = pick_from_map("User", u_user_map)
    article_id = pick_from_map("Article", u_article_map)
    content    = input_prompt("Comment text")
    date       = input_prompt("Date", str(datetime.date.today()))
    if not user_id or not article_id:
        return
    if execute("INSERT INTO `comment`(Comment_id, Article_id, User_id, Content, Comment_date) VALUES (%s,%s,%s,%s,%s)",
               (new_id, article_id, user_id, content, date)):
        print("  ✓ Comment posted!")


def view_comments():
    print("\n  ── Comments ──")
    cursor.execute("""
        SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
        FROM `comment` c
        JOIN `user` u ON c.User_id = u.User_id
        JOIN `article` a ON c.Article_id = a.Article_id
    """)
    print_table(["Comment_id", "User", "Article", "Comment", "Date"], cursor.fetchall(), col_width=25)


def view_tags():
    print("\n  ── Tags & Articles ──")
    cursor.execute("""
        SELECT t.Name, a.Title
        FROM `tag` t
        JOIN `article_tag` at_ ON t.Tag_ID = at_.TAG_ID
        JOIN `article` a ON at_.ARTICLE_ID = a.Article_id
        ORDER BY t.Name ASC
    """)
    print_table(["Tag_Name", "Article_Title"], cursor.fetchall(), col_width=30)


def view_categories():
    print("\n  ── Categories & Articles ──")
    cursor.execute("""
        SELECT c.Name, a.Title
        FROM `category` c
        JOIN `article_category` ac ON c.Category_id = ac.Category_ID
        JOIN `article` a ON ac.Article_ID = a.Article_id
        ORDER BY c.Name ASC
    """)
    print_table(["Category_Name", "Article_Title"], cursor.fetchall(), col_width=30)


def search_articles():
    print("\n  ── Search Articles ──")
    u_user_map = load_map("SELECT User_id, Name FROM `user`")
    if not u_user_map:
        print("  No users found. Please register first.")
        return
    log_id  = generate_log_id()
    query   = input_prompt("Search query")
    if not query:
        print("  [Error] Search query is required.")
        return
    user_id = pick_from_map("User (who is searching)", u_user_map)
    date    = input_prompt("Date", str(datetime.date.today()))
    execute("INSERT INTO `search_log`(Log_id, Query_Text, Search_date, User_id) VALUES (%s,%s,%s,%s)",
            (log_id, query, date, user_id))
    cursor.execute(
        "SELECT Title, Content FROM `article` WHERE Title LIKE %s OR Content LIKE %s",
        ('%' + query + '%', '%' + query + '%')
    )
    results = cursor.fetchall()
    if results:
        print(f"\n  Search results for '{query}':")
        print_table(["Title", "Content"], results, col_width=40)
    else:
        print(f"  No articles found for '{query}'.")


# ─────────────────────────────────────────────
#  AUTHOR PORTAL
# ─────────────────────────────────────────────
def author_portal():
    while True:
        choice = menu("✍  AUTHOR PORTAL", [
            "Add Article",
            "View Articles",
            "Upload Media",
            "View Media",
            "View Comments on Articles",
            "View Article View Count",
            "Views by Age Category",
        ])
        if choice == 0:
            break
        elif choice == 1:
            author_add_article()
        elif choice == 2:
            author_view_articles()
        elif choice == 3:
            author_upload_media()
        elif choice == 4:
            author_view_media()
        elif choice == 5:
            author_view_comments()
        elif choice == 6:
            author_view_count()
        elif choice == 7:
            author_views_by_age()


def author_add_article():
    print("\n  ── Add Article ──")
    author_map = load_map("SELECT Author_Id, Name FROM `author`")
    if not author_map:
        print("  No authors registered. Please register an author via Admin Portal first.")
        return
    new_id  = generate_id("article", "Article_id", "A")
    print(f"  Auto-generated Article ID: {new_id}")
    title   = input_prompt("Title")
    content = input_prompt("Content")
    date    = input_prompt("Published Date", str(datetime.date.today()))
    if not title:
        print("  [Error] Title is required.")
        return
    author_id = pick_from_map("Author", author_map)
    if execute("INSERT INTO `article`(Article_id, Title, Content, Published_Date, Author_id) VALUES (%s,%s,%s,%s,%s)",
               (new_id, title, content, date, author_id)):
        print(f"  ✓ Article '{title}' added! ID: {new_id}")


def author_view_articles():
    print("\n  ── All Articles ──")
    cursor.execute("SELECT Article_id, Title, Content, Published_Date, Author_id FROM `article`")
    print_table(["Article_id", "Title", "Content", "Published_Date", "Author_id"], cursor.fetchall(), col_width=28)


def author_upload_media():
    print("\n  ── Upload Media ──")
    art_map = load_map("SELECT Article_id, Title FROM `article`")
    if not art_map:
        print("  No articles found.")
        return
    new_id     = generate_id("media", "Media_id", "M")
    print(f"  Auto-generated Media ID: {new_id}")
    media_type = input_prompt("Type (Image/Video)")
    url        = input_prompt("URL / File Path")
    article_id = pick_from_map("Article", art_map)
    if not article_id:
        return
    if execute("INSERT INTO `media`(Media_id, Type, URL, Article_id) VALUES (%s,%s,%s,%s)",
               (new_id, media_type, url, article_id)):
        print(f"  ✓ Media uploaded! ID: {new_id}")


def author_view_media():
    print("\n  ── Media Records ──")
    cursor.execute("SELECT Media_id, Type, URL, Article_id FROM `media`")
    print_table(["Media_id", "Type", "URL", "Article_id"], cursor.fetchall(), col_width=30)


def author_view_comments():
    print("\n  ── Comments (filter by article name) ──")
    f = input_prompt("Filter by article title (leave blank for all)", "")
    if f:
        cursor.execute("""
            SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
            FROM `comment` c
            JOIN `user` u ON c.User_id = u.User_id
            JOIN `article` a ON c.Article_id = a.Article_id
            WHERE a.Title LIKE %s
        """, ('%' + f + '%',))
    else:
        cursor.execute("""
            SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
            FROM `comment` c
            JOIN `user` u ON c.User_id = u.User_id
            JOIN `article` a ON c.Article_id = a.Article_id
        """)
    print_table(["Comment_id", "User", "Article", "Comment", "Date"], cursor.fetchall(), col_width=25)


def author_view_count():
    print("\n  ── Article View Count ──")
    cursor.execute("""
        SELECT a.Title, COUNT(*) 
        FROM article_view av
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY a.Title
    """)
    print_table(["Article Title", "Views"], cursor.fetchall(), col_width=35)


def author_views_by_age():
    print("\n  ── Views by Age Category ──")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                ELSE '55+'
            END AS Age_Category,
            a.Title AS Article_Name,
            COUNT(*) AS Number_of_Views
        FROM `article_view` av
        JOIN `user` u ON av.User_id = u.User_id
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY Age_Category, a.Title
        ORDER BY Age_Category, Number_of_Views DESC
    """)
    print_table(["Age_Category", "Article_Name", "Views"], cursor.fetchall(), col_width=30)


# ─────────────────────────────────────────────
#  ADMIN PORTAL
# ─────────────────────────────────────────────
def admin_portal():
    while True:
        choice = menu("🔧  ADMIN PORTAL", [
            "Manage Users",
            "Manage Authors",
            "Manage Articles",
            "Manage Categories",
            "Manage Tags",
            "Manage Media",
            "Manage Comments",
            "Manage Search Logs",
            "View Count",
            "Views by Age Category",
            "Reports",
        ])
        if choice == 0:
            break
        elif choice == 1:
            admin_users()
        elif choice == 2:
            admin_authors()
        elif choice == 3:
            admin_articles()
        elif choice == 4:
            admin_categories()
        elif choice == 5:
            admin_tags()
        elif choice == 6:
            admin_media()
        elif choice == 7:
            admin_comments()
        elif choice == 8:
            admin_search_logs()
        elif choice == 9:
            admin_view_count()
        elif choice == 10:
            admin_views_by_age()
        elif choice == 11:
            admin_reports()


# ── Users ──
def admin_users():
    while True:
        choice = menu("Admin › Users", ["List All", "Add", "Update", "Delete", "Search"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT User_id, Name, Email, DOB FROM `user`")
            print_table(["User_id", "Name", "Email", "DOB"], cursor.fetchall())
        elif choice == 2:
            uid   = input_prompt("User ID")
            name  = input_prompt("Name")
            email = input_prompt("Email")
            dob   = input_prompt("DOB (YYYY-MM-DD)")
            if not uid:
                print("  [Error] User ID is required.")
                continue
            execute("INSERT INTO `user`(User_id, Name, Email, DOB) VALUES (%s,%s,%s,%s)",
                    (uid, name, email, dob))
            print("  ✓ User added.")
        elif choice == 3:
            uid   = input_prompt("User ID to update")
            name  = input_prompt("New Name")
            email = input_prompt("New Email")
            dob   = input_prompt("New DOB (YYYY-MM-DD)")
            execute("UPDATE `user` SET Name=%s, Email=%s, DOB=%s WHERE User_id=%s",
                    (name, email, dob, uid))
            print("  ✓ User updated.")
        elif choice == 4:
            uid = input_prompt("User ID to delete")
            if not uid:
                print("  [Error] User ID is required.")
                continue
            confirm = input(f"  Delete user {uid} and all related records? (yes/no): ").strip().lower()
            if confirm == "yes":
                execute("DELETE FROM `comment` WHERE User_id=%s",     (uid,))
                execute("DELETE FROM `search_log` WHERE User_id=%s",  (uid,))
                execute("DELETE FROM `article_view` WHERE User_id=%s",(uid,))
                execute("DELETE FROM `user` WHERE User_id=%s",        (uid,))
                print(f"  ✓ User {uid} and related records deleted.")
        elif choice == 5:
            term = input_prompt("Search term (ID / Name / Email)")
            cursor.execute(
                "SELECT User_id, Name, Email, DOB FROM `user` WHERE CONCAT(User_id, Name, Email) LIKE %s",
                ('%' + term + '%',))
            print_table(["User_id", "Name", "Email", "DOB"], cursor.fetchall())


# ── Authors ──
def admin_authors():
    while True:
        choice = menu("Admin › Authors", ["List All", "Add", "Update", "Delete", "Search"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT Author_Id, Name, Bio, Email FROM `author`")
            print_table(["Author_Id", "Name", "Bio", "Email"], cursor.fetchall())
        elif choice == 2:
            aid   = input_prompt("Author ID")
            name  = input_prompt("Name")
            bio   = input_prompt("Bio")
            email = input_prompt("Email")
            if not name:
                print("  [Error] Name is required.")
                continue
            if execute("INSERT INTO `author`(Author_Id, Name, Bio, Email) VALUES (%s,%s,%s,%s)",
                       (aid, name, bio, email)):
                print(f"  ✓ Author '{name}' registered.")
        elif choice == 3:
            aid   = input_prompt("Author ID to update")
            name  = input_prompt("New Name")
            bio   = input_prompt("New Bio")
            email = input_prompt("New Email")
            execute("UPDATE `author` SET Name=%s, Bio=%s, Email=%s WHERE Author_Id=%s",
                    (name, bio, email, aid))
            print("  ✓ Author updated.")
        elif choice == 4:
            aid = input_prompt("Author ID to delete")
            if not aid:
                print("  [Error] Author ID is required.")
                continue
            confirm = input(f"  Delete author {aid} and all their articles/media? (yes/no): ").strip().lower()
            if confirm == "yes":
                cursor.execute("SELECT Article_id FROM `article` WHERE Author_id=%s", (aid,))
                articles = cursor.fetchall()
                for (article_id,) in articles:
                    execute("DELETE FROM `media` WHERE Article_id=%s",            (article_id,))
                    execute("DELETE FROM `comment` WHERE Article_id=%s",          (article_id,))
                    execute("DELETE FROM `article_tag` WHERE ARTICLE_ID=%s",      (article_id,))
                    execute("DELETE FROM `article_category` WHERE Article_ID=%s", (article_id,))
                    execute("DELETE FROM `article_view` WHERE Article_id=%s",     (article_id,))
                execute("DELETE FROM `article` WHERE Author_id=%s", (aid,))
                execute("DELETE FROM `author` WHERE Author_Id=%s",  (aid,))
                print(f"  ✓ Author {aid} and all related records deleted.")
        elif choice == 5:
            term = input_prompt("Search term (ID / Name / Email)")
            cursor.execute(
                "SELECT Author_Id, Name, Bio, Email FROM `author` WHERE CONCAT(Author_Id, Name, Bio, Email) LIKE %s",
                ('%' + term + '%',))
            print_table(["Author_Id", "Name", "Bio", "Email"], cursor.fetchall())


# ── Articles ──
def admin_articles():
    while True:
        choice = menu("Admin › Articles", ["List All", "Add", "Update", "Delete"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT Article_id, Title, Content FROM `article`")
            print_table(["Article_id", "Title", "Content"], cursor.fetchall(), col_width=35)
        elif choice == 2:
            aid     = input_prompt("Article ID")
            title   = input_prompt("Title")
            content = input_prompt("Content")
            execute("INSERT INTO `article`(Article_id,Title,Content,Published_Date,Author_id) VALUES (%s,%s,%s,%s,%s)",
                    (aid, title, content, str(datetime.date.today()), "Au001"))
            print("  ✓ Article added.")
        elif choice == 3:
            aid     = input_prompt("Article ID to update")
            title   = input_prompt("New Title")
            content = input_prompt("New Content")
            execute("UPDATE `article` SET Title=%s, Content=%s WHERE Article_id=%s",
                    (title, content, aid))
            print("  ✓ Article updated.")
        elif choice == 4:
            aid = input_prompt("Article ID to delete")
            if not aid:
                print("  [Error] Article ID is required.")
                continue
            confirm = input(f"  Delete article {aid} and all related records? (yes/no): ").strip().lower()
            if confirm == "yes":
                execute("DELETE FROM `media` WHERE Article_id=%s",            (aid,))
                execute("DELETE FROM `comment` WHERE Article_id=%s",          (aid,))
                execute("DELETE FROM `article_tag` WHERE ARTICLE_ID=%s",      (aid,))
                execute("DELETE FROM `article_category` WHERE Article_ID=%s", (aid,))
                execute("DELETE FROM `article_view` WHERE Article_id=%s",     (aid,))
                execute("DELETE FROM `article` WHERE Article_id=%s",          (aid,))
                print(f"  ✓ Article {aid} and related records deleted.")


# ── Categories ──
def admin_categories():
    while True:
        choice = menu("Admin › Categories", ["List All", "Add"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT * FROM category")
            print_table(["Category_id", "Name", "Description"], cursor.fetchall())
        elif choice == 2:
            cid  = generate_id("category", "Category_Id", "C")
            print(f"  Auto-generated Category ID: {cid}")
            name = input_prompt("Category Name")
            if execute("INSERT INTO category VALUES (%s,%s,%s)", (cid, name, "")):
                print(f"  ✓ Category '{name}' added.")


# ── Tags ──
def admin_tags():
    while True:
        choice = menu("Admin › Tags", ["List All", "Add"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT * FROM `tag`")
            print_table(["Tag_Id", "Name"], cursor.fetchall())
        elif choice == 2:
            tid  = generate_id("tag", "Tag_Id", "T")
            print(f"  Auto-generated Tag ID: {tid}")
            name = input_prompt("Tag Name")
            if not name:
                print("  [Error] Tag Name is required.")
                continue
            if execute("INSERT INTO `tag` VALUES (%s,%s)", (tid, name)):
                print(f"  ✓ Tag '{name}' added.")


# ── Media ──
def admin_media():
    while True:
        choice = menu("Admin › Media", ["List All", "Add", "Update", "Delete", "Search by URL"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT Media_id, Article_id, URL FROM `media`")
            print_table(["Media_id", "Article_id", "URL"], cursor.fetchall(), col_width=35)
        elif choice == 2:
            media_map = load_map("SELECT Article_id, Title FROM `article`")
            mid       = input_prompt("Media ID")
            art_id    = pick_from_map("Article", media_map)
            url       = input_prompt("File Path / URL")
            execute("INSERT INTO `media`(Media_id, Type, URL, Article_id) VALUES (%s,%s,%s,%s)",
                    (mid, "Image", url, art_id))
            print("  ✓ Media added.")
        elif choice == 3:
            media_map = load_map("SELECT Article_id, Title FROM `article`")
            mid       = input_prompt("Media ID to update")
            art_id    = pick_from_map("Article", media_map)
            url       = input_prompt("New File Path / URL")
            execute("UPDATE `media` SET Article_id=%s, URL=%s WHERE Media_id=%s",
                    (art_id, url, mid))
            print("  ✓ Media updated.")
        elif choice == 4:
            mid = input_prompt("Media ID to delete")
            execute("DELETE FROM `media` WHERE Media_id=%s", (mid,))
            print("  ✓ Media deleted.")
        elif choice == 5:
            term = input_prompt("Search URL keyword")
            cursor.execute("SELECT Media_id, Article_id, URL FROM `media` WHERE URL LIKE %s",
                           ('%' + term + '%',))
            print_table(["Media_id", "Article_id", "URL"], cursor.fetchall(), col_width=35)


# ── Comments ──
def admin_comments():
    while True:
        choice = menu("Admin › Comments", ["List All", "Filter by Comment ID", "Delete a Comment"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("""
                SELECT c.Comment_id, c.User_id, u.Name, c.Article_id, a.Title, c.Content, c.Comment_date
                FROM `comment` c
                JOIN `user` u ON c.User_id = u.User_id
                JOIN `article` a ON c.Article_id = a.Article_id
                ORDER BY c.Comment_id ASC
            """)
            print_table(["Comment_id", "User_id", "User", "Article_id", "Article", "Content", "Date"],
                        cursor.fetchall(), col_width=22)
        elif choice == 2:
            term = input_prompt("Comment ID filter")
            cursor.execute("""
                SELECT c.Comment_id, c.User_id, u.Name, c.Article_id, a.Title, c.Content, c.Comment_date
                FROM `comment` c
                JOIN `user` u ON c.User_id = u.User_id
                JOIN `article` a ON c.Article_id = a.Article_id
                WHERE c.Comment_id LIKE %s ORDER BY c.Comment_id ASC
            """, ('%' + term + '%',))
            print_table(["Comment_id", "User_id", "User", "Article_id", "Article", "Content", "Date"],
                        cursor.fetchall(), col_width=22)
        elif choice == 3:
            cid = input_prompt("Comment ID to delete")
            execute("DELETE FROM `comment` WHERE Comment_id=%s", (cid,))
            print("  ✓ Comment deleted.")


# ── Search Logs ──
def admin_search_logs():
    while True:
        choice = menu("Admin › Search Logs", ["List All", "Filter by Query", "Delete a Log Entry"])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT Log_id, Query_Text, Search_date, User_id FROM `search_log`")
            print_table(["Log_id", "Query_Text", "Search_date", "User_id"], cursor.fetchall())
        elif choice == 2:
            term = input_prompt("Query filter")
            cursor.execute(
                "SELECT Log_id, Query_Text, Search_date, User_id FROM `search_log` WHERE Query_Text LIKE %s",
                ('%' + term + '%',))
            print_table(["Log_id", "Query_Text", "Search_date", "User_id"], cursor.fetchall())
        elif choice == 3:
            lid = input_prompt("Log ID to delete")
            execute("DELETE FROM `search_log` WHERE Log_id=%s", (lid,))
            print("  ✓ Log entry deleted.")


# ── View Count ──
def admin_view_count():
    print("\n  ── Article View Count ──")
    cursor.execute("""
        SELECT a.Title, COUNT(*) 
        FROM article_view av
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY a.Title
    """)
    print_table(["Article Title", "Views"], cursor.fetchall(), col_width=35)


# ── Views by Age ──
def admin_views_by_age():
    print("\n  ── Views by Age Category ──")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                ELSE '55+'
            END AS Age_Category,
            a.Title AS Article_Name,
            COUNT(*) AS Number_of_Views
        FROM `article_view` av
        JOIN `user` u ON av.User_id = u.User_id
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY Age_Category, a.Title
        ORDER BY Age_Category, Number_of_Views DESC
    """)
    print_table(["Age_Category", "Article_Name", "Views"], cursor.fetchall(), col_width=30)


# ── Reports ──
def admin_reports():
    while True:
        choice = menu("Admin › Reports (text output)", [
            "Article Views Summary",
            "Comments per Article",
            "User Activity (Comments per User)",
            "Articles per Category",
            "Tag Usage",
            "Media per Article",
            "Most Popular Article per Age Group",
            "Total Views per Age Group",
            "Most Used Search Keyword per Age Group",
            "Age Group vs Category Preference",
        ])
        if choice == 0:
            break
        elif choice == 1:
            cursor.execute("SELECT Article_id, COUNT(*) FROM `article_view` GROUP BY Article_id")
            print_table(["Article_id", "Views"], cursor.fetchall())
        elif choice == 2:
            cursor.execute("SELECT Article_id, COUNT(*) FROM `comment` GROUP BY Article_id")
            print_table(["Article_id", "Comments"], cursor.fetchall())
        elif choice == 3:
            cursor.execute("SELECT User_id, COUNT(*) FROM `comment` GROUP BY User_id")
            print_table(["User_id", "Comments"], cursor.fetchall())
        elif choice == 4:
            cursor.execute("SELECT Category_ID, COUNT(*) FROM `article_category` GROUP BY Category_ID")
            print_table(["Category_ID", "Articles"], cursor.fetchall())
        elif choice == 5:
            cursor.execute("""
                SELECT t.Name, COUNT(*) 
                FROM `article_tag` at_ JOIN `tag` t ON at_.TAG_ID = t.Tag_ID
                GROUP BY t.Name ORDER BY COUNT(*) DESC
            """)
            print_table(["Tag Name", "Articles"], cursor.fetchall())
        elif choice == 6:
            cursor.execute("""
                SELECT a.Title, COUNT(*) 
                FROM `media` m JOIN `article` a ON m.Article_id = a.Article_id
                GROUP BY a.Title ORDER BY COUNT(*) DESC
            """)
            print_table(["Article Title", "Media Count"], cursor.fetchall(), col_width=35)
        elif choice == 7:
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category, a.Title, COUNT(*) AS Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                JOIN `article` a ON av.Article_id = a.Article_id
                GROUP BY Age_Category, a.Title ORDER BY Age_Category, Views DESC
            """)
            rows = cursor.fetchall()
            best = {}
            for age, title, views in rows:
                if age not in best:
                    best[age] = (title, views)
            print_table(["Age Group", "Most Popular Article", "Views"],
                        [(age, *val) for age, val in best.items()])
        elif choice == 8:
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category, COUNT(*) AS Total_Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                GROUP BY Age_Category ORDER BY Age_Category
            """)
            print_table(["Age Group", "Total Views"], cursor.fetchall())
        elif choice == 9:
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category, s.Query_Text, COUNT(*) AS Search_Count
                FROM `search_log` s
                JOIN `user` u ON s.User_id = u.User_id
                GROUP BY Age_Category, s.Query_Text
                ORDER BY Age_Category, Search_Count DESC
            """)
            rows = cursor.fetchall()
            best = {}
            for age, keyword, count in rows:
                if age not in best:
                    best[age] = (keyword, count)
            print_table(["Age Group", "Top Keyword", "Count"],
                        [(age, *val) for age, val in best.items()])
        elif choice == 10:
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category, c.Name AS Category_Name, COUNT(*) AS Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                JOIN `article` a ON av.Article_id = a.Article_id
                JOIN `article_category` ac ON a.Article_id = ac.Article_ID
                JOIN `category` c ON ac.Category_ID = c.Category_id
                GROUP BY Age_Category, c.Name
                ORDER BY Age_Category, Views DESC
            """)
            print_table(["Age Group", "Category", "Views"], cursor.fetchall())


# ─────────────────────────────────────────────
#  MAIN / HOME
# ─────────────────────────────────────────────
def main():
    print("\n" + "═" * 50)
    print("       UOM NEWS PORTAL  — CLI Version")
    print("═" * 50)
    while True:
        choice = menu("HOME — Select Portal", [
            "👤  User Portal",
            "✍   Author Portal",
            "🔧  Admin Portal",
        ])
        if choice == 0:
            print("\n  Goodbye!\n")
            break
        elif choice == 1:
            user_portal()
        elif choice == 2:
            author_portal()
        elif choice == 3:
            admin_portal()


if __name__ == "__main__":
    try:
        main()
    finally:
        cursor.close()
        conn.close()
