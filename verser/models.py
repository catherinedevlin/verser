from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="../verser.db", create_db=True)


class Writing(db.Entity):
    name = Required(str, unique=True)
    abbrev = Optional(str)
    editions = Set("Edition")

    @classmethod
    def cleanout(cls, name: str) -> None:
        if old := select(w for w in cls if w.name == name).first():
            old.delete()


class Edition(db.Entity):
    writing = Required(Writing)
    name = Required(str)
    abbrev = Optional(str)
    language = Optional(str)
    year = Optional(int)
    divisions = Set("Division")
    division_scheme = Optional(StrArray)
    url = Optional(str)


class Division(db.Entity):
    ordinal = Required(int)
    name = Optional(str)
    abbrev = Optional(str)
    edition = Optional(Edition)
    parent = Optional("Division", reverse="subdivisions")
    subdivisions = Set("Division", reverse="parent")
    verses = Set("Verse")
    url = Optional(str)


class Verse(db.Entity):
    division = Required(Division)
    ordinal = Required(int)
    name = Optional(str)
    abbrev = Optional(str)
    content = Required(str)
    url = Optional(str)


db.generate_mapping(create_tables=True)
