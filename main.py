from taipy.gui import Gui
from frontend.pages.business import business_page
from frontend.pages.sweden import sweden_page
from frontend.pages.municipality import municipality_page
from frontend.pages.course_analysis import course_analysis_page


pages = {
    "Översikt": sweden_page,
    "Kommuner": municipality_page,
    "Yrkeshögskolor": business_page,
    "Kursanalys": course_analysis_page  
}

app = Gui(pages=pages, css_file="assets/main.css")

if __name__ == "__main__":
    app.run(dark_mode=False, use_reloader=False, port=5656)
