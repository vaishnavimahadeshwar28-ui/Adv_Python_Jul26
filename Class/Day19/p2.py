# CRUD SQLAlchemyORM
from datetime import datetime


from sqlalchemy import create_engine, String, Integer, Float, DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)




# ============================================================
# DATABASE CONFIGURATION
# ============================================================


DATABASE_URL = "sqlite:///example.db"


engine = create_engine(
    DATABASE_URL,
    echo=False
)




# ============================================================
# DECLARATIVE BASE
# ============================================================


class Base(DeclarativeBase):
    pass




# ============================================================
# ORM MODELS
# ============================================================


class User(Base):
    """User ORM model."""


    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )


    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"age={self.age}, "
            f"city='{self.city}'"
            f")"
        )




class Product(Base):
    """Product ORM model."""


    __tablename__ = "products"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    def __repr__(self):
        return (
            f"Product("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"price={self.price}, "
            f"stock={self.stock}, "
            f"category='{self.category}'"
            f")"
        )




# ============================================================
# CREATE TABLES
# ============================================================


Base.metadata.create_all(engine)




# ============================================================
# SESSION CONFIGURATION
# ============================================================


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


session = SessionLocal()




# ============================================================
# CREATE OPERATIONS
# ============================================================


def create_users():
    """Create new users using the ORM."""


    user1 = User(
        name="Alice",
        age=30,
        city="New York"
    )


    user2 = User(
        name="Bob",
        age=25,
        city="Los Angeles"
    )


    user3 = User(
        name="Charlie",
        age=35,
        city="Chicago"
    )


    session.add_all([user1, user2, user3])
    session.commit()


    print(f"Created users:")
    print(f"  {user1}")
    print(f"  {user2}")
    print(f"  {user3}")


    return [user1, user2, user3]




def create_products():
    """Create new products using the ORM."""


    product1 = Product(
        name="Laptop",
        price=999.99,
        stock=10,
        category="Electronics"
    )


    product2 = Product(
        name="Mouse",
        price=29.99,
        stock=50,
        category="Electronics"
    )


    product3 = Product(
        name="Book",
        price=19.99,
        stock=100,
        category="Books"
    )


    session.add_all([product1, product2, product3])
    session.commit()


    print(f"\nCreated products:")
    print(f"  {product1}")
    print(f"  {product2}")
    print(f"  {product3}")


    return [product1, product2, product3]




# ============================================================
# READ OPERATIONS
# ============================================================


def query_users():
    """Query users using the ORM."""


    # Get all users
    all_users = session.query(User).all()
    print(f"\nAll users:")
    for user in all_users:
        print(f"  {user}")


    # Get the first user
    first_user = session.query(User).first()
    print(f"\nFirst user:")
    print(f"  {first_user}")


    # Get a user by primary key
    user = session.get(User, 2)
    print(f"\nUser with ID 2:")
    print(f"  {user}")


    # Filter users by city
    nyc_users = (
        session.query(User)
        .filter(User.city == "New York")
        .all()
    )


    print(f"\nUsers in New York:")
    for user in nyc_users:
        print(f"  {user}")


    # Filter using multiple conditions
    older_users = (
        session.query(User)
        .filter(
            User.age >= 25,
            User.city == "New York"
        )
        .all()
    )


    print(f"\nNew York users aged 25 or older:")
    for user in older_users:
        print(f"  {user}")


    # Filter using OR condition
    city_users = (
        session.query(User)
        .filter(
            (User.city == "New York") |
            (User.city == "Chicago")
        )
        .all()
    )


    print(f"\nUsers in New York or Chicago:")
    for user in city_users:
        print(f"  {user}")


    # Order users by age in descending order
    sorted_users = (
        session.query(User)
        .order_by(User.age.desc())
        .all()
    )


    print(f"\nUsers sorted by age:")
    for user in sorted_users:
        print(f"  {user}")


    # Limit results
    limited_users = (
        session.query(User)
        .limit(2)
        .all()
    )


    print(f"\nFirst two users:")
    for user in limited_users:
        print(f"  {user}")


    # Count users
    user_count = session.query(User).count()
    print(f"\nTotal users: {user_count}")


    # Select specific columns
    user_names = (
        session.query(User.name, User.city)
        .all()
    )


    print(f"\nUser names and cities:")
    for name, city in user_names:
        print(f"  Name: {name}, City: {city}")


    return all_users




def query_products():
    """Query products using the ORM."""


    # Products with stock greater than zero
    available_products = (
        session.query(Product)
        .filter(Product.stock > 0)
        .all()
    )


    print(f"\nAvailable products:")
    for product in available_products:
        print(f"  {product}")


    # Products with price greater than or equal to 50
    expensive_products = (
        session.query(Product)
        .filter(Product.price >= 50.00)
        .all()
    )


    print(f"\nProducts priced at 50 or more:")
    for product in expensive_products:
        print(f"  {product}")


    return available_products




# ============================================================
# UPDATE OPERATIONS
# ============================================================


def update_user():
    """Update a user using the ORM."""


    user = (
        session.query(User)
        .filter(User.name == "Bob")
        .first()
    )


    if user:
        print(f"\nBefore user update:")
        print(f"  {user}")


        user.age = 26
        user.city = "San Francisco"


        session.commit()


        print(f"After user update:")
        print(f"  {user}")


    else:
        print("\nUser Bob was not found.")




def update_product():
    """Update a product using the ORM."""


    product = (
        session.query(Product)
        .filter(Product.name == "Laptop")
        .first()
    )


    if product:
        print(f"\nBefore product update:")
        print(f"  {product}")


        product.stock += 5


        session.commit()


        print(f"After product update:")
        print(f"  {product}")


    else:
        print("\nLaptop was not found.")




# ============================================================
# DELETE OPERATIONS
# ============================================================


def delete_user():
    """Delete a user using the ORM."""


    user = (
        session.query(User)
        .filter(User.name == "Alice")
        .first()
    )


    if user:
        print(f"\nDeleting user:")
        print(f"  {user}")


        session.delete(user)
        session.commit()


        print("User deleted successfully.")


    else:
        print("\nUser Alice was not found.")




def delete_products_under_price():
    """Delete products priced below 25."""


    products = (
        session.query(Product)
        .filter(Product.price < 25.00)
        .all()
    )


    if products:
        for product in products:
            session.delete(product)


        session.commit()


        print(
            f"\nDeleted {len(products)} product(s) "
            f"priced below 25."
        )


    else:
        print("\nNo products were found below 25.")




# ============================================================
# ORM DEMONSTRATION
# ============================================================


def demonstrate_orm():
    """Demonstrate SQLAlchemy ORM operations."""


    print("=" * 60)
    print("SQLALCHEMY ORM DEMONSTRATION")
    print("=" * 60)


    # 1. Create data
    print("\nCREATE OPERATIONS")
    print("-" * 60)


    create_users()
    create_products()


    # 2. Read data
    print("\nREAD OPERATIONS")
    print("-" * 60)


    query_users()
    query_products()


    # 3. Update data
    print("\nUPDATE OPERATIONS")
    print("-" * 60)


    update_user()
    update_product()


    # 4. Delete data
    print("\nDELETE OPERATIONS")
    print("-" * 60)


    delete_user()
    delete_products_under_price()


    # 5. Final state
    print("\nFINAL DATABASE STATE")
    print("-" * 60)


    remaining_users = session.query(User).all()
    remaining_products = session.query(Product).all()


    print("Remaining users:")
    for user in remaining_users:
        print(f"  {user}")


    print("\nRemaining products:")
    for product in remaining_products:
        print(f"  {product}")




# ============================================================
# PROGRAM ENTRY POINT
# ============================================================


if __name__ == "__main__":
    try:
        demonstrate_orm()


    except Exception as error:
        session.rollback()
        print(f"\nAn error occurred: {error}")


    finally:
        session.close()