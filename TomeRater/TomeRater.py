class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("E-mail address updated.")

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        sum = 0
        num_rated_books = 0
        for book in self.books.keys():
            if self.books[book] != None:
                sum += self.books[book]
                num_rated_books += 1
        return sum / num_rated_books

    def __repr__(self):
        return "User {name}, e-mail: {address}, books read: {num_books}".format(name=self.name, address=self.email, num_books=len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

class Book():

    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Updated ISBN for {title}".format(title=self.title))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        if len(self.ratings) == 0:
            return None
        sum = 0
        for rating in self.ratings:
                sum += rating
        return sum / len(self.ratings)

    def __repr__(self):
        return self.title

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn and self.price == other_book.price

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "Users: \n{users}\n\nBooks: \n{books}".format(users=self.users, books=self.books)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.users == other.users and self.books == other.books
        return False

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print("No user with e-mail {email}!".format(email=email))
        else:
            self.users[email].read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("Error: That user already exists.")
        else:
            user = User(name, email)
            self.users[email] = user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def highest_rated_book(self):
        highest_rated = None
        highest_rating = 0
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > highest_rating:
                highest_rated = book                
                highest_rating = rating
        return highest_rated

    def most_positive_user(self):
        positive_user = None
        highest_rating = 0
        for user in self.users.values():
            avg_user_rating = user.get_average_rating()
            if avg_user_rating > highest_rating:
                positive_user = user
                highest_rating = avg_user_rating
        return positive_user

    def most_read_book(self):
        read_most = None
        read_count = 0
        for book in self.books.keys():
            if self.books[book] > read_count:
                read_count = self.books[book]
            if self.books[book] == read_count:
                read_most = book
        return read_most


Tome_Rater = TomeRater()

# Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678, 5.00)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345, 10.00)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452, 15.00)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938, 20.00)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010, 25.00)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000, 30.00)

# Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

# Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

# Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)


# Test Print Functions
print("Catalog:")
Tome_Rater.print_catalog()
print("Users:")
Tome_Rater.print_users()

print("Most positive user:")
print(Tome_Rater.most_positive_user())
print("Highest rated book:")
print(Tome_Rater.highest_rated_book())
print("Most read book:")
print(Tome_Rater.most_read_book())

#Testing the Print Tome Rater object scenario...unsure on this.
print(Tome_Rater)
#print()
