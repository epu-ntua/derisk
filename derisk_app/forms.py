from django import forms
from derisk_app.models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('created_by',)
        labels = {
            "title_2": "Rule Title",
            "title_2":"Project Title", 
            "description":"Description", 
            "country_3":"Country", 
            "nutscode_4":"ZIP Code", 
            "city_5":"City/locality", 
            "fulladdress_6":"Full Address", 
            "organizationname_7":"Company name", 
            "sitename_8":"Site name - location of investment", 
            "contactperson_9":"Contact person", 
            "email_10":"Email", 
            "telephone_11":"Telephone", 
            "istheinvestmentinabuilding_12":"Is the investment in a building, in industry, or in infrastructure?", 
            "industrysector_13":"Industry Sector/Organisation type", 
            "organizationsize_14":"Organisation size", 
            "buildingtype_15":"Building type", 
            "ownership_16":"Ownership", 
            "floorarea_17":"Floor area of building m2 ", 
            "measures_18":"Which Measures are included in the investment", 
            "energydemandbefore_19":"energy demand before investment (kWh)", 
            "energydemandafter_20":"energy demand after investment (kWh)", 
            "initialcapacity_21":"size (kW)", 
            "uvaluebefore_22":"U-value before investment (W/m2K)", 
            "uvalueafter_23":"U-value after investment  (W/m2K)", 
            "arearenovated_24":"area renovated (m2)", 
            "efficiencybefore_25":"efficiency before investment (%)", 
            "efficiencyafter_26":"efficiency after investment  (%)", 
            "sizeoftheHVACPlant_27":"size (kW)", 
            "projectstartdate_28":"Project start date  (month/year)", 
            "dateinvestmentbecameoperational_29":"Date investment became operational (month/year)", 
            "averagelifetimeofmeasures_30":"Average lifetime of measures (approx) (years)", 
            "energyconsumptionbefore_31":"Energy Consumption BEFORE intervention (MWh/a)", 
            "energyperformancecertificatebefore_32":"Energy Performance Certificate rating BEFORE intervention", 
            "breakdownofconsumptionbyfueltype_33":"Breakdown of consumption by fuel type (MWh/a)", 
            "breakdownofconsumptionbyenduse_34":"Breakdown of consumption by end use", 
            "sourceofconsumptionbefore_35":"Source of consumption BEFORE intervention", 
            "predictedenergyconsumptionafter_36":"Predicted Energy Consumption AFTER intervention (MWh/a)", 
            "whatisthebasisoftheforecast_37":"What is the basis of the forecast?", 
            "energyconsumptionafter_38":"Energy Consumption AFTER intervention (actual) (MWh/a)", 
            "energyperformancecertificateafter_39":"Energy Performance Certificate rating AFTER intervention", 
            "breakdownofconsumptionbyfueltype_40":"Breakdown of consumption by fuel type (MWh/a)", 
            "sourceofconsumptionafter_41":"Source of consumption AFTER intervention (actual)", 
            "havetheprojectenergysavingsbeenverified_42":"Have the project energy savings been independently verified?", 
            "methodologyforindependentverification_43":"Methodology for independent verification", 
            "productionrate_44":"Productivity", 
            "floorarea_45":"floor area", 
            "comfort_46":"comfort", 
            "heatingload_47":"heating load", 
            "coolingload_48":"cooling load", 
            "totalvalueofasset_49":"Total Value  of Asset (€)", 
            "totalvalueofinvestment_50":"Total Value  of investment (inclusive of EE component)", 
            "valueofeeinvestment_51":"Value of EE investment (€)", 
            "annualenergycostsavings_52":"Annual energy cost savings (latest, or representative year) (€)", 
            "additionalfinancialbenefits_53":"Additional financial benefits (e.g. maintenance savings) (€)", 
            "additionalcosts_54":"Additional costs (€)", 
            "netannualsaving_55":"Net annual saving (€)", 
            "npvprior_56":"NPV (computed prior to investment)", 
            "npvactual_57":"NPV actual", 
            "irrprior_58":"IRR (computed prior to investment)", 
            "irractual_59":"IRR actual", 
            "sourceoffinance_60":"Source of finance", 
            "valueofgrant_61":"Value of grant/subsidy (if any) (€)", 
            "provider_62":"Provider", 
            "valueofloan_63":"Value of loan (if any) (€)", 
            "loanrepaymentterm_64":"Loan repayment term (years)", 
            "interestrate_65":"Interest rate (%)", 
            "keyreasonsformakinginvestment_66":"Please state key reasons for making investment", 
            "nonfinancialbenefits_67":"Please state any non-financial benefits realised by the project", 
            "financialperformance_68":"Please rate actual financial performance compared with expectation", 
            "overallsatisfaction_69":"Please rate overall satisfaction with the investment", 
            "otherinformation_70":"Please describe any other information you would like to share concerning your investment, e.g. technical specifications, before/after status, etc",
            "energysavingstotal_71":"Energy savings, kWh/y , total", 
            "energysavingsgridelectricity_72":"Energy savings, kWh/y , grid electricity", 
            "energysavingsgas_73":"Energy savings, kWh/y , gas", 
            "energysavingsoil_74":"Energy savings, kWh/y , oil", 
            "energysavingscoal_75":"Energy savings, kWh/y , coal/coal-based products", 
            "energysavingsdistrictheating_76":"Energy savings, kWh/y , district heating", 
            "energysavingsdistrictcooling_77":"Energy savings, kWh/y , district cooling", 
            "energysavingsCHP_78":"Energy savings, kWh/y , CHP", 
            "energysavingsbiomass_79":"Energy savings, kWh/y , biomass", 
            "energysavingsbiofuels_80":"Energy savings, kWh/y , biofuels", 
            "energysavingselectricity_81":"Energy savings, kWh/y , renewable electricity", 
            "energysavingsrenewableheat_82":"Energy savings, kWh/y , renewable heat", 
            "adjustedenergysavingstotal_83":"Adjusted energy savings, kWh/y , total", 
            "adjustedenergysavingstotalgridelectricity_84":"Adjusted energy savings, kWh/y , grid electricity", 
            "adjustedenergysavingstotalgas_85":"Adjusted energy savings, kWh/y , gas", 
            "adjustedenergysavingstotaloil_86":"Adjusted energy savings, kWh/y , oil", 
            "adjustedenergysavingstotalcoal_87":"Adjusted energy savings, kWh/y , coal/coal-based products", 
            "adjustedenergysavingstotaldistrictheating_88":"Adjusted energy savings, kWh/y , district heating", 
            "adjustedenergysavingstotaldistrictcooling_89":"Adjusted energy savings, kWh/y , district cooling", 
            "adjustedenergysavingstotalCHP_90":"Adjusted energy savings, kWh/y , CHP", 
            "adjustedenergysavingstotalbiomass_91":"Adjusted energy savings, kWh/y , biomass", 
            "adjustedenergysavingstotalbiofuels_92":"Adjusted energy savings, kWh/y , biofuels", 
            "adjustedenergysavingstotalrenewableelectricity_93":"Adjusted energy savings, kWh/y , renewable electricity", 
            "adjustedenergysavingstotalrenewableheat_94":"Adjusted energy savings, kWh/y , renewable heat", 
            "hastheadjustedenergysavingsverified_95":"Have the adjusted project energy savings been independently verified?", 
            "energypricebeforetotal_96":"Energy price before, EUR/kWh, total", 
            "energypricebeforegridelectricity_97":"Energy price before, EUR/kWh, grid electricity", 
            "energypricebeforegas_98":"Energy price before, EUR/kWh, gas", 
            "energypricebeforeoil_99":"Energy price before, EUR/kWh, oil", 
            "energypricebeforecoal_100":"Energy price before, EUR/kWh, coal/coal-based products", 
            "energypricebeforedistrictheating_101":"Energy price before, EUR/kWh, district heating", 
            "energypricebeforedistrictcooling_102":"Energy price before, EUR/kWh, district cooling", 
            "energypricebeforeCHP_103":"Energy price before, EUR/kWh, CHP", 
            "energypricebeforebiomass_104":"Energy price before, EUR/kWh, biomass", 
            "energypricebeforebiofuels_105":"Energy price before, EUR/kWh, biofuels", 
            "energypricebeforerenewableelectricity_106":"Energy price before, EUR/kWh, renewable electricity", 
            "energypricebeforerenewableheat_107":"Energy price before, EUR/kWh, renewable heat", 
            "energypriceaftertotal_108":"Energy price after, EUR/kWh, Total", 
            "energypriceaftergridelectricity_109":"Energy price after, EUR/kWh, grid electricity", 
            "energypriceaftergas_110":"Energy price after, EUR/kWh, gas", 
            "energypriceafteroil_111":"Energy price after, EUR/kWh, oil", 
            "energypriceaftercoal_112":"Energy price after, EUR/kWh, coal/coal-based products", 
            "energypriceafterdistrictheating_113":"Energy price after, EUR/kWh, district heating", 
            "energypriceafterdistrictcooling_114":"Energy price after, EUR/kWh, district cooling", 
            "energypriceafterCHP_115":"Energy price after, EUR/kWh, CHP", 
            "energypriceafterbiomass_116":"Energy price after, EUR/kWh, biomass", 
            "energypriceafterbiofuels_117":"Energy price after, EUR/kWh, biofuels", 
            "energypriceafterrenewableelectricity_118":"Energy price after, EUR/kWh, renewable electricity", 
            "energypriceafterrenewableheat_119":"Energy price after, EUR/kWh, renewable heat", 
            "energyconsbeforegridelectricity_120":"Energy cons. before, kWh/y, grid electricity", 
            "energyconsbeforegas_121":"Energy cons. before, kWh/y, gas", 
            "energyconsbeforeoil_122":"Energy cons. before, kWh/y, oil", 
            "energyconsbeforecoal_123":"Energy cons. before, kWh/y, coal/coal-based products", 
            "energyconsbeforedistrictheating_124":"Energy cons. before, kWh/y, district heating", 
            "energyconsbeforedistrictcooling_125":"Energy cons. before, kWh/y, district cooling", 
            "energyconsbeforeCHP_126":"Energy cons. before, kWh/y, CHP", 
            "energyconsbeforebiomass_127":"Energy cons. before, kWh/y, biomass", 
            "energyconsbeforebiofuels_128":"Energy cons. before, kWh/y, biofuels", 
            "energyconsbeforerenewableelectricity_129":"Energy cons. before, kWh/y, renewable electricity", 
            "energyconsbeforerenewableheat_130":"Energy cons. before, kWh/y, renewable heat", 
            "energyconsbeforespaceheating_131":"Energy cons. before, kWh/y, space heating", 
            "energyconsbeforespacecooling_132":"Energy cons. before, kWh/y, space cooling", 
            "energyconsbeforewaterheating_133":"Energy cons. before, kWh/y, water heating", 
            "energyconsbeforeventilation_134":"Energy cons. before, kWh/y, ventilation", 
            "energyconsbeforerefrigeration_135":"Energy cons. before, kWh/y, refrigeration", 
            "energyconsbeforepumps_136":"Energy cons. before, kWh/y, pumps and fans", 
            "energyconsbeforecatering_137":"Energy cons. before, kWh/y, catering", 
            "energyconsbeforeprocessenergy_138":"Energy cons. before, kWh/y, process energy", 
            "energyconsbeforelighting_139":"Energy cons. before, kWh/y, lighting", 
            "energyconsbeforeappliances_140":"Energy cons. before, kWh/y, appliances", 
            "energyconsaftergridelectricity_141":"Energy cons. after, kWh/y, grid electricity", 
            "energyconsaftergas_142":"Energy cons. after, kWh/y, gas", 
            "energyconsafteroil_143":"Energy cons. after, kWh/y, oil", 
            "energyconsaftercoal_144":"Energy cons. after, kWh/y, coal/coal-based products", 
            "energyconsafterdistrictheating_145":"Energy cons. after, kWh/y, district heating", 
            "energyconsafterdistrictcooling_146":"Energy cons. after, kWh/y, district cooling", 
            "energyconsafterCHP_147":"Energy cons. after, kWh/y, CHP", 
            "energyconsafterbiomass_148":"Energy cons. after, kWh/y, biomass", 
            "energyconsafterbiofuels_149":"Energy cons. after, kWh/y, biofuels", 
            "energyconsafterrenewableelectricity_150":"Energy cons. after, kWh/y, renewable electricity", 
            "energyconsafterrenewableheat_151":"Energy cons. after, kWh/y, renewable heat", 
            "energyconsafterspaceheating_152":"Energy cons. after, kWh/y, space heating", 
            "energyconsafterspacecooling_153":"Energy cons. after, kWh/y, space cooling", 
            "energyconsafterwaterheating_154":"Energy cons. after, kWh/y, water heating", 
            "energyconsafterventilation_155":"Energy cons. after, kWh/y, ventilation", 
            "energyconsafterrefrigeration_156":"Energy cons. after, kWh/y, refrigeration", 
            "energyconsafterpumps_157":"Energy cons. after, kWh/y, pumps and fans", 
            "energyconsaftercatering_158":"Energy cons. after, kWh/y, catering", 
            "energyconsafterprocessenergy_159":"Energy cons. after, kWh/y, process energy", 
            "energyconsafterlighting_160":"Energy cons. after, kWh/y, lighting", 
            "energyconsafterppliances_161":"Energy cons. after, kWh/y, appliances", 
            "adjustedenergyconsbeforetotal_162":"Adjusted energy cons. before, kWh/y, total", 
            "adjustedenergyconsbeforegridelectricity_163":"Adjusted energy cons. before, kWh/y, grid electricity", 
            "adjustedenergyconsbeforegas_164":"Adjusted energy cons. before, kWh/y, gas", 
            "adjustedenergyconsbeforeoil_165":"Adjusted energy cons. before, kWh/y, oil", 
            "adjustedenergyconsbeforecoal_166":"Adjusted energy cons. before, kWh/y, coal/coal-based products", 
            "adjustedenergyconsbeforedistrictheating_167":"Adjusted energy cons. before, kWh/y, district heating", 
            "adjustedenergyconsbeforedistrictcooling_168":"Adjusted energy cons. before, kWh/y, district cooling", 
            "adjustedenergyconsbeforeCHP_169":"Adjusted energy cons. before, kWh/y, CHP", 
            "adjustedenergyconsbeforebiomass_170":"Adjusted energy cons. before, kWh/y, biomass", 
            "adjustedenergyconsbeforebiofuels_171":"Adjusted energy cons. before, kWh/y, biofuels", 
            "adjustedenergyconsbeforerenewableelectricity_172":"Adjusted energy cons. before, kWh/y, renewable electricity", 
            "adjustedenergyconsbeforerenewableheat_173":"Adjusted energy cons. before, kWh/y, renewable heat", 
            "adjustedenergyconsbeforespaceheating_174":"Adjusted energy cons. before, kWh/y, space heating", 
            "adjustedenergyconsbeforespacecooling_175":"Adjusted energy cons. before, kWh/y, space cooling", 
            "adjustedenergyconsbeforewaterheating_176":"Adjusted energy cons. before, kWh/y, water heating", 
            "adjustedenergyconsbeforeventilation_177":"Adjusted energy cons. before, kWh/y, ventilation", 
            "adjustedenergyconsbeforerefrigeration_178":"Adjusted energy cons. before, kWh/y, refrigeration", 
            "adjustedenergyconsbeforepumps_179":"Adjusted energy cons. before, kWh/y, pumps and fans", 
            "adjustedenergyconsbeforecatering_180":"Adjusted energy cons. before, kWh/y, catering", 
            "adjustedenergyconsbeforeprocessenergy_181":"Adjusted energy cons. before, kWh/y, process energy", 
            "adjustedenergyconsbeforelighting_182":"Adjusted energy cons. before, kWh/y, lighting", 
            "adjustedenergyconsbeforeappliances_183":"Adjusted energy cons. before, kWh/y, appliances", 
            "adjustedenergyconsaftertotal_184":"Adjusted energy cons. after, split by fuel", 
            "adjustedenergyconsaftergridelectricity_185":"Adjusted energy cons. after, kWh/y, grid electricity", 
            "adjustedenergyconsaftergas_186":"Adjusted energy cons. after, kWh/y, gas", 
            "adjustedenergyconsafteroil_187":"Adjusted energy cons. after, kWh/y, oil", 
            "adjustedenergyconsaftercoal_188":"Adjusted energy cons. after, kWh/y, coal/coal-based products", 
            "adjustedenergyconsafterdistrictheating_189":"Adjusted energy cons. after, kWh/y, district heating", 
            "adjustedenergyconsafterdistrictcooling_190":"Adjusted energy cons. after, kWh/y, district cooling", 
            "adjustedenergyconsafterCHP_191":"Adjusted energy cons. after, kWh/y, CHP", 
            "adjustedenergyconsafterbiomass_192":"Adjusted energy cons. after, kWh/y, biomass", 
            "adjustedenergyconsafterbiofuels_193":"Adjusted energy cons. after, kWh/y, biofuels", 
            "adjustedenergyconsafterrenewableelectricity_194":"Adjusted energy cons. after, kWh/y, renewable electricity", 
            "adjustedenergyconsafterrenewableheat_195":"Adjusted energy cons. after, kWh/y, renewable heat", 
            "adjustedenergyconsafterspaceheating_196":"Adjusted energy cons. after, kWh/y, space heating", 
            "adjustedenergyconsafterspacecooling_197":"Adjusted energy cons. after, kWh/y, space cooling", 
            "adjustedenergyconsafterwaterheating_198":"Adjusted energy cons. after, kWh/y, water heating", 
            "adjustedenergyconsafterventilation_199":"Adjusted energy cons. after, kWh/y, ventilation", 
            "adjustedenergyconsafterrefrigeration_200":"Adjusted energy cons. after, kWh/y, refrigeration", 
            "adjustedenergyconsafterpumps_201":"Adjusted energy cons. after, kWh/y, pumps and fans", 
            "adjustedenergyconsaftercatering_202":"Adjusted energy cons. after, kWh/y, catering", 
            "adjustedenergyconsafterprocessenergy_203":"Adjusted energy cons. after, kWh/y, process energy", 
            "adjustedenergyconsafterlighting_204":"Adjusted energy cons. after, kWh/y, lighting", 
            "adjustedenergyconsafterappliances_205":"Adjusted energy cons. after, kWh/y, appliances", 
            "occupancylevel_206":"Occupancy level", 
            "typeofproductsbeingproduced_207":"Type of products being produced"
        }