from taipy.gui import Gui
from frontend.pages.home import home_page
from frontend.pages.generaldash import general_page
from frontend.pages.sweden import sweden_page


pages = {"home": home_page, "generelt": general_page, "Overview": sweden_page}


if __name__ == "__main__":
    app = Gui(pages=pages, css_file="assets/main.css")

    app.run(dark_mode=False, port=5656)