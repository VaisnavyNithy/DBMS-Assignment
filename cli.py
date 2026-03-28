import mysql.connector
import datetime

# ================= DATABASE =================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uomnewssportal"
)
cursor = conn.cursor()

# ================= UTIL =================
def execute(query, params=()):
    try:
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f"  [DB Error] {e}")

def generate_id(table, column, prefix):
    cursor.execute(f"SELECT MAX({column}) FROM {table}")
    result = cursor.fetchone()[0]
    if result is None:
        return prefix + "001"
    num = int(result.replace(prefix, ""))
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

def print_separator(char="─", width=60):
    print(char * width)

def print_header(title):
    print_separator("═")
    print(f"  {title}")
    print_separator("═")

def print_table(headers, rows, col_width=20):
    fmt = "  " + "  ".join(f"{{:<{col_width}}}" for _ in headers)
    print_separator()
    print(fmt.format(*[str(h) for h in headers]))
    print_separator()
    if not rows:
        print("  (no records found)")
    for row in rows:
        print(fmt.format(*[str(c)[:col_width] for c in row]))
    print_separator()

def pick_from_map(name_map, prompt="Select"):
    names = list(name_map.keys())
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n}")
    choice = input(f"  {prompt} (number): ").strip()
    try:
        return names[int(choice) - 1], name_map[names[int(choice) - 1]]
    except (ValueError, IndexError):
        print("  Invalid choice.")
        return None, None

def pause():
    input("\n  Press Enter to continue...")

# =========================================================
#  USER PORTAL
# =========================================================
def user_portal():
    while True:
        print_header("👤  USER PORTAL")
        print("  1. Register / View Users")
        print("  2. View Articles")
        print("  3. Comment on Articles")
        print("  4. View Tags")
        print("  5. View Categories")
        print("  6. Search Log")
        print("  0. Back to Home")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            user_register()
        elif choice == "2":
            user_view_articles()
        elif choice == "3":
            user_comment()
        elif choice == "4":
            user_view_tags()
        elif choice == "5":
            user_view_categories()
        elif choice == "6":
            user_search_log()
        elif choice == "0":
            break
        else:
            print("  Invalid option.")

# ---------- REGISTER ----------
def user_register():
    while True:
        print_header("Register / View Users")
        print("  1. Register New User")
        print("  2. View All Users")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            new_id = generate_id("user", "User_id", "U")
            print(f"\n  Auto-generated User ID: {new_id}")
            name  = input("  Name  : ").strip()
            email = input("  Email : ").strip()
            if not name:
                print("  Name is required.")
                pause()
                continue
            execute("INSERT INTO `user`(User_id, Name, Email) VALUES (%s,%s,%s)",
                    (new_id, name, email))
            print(f"  ✓ User registered with ID {new_id}!")
            pause()

        elif choice == "2":
            cursor.execute("SELECT User_id, Name, Email FROM `user`")
            print_table(["User_id", "Name", "Email"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- VIEW ARTICLES ----------
def user_view_articles():
    print_header("View Articles")
    keyword = input("  Search keyword (leave blank for all): ").strip()
    if keyword:
        cursor.execute(
            "SELECT Article_id, Title, Content, Published_Date, Author_id FROM `article` "
            "WHERE Title LIKE %s OR Content LIKE %s",
            (f'%{keyword}%', f'%{keyword}%')
        )
    else:
        cursor.execute("SELECT Article_id, Title, Content, Published_Date, Author_id FROM `article`")
    print_table(["Article_id", "Title", "Content", "Published_Date", "Author_id"], cursor.fetchall())
    pause()

# ---------- COMMENT ----------
def user_comment():
    while True:
        print_header("Comment on Articles")
        print("  1. Post Comment")
        print("  2. View All Comments")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            u_user_map    = load_map("SELECT User_id, Name FROM `user`")
            u_article_map = load_map("SELECT Article_id, Title FROM `article`")

            if not u_user_map:
                print("  No users found. Please register first.")
                pause()
                continue
            if not u_article_map:
                print("  No articles found.")
                pause()
                continue

            new_id = generate_id("comment", "Comment_id", "C")
            print(f"\n  Auto-generated Comment ID: {new_id}")

            print("\n  Select your name:")
            _, user_id = pick_from_map(u_user_map, "Your name")
            if not user_id:
                pause()
                continue

            print("\n  Select article:")
            _, article_id = pick_from_map(u_article_map, "Article")
            if not article_id:
                pause()
                continue

            text = input("  Your comment: ").strip()
            date = input(f"  Date [{datetime.date.today()}]: ").strip() or str(datetime.date.today())

            execute(
                "INSERT INTO `comment`(Comment_id, Article_id, User_id, Content, Comment_date) "
                "VALUES (%s,%s,%s,%s,%s)",
                (new_id, article_id, user_id, text, date)
            )
            print("  ✓ Comment posted!")
            pause()

        elif choice == "2":
            cursor.execute("""
                SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
                FROM `comment` c
                JOIN `user` u ON c.User_id = u.User_id
                JOIN `article` a ON c.Article_id = a.Article_id
            """)
            print_table(["Comment_id", "User", "Article", "Comment", "Date"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- TAGS ----------
def user_view_tags():
    print_header("Tags")
    cursor.execute("SELECT * FROM tag")
    print_table(["Tag_id", "Name"], cursor.fetchall())
    pause()

# ---------- CATEGORIES ----------
def user_view_categories():
    print_header("Categories")
    cursor.execute("SELECT Category_id, Name FROM category")
    print_table(["Category_id", "Name"], cursor.fetchall())
    pause()

# ---------- SEARCH LOG ----------
def user_search_log():
    while True:
        print_header("Search Log")
        print("  1. Search & Save")
        
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            sl_user_map = load_map("SELECT User_id, Name FROM `user`")
            if not sl_user_map:
                print("  No users found.")
                pause()
                continue

            log_id = generate_log_id()
            print(f"\n  Auto-generated Log ID: {log_id}")
            query  = input("  Search query : ").strip()
            if not query:
                print("  Query is required.")
                pause()
                continue

            print("\n  Select your name:")
            _, user_id = pick_from_map(sl_user_map, "Your name")
            if not user_id:
                pause()
                continue

            date = input(f"  Date [{datetime.date.today()}]: ").strip() or str(datetime.date.today())
            execute(
                "INSERT INTO `search_log`(Log_id, Query_Text, Search_date, User_id) VALUES (%s,%s,%s,%s)",
                (log_id, query, date, user_id)
            )
            print(f"  ✓ Search saved (ID: {log_id}). Showing results:")
            cursor.execute(
                "SELECT Article_id, Title, Content, Published_Date, Author_id FROM article "
                "WHERE Title LIKE %s OR Content LIKE %s",
                (f'%{query}%', f'%{query}%')
            )
            print_table(["Article_id", "Title", "Content", "Date", "Author_id"], cursor.fetchall())
            pause()

      

        elif choice == "0":
            break


# =========================================================
#  AUTHOR PORTAL
# =========================================================
def author_portal():
    while True:
        print_header("✍  AUTHOR PORTAL")
        print("  1. Add Article")
        print("  2. Upload Media")
        print("  3. View Comments")
        print("  4. View Count")
        print("  5. Views by Age Category")
        print("  0. Back to Home")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            author_add_article()
        elif choice == "2":
            author_upload_media()
        elif choice == "3":
            author_view_comments()
        elif choice == "4":
            author_view_count()
        elif choice == "5":
            author_views_by_age()
        elif choice == "0":
            break
        else:
            print("  Invalid option.")

# ---------- ADD ARTICLE ----------
def author_add_article():
    while True:
        print_header("Add Article")
        print("  1. Add New Article")
        print("  2. View All Articles")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            author_map = load_map("SELECT Author_Id, Name FROM `author`")
            if not author_map:
                print("  No authors found in database.")
                pause()
                continue

            new_id = generate_id("article", "Article_id", "A")
            print(f"\n  Auto-generated Article ID: {new_id}")
            title   = input("  Title   : ").strip()
            content = input("  Content : ").strip()
            date    = input(f"  Published Date [{datetime.date.today()}]: ").strip() or str(datetime.date.today())

            print("\n  Select author:")
            _, author_id = pick_from_map(author_map, "Author")
            if not author_id:
                pause()
                continue

            if not title:
                print("  Title is required.")
                pause()
                continue

            execute(
                "INSERT INTO `article`(Article_id, Title, Content, Published_Date, Author_id) "
                "VALUES (%s,%s,%s,%s,%s)",
                (new_id, title, content, date, author_id)
            )
            print(f"  ✓ Article added (ID: {new_id})!")
            pause()

        elif choice == "2":
            cursor.execute("SELECT Article_id, Title, Content, Published_Date, Author_id FROM `article`")
            print_table(["Article_id", "Title", "Content", "Date", "Author_id"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- UPLOAD MEDIA ----------
def author_upload_media():
    while True:
        print_header("Upload Media")
        print("  1. Upload New Media")
        print("  2. View All Media")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            med_art_map = load_map("SELECT Article_id, Title FROM `article`")
            if not med_art_map:
                print("  No articles found.")
                pause()
                continue

            new_id = generate_id("media", "Media_id", "M")
            print(f"\n  Auto-generated Media ID: {new_id}")
            mtype = input("  Type (Image/Video): ").strip()
            url   = input("  URL/Path          : ").strip()

            print("\n  Select article:")
            _, article_id = pick_from_map(med_art_map, "Article")
            if not article_id:
                pause()
                continue

            execute("INSERT INTO `media`(Media_id, Type, URL, Article_id) VALUES (%s,%s,%s,%s)",
                    (new_id, mtype, url, article_id))
            print(f"  ✓ Media uploaded (ID: {new_id})!")
            pause()

        elif choice == "2":
            cursor.execute("SELECT Media_id, Type, URL, Article_id FROM `media`")
            print_table(["Media_id", "Type", "URL", "Article_id"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- VIEW COMMENTS ----------
def author_view_comments():
    print_header("View Comments")
    keyword = input("  Filter by article title (blank for all): ").strip()
    if keyword:
        cursor.execute("""
            SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
            FROM `comment` c
            JOIN `user` u ON c.User_id = u.User_id
            JOIN `article` a ON c.Article_id = a.Article_id
            WHERE a.Title LIKE %s
        """, (f'%{keyword}%',))
    else:
        cursor.execute("""
            SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
            FROM `comment` c
            JOIN `user` u ON c.User_id = u.User_id
            JOIN `article` a ON c.Article_id = a.Article_id
        """)
    print_table(["Comment_id", "User", "Article", "Comment", "Date"], cursor.fetchall())
    pause()

# ---------- VIEW COUNT ----------
def author_view_count():
    print_header("Article View Count")
    cursor.execute("SELECT Article_id, COUNT(*) FROM article_view GROUP BY Article_id")
    print_table(["Article_id", "Views"], cursor.fetchall())
    pause()

# ---------- VIEWS BY AGE ----------
def author_views_by_age():
    print_header("Views by Age Category")
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
            COUNT(*) AS Views
        FROM `article_view` av
        JOIN `user` u ON av.User_id = u.User_id
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY Age_Category, a.Title
        ORDER BY Age_Category, Views DESC
    """)
    print_table(["Age Category", "Article", "Views"], cursor.fetchall())
    pause()


# =========================================================
#  ADMIN PORTAL
# =========================================================
def admin_portal():
    while True:
        print_header("🔧  ADMIN PORTAL")
        print("  1.  Users")
        print("  2.  Categories")
        print("  3.  Tags")
        print("  4.  Articles")
        print("  5.  Comments")
        print("  6.  Media")
        print("  7.  Search Log")
        print("  8.  View Count")
        print("  9.  Views by Age")
        print("  10. Reports")
        print("  0.  Back to Home")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            admin_users()
        elif choice == "2":
            admin_categories()
        elif choice == "3":
            admin_tags()
        elif choice == "4":
            admin_articles()
        elif choice == "5":
            admin_comments()
        elif choice == "6":
            admin_media()
        elif choice == "7":
            admin_search_log()
        elif choice == "8":
            admin_view_count()
        elif choice == "9":
            admin_views_by_age()
        elif choice == "10":
            admin_reports()
        elif choice == "0":
            break
        else:
            print("  Invalid option.")

# ---------- USERS ----------
def admin_users():
    while True:
        print_header("Admin — Users")
        print("  1. Add User")
        print("  2. Update User")
        print("  3. Delete User")
        print("  4. Search / View Users")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            uid   = input("  User ID : ").strip()
            name  = input("  Name    : ").strip()
            email = input("  Email   : ").strip()
            dob   = input("  DOB (YYYY-MM-DD): ").strip()
            execute("INSERT INTO `user`(User_id, Name, Email, DOB) VALUES (%s,%s,%s,%s)",
                    (uid, name, email, dob))
            print("  ✓ User added.")
            pause()

        elif choice == "2":
            uid   = input("  User ID to update: ").strip()
            name  = input("  New Name  : ").strip()
            email = input("  New Email : ").strip()
            dob   = input("  New DOB   : ").strip()
            execute("UPDATE `user` SET Name=%s, Email=%s, DOB=%s WHERE User_id=%s",
                    (name, email, dob, uid))
            print("  ✓ User updated.")
            pause()

        elif choice == "3":
            uid = input("  User ID to delete: ").strip()
            execute("DELETE FROM `user` WHERE User_id=%s", (uid,))
            print("  ✓ User deleted.")
            pause()

        elif choice == "4":
            keyword = input("  Search (blank for all): ").strip()
            if keyword:
                cursor.execute(
                    "SELECT User_id, Name, Email, DOB FROM `user` "
                    "WHERE CONCAT(User_id, Name, Email) LIKE %s",
                    (f'%{keyword}%',)
                )
            else:
                cursor.execute("SELECT User_id, Name, Email, DOB FROM `user`")
            print_table(["User_id", "Name", "Email", "DOB"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- CATEGORIES ----------
def admin_categories():
    while True:
        print_header("Admin — Categories")
        print("  1. Add Category")
        print("  2. View All Categories")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            new_id = generate_id("category", "Category_Id", "C")
            print(f"  Auto-generated Category ID: {new_id}")
            name = input("  Category Name: ").strip()
            execute("INSERT INTO category VALUES (%s,%s,%s)", (new_id, name, ""))
            print("  ✓ Category added.")
            pause()

        elif choice == "2":
            cursor.execute("SELECT * FROM category")
            print_table(["Category_id", "Name"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- TAGS ----------
def admin_tags():
    while True:
        print_header("Admin — Tags")
        print("  1. Add Tag")
        print("  2. View All Tags")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            new_id = generate_id("tag", "Tag_Id", "T")
            print(f"  Auto-generated Tag ID: {new_id}")
            name = input("  Tag Name: ").strip()
            if not name:
                print("  Tag name is required.")
                pause()
                continue
            execute("INSERT INTO `tag` VALUES (%s,%s)", (new_id, name))
            print("  ✓ Tag added.")
            pause()

        elif choice == "2":
            cursor.execute("SELECT * FROM `tag`")
            print_table(["Tag_id", "Name"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- ARTICLES ----------
def admin_articles():
    while True:
        print_header("Admin — Articles")
        print("  1. Add Article")
        print("  2. Update Article")
        print("  3. Delete Article")
        print("  4. View All Articles")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            aid     = input("  Article ID : ").strip()
            title   = input("  Title      : ").strip()
            content = input("  Content    : ").strip()
            execute(
                "INSERT INTO `article`(Article_id,Title,Content,Published_Date,Author_id) "
                "VALUES (%s,%s,%s,%s,%s)",
                (aid, title, content, str(datetime.date.today()), "Au001")
            )
            print("  ✓ Article added.")
            pause()

        elif choice == "2":
            aid     = input("  Article ID to update: ").strip()
            title   = input("  New Title  : ").strip()
            content = input("  New Content: ").strip()
            execute("UPDATE `article` SET Title=%s, Content=%s WHERE Article_id=%s",
                    (title, content, aid))
            print("  ✓ Article updated.")
            pause()

        elif choice == "3":
            aid = input("  Article ID to delete: ").strip()
            execute("DELETE FROM `article` WHERE Article_id=%s", (aid,))
            print("  ✓ Article deleted.")
            pause()

        elif choice == "4":
            cursor.execute("SELECT Article_id, Title, Content FROM `article`")
            print_table(["Article_id", "Title", "Content"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- COMMENTS ----------
def admin_comments():
    while True:
        print_header("Admin — Comments")
        print("  1. Add Comment")
        print("  2. Update Comment")
        print("  3. Delete Comment")
        print("  4. Search / View Comments")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        user_map    = load_map("SELECT User_id, Name FROM `user`")
        article_map = load_map("SELECT Article_id, Title FROM `article`")

        if choice == "1":
            cid     = input("  Comment ID: ").strip()
            print("\n  Select user:")
            _, uid = pick_from_map(user_map)
            print("\n  Select article:")
            _, artid = pick_from_map(article_map)
            content = input("  Content: ").strip()
            date    = input(f"  Date [{datetime.date.today()}]: ").strip() or str(datetime.date.today())
            execute(
                "INSERT INTO `comment`(Comment_id, Article_id, User_id, Content, Comment_date) "
                "VALUES (%s,%s,%s,%s,%s)",
                (cid, artid, uid, content, date)
            )
            print("  ✓ Comment added.")
            pause()

        elif choice == "2":
            cid     = input("  Comment ID to update: ").strip()
            print("\n  Select new user:")
            _, uid = pick_from_map(user_map)
            print("\n  Select new article:")
            _, artid = pick_from_map(article_map)
            content = input("  New content: ").strip()
            date    = input(f"  New date [{datetime.date.today()}]: ").strip() or str(datetime.date.today())
            execute(
                "UPDATE `comment` SET User_id=%s, Article_id=%s, Content=%s, Comment_date=%s WHERE Comment_id=%s",
                (uid, artid, content, date, cid)
            )
            print("  ✓ Comment updated.")
            pause()

        elif choice == "3":
            cid = input("  Comment ID to delete: ").strip()
            execute("DELETE FROM `comment` WHERE Comment_id=%s", (cid,))
            print("  ✓ Comment deleted.")
            pause()

        elif choice == "4":
            keyword = input("  Search by content (blank for all): ").strip()
            if keyword:
                cursor.execute(
                    "SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date "
                    "FROM `comment` c "
                    "JOIN `user` u ON c.User_id = u.User_id "
                    "JOIN `article` a ON c.Article_id = a.Article_id "
                    "WHERE c.Content LIKE %s",
                    (f'%{keyword}%',)
                )
            else:
                cursor.execute("""
                    SELECT c.Comment_id, u.Name, a.Title, c.Content, c.Comment_date
                    FROM `comment` c
                    JOIN `user` u ON c.User_id = u.User_id
                    JOIN `article` a ON c.Article_id = a.Article_id
                """)
            print_table(["Comment_id", "User", "Article", "Content", "Date"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- MEDIA ----------
def admin_media():
    while True:
        print_header("Admin — Media")
        print("  1. Add Media")
        print("  2. Update Media")
        print("  3. Delete Media")
        print("  4. Search / View Media")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        media_map = load_map("SELECT Article_id, Title FROM `article`")

        if choice == "1":
            mid  = input("  Media ID: ").strip()
            print("\n  Select article:")
            _, artid = pick_from_map(media_map)
            url  = input("  File path/URL: ").strip()
            execute("INSERT INTO `media`(Media_id, Type, URL, Article_id) VALUES (%s,%s,%s,%s)",
                    (mid, "Image", url, artid))
            print("  ✓ Media added.")
            pause()

        elif choice == "2":
            mid  = input("  Media ID to update: ").strip()
            print("\n  Select new article:")
            _, artid = pick_from_map(media_map)
            url  = input("  New file path/URL: ").strip()
            execute("UPDATE `media` SET Article_id=%s, URL=%s WHERE Media_id=%s",
                    (artid, url, mid))
            print("  ✓ Media updated.")
            pause()

        elif choice == "3":
            mid = input("  Media ID to delete: ").strip()
            execute("DELETE FROM `media` WHERE Media_id=%s", (mid,))
            print("  ✓ Media deleted.")
            pause()

        elif choice == "4":
            keyword = input("  Search by URL (blank for all): ").strip()
            if keyword:
                cursor.execute(
                    "SELECT Media_id, Article_id, URL FROM `media` WHERE URL LIKE %s",
                    (f'%{keyword}%',)
                )
            else:
                cursor.execute("SELECT Media_id, Article_id, URL FROM `media`")
            print_table(["Media_id", "Article_id", "URL"], cursor.fetchall())
            pause()

        elif choice == "0":
            break

# ---------- SEARCH LOG ----------
def admin_search_log():
    while True:
        print_header("Admin — Search Log")
        print("  1. View / Filter Logs")
        print("  2. Delete a Log")
        print("  0. Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            keyword = input("  Filter by query (blank for all): ").strip()
            if keyword:
                cursor.execute(
                    "SELECT Log_id, Query_Text, Search_date, User_id FROM `search_log` WHERE Query_Text LIKE %s",
                    (f'%{keyword}%',)
                )
            else:
                cursor.execute("SELECT Log_id, Query_Text, Search_date, User_id FROM `search_log`")
            print_table(["Log_id", "Query", "Date", "User_id"], cursor.fetchall())
            pause()

        elif choice == "2":
            cursor.execute("SELECT Log_id, Query_Text, Search_date, User_id FROM `search_log`")
            print_table(["Log_id", "Query", "Date", "User_id"], cursor.fetchall())
            log_id = input("  Enter Log ID to delete: ").strip()
            if log_id:
                execute("DELETE FROM `search_log` WHERE Log_id=%s", (log_id,))
                print("  ✓ Log deleted.")
            pause()

        elif choice == "0":
            break

# ---------- VIEW COUNT ----------
def admin_view_count():
    print_header("Admin — View Count")
    cursor.execute("SELECT Article_id, COUNT(*) FROM article_view GROUP BY Article_id")
    print_table(["Article_id", "Views"], cursor.fetchall())
    pause()

# ---------- VIEWS BY AGE ----------
def admin_views_by_age():
    print_header("Admin — Views by Age Category")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                ELSE '55+'
            END AS Age_Category,
            a.Title,
            COUNT(*) AS Views
        FROM `article_view` av
        JOIN `user` u ON av.User_id = u.User_id
        JOIN `article` a ON av.Article_id = a.Article_id
        GROUP BY Age_Category, a.Title
        ORDER BY Age_Category, Views DESC
    """)
    print_table(["Age Category", "Article", "Views"], cursor.fetchall())
    pause()

# ---------- REPORTS (text-based summaries) ----------
def admin_reports():
    while True:
        print_header("Admin — Reports")
        print("  1.  Article Views Summary")
        print("  2.  Comments Distribution")
        print("  3.  User Activity (Comments per User)")
        print("  4.  Articles per Category")
        print("  5.  Tag Usage")
        print("  6.  Media per Article")
        print("  7.  Most Popular Article per Age Group")
        print("  8.  Total Views per Age Group")
        print("  9.  Most Used Search Keyword per Age Group")
        print("  10. Age Group vs Category Preference")
        print("  0.  Back")
        print_separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            cursor.execute("SELECT Article_id, COUNT(*) FROM `article_view` GROUP BY Article_id")
            print_table(["Article_id", "Views"], cursor.fetchall())
            pause()

        elif choice == "2":
            cursor.execute("SELECT Article_id, COUNT(*) FROM `comment` GROUP BY Article_id")
            print_table(["Article_id", "Comment Count"], cursor.fetchall())
            pause()

        elif choice == "3":
            cursor.execute("SELECT User_id, COUNT(*) FROM `comment` GROUP BY User_id")
            print_table(["User_id", "Comments"], cursor.fetchall())
            pause()

        elif choice == "4":
            cursor.execute("SELECT Category_ID, COUNT(*) FROM `article_category` GROUP BY Category_ID")
            print_table(["Category_id", "Article Count"], cursor.fetchall())
            pause()

        elif choice == "5":
            cursor.execute("""
                SELECT t.Name, COUNT(*) 
                FROM `article_tag` at_
                JOIN `tag` t ON at_.TAG_ID = t.Tag_ID
                GROUP BY t.Name ORDER BY COUNT(*) DESC
            """)
            print_table(["Tag Name", "Usage Count"], cursor.fetchall())
            pause()

        elif choice == "6":
            cursor.execute("""
                SELECT a.Title, COUNT(*) 
                FROM `media` m
                JOIN `article` a ON m.Article_id = a.Article_id
                GROUP BY a.Title ORDER BY COUNT(*) DESC
            """)
            print_table(["Article Title", "Media Count"], cursor.fetchall())
            pause()

        elif choice == "7":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category,
                    a.Title, COUNT(*) AS Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                JOIN `article` a ON av.Article_id = a.Article_id
                GROUP BY Age_Category, a.Title
                ORDER BY Age_Category, Views DESC
            """)
            rows = cursor.fetchall()
            best = {}
            for age, title, views in rows:
                if age not in best:
                    best[age] = (title, views)
            print_table(["Age Group", "Most Popular Article", "Views"],
                        [(age, *data) for age, data in best.items()])
            pause()

        elif choice == "8":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category,
                    COUNT(*) AS Total_Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                GROUP BY Age_Category ORDER BY Age_Category
            """)
            print_table(["Age Group", "Total Views"], cursor.fetchall())
            pause()

        elif choice == "9":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category,
                    s.Query_Text, COUNT(*) AS cnt
                FROM `search_log` s
                JOIN `user` u ON s.User_id = u.User_id
                GROUP BY Age_Category, s.Query_Text
                ORDER BY Age_Category, cnt DESC
            """)
            rows = cursor.fetchall()
            best = {}
            for age, kw, cnt in rows:
                if age not in best:
                    best[age] = (kw, cnt)
            print_table(["Age Group", "Top Keyword", "Count"],
                        [(age, *data) for age, data in best.items()])
            pause()

        elif choice == "10":
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 18 AND 25 THEN '18-25'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 26 AND 35 THEN '26-35'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 36 AND 45 THEN '36-45'
                        WHEN TIMESTAMPDIFF(YEAR, u.DOB, CURDATE()) BETWEEN 46 AND 55 THEN '46-55'
                        ELSE '55+'
                    END AS Age_Category,
                    c.Name AS Category_Name,
                    COUNT(*) AS Views
                FROM `article_view` av
                JOIN `user` u ON av.User_id = u.User_id
                JOIN `article` a ON av.Article_id = a.Article_id
                JOIN `article_category` ac ON a.Article_id = ac.Article_ID
                JOIN `category` c ON ac.Category_ID = c.Category_id
                GROUP BY Age_Category, c.Name
                ORDER BY Age_Category, Views DESC
            """)
            print_table(["Age Group", "Category", "Views"], cursor.fetchall())
            pause()

        elif choice == "0":
            break
        else:
            print("  Invalid option.")


# =========================================================
#  HOME / ENTRY POINT
# =========================================================
def home_screen():
    while True:
        print_header("UOM NEWS PORTAL")
        print("  1. 👤  User Portal")
        print("  2. ✍   Author Portal")
        print("  3. 🔧  Admin Portal")
        print("  0. Exit")
        print_separator()
        choice = input("  Select portal: ").strip()

        if choice == "1":
            user_portal()
        elif choice == "2":
            author_portal()
        elif choice == "3":
            admin_portal()
        elif choice == "0":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid option.")

if __name__ == "__main__":
    try:
        home_screen()
    finally:
        cursor.close()
        conn.close()
