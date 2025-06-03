from taipy.gui import Gui
from frontend.pages.home import home_page
from frontend.pages.business import business_page
from frontend.pages.sweden import sweden_page
from frontend.pages.municipality import municipality_page



pages = {"home": home_page, "Overview": sweden_page, "Municipalities": municipality_page, "Business": business_page}


if __name__ == "__main__":
    app = Gui(pages=pages, css_file="assets/main.css")

    app.run(dark_mode=False, use_reloader=True, port=5656)