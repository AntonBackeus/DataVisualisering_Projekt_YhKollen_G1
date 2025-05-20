from taipy.gui import Gui
from frontend.pages.dashboard import dashboard_page
from frontend.pages.home import home_page
from frontend.pages.data import data_page
from frontend.pages.generaldash import general_page


pages = {"home": home_page, "dashboard": dashboard_page, "data": data_page, "generelt": general_page}


if __name__ == "__main__":
    app = Gui(pages=pages, css_file="assets/main.css")

    app.run(dark_mode=False, port=5757)

#Test