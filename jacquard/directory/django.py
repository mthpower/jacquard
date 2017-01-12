import sqlalchemy

from .base import Directory, UserEntry


class DjangoDirectory(Directory):
    query = """
    SELECT
        auth_user.id,
        auth_user.date_joined,
        auth_user.is_superuser
    FROM
        auth_user
    """

    def __init__(self, url):
        self.engine = sqlalchemy.create_engine(url)

    def describe_user(self, row):
        tags = []

        if row.is_superuser:
            tags.append('superuser')

        return UserEntry(
            id=row.id,
            join_date=row.date_joined,
            tags=tuple(tags),
        )

    def lookup(self, user_id):
        query = self.query + " WHERE id = ?"

        result = self.engine.execute(query, int(user_id))

        return describe_user(next(iter(result)))

    def all_users(self):
        query = self.query + " ORDER BY id ASC"

        result = self.engine.execute(query)

        for row in result:
            yield self.describe_user(row)