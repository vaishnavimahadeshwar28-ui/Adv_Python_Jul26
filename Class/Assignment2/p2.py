class Book:

    def __init__(self, book_id, title, author, total_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow_book(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            print("Book borrowed successfully.")
        else:
            print("No copies available.")

    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            print("Book returned successfully.")
        else:
            print("All copies are already in the library.")

    def display_details(self):
        print("Book ID :", self.book_id)
        print("Title :", self.title)
        print("Author :", self.author)
        print("Available Copies :", self.available_copies, "/", self.total_copies)

b1=Book(101, "Advanced Python Programming", "Vaishnavi", 10)

b1.display_details()

b1.borrow_book()
b1.borrow_book()

b1.display_details()

b1.borrow_book()
b1.borrow_book()

b1.return_book()

b1.display_details()
