# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.ng_word import NgWords  # noqa
from app.models.group import Groups  # noqa