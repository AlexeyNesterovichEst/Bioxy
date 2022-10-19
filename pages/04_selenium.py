# import streamlit and other libraries
import streamlit as st
from requests_html import HTMLSession
import pandas as pd

# give our application a title
st.title("Real-time web scraper with Python")


# add our web scraping code
session = HTMLSession()
main_url = "http://books.toscrape.com/"
main_page = session.get(main_url)

navlinks = "div.side_categories>ul.nav.nav-list>li>ul>li>a"
genres = [element.text for element in main_page.html.find(navlinks)]
list_urls = [
    f"{main_url}/{element.attrs['href']}" for element in main_page.html.find(navlinks)
]
genre_urls = dict(zip(genres, list_urls))


@st.cache
def data_extract(genre):
    webpage = genre_urls.get(genre)
    webpage = session.get(webpage)
    urls = [
        element.attrs["href"].strip("../")
        for element in webpage.html.find("div.image_container>a")
    ]

    titles = [element.attrs["title"] for element in webpage.html.find("h3>a")]

    imgs = [
        element.attrs["src"].strip("../")
        for element in webpage.html.find("div.image_container>a>img")
    ]

    ratings = [
        element.attrs["class"][-1] for element in webpage.html.find("p.star-rating")
    ]

    prices = [element.text for element in webpage.html.find("p.price_color")]

    availability = [element.text for element in webpage.html.find("p.instock")]

    data = dict(
        Title=titles,
        URL=urls,
        SourceImage=imgs,
        Rating=ratings,
        Price=prices,
        Availability=availability,
    )

    return pd.DataFrame(data).to_markdown(index=False)


# add a sidebar to select genre
option = st.sidebar.selectbox("Genres", genres)

# add a line of code to show the result
st.markdown(data_extract(option), unsafe_allow_html=True)
