from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    """
    Mixin providing an integer primary key with auto-increment.

    This mixin can be used to add a primary key field (`id`) to SQLAlchemy models.

    Attributes:
        id (Mapped[int]): The primary key column, auto-incremented.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
