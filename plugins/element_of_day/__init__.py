"""Display a periodic table element that changes daily."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests
import datetime
from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{element}/JSON"
USER_AGENT = "FiestaBoard Element of the Day Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--element-of-day)"


class ElementOfDayPlugin(PluginBase):
    """Element of the Day plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "element_of_day"

    def fetch_data(self) -> PluginResult:
        # Ordered list of elements by atomic number 1–118
        ELEMENTS = [
            ("Hydrogen", "H", 1, "1.008", "nonmetal"),
            ("Helium", "He", 2, "4.003", "noble gas"),
            ("Lithium", "Li", 3, "6.941", "alkali metal"),
            ("Beryllium", "Be", 4, "9.012", "alkaline earth"),
            ("Boron", "B", 5, "10.811", "metalloid"),
            ("Carbon", "C", 6, "12.011", "nonmetal"),
            ("Nitrogen", "N", 7, "14.007", "nonmetal"),
            ("Oxygen", "O", 8, "15.999", "nonmetal"),
            ("Fluorine", "F", 9, "18.998", "halogen"),
            ("Neon", "Ne", 10, "20.180", "noble gas"),
            ("Sodium", "Na", 11, "22.990", "alkali metal"),
            ("Magnesium", "Mg", 12, "24.305", "alkaline earth"),
            ("Aluminum", "Al", 13, "26.982", "post-transition"),
            ("Silicon", "Si", 14, "28.086", "metalloid"),
            ("Phosphorus", "P", 15, "30.974", "nonmetal"),
            ("Sulfur", "S", 16, "32.065", "nonmetal"),
            ("Chlorine", "Cl", 17, "35.453", "halogen"),
            ("Argon", "Ar", 18, "39.948", "noble gas"),
            ("Potassium", "K", 19, "39.098", "alkali metal"),
            ("Calcium", "Ca", 20, "40.078", "alkaline earth"),
            ("Scandium", "Sc", 21, "44.956", "transition metal"),
            ("Titanium", "Ti", 22, "47.867", "transition metal"),
            ("Vanadium", "V", 23, "50.942", "transition metal"),
            ("Chromium", "Cr", 24, "51.996", "transition metal"),
            ("Manganese", "Mn", 25, "54.938", "transition metal"),
            ("Iron", "Fe", 26, "55.845", "transition metal"),
            ("Cobalt", "Co", 27, "58.933", "transition metal"),
            ("Nickel", "Ni", 28, "58.693", "transition metal"),
            ("Copper", "Cu", 29, "63.546", "transition metal"),
            ("Zinc", "Zn", 30, "65.38", "transition metal"),
            ("Gallium", "Ga", 31, "69.723", "post-transition"),
            ("Germanium", "Ge", 32, "72.63", "metalloid"),
            ("Arsenic", "As", 33, "74.922", "metalloid"),
            ("Selenium", "Se", 34, "78.96", "nonmetal"),
            ("Bromine", "Br", 35, "79.904", "halogen"),
            ("Krypton", "Kr", 36, "83.798", "noble gas"),
            ("Rubidium", "Rb", 37, "85.468", "alkali metal"),
            ("Strontium", "Sr", 38, "87.62", "alkaline earth"),
            ("Yttrium", "Y", 39, "88.906", "transition metal"),
            ("Zirconium", "Zr", 40, "91.224", "transition metal"),
            ("Niobium", "Nb", 41, "92.906", "transition metal"),
            ("Molybdenum", "Mo", 42, "95.96", "transition metal"),
            ("Technetium", "Tc", 43, "98", "transition metal"),
            ("Ruthenium", "Ru", 44, "101.07", "transition metal"),
            ("Rhodium", "Rh", 45, "102.906", "transition metal"),
            ("Palladium", "Pd", 46, "106.42", "transition metal"),
            ("Silver", "Ag", 47, "107.868", "transition metal"),
            ("Cadmium", "Cd", 48, "112.411", "transition metal"),
            ("Indium", "In", 49, "114.818", "post-transition"),
            ("Tin", "Sn", 50, "118.71", "post-transition"),
            ("Antimony", "Sb", 51, "121.76", "metalloid"),
            ("Tellurium", "Te", 52, "127.6", "metalloid"),
            ("Iodine", "I", 53, "126.904", "halogen"),
            ("Xenon", "Xe", 54, "131.293", "noble gas"),
            ("Cesium", "Cs", 55, "132.905", "alkali metal"),
            ("Barium", "Ba", 56, "137.327", "alkaline earth"),
            ("Lanthanum", "La", 57, "138.905", "lanthanide"),
            ("Cerium", "Ce", 58, "140.116", "lanthanide"),
            ("Praseodymium", "Pr", 59, "140.908", "lanthanide"),
            ("Neodymium", "Nd", 60, "144.242", "lanthanide"),
            ("Promethium", "Pm", 61, "145", "lanthanide"),
            ("Samarium", "Sm", 62, "150.36", "lanthanide"),
            ("Europium", "Eu", 63, "151.964", "lanthanide"),
            ("Gadolinium", "Gd", 64, "157.25", "lanthanide"),
            ("Terbium", "Tb", 65, "158.925", "lanthanide"),
            ("Dysprosium", "Dy", 66, "162.5", "lanthanide"),
            ("Holmium", "Ho", 67, "164.930", "lanthanide"),
            ("Erbium", "Er", 68, "167.259", "lanthanide"),
            ("Thulium", "Tm", 69, "168.934", "lanthanide"),
            ("Ytterbium", "Yb", 70, "173.054", "lanthanide"),
            ("Lutetium", "Lu", 71, "174.967", "lanthanide"),
            ("Hafnium", "Hf", 72, "178.49", "transition metal"),
            ("Tantalum", "Ta", 73, "180.948", "transition metal"),
            ("Tungsten", "W", 74, "183.84", "transition metal"),
            ("Rhenium", "Re", 75, "186.207", "transition metal"),
            ("Osmium", "Os", 76, "190.23", "transition metal"),
            ("Iridium", "Ir", 77, "192.217", "transition metal"),
            ("Platinum", "Pt", 78, "195.084", "transition metal"),
            ("Gold", "Au", 79, "196.967", "transition metal"),
            ("Mercury", "Hg", 80, "200.59", "transition metal"),
            ("Thallium", "Tl", 81, "204.383", "post-transition"),
            ("Lead", "Pb", 82, "207.2", "post-transition"),
            ("Bismuth", "Bi", 83, "208.980", "post-transition"),
            ("Polonium", "Po", 84, "209", "post-transition"),
            ("Astatine", "At", 85, "210", "halogen"),
            ("Radon", "Rn", 86, "222", "noble gas"),
            ("Francium", "Fr", 87, "223", "alkali metal"),
            ("Radium", "Ra", 88, "226", "alkaline earth"),
            ("Actinium", "Ac", 89, "227", "actinide"),
            ("Thorium", "Th", 90, "232.038", "actinide"),
            ("Protactinium", "Pa", 91, "231.036", "actinide"),
            ("Uranium", "U", 92, "238.029", "actinide"),
            ("Neptunium", "Np", 93, "237", "actinide"),
            ("Plutonium", "Pu", 94, "244", "actinide"),
            ("Americium", "Am", 95, "243", "actinide"),
            ("Curium", "Cm", 96, "247", "actinide"),
            ("Berkelium", "Bk", 97, "247", "actinide"),
            ("Californium", "Cf", 98, "251", "actinide"),
            ("Einsteinium", "Es", 99, "252", "actinide"),
            ("Fermium", "Fm", 100, "257", "actinide"),
            ("Mendelevium", "Md", 101, "258", "actinide"),
            ("Nobelium", "No", 102, "259", "actinide"),
            ("Lawrencium", "Lr", 103, "262", "actinide"),
            ("Rutherfordium", "Rf", 104, "267", "transition metal"),
            ("Dubnium", "Db", 105, "268", "transition metal"),
            ("Seaborgium", "Sg", 106, "269", "transition metal"),
            ("Bohrium", "Bh", 107, "270", "transition metal"),
            ("Hassium", "Hs", 108, "277", "transition metal"),
            ("Meitnerium", "Mt", 109, "278", "transition metal"),
            ("Darmstadtium", "Ds", 110, "281", "transition metal"),
            ("Roentgenium", "Rg", 111, "282", "transition metal"),
            ("Copernicium", "Cn", 112, "285", "transition metal"),
            ("Nihonium", "Nh", 113, "286", "post-transition"),
            ("Flerovium", "Fl", 114, "289", "post-transition"),
            ("Moscovium", "Mc", 115, "290", "post-transition"),
            ("Livermorium", "Lv", 116, "293", "post-transition"),
            ("Tennessine", "Ts", 117, "294", "halogen"),
            ("Oganesson", "Og", 118, "294", "noble gas"),
        ]

        try:
            day_of_year = datetime.date.today().timetuple().tm_yday
            idx = (day_of_year - 1) % len(ELEMENTS)
            name, symbol, atomic_number, atomic_weight, category = ELEMENTS[idx]

            return PluginResult(
                available=True,
                data={
                    "element_name": name,
                    "symbol": symbol,
                    "atomic_number": atomic_number,
                    "atomic_weight": atomic_weight,
                    "category": category,
                },
            )
        except Exception as e:
            logger.exception("Error selecting element of the day")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
