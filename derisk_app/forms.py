import sys
from django import forms
from django.forms import Textarea
from derisk_app.models import *
from django.utils.translation import ugettext_lazy as _

from django.forms import SelectMultiple

if not('migrate' in sys.argv
       or 'makemigrations' in sys.argv
       or 'collectstatic' in sys.argv):
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

class UserForm(BaseModelForm):
    class Meta:
        model = User
        exclude = ()

class UserProfileForm(BaseModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        widgets = {
        }
        labels = {
             "name":_("Your name"),
             "telephone": _("Your telephone"),
             "organization": _("Your organization name"),
             "organizationnature": _("Nature of your organization"),
             "organizationnatureother": _("If other, please specify nature of organization"),
             "sample_size_limit": _("Please select the sample size limit on charts")
        }

class ProjectForm(BaseModelForm):
    class Meta:
        model = Project
        exclude = ('created_by', 'sharing_level', 'original_project_id_1', 'measures_main')
        widgets = {
          'description': Textarea(attrs={'cols': 80, 'rows': 1}),
          'measures_18': CustomSelectWidget(attrs={'multiple': 'multiple'}),
        }
        labels = {
            "title_2":_("Project Title"),
            "description":_("Description"),
            "country_3":_("Country"),
            "user_note": _("A user-defined field to assist you later searching the project"),
            "nutscode_4":_("NUTS-2 Code"),
            "city_5":_("City/locality"),
            "fulladdress_6":_("Full Address"),
            "organizationname_7":_("Company name"),
            "sitename_8":_("Site name - location of investment"),
            "contactperson_9":_("Contact person"),
            "email_10":_("Email"),
            "telephone_11":_("Telephone"),
            "istheinvestmentinabuilding_12":_("Is the investment in a building, in industry, or in infrastructure?"),
            "industrysector_13":_("Industry Sector / Organisation type"),
            "organizationsize_14":_("Organisation size"),
            "buildingtype_15":_("Building type"),
            "ownership_16":_("Ownership"),
            "floorarea_17":_("Floor area of building m2 "),
            "measures_18":_("Which Measures are included in the investment"),
            "energydemandbefore_19":_("energy demand before investment (kWh)"),
            "energydemandafter_20":_("energy demand after investment (kWh)"),
            "initialcapacity_21":_("size (kW)"),
            "uvaluebefore_22":_("U-value before investment (W/m2K)"),
            "uvalueafter_23":_("U-value after investment  (W/m2K)"),
            "arearenovated_24":_("area renovated (m2)"),
            "efficiencybefore_25":_("efficiency before investment (%)"),
            "efficiencyafter_26":_("efficiency after investment  (%)"),
            "sizeoftheHVACPlant_27":_("size (kW)"),
            "projectstartdate_28":_("Project start date  (month/year)"),
            "dateinvestmentbecameoperational_29":_("Date investment became operational (month/year)"),
            "averagelifetimeofmeasures_30":_("Average lifetime of measures (approx) (years)"),
            "energyconsumptionbefore_31":_("Energy Consumption BEFORE intervention (KWh/a)"),
            "energyperformancecertificatebefore_32":_("Energy Performance Certificate rating BEFORE intervention"),
            "breakdownofconsumptionbyfueltype_33":_("Breakdown of consumption by fuel type (KWh/a)"),
            "breakdownofconsumptionbyenduse_34":_("Breakdown of consumption by end use"),
            "sourceofconsumptionbefore_35":_("Source of consumption BEFORE intervention"),
            "predictedenergyconsumptionafter_36":_("Predicted Energy Consumption AFTER intervention (KWh/a)"),
            "whatisthebasisoftheforecast_37":_("What is the basis of the forecast?"),
            "energyconsumptionafter_38":_("Energy Consumption AFTER intervention (actual) (KWh/a)"),
            "energyperformancecertificateafter_39":_("Energy Performance Certificate rating AFTER intervention"),
            "breakdownofconsumptionbyfueltype_40":_("Breakdown of consumption by fuel type (MWh/a)"),
            "sourceofconsumptionafter_41":_("Source of consumption AFTER intervention (actual)"),
            "havetheprojectenergysavingsbeenverified_42":_("Have the project energy savings been independently verified?"),
            "methodologyforindependentverification_43":_("Methodology for independent verification"),
            "productionrate_44":_("Productivity"),
            "floorarea_45":_("floor area"),
            "comfort_46":_("comfort"),
            "heatingload_47":_("heating load"),
            "coolingload_48":_("cooling load"),
            "totalvalueofasset_49":_("Total Value  of Asset (€)"),
            "totalvalueofinvestment_50":_("Total Value  of investment (inclusive of EE component)"),
            "valueofeeinvestment_51":_("Value of EE investment (€)"),
            "annualenergycostsavings_52":_("Annual energy cost savings (latest, or representative year) (€)"),
            "additionalfinancialbenefits_53":_("Additional financial benefits (e.g. maintenance savings) (€)"),
            "additionalcosts_54":_("Additional costs (€)"),
            "netannualsaving_55":_("Net annual saving (€)"),
            "npvprior_56":_("NPV (computed prior to investment)"),
            "npvactual_57":_("NPV actual"),
            "irrprior_58":_("IRR (computed prior to investment)"),
            "irractual_59":_("IRR actual"),
            "sourceoffinance_60":_("Source of finance"),
            "valueofgrant_61":_("Value of grant/subsidy (if any) (€)"),
            "provider_62":_("Provider"),
            "valueofloan_63":_("Value of loan (if any) (€)"),
            "loanrepaymentterm_64":_("Loan repayment term (years)"),
            "interestrate_65":_("Interest rate (%)"),
            "keyreasonsformakinginvestment_66":_("Please state key reasons for making investment"),
            "nonfinancialbenefits_67":_("Please state any non-financial benefits realised by the project"),
            "financialperformance_68":_("Please rate actual financial performance compared with expectation"),
            "overallsatisfaction_69":_("Please rate overall satisfaction with the investment"),
            "otherinformation_70":_("Please describe any other information you would like to share concerning your investment, e.g. technical specifications, before/after status, etc"),
            "energysavingstotal_71":_("total"),
            "energysavingsgridelectricity_72":_("grid electricity"),
            "energysavingsgas_73":_("gas"),
            "energysavingsoil_74":_("oil"),
            "energysavingscoal_75":_("coal/coal-based products"),
            "energysavingsdistrictheating_76":_("district heating"),
            "energysavingsdistrictcooling_77":_("district cooling"),
            "energysavingsCHP_78":_("CHP"),
            "energysavingsbiomass_79":_("biomass"),
            "energysavingsbiofuels_80":_("biofuels"),
            "energysavingselectricity_81":_("renewable electricity"),
            "energysavingsrenewableheat_82":_("renewable heat"),
            "adjustedenergysavingstotal_83":_("total"),
            "adjustedenergysavingstotalgridelectricity_84":_("grid electricity"),
            "adjustedenergysavingstotalgas_85":_("gas"),
            "adjustedenergysavingstotaloil_86":_("oil"),
            "adjustedenergysavingstotalcoal_87":_("coal/coal-based products"),
            "adjustedenergysavingstotaldistrictheating_88":_("district heating"),
            "adjustedenergysavingstotaldistrictcooling_89":_("district cooling"),
            "adjustedenergysavingstotalCHP_90":_("CHP"),
            "adjustedenergysavingstotalbiomass_91":_("biomass"),
            "adjustedenergysavingstotalbiofuels_92":_("biofuels"),
            "adjustedenergysavingstotalrenewableelectricity_93":_("renewable electricity"),
            "adjustedenergysavingstotalrenewableheat_94":_("renewable heat"),
            "hastheadjustedenergysavingsverified_95":_("Have the adjusted project energy savings been independently verified?"),
            "energypricebeforetotal_96":_("total"),
            "energypricebeforegridelectricity_97":_("grid electricity"),
            "energypricebeforegas_98":_("gas"),
            "energypricebeforeoil_99":_("oil"),
            "energypricebeforecoal_100":_("coal/coal-based products"),
            "energypricebeforedistrictheating_101":_("district heating"),
            "energypricebeforedistrictcooling_102":_("district cooling"),
            "energypricebeforeCHP_103":_("CHP"),
            "energypricebeforebiomass_104":_("biomass"),
            "energypricebeforebiofuels_105":_("biofuels"),
            "energypricebeforerenewableelectricity_106":_("renewable electricity"),
            "energypricebeforerenewableheat_107":_("renewable heat"),
            "energypriceaftertotal_108":_("Total"),
            "energypriceaftergridelectricity_109":_("grid electricity"),
            "energypriceaftergas_110":_("gas"),
            "energypriceafteroil_111":_("oil"),
            "energypriceaftercoal_112":_("coal/coal-based products"),
            "energypriceafterdistrictheating_113":_("district heating"),
            "energypriceafterdistrictcooling_114":_("district cooling"),
            "energypriceafterCHP_115":_("CHP"),
            "energypriceafterbiomass_116":_("biomass"),
            "energypriceafterbiofuels_117":_("biofuels"),
            "energypriceafterrenewableelectricity_118":_("renewable electricity"),
            "energypriceafterrenewableheat_119":_("renewable heat"),
            "energyconsbeforegridelectricity_120":_("grid electricity"),
            "energyconsbeforegas_121":_("gas"),
            "energyconsbeforeoil_122":_("oil"),
            "energyconsbeforecoal_123":_("coal/coal-based products"),
            "energyconsbeforedistrictheating_124":_("district heating"),
            "energyconsbeforedistrictcooling_125":_("district cooling"),
            "energyconsbeforeCHP_126":_("CHP"),
            "energyconsbeforebiomass_127":_("biomass"),
            "energyconsbeforebiofuels_128":_("biofuels"),
            "energyconsbeforerenewableelectricity_129":_("renewable electricity"),
            "energyconsbeforerenewableheat_130":_("renewable heat"),
            "energyconsbeforespaceheating_131":_("space heating"),
            "energyconsbeforespacecooling_132":_("space cooling"),
            "energyconsbeforewaterheating_133":_("water heating"),
            "energyconsbeforeventilation_134":_("ventilation"),
            "energyconsbeforerefrigeration_135":_("refrigeration"),
            "energyconsbeforepumps_136":_("pumps and fans"),
            "energyconsbeforecatering_137":_("catering"),
            "energyconsbeforeprocessenergy_138":_("process energy"),
            "energyconsbeforelighting_139":_("lighting"),
            "energyconsbeforeappliances_140":_("appliances"),
            "energyconsaftergridelectricity_141":_("grid electricity"),
            "energyconsaftergas_142":_("gas"),
            "energyconsafteroil_143":_("oil"),
            "energyconsaftercoal_144":_("coal/coal-based products"),
            "energyconsafterdistrictheating_145":_("district heating"),
            "energyconsafterdistrictcooling_146":_("district cooling"),
            "energyconsafterCHP_147":_("CHP"),
            "energyconsafterbiomass_148":_("biomass"),
            "energyconsafterbiofuels_149":_("biofuels"),
            "energyconsafterrenewableelectricity_150":_("renewable electricity"),
            "energyconsafterrenewableheat_151":_("renewable heat"),
            "energyconsafterspaceheating_152":_("space heating"),
            "energyconsafterspacecooling_153":_("space cooling"),
            "energyconsafterwaterheating_154":_("water heating"),
            "energyconsafterventilation_155":_("ventilation"),
            "energyconsafterrefrigeration_156":_("refrigeration"),
            "energyconsafterpumps_157":_("pumps and fans"),
            "energyconsaftercatering_158":_("catering"),
            "energyconsafterprocessenergy_159":_("process energy"),
            "energyconsafterlighting_160":_("lighting"),
            "energyconsafterppliances_161":_("appliances"),
            "adjustedenergyconsbeforetotal_162":_("total"),
            "adjustedenergyconsbeforegridelectricity_163":_("grid electricity"),
            "adjustedenergyconsbeforegas_164":_("gas"),
            "adjustedenergyconsbeforeoil_165":_("oil"),
            "adjustedenergyconsbeforecoal_166":_("coal/coal-based products"),
            "adjustedenergyconsbeforedistrictheating_167":_("district heating"),
            "adjustedenergyconsbeforedistrictcooling_168":_("district cooling"),
            "adjustedenergyconsbeforeCHP_169":_("CHP"),
            "adjustedenergyconsbeforebiomass_170":_("biomass"),
            "adjustedenergyconsbeforebiofuels_171":_("biofuels"),
            "adjustedenergyconsbeforerenewableelectricity_172":_("renewable electricity"),
            "adjustedenergyconsbeforerenewableheat_173":_("renewable heat"),
            "adjustedenergyconsbeforespaceheating_174":_("space heating"),
            "adjustedenergyconsbeforespacecooling_175":_("space cooling"),
            "adjustedenergyconsbeforewaterheating_176":_("water heating"),
            "adjustedenergyconsbeforeventilation_177":_("ventilation"),
            "adjustedenergyconsbeforerefrigeration_178":_("refrigeration"),
            "adjustedenergyconsbeforepumps_179":_("pumps and fans"),
            "adjustedenergyconsbeforecatering_180":_("catering"),
            "adjustedenergyconsbeforeprocessenergy_181":_("process energy"),
            "adjustedenergyconsbeforelighting_182":_("lighting"),
            "adjustedenergyconsbeforeappliances_183":_("appliances"),
            "adjustedenergyconsaftertotal_184":_("Total"),
            "adjustedenergyconsaftergridelectricity_185":_("grid electricity"),
            "adjustedenergyconsaftergas_186":_("gas"),
            "adjustedenergyconsafteroil_187":_("oil"),
            "adjustedenergyconsaftercoal_188":_("coal/coal-based products"),
            "adjustedenergyconsafterdistrictheating_189":_("district heating"),
            "adjustedenergyconsafterdistrictcooling_190":_("district cooling"),
            "adjustedenergyconsafterCHP_191":_("CHP"),
            "adjustedenergyconsafterbiomass_192":_("biomass"),
            "adjustedenergyconsafterbiofuels_193":_("biofuels"),
            "adjustedenergyconsafterrenewableelectricity_194":_("renewable electricity"),
            "adjustedenergyconsafterrenewableheat_195":_("renewable heat"),
            "adjustedenergyconsafterspaceheating_196":_("space heating"),
            "adjustedenergyconsafterspacecooling_197":_("space cooling"),
            "adjustedenergyconsafterwaterheating_198":_("water heating"),
            "adjustedenergyconsafterventilation_199":_("ventilation"),
            "adjustedenergyconsafterrefrigeration_200":_("refrigeration"),
            "adjustedenergyconsafterpumps_201":_("pumps and fans"),
            "adjustedenergyconsaftercatering_202":_("catering"),
            "adjustedenergyconsafterprocessenergy_203":_("process energy"),
            "adjustedenergyconsafterlighting_204":_("lighting"),
            "adjustedenergyconsafterappliances_205":_("appliances")
        }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        #self.fields['valueofeeinvestment_51'].widget.attrs['step'] = 0.02


class FactSheetSelectorForm(forms.Form):
        country = forms.ChoiceField(label='Country', choices = COUNTRIES)
        measuretype = forms.ChoiceField(label='Measure Type', choices = MEASURETYPES)
        companysize = forms.ChoiceField(label='Company Size', choices = ORGANIZATIONSIZE)
        verification = forms.ChoiceField(label='Verification', choices=VERIFIED_SIMPLE)
        buildingtype = forms.ChoiceField(label='Building Type', choices = BUILDINGTYPE)
        measuretypeindustry = forms.ChoiceField(label='Measure Type', choices=MEASURETYPES_INDUSTRY)
        measuretypebuilding = forms.ChoiceField(label='Measure Type', choices=MEASURETYPES_BUILDING)
        discountrate = forms.ChoiceField(label='Discount rate', choices=DISCOUNT_RATE)

class BenchmarkSelectorForm(forms.Form):
    country = forms.ChoiceField(label='Country', choices=COUNTRIES)
    measuretype = forms.ChoiceField(label='Measure Type', choices=MEASURETYPES)
    companysize = forms.ChoiceField(label='Company Size', choices=ORGANIZATIONSIZE)
    verification = forms.ChoiceField(label='Verification', choices=VERIFIED_SIMPLE)
    benchmarkmethod = forms.ChoiceField(label='Benchmark type', choices=BENCHMARKMETHOD)
    benchmarksector = forms.ChoiceField(label='Sector', choices=BENCHMARKSECTOR)
    buildingtype = forms.ChoiceField(label='Building Type', choices=BUILDINGTYPE)
    discountrate = forms.ChoiceField(label='Discount rate', choices=DISCOUNT_RATE)

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Upload the excel template file with project information')

    def __init__(self, *args, **kwargs):
        super(UploadExcelForm, self).__init__(*args, **kwargs)
        # only accept .xlsx files
        mime_types = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel.sheet.macroEnabled.12'
        ]
        self.fields['excel_file'].widget.attrs['accept'] = ','.join(mime_types)

class UploadExcelForVerificationForm(forms.Form):
    excel_file = forms.FileField(label='Please upload your data file according to our excel template')

    def __init__(self, *args, **kwargs):
        super(UploadExcelForVerificationForm, self).__init__(*args, **kwargs)
        # only accept .xlsx files
        mime_types = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel.sheet.macroEnabled.12'
        ]
        self.fields['excel_file'].widget.attrs['accept'] = ','.join(mime_types)


from captcha.fields import ReCaptchaField

class AllauthSignupForm(forms.Form):

    captcha = ReCaptchaField()

    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass