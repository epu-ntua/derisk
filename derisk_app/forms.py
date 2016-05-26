from django import forms
from django.forms import Textarea
from derisk_app.models import *

from django.forms import SelectMultiple

MEASURE_CODES = {m.pk: m.code for m in Measure.objects.all()}

class CustomSelectWidget(SelectMultiple):
    def render(self, name, value, attrs=None):
        # create the select tag
        result = '<select name="' + name + '"'
        # get current & default attributes
        for attr in self.attrs:
            result += ' ' + attr + '="' + self.attrs[attr] + '"'
        for attr in attrs:
            result += ' ' + attr + '="' + attrs[attr] + '"'

        result += '>'

        if value:
            if type(value) == int:
                values = [int(value)]
            else:
                values = [int(val) for val in value]

        # build options
        for choice in self.choices:
            result += '<option value="' + str(choice[0]) + '"'
            if not value:
                if choice[0] == '':
                    result += ' selected="selected"'
            elif choice[0] in values:
                result += ' selected="selected"'
    
            # TODO add the custom data-attribute here
            result += ' data-tree-code="' + MEASURE_CODES[choice[0]] + '"'
            result += '>' + choice[1] + '</option>'
   
        # close select & return
        result += '</select>'
        return result


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseForm, self).__init__(*args, **kwargs)

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(BaseModelForm, self).__init__(*args, **kwargs)

class ProjectForm(BaseModelForm):
    class Meta:
        model = Project
        exclude = ('created_by','sharing_level')
        widgets = {
          'description': Textarea(attrs={'cols': 80, 'rows': 1}),
          'measures_18': CustomSelectWidget(attrs={'multiple': 'multiple'}),
        }
        labels = {
            "title_2":"Project Title", 
            "description":"Description", 
            "country_3":"Country", 
            "nutscode_4":"NUTS-2 Code", 
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
            "energysavingstotal_71":"total", 
            "energysavingsgridelectricity_72":"grid electricity", 
            "energysavingsgas_73":"gas", 
            "energysavingsoil_74":"oil", 
            "energysavingscoal_75":"coal/coal-based products", 
            "energysavingsdistrictheating_76":"district heating", 
            "energysavingsdistrictcooling_77":"district cooling", 
            "energysavingsCHP_78":"CHP", 
            "energysavingsbiomass_79":"biomass", 
            "energysavingsbiofuels_80":"biofuels", 
            "energysavingselectricity_81":"renewable electricity", 
            "energysavingsrenewableheat_82":"renewable heat", 
            "adjustedenergysavingstotal_83":"total", 
            "adjustedenergysavingstotalgridelectricity_84":"grid electricity", 
            "adjustedenergysavingstotalgas_85":"gas", 
            "adjustedenergysavingstotaloil_86":"oil", 
            "adjustedenergysavingstotalcoal_87":"coal/coal-based products", 
            "adjustedenergysavingstotaldistrictheating_88":"district heating", 
            "adjustedenergysavingstotaldistrictcooling_89":"district cooling", 
            "adjustedenergysavingstotalCHP_90":"CHP", 
            "adjustedenergysavingstotalbiomass_91":"biomass", 
            "adjustedenergysavingstotalbiofuels_92":"biofuels", 
            "adjustedenergysavingstotalrenewableelectricity_93":"renewable electricity", 
            "adjustedenergysavingstotalrenewableheat_94":"renewable heat", 
            "hastheadjustedenergysavingsverified_95":"Have the adjusted project energy savings been independently verified?", 
            "energypricebeforetotal_96":"total", 
            "energypricebeforegridelectricity_97":"grid electricity", 
            "energypricebeforegas_98":"gas", 
            "energypricebeforeoil_99":"oil", 
            "energypricebeforecoal_100":"coal/coal-based products", 
            "energypricebeforedistrictheating_101":"district heating", 
            "energypricebeforedistrictcooling_102":"district cooling", 
            "energypricebeforeCHP_103":"CHP", 
            "energypricebeforebiomass_104":"biomass", 
            "energypricebeforebiofuels_105":"biofuels", 
            "energypricebeforerenewableelectricity_106":"renewable electricity", 
            "energypricebeforerenewableheat_107":"renewable heat", 
            "energypriceaftertotal_108":"Total", 
            "energypriceaftergridelectricity_109":"grid electricity", 
            "energypriceaftergas_110":"gas", 
            "energypriceafteroil_111":"oil", 
            "energypriceaftercoal_112":"coal/coal-based products", 
            "energypriceafterdistrictheating_113":"district heating", 
            "energypriceafterdistrictcooling_114":"district cooling", 
            "energypriceafterCHP_115":"CHP", 
            "energypriceafterbiomass_116":"biomass", 
            "energypriceafterbiofuels_117":"biofuels", 
            "energypriceafterrenewableelectricity_118":"renewable electricity", 
            "energypriceafterrenewableheat_119":"renewable heat", 
            "energyconsbeforegridelectricity_120":"grid electricity", 
            "energyconsbeforegas_121":"gas", 
            "energyconsbeforeoil_122":"oil", 
            "energyconsbeforecoal_123":"coal/coal-based products", 
            "energyconsbeforedistrictheating_124":"district heating", 
            "energyconsbeforedistrictcooling_125":"district cooling", 
            "energyconsbeforeCHP_126":"CHP", 
            "energyconsbeforebiomass_127":"biomass", 
            "energyconsbeforebiofuels_128":"biofuels", 
            "energyconsbeforerenewableelectricity_129":"renewable electricity", 
            "energyconsbeforerenewableheat_130":"renewable heat", 
            "energyconsbeforespaceheating_131":"space heating", 
            "energyconsbeforespacecooling_132":"space cooling", 
            "energyconsbeforewaterheating_133":"water heating", 
            "energyconsbeforeventilation_134":"ventilation", 
            "energyconsbeforerefrigeration_135":"refrigeration", 
            "energyconsbeforepumps_136":"pumps and fans", 
            "energyconsbeforecatering_137":"catering", 
            "energyconsbeforeprocessenergy_138":"process energy", 
            "energyconsbeforelighting_139":"lighting", 
            "energyconsbeforeappliances_140":"appliances", 
            "energyconsaftergridelectricity_141":"grid electricity", 
            "energyconsaftergas_142":"gas", 
            "energyconsafteroil_143":"oil", 
            "energyconsaftercoal_144":"coal/coal-based products", 
            "energyconsafterdistrictheating_145":"district heating", 
            "energyconsafterdistrictcooling_146":"district cooling", 
            "energyconsafterCHP_147":"CHP", 
            "energyconsafterbiomass_148":"biomass", 
            "energyconsafterbiofuels_149":"biofuels", 
            "energyconsafterrenewableelectricity_150":"renewable electricity", 
            "energyconsafterrenewableheat_151":"renewable heat", 
            "energyconsafterspaceheating_152":"space heating", 
            "energyconsafterspacecooling_153":"space cooling", 
            "energyconsafterwaterheating_154":"water heating", 
            "energyconsafterventilation_155":"ventilation", 
            "energyconsafterrefrigeration_156":"refrigeration", 
            "energyconsafterpumps_157":"pumps and fans", 
            "energyconsaftercatering_158":"catering", 
            "energyconsafterprocessenergy_159":"process energy", 
            "energyconsafterlighting_160":"lighting", 
            "energyconsafterppliances_161":"appliances", 
            "adjustedenergyconsbeforetotal_162":"total", 
            "adjustedenergyconsbeforegridelectricity_163":"grid electricity", 
            "adjustedenergyconsbeforegas_164":"gas", 
            "adjustedenergyconsbeforeoil_165":"oil", 
            "adjustedenergyconsbeforecoal_166":"coal/coal-based products", 
            "adjustedenergyconsbeforedistrictheating_167":"district heating", 
            "adjustedenergyconsbeforedistrictcooling_168":"district cooling", 
            "adjustedenergyconsbeforeCHP_169":"CHP", 
            "adjustedenergyconsbeforebiomass_170":"biomass", 
            "adjustedenergyconsbeforebiofuels_171":"biofuels", 
            "adjustedenergyconsbeforerenewableelectricity_172":"renewable electricity", 
            "adjustedenergyconsbeforerenewableheat_173":"renewable heat", 
            "adjustedenergyconsbeforespaceheating_174":"space heating", 
            "adjustedenergyconsbeforespacecooling_175":"space cooling", 
            "adjustedenergyconsbeforewaterheating_176":"water heating", 
            "adjustedenergyconsbeforeventilation_177":"ventilation", 
            "adjustedenergyconsbeforerefrigeration_178":"refrigeration", 
            "adjustedenergyconsbeforepumps_179":"pumps and fans", 
            "adjustedenergyconsbeforecatering_180":"catering", 
            "adjustedenergyconsbeforeprocessenergy_181":"process energy", 
            "adjustedenergyconsbeforelighting_182":"lighting", 
            "adjustedenergyconsbeforeappliances_183":"appliances", 
            "adjustedenergyconsaftertotal_184":"Total", 
            "adjustedenergyconsaftergridelectricity_185":"grid electricity", 
            "adjustedenergyconsaftergas_186":"gas", 
            "adjustedenergyconsafteroil_187":"oil", 
            "adjustedenergyconsaftercoal_188":"coal/coal-based products", 
            "adjustedenergyconsafterdistrictheating_189":"district heating", 
            "adjustedenergyconsafterdistrictcooling_190":"district cooling", 
            "adjustedenergyconsafterCHP_191":"CHP", 
            "adjustedenergyconsafterbiomass_192":"biomass", 
            "adjustedenergyconsafterbiofuels_193":"biofuels", 
            "adjustedenergyconsafterrenewableelectricity_194":"renewable electricity", 
            "adjustedenergyconsafterrenewableheat_195":"renewable heat", 
            "adjustedenergyconsafterspaceheating_196":"space heating", 
            "adjustedenergyconsafterspacecooling_197":"space cooling", 
            "adjustedenergyconsafterwaterheating_198":"water heating", 
            "adjustedenergyconsafterventilation_199":"ventilation", 
            "adjustedenergyconsafterrefrigeration_200":"refrigeration", 
            "adjustedenergyconsafterpumps_201":"pumps and fans", 
            "adjustedenergyconsaftercatering_202":"catering", 
            "adjustedenergyconsafterprocessenergy_203":"process energy", 
            "adjustedenergyconsafterlighting_204":"lighting", 
            "adjustedenergyconsafterappliances_205":"appliances"
        }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        #self.fields['valueofeeinvestment_51'].widget.attrs['step'] = 0.02