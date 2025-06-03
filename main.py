from taipy.gui import Gui
from frontend.pages.business import business_page
from frontend.pages.sweden import sweden_page
from frontend.pages.municipality import municipality_page



pages = {"Översikt": sweden_page, "Kommuner": municipality_page, "Yrkeshögskolor": business_page}


if __name__ == "__main__":
    app = Gui(pages=pages, css_file="assets/main.css")

    app.run(dark_mode=False, use_reloader=True, port=5656)