from itertools import count

import requests
from bs4 import BeautifulSoup
from pony.orm import db_session

from .. import utils
from ..models import Division, Edition, Verse, Writing

# The UN's site is more natural for citation, but it 403s requests,
# so pulling test from Australia
source_urls = {
    "en": "https://humanrights.gov.au/our-work/commission-general/universal-declaration-human-rights-human-rights-your-fingertips-human"
}

urls = {
    "en": "https://www.ohchr.org/en/human-rights/universal-declaration/translations/english"
}


@db_session
def ingest():
    for (lang_abbrev, source_url) in source_urls.items():
        url = urls[lang_abbrev]
        lang = utils.language_names[lang_abbrev]
        resp = requests.get(source_url)
        soup = BeautifulSoup(resp.content, features="html.parser")
        title = soup.title.text.split("-")[0].strip()
        Writing.cleanout(name=title)
        writing = Writing(
            name=title,
            abbrev=utils.abbrev(title),
        )
        edition = Edition(
            writing=writing,
            name=f"{title} - {lang}",
            abbrev=f"{writing.abbrev}-{lang_abbrev}",
            url=url,
            year=1948,
            division_scheme=[
                "Article",
            ],
            language=lang,
        )
        article_count = count(1)
        article = Division(ordinal=next(article_count), edition=edition, url=url)
        verse_count = count(1)
        next_para = soup.select_one("#Heading333").parent.find_next("p")
        while next_para:
            if next_para.b:
                article = Division(
                    ordinal=next(article_count),
                    name=next_para.b.text,
                    edition=edition,
                    url=url,
                )
                verse_count = count(1)
            elif content := next_para.text.strip():
                Verse(
                    division=article,
                    ordinal=next(verse_count),
                    content=next_para.text,
                    url=url,
                )
            if next_para := next_para.find_next("p"):
                if "^Top" in next_para.text:
                    break
