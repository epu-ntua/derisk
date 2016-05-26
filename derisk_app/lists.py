COUNTRIES = (
    ('', ''),
    ('AT', 'Austria'),
    ('BE', 'Belgium'),
    ('BG', 'Bulgaria'),
    ('CA', 'Canada'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DE', 'Germany'),
    ('DK', 'Denmark'),
    ('EE', 'Estonia'),
    ('EL', 'Greece'),
    ('ES', 'Spain'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('HR', 'Croatia'),
    ('HU', 'Hungary'),
    ('IE', 'Ireland'),
    ('IT', 'Italy'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('LV', 'Latvia'),
    ('MT', 'Malta'),
    ('NL', 'Netherlands'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('RO', 'Romania'),
    ('SE', 'Sweden'),
    ('SI', 'Slovenia'),
    ('SK', 'Slovak Republic'),
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
)

ORGANIZATIONSIZE = (
    ('',''),
    ('MICRO','micro enterprises: with less than 10 persons employed'),
    ('SMALL','small enterprises: with 10-49 persons employed'),
    ('MEDIUM','medium-sized enterprises: with 50-249 persons employed'),
    ('LARGE','large enterprises: with 250 or more persons employed'),
)

BUILDINGTYPE = (
   ('',''),
   ('DETACHED','detached single family dwellings'),
   ('SINGLE','other single family dwellings'),
   ('MULTI4','multi-family buildings 1-4 storeys'),
   ('MULTI5','multi-family buidings 5+ storeys'),
   ('PRIVATE','private offices'),
   ('PUBLIC','public buildings'),
   ('WHOLESALE','wholesale and retail trade'),
   ('HOTEL','hotel & restaurants'),
   ('HEALTH','health care'),
   ('EDUCATION','educational buildings'),
   ('SPORT','sport facilities'),
   ('INDUSTRY','industry'),
)

OWNERSHIP = (
   ('',''),
   ('OWN','owned'),
   ('RENT','rented'),
)

VERIFIED = (
  ('',''),
  ('By third party','By third party'),
  ('by ESCO','by ESCO'),
  ('by other','by other'),
  ('not verified','not verified'),
)

SHARINGLEVEL = (
  ('PRI','Private'),
  ('ANA','Share for analysis'),
)

#Dropdownlist contain other

INVESTMENTBUILDING =(
  ('Building','Building'),
  ('Industry','Industry'),
  ('District heating','District heating'),
  ('Street lighting','Street lighting'),
  ('Other','Other'),
)

INDUSTRYSECTOR =(
  ('Accommodation and food service','Accommodation and food service'),
  ('Administrative and support services','Administrative and support services'),
  ('Agriculture/forestry/fishing','Agriculture/forestry/fishing'),
  ('Arts, entertainment and recreation','Arts, entertainment and recreation'),
  ('Construction','Construction'),
  ('Education','Education'),
  ('Electricity, gas, steam and air conditioning supply','Electricity, gas, steam and air conditioning supply'),
  ('Finance/insurance','Finance/insurance'),
  ('Human health and social work','Human health and social work'),
  ('Information and communication','Information and communication'),
  ('Manufacturing','Manufacturing'),
  ('Mining/quarrying','Mining/quarrying'),
  ('Professional, scientific and technical','Professional, scientific and technical'),
  ('Public administration and defence','Public administration and defence'),
  ('Real estate','Real estate'),
  ('Transportation and storage','Transportation and storage'),
  ('Water/waste management','Water/waste management'),
  ('Wholesale and retail trade/motor vehicles','Wholesale and retail trade/motor vehicles'),
  ('Other','other')
)

SOURCECONSUMPTIONBEFORE = (
  ('Energy audit actual','Energy audit actual'),
  ('energy audit norm','energy audit norm'),
  ('feasibility study','feasibility study'),
  ('other','other')
)

BASISFORECAST = (
  ('Energy audit actual','Energy audit actual'),
  ('energy audit norm','energy audit norm'),
  ('feasibility study','feasibility study'),
  ('other','other')
)

SOURCECONSUMPTIONAFTER = (
  ('Ex post energy audit actual','Ex post energy audit actual'),
  ('ex post energy audit norm','ex post energy audit norm'),
  ('actual reported by building manager','actual reported by building manager'),
  ('other','other'),
)

SATISFACTION = (
  ('signficantly worse than expected','signficantly worse than expected'),
  ('slightly worse than expected','slightly worse than expected'),
  ('as expected','as expected'),
  ('slightly better than expected','slightly better than expected'),
  ('signficantly better than expected','signficantly better than expected'),
)