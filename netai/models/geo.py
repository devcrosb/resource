
### Validators
### ==========================================

def isCountryID(value):

	try: val = value.upper()
	except: return

	if DATA["iso2"].get(val):
		return True


def isCountry(value):

	val = Token(value)
	if not val:
		return
	
	if DATA["country"].get(val):
		return True


### Parsers
### ==========================================

def CountryID(value):

	if not isinstance(value,str):
		return

	if DATA["iso2"].get(value):
		return value

	val = Token(value)
	if not val:
		return
	
	if DATA["country"].get(val):
		return DATA["country"][val]["iso2"]

	
def Country(value):

	val = Token(value)
	if not val:
		return
	
	if DATA["country"].get(val):
		return DATA["country"][val]["country"]
	
	if isCountryID(value):
		return DATA["iso2-country"].get(val.upper())


def Token(value):

	value = str(value).lower().strip()

	if len(value) == 0:
		return
	
	for tag in [". ",";",","," "]:
		value = value.replace(tag,"-")

	value = value.replace("'","")

	res = []
	for val in value.split("-"):
		if isTokenVal(val):
			res.append(val)

	if res:
		return "-".join(res)


def isTokenVal(val):

	if len(val) == 0:
		return False
	
	if val in {"the","of","and","to","in","a","the","republic","democratic","peoples"}:
		return False

	return True


DATA = {
	"iso2":{
		"AF": "Afghanistan",
		"AL": "Albania",
		"DZ": "Algeria",
		"AD": "Andorra",
		"AO": "Angola",
		"AG": "Antigua and Barbuda",
		"AR": "Argentina",
		"AM": "Armenia",
		"AU": "Australia",
		"AT": "Austria",
		"AZ": "Azerbaijan",
		"BS": "Bahamas",
		"BH": "Bahrain",
		"BD": "Bangladesh",
		"BB": "Barbados",
		"BY": "Belarus",
		"BE": "Belgium",
		"BZ": "Belize",
		"BJ": "Benin",
		"BT": "Bhutan",
		"BO": "Bolivia",
		"BA": "Bosnia and Herzegovina",
		"BW": "Botswana",
		"BR": "Brazil",
		"BN": "Brunei",
		"BG": "Bulgaria",
		"BF": "Burkina Faso",
		"BI": "Burundi",
		"CV": "Cabo Verde",
		"KH": "Cambodia",
		"CM": "Cameroon",
		"CA": "Canada",
		"CF": "Central African Republic",
		"TD": "Chad",
		"CL": "Chile",
		"CN": "China",
		"CO": "Colombia",
		"KM": "Comoros",
		"CG": "Congo",
		"CD": "Congo, Democratic Republic of the",
		"CR": "Costa Rica",
		"CI": "Cote dIvoire",
		"HR": "Croatia",
		"CU": "Cuba",
		"CY": "Cyprus",
		"CZ": "Czechia",
		"DK": "Denmark",
		"DJ": "Djibouti",
		"DM": "Dominica",
		"DO": "Dominican Republic",
		"EC": "Ecuador",
		"EG": "Egypt",
		"SV": "El Salvador",
		"GQ": "Equatorial Guinea",
		"ER": "Eritrea",
		"EE": "Estonia",
		"SZ": "Eswatini",
		"ET": "Ethiopia",
		"FJ": "Fiji",
		"FI": "Finland",
		"FR": "France",
		"GA": "Gabon",
		"GM": "Gambia",
		"GE": "Georgia",
		"DE": "Germany",
		"GH": "Ghana",
		"GR": "Greece",
		"GD": "Grenada",
		"GT": "Guatemala",
		"GN": "Guinea",
		"GW": "Guinea-Bissau",
		"GY": "Guyana",
		"HT": "Haiti",
		"HN": "Honduras",
		"HU": "Hungary",
		"IS": "Iceland",
		"IN": "India",
		"ID": "Indonesia",
		"IR": "Iran",
		"IQ": "Iraq",
		"IE": "Ireland",
		"IL": "Israel",
		"IT": "Italy",
		"JM": "Jamaica",
		"JP": "Japan",
		"JO": "Jordan",
		"KZ": "Kazakhstan",
		"KE": "Kenya",
		"KI": "Kiribati",
		"KP": "Korea, North",
		"KR": "Korea, South",
		"KW": "Kuwait",
		"KG": "Kyrgyzstan",
		"LA": "Laos",
		"LV": "Latvia",
		"LB": "Lebanon",
		"LS": "Lesotho",
		"LR": "Liberia",
		"LY": "Libya",
		"LI": "Liechtenstein",
		"LT": "Lithuania",
		"LU": "Luxembourg",
		"MG": "Madagascar",
		"MW": "Malawi",
		"MY": "Malaysia",
		"MV": "Maldives",
		"ML": "Mali",
		"MT": "Malta",
		"MH": "Marshall Islands",
		"MR": "Mauritania",
		"MU": "Mauritius",
		"MX": "Mexico",
		"FM": "Micronesia",
		"MD": "Moldova",
		"MC": "Monaco",
		"MN": "Mongolia",
		"ME": "Montenegro",
		"MA": "Morocco",
		"MZ": "Mozambique",
		"MM": "Myanmar",
		"NA": "Namibia",
		"NR": "Nauru",
		"NP": "Nepal",
		"NL": "Netherlands",
		"NZ": "New Zealand",
		"NI": "Nicaragua",
		"NE": "Niger",
		"NG": "Nigeria",
		"MK": "North Macedonia",
		"NO": "Norway",
		"OM": "Oman",
		"PK": "Pakistan",
		"PW": "Palau",
		"PS": "Palestine",
		"PA": "Panama",
		"PG": "Papua New Guinea",
		"PY": "Paraguay",
		"PE": "Peru",
		"PH": "Philippines",
		"PL": "Poland",
		"PT": "Portugal",
		"QA": "Qatar",
		"RO": "Romania",
		"RU": "Russia",
		"RW": "Rwanda",
		"KN": "Saint Kitts and Nevis",
		"LC": "Saint Lucia",
		"VC": "Saint Vincent and the Grenadines",
		"WS": "Samoa",
		"SM": "San Marino",
		"ST": "Sao Tome and Principe",
		"SA": "Saudi Arabia",
		"SN": "Senegal",
		"RS": "Serbia",
		"SC": "Seychelles",
		"SL": "Sierra Leone",
		"SG": "Singapore",
		"SK": "Slovakia",
		"SI": "Slovenia",
		"SB": "Solomon Islands",
		"SO": "Somalia",
		"ZA": "South Africa",
		"SS": "South Sudan",
		"ES": "Spain",
		"LK": "Sri Lanka",
		"SD": "Sudan",
		"SR": "Suriname",
		"SE": "Sweden",
		"CH": "Switzerland",
		"SY": "Syria",
		"TW": "Taiwan",
		"TJ": "Tajikistan",
		"TZ": "Tanzania",
		"TH": "Thailand",
		"TL": "Timor-Leste",
		"TG": "Togo",
		"TO": "Tonga",
		"TT": "Trinidad and Tobago",
		"TN": "Tunisia",
		"TR": "Turkey",
		"TM": "Turkmenistan",
		"TV": "Tuvalu",
		"UG": "Uganda",
		"UA": "Ukraine",
		"AE": "United Arab Emirates",
		"GB": "United Kingdom",
		"US": "United States",
		"UY": "Uruguay",
		"UZ": "Uzbekistan",
		"VU": "Vanuatu",
		"VA": "Vatican City",
		"VE": "Venezuela",
		"VN": "Vietnam",
		"YE": "Yemen",
		"ZM": "Zambia",
		"ZW": "Zimbabwe"
	},
	"country":{
		"afghanistan": {
			"country": "Afghanistan",
			"iso2": "AF",
			"iso3": "AFG"
		},
		"albania": {
			"country": "Albania",
			"iso2": "AL",
			"iso3": "ALB"
		},
		"algeria": {
			"country": "Algeria",
			"iso2": "DZ",
			"iso3": "DZA"
		},
		"andorra": {
			"country": "Andorra",
			"iso2": "AD",
			"iso3": "AND"
		},
		"angola": {
			"country": "Angola",
			"iso2": "AO",
			"iso3": "AGO"
		},
		"antigua-barbuda": {
			"country": "Antigua and Barbuda",
			"iso2": "AG",
			"iso3": "ATG"
		},
		"argentina": {
			"country": "Argentina",
			"iso2": "AR",
			"iso3": "ARG"
		},
		"armenia": {
			"country": "Armenia",
			"iso2": "AM",
			"iso3": "ARM"
		},
		"australia": {
			"country": "Australia",
			"iso2": "AU",
			"iso3": "AUS"
		},
		"austria": {
			"country": "Austria",
			"iso2": "AT",
			"iso3": "AUT"
		},
		"azerbaijan": {
			"country": "Azerbaijan",
			"iso2": "AZ",
			"iso3": "AZE"
		},
		"bahamas": {
			"country": "Bahamas",
			"iso2": "BS",
			"iso3": "BHS"
		},
		"bahrain": {
			"country": "Bahrain",
			"iso2": "BH",
			"iso3": "BHR"
		},
		"bangladesh": {
			"country": "Bangladesh",
			"iso2": "BD",
			"iso3": "BGD"
		},
		"barbados": {
			"country": "Barbados",
			"iso2": "BB",
			"iso3": "BRB"
		},
		"belarus": {
			"country": "Belarus",
			"iso2": "BY",
			"iso3": "BLR"
		},
		"belgium": {
			"country": "Belgium",
			"iso2": "BE",
			"iso3": "BEL"
		},
		"belize": {
			"country": "Belize",
			"iso2": "BZ",
			"iso3": "BLZ"
		},
		"benin": {
			"country": "Benin",
			"iso2": "BJ",
			"iso3": "BEN"
		},
		"bhutan": {
			"country": "Bhutan",
			"iso2": "BT",
			"iso3": "BTN"
		},
		"bolivia": {
			"country": "Bolivia",
			"iso2": "BO",
			"iso3": "BOL"
		},
		"bosnia-herzegovina": {
			"country": "Bosnia and Herzegovina",
			"iso2": "BA",
			"iso3": "BIH"
		},
		"botswana": {
			"country": "Botswana",
			"iso2": "BW",
			"iso3": "BWA"
		},
		"brazil": {
			"country": "Brazil",
			"iso2": "BR",
			"iso3": "BRA"
		},
		"brunei": {
			"country": "Brunei",
			"iso2": "BN",
			"iso3": "BRN"
		},
		"bulgaria": {
			"country": "Bulgaria",
			"iso2": "BG",
			"iso3": "BGR"
		},
		"burkina-faso": {
			"country": "Burkina Faso",
			"iso2": "BF",
			"iso3": "BFA"
		},
		"burundi": {
			"country": "Burundi",
			"iso2": "BI",
			"iso3": "BDI"
		},
		"cabo-verde": {
			"country": "Cabo Verde",
			"iso2": "CV",
			"iso3": "CPV"
		},
		"cambodia": {
			"country": "Cambodia",
			"iso2": "KH",
			"iso3": "KHM"
		},
		"cameroon": {
			"country": "Cameroon",
			"iso2": "CM",
			"iso3": "CMR"
		},
		"canada": {
			"country": "Canada",
			"iso2": "CA",
			"iso3": "CAN"
		},
		"central-african-republic": {
			"country": "Central African Republic",
			"iso2": "CF",
			"iso3": "CAF"
		},
		"chad": {
			"country": "Chad",
			"iso2": "TD",
			"iso3": "TCD"
		},
		"chile": {
			"country": "Chile",
			"iso2": "CL",
			"iso3": "CHL"
		},
		"china": {
			"country": "China",
			"iso2": "CN",
			"iso3": "CHN"
		},
		"colombia": {
			"country": "Colombia",
			"iso2": "CO",
			"iso3": "COL"
		},
		"comoros": {
			"country": "Comoros",
			"iso2": "KM",
			"iso3": "COM"
		},
		"congo": {
			"country": "Congo",
			"iso2": "CG",
			"iso3": "COG"
		},
		"costa-rica": {
			"country": "Costa Rica",
			"iso2": "CR",
			"iso3": "CRI"
		},
		"cote-divoire": {
			"country": "Côte dIvoire",
			"iso2": "CI",
			"iso3": "CIV"
		},
		"croatia": {
			"country": "Croatia",
			"iso2": "HR",
			"iso3": "HRV"
		},
		"cuba": {
			"country": "Cuba",
			"iso2": "CU",
			"iso3": "CUB"
		},
		"cyprus": {
			"country": "Cyprus",
			"iso2": "CY",
			"iso3": "CYP"
		},
		"czechia": {
			"country": "Czechia",
			"iso2": "CZ",
			"iso3": "CZE"
		},
		"denmark": {
			"country": "Denmark",
			"iso2": "DK",
			"iso3": "DNK"
		},
		"djibouti": {
			"country": "Djibouti",
			"iso2": "DJ",
			"iso3": "DJI"
		},
		"dominica": {
			"country": "Dominica",
			"iso2": "DM",
			"iso3": "DMA"
		},
		"dominican-republic": {
			"country": "Dominican Republic",
			"iso2": "DO",
			"iso3": "DOM"
		},
		"ecuador": {
			"country": "Ecuador",
			"iso2": "EC",
			"iso3": "ECU"
		},
		"egypt": {
			"country": "Egypt",
			"iso2": "EG",
			"iso3": "EGY"
		},
		"el-salvador": {
			"country": "El Salvador",
			"iso2": "SV",
			"iso3": "SLV"
		},
		"equatorial-guinea": {
			"country": "Equatorial Guinea",
			"iso2": "GQ",
			"iso3": "GNQ"
		},
		"eritrea": {
			"country": "Eritrea",
			"iso2": "ER",
			"iso3": "ERI"
		},
		"estonia": {
			"country": "Estonia",
			"iso2": "EE",
			"iso3": "EST"
		},
		"eswatini": {
			"country": "Eswatini",
			"iso2": "SZ",
			"iso3": "SWZ"
		},
		"ethiopia": {
			"country": "Ethiopia",
			"iso2": "ET",
			"iso3": "ETH"
		},
		"fiji": {
			"country": "Fiji",
			"iso2": "FJ",
			"iso3": "FJI"
		},
		"finland": {
			"country": "Finland",
			"iso2": "FI",
			"iso3": "FIN"
		},
		"france": {
			"country": "France",
			"iso2": "FR",
			"iso3": "FRA"
		},
		"gabon": {
			"country": "Gabon",
			"iso2": "GA",
			"iso3": "GAB"
		},
		"gambia": {
			"country": "Gambia",
			"iso2": "GM",
			"iso3": "GMB"
		},
		"georgia": {
			"country": "Georgia",
			"iso2": "GE",
			"iso3": "GEO"
		},
		"germany": {
			"country": "Germany",
			"iso2": "DE",
			"iso3": "DEU"
		},
		"ghana": {
			"country": "Ghana",
			"iso2": "GH",
			"iso3": "GHA"
		},
		"greece": {
			"country": "Greece",
			"iso2": "GR",
			"iso3": "GRC"
		},
		"grenada": {
			"country": "Grenada",
			"iso2": "GD",
			"iso3": "GRD"
		},
		"guatemala": {
			"country": "Guatemala",
			"iso2": "GT",
			"iso3": "GTM"
		},
		"guinea": {
			"country": "Guinea",
			"iso2": "GN",
			"iso3": "GIN"
		},
		"guinea-bissau": {
			"country": "Guinea-Bissau",
			"iso2": "GW",
			"iso3": "GNB"
		},
		"guyana": {
			"country": "Guyana",
			"iso2": "GY",
			"iso3": "GUY"
		}
	}         
}