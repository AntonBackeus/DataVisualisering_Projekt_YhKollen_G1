from pathlib import Path

PROGRAM_DIRECTORY = Path(__file__).parents[1] / "data/program"
COURSE_DIRECTORY = Path(__file__).parents[1] / "data/course"
GRANT_DIRECTORY = Path(__file__).parents[1] / "data/grant"
PROGRAM_NAMES = {
    2020: "resultat-ansokningsomgang-2020.xlsx",
    2021: "resultat-ansokningsomgang-2021.xlsx",
    2022: "resultat-ansokningsomgang-2022.xlsx",
    2023: "resultat-ansokningsomgang-2023.xlsx",
    2024: "resultat-ansokningsomgang-2024.xlsx"
}
GRANT_NAMES = {
    "Platser": "ek_4_utbet_arsplatser_utbomr.xlsx",
    "Kronor": "ek_1_utbet_statliga_medel_utbomr.xlsx" 
}
COURSE_NAMES = {
    "Inkommna" : {
        2023: "inkomna-ansokningar-2023-for-kurser.xlsx",
        2024: "inkomna-ansokningar-2024-for-kurser.xlsx",
        2025: "inkomna-ansokningar-2025-for-kurser.xlsx"
    },
    "Resultat" : {
        2020: "resultat_kurs_2020.xlsx",
        2021: "resultat_kurs_2021.xlsx",
        2022: "resultat_kurs_2022.xlsx",
        2023: "resultat_kurs_2023.xlsx",
        2024: "resultat_kurs_2024.xlsx"
    }
}