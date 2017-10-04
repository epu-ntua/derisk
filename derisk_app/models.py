import ast

from django.db import models
from django.contrib.auth.models import User
from derisk_app.lists import *
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Sum, Max

from derisk_app.util.formula_functions import *

import sympy
import re
from decimal import *

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def paybackgroup(paybacktime):
    paybackgrp =''
    if paybacktime > 0 and paybacktime < 1:
        paybackgrp = '00-01'
    elif paybacktime >= 1 and paybacktime < 2:
        paybackgrp = '01-02'
    elif paybacktime >= 2 and paybacktime < 3:
        paybackgrp = '02-03'
    elif paybacktime >= 3 and paybacktime < 4:
        paybackgrp = '03-04'
    elif paybacktime >= 4 and paybacktime < 5:
        paybackgrp = '04-05'
    elif paybacktime >= 5 and paybacktime < 6:
        paybackgrp = '05-06'
    elif paybacktime >= 6 and paybacktime < 7:
        paybackgrp = '06-07'
    elif paybacktime >= 7 and paybacktime < 8:
        paybackgrp = '07-08'
    elif paybacktime >= 8 and paybacktime < 9:
        paybackgrp = '08-09'
    elif paybacktime >= 9 and paybacktime < 10:
        paybackgrp = '09-10'
    elif paybacktime >= 10 and paybacktime < 12:
        paybackgrp = '10-12'
    elif paybacktime >= 12 and paybacktime < 16:
        paybackgrp = '12-15'
    elif paybacktime >= 16 and paybacktime < 21:
        paybackgrp = '16-20'
    elif paybacktime >= 21 and paybacktime < 26:
        paybackgrp = '21-25'
    elif paybacktime >= 26 and paybacktime < 30:
        paybackgrp = '26-30'
    elif paybacktime >= 30:
        paybackgrp = '30-'
    return paybackgrp

class UserProfile(models.Model):
    """
    Extends basic User class in django.contrib.auth
    """
    user = models.OneToOneField(User)
    name = models.CharField(max_length=256, blank=True,null=True)
    telephone = models.CharField(max_length=256, blank=True,null=True)  
    organization = models.CharField(max_length=256, blank=True,null=True)
    organizationnature = models.CharField(max_length=256, blank=True,null=True, choices = NATUREORGANIZATION)
    organizationnatureother = models.CharField(max_length=256, blank=True,null=True)
    sample_size_limit = models.CharField(max_length=80, blank=False,null=False, default = 10, choices = SAMPLE_SIZE_LIMIT)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Measure(models.Model):
    def __str__(self):
        return self.title
    code = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=200, blank=False)
    root_title = models.CharField(max_length=200, blank=False)
    lifetime = models.IntegerField(blank=True, null=True, default=None)


class Benefit(models.Model):
  def __str__(self):
     return self.description
  description = models.CharField(max_length=50, blank=False)
 
# Create your models here.
class Project(models.Model):
    # General information
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    sharing_level = models.CharField(help_text = 'Please describe the sharing level of this project',max_length=3,blank=False, default = 'PRI',choices = SHARINGLEVEL)
    original_project_id_1 = models.IntegerField(blank=True, null=True, default=None)
    title_2 = models.CharField(max_length=500, blank=True, null=True)
    user_note = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country_3 = models.CharField(help_text = 'The country of where the investment is located',max_length=4, blank=True, null=True, choices = COUNTRIES)
    zipcode_4 = models.CharField(help_text = 'The Zip code of where the investment is located',max_length=500, blank=True, null=True)
    nutscode_4 = models.CharField(help_text = 'The NUTS code of where the investment is located',max_length=500, blank=True, null=True)
    city_5 = models.CharField(help_text = 'The city of where the investment is located',max_length=500, blank=True, null=True)
    fulladdress_6 = models.CharField(help_text = 'The full address of where the investment is located', max_length=500, blank=True, null=True)
    organizationname_7 = models.CharField(help_text = 'Host organization name', max_length=500, blank=True, null=True)
    sitename_8 = models.CharField(help_text = 'Host organization - Site name - location of investment',max_length=500, blank=True, null=True)
    contactperson_9 = models.CharField(help_text = 'The country of where the investment is located',max_length=500, blank=True, null=True)
    email_10 = models.EmailField(help_text = 'Host organization - Email',blank=True, null=True)
    telephone_11 = models.CharField(max_length=500, help_text='Host organization - Telephone',blank=True, null=True)
    istheinvestmentinabuilding_12 = models.CharField(max_length=500, help_text='Please select if  the investment is in a building, industry or infrastructure',blank=True, null=True, choices = INVESTMENTBUILDING)
    istheinvestmentinabuildingother_12 = models.CharField(max_length=500, help_text='Please specify other option',blank=True, null=True)
    industrysector_13 = models.CharField(max_length=500, help_text='Please select the Industry Sector/Organisation type.',blank=True, null=True, choices = INDUSTRYSECTOR)
    industrysectorother_13 = models.CharField(max_length=500, help_text='Please specify other for the Industry Sector/Organisation type. ',blank=True, null=True)
    organizationsize_14 = models.CharField(max_length=50, help_text='Please select the Organisation size. Leave blank for buildings.',blank=True, null=True, choices = ORGANIZATIONSIZE)
    buildingtype_15 = models.CharField(max_length=50, help_text='Please select the Building type',blank=True, null=True, choices = BUILDINGTYPE)
    ownership_16 = models.CharField(max_length=50, help_text='Please select the Ownership type',blank=True, null=True, choices = OWNERSHIP)
    floorarea_17 = models.DecimalField(max_digits=25, decimal_places=0,help_text='Please specify  the Floor area of building in m2 ',blank=True, null=True)
    measures_18 = models.ManyToManyField(Measure,help_text='Please select which measures are included in the investment. You can add more than one.',blank=True)
    energydemandbefore_19 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Only valid for measures 1 (Heating) to 10 (Pumps), Please  specify total annual energy demand for relevant components before investment (kWh/y). Relevant components means the components that are included in the project. ',blank=True, null=True)
    energydemandafter_20 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please  specify total annual energy demand for relevant components after investment (kWh/y). Relevant components means the components that are included in the project. Only valid for measures 1 (Heating) to 10 (Pumps)',blank=True, null=True)
    initialcapacity_21 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please  specify total initial capacity (kW) for relevant components. Relevant components means the components that are included in the project. If more components, use weighed average of relevant components. Only valid for measures 1 (Heating) to 10 (Pumps)',blank=True, null=True)
    uvaluebefore_22 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify U-value (W/m2K), for relevant building components before investment. If more individual components, enter weighed average value for relevant components. Only valid for measures 12 - Building Fabric Measures',blank=True, null=True)
    uvalueafter_23 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify U-value (W/m2K), for relevant building components after investment. If more individual components, enter weighed average value for relevant components. Only valid for measures 12 - Building Fabric Measures',blank=True, null=True)
    arearenovated_24 = models.DecimalField(max_digits=25, decimal_places=0,help_text='Please specify area renovated (m2). Only valid for measures 12 - Building Fabric Measures',blank=True, null=True)
    efficiencybefore_25 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify efficiency before investment (%). Only valid for measures 13 - HVAC Plant',blank=True, null=True)
    efficiencyafter_26 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify  efficiency after investment  (%).Only valid for measures 13 - HVAC Plant',blank=True, null=True)
    sizeoftheHVACPlant_27 = models.DecimalField(max_digits=25, decimal_places=4,max_length=500, help_text='Please specify  size (kW).Only valid for measures 13 - HVAC Plant',blank=True, null=True)
    projectstartdate_28 = models.CharField(max_length=10,help_text='Please state the project start date for energy efficiency investment (month /year)',blank=True, null=True)
    dateinvestmentbecameoperational_29 = models.CharField(max_length=10,help_text='Please state the Date investment became operational (month/year)',blank=True, null=True)
    averagelifetimeofmeasures_30 = models.IntegerField(help_text='Please state the  Average lifetime of measures (approx) (years)',blank=True, null=True)
    energyconsumptionbefore_31 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please state the energy consumption before intervention in KWh/a. Total billed annual energy use (all sources)',blank=True, null=True)
    energyperformancecertificatebefore_32 = models.CharField(max_length=500, help_text='What was the energy performance cerificate rating before intervention?',blank=True, null=True)
    breakdownofconsumptionbyfueltype_33 = models.CharField(max_length=500, help_text='Energy consumption before intervention breakdown by fuel',blank=True, null=True)
    breakdownofconsumptionbyenduse_34 = models.CharField(max_length=500, help_text='Energy consumption before intervention end use',blank=True, null=True)
    sourceofconsumptionbefore_35 = models.CharField(max_length=500, help_text='Please select what was the source of consumption before intervention from the list', choices = SOURCECONSUMPTIONBEFORE, blank=True, null=True)
    sourceofconsumptionbeforeother_35 = models.CharField(max_length=500, help_text='Please specify the source of consumption',blank=True, null=True)
    predictedenergyconsumptionafter_36 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify the Predicted Energy Consumption AFTER intervention in KWh/a',blank=True, null=True)
    whatisthebasisoftheforecast_37 = models.CharField(max_length=500, help_text='Please select what is the basis of the forecast',choices = BASISFORECAST, blank=True, null=True)
    whatisthebasisoftheforecastother_37 = models.CharField(max_length=500, help_text='Please specify other',blank=True, null=True)
    energyconsumptionafter_38 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify the Energy Consumption AFTER intervention (actual) in KWh/a.Total billed annual energy use (all sources)',blank=True, null=True)
    energyperformancecertificateafter_39 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Energy Performance Certificate rating AFTER intervention',blank=True, null=True)
    breakdownofconsumptionbyfueltype_40 = models.CharField(max_length=500, help_text='Energy consumption after intervention breakdown by fuel to be filled in indicator (141) - (151)',blank=True, null=True)
    sourceofconsumptionafter_41 = models.CharField(max_length=500, help_text='Please specify source of consumption after intervention (actual)',choices = SOURCECONSUMPTIONAFTER, blank=True, null=True)
    sourceofconsumptionafterother_41 = models.CharField(max_length=500, help_text='Please specify other',blank=True,null=True)
    havetheprojectenergysavingsbeenverified_42 = models.CharField(max_length=50, help_text='Please select if and how the project energy savings have been independently verified',blank=True, null=True, choices = VERIFIED)
    methodologyforindependentverification_43 = models.CharField(max_length=500, help_text='Please state the methodology for independent verification (e.g. IPMVP)',blank=True, null=True)
    productionrate_44 = models.DecimalField(max_digits=25, decimal_places=2, help_text='Please specify any adjustments that need to be made in order to make the BEFORE and ACTUAL AFTER energy use directly comparable.  For example, if production rate is increased by 10% in the AFTER period compared to BEFORE, insert +10% .  LEAVE BLANK IF NO SIGNIFICANT CHANGE',blank=True, null=True)
    floorarea_45 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify the floor area',blank=True, null=True)
    comfort_46 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify comfort',blank=True, null=True)
    heatingload_47 = models.DecimalField(max_digits=25,decimal_places=2, help_text='Please specify heating load',blank=True, null=True)
    coolingload_48 = models.DecimalField(max_digits=25,decimal_places=2, help_text='Please specify cooling load',blank=True, null=True)
    totalvalueofasset_49 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Total Value  of Asset (in Euro)',blank=True, null=True)
    totalvalueofinvestment_50 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Total Value  of investment (inclusive of EE component)',blank=True, null=True)
    valueofeeinvestment_51 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Value of EE investment (in Euro)',blank=True, null=True)
    annualenergycostsavings_52 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Annual energy cost savings (latest, or representative year) (in Euro)',blank=True, null=True)
    additionalfinancialbenefits_53 = models.DecimalField(max_digits=25, decimal_places=2,max_length=500, help_text='Please specify Additional financial benefits (e.g. maintenance savings) (in Euro)',blank=True, null=True)
    additionalcosts_54 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Additional costs (in Euro)',blank=True, null=True)
    netannualsaving_55 = models.DecimalField(max_digits=25, decimal_places=2,max_length=500, help_text='Please specify Net annual saving',blank=True, null=True)
    npvprior_56 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify NPV (computed prior to investment)',blank=True, null=True)
    npvactual_57 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify NPV actual',blank=True, null=True)
    irrprior_58 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify IRR (computed prior to investment)',blank=True, null=True)
    irractual_59 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify IRR actual',blank=True, null=True)
    sourceoffinance_60 = models.CharField(max_length=500,help_text='Please specify Source of finance',blank=True, null=True)
    valueofgrant_61 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify Value of grant/subsidy (if any) (in Euro)',blank=True, null=True)
    provider_62 = models.CharField(max_length=500, help_text='Please specify Provider',blank=True, null=True)
    valueofloan_63 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify Value of loan (if any) (in Euro)',blank=True, null=True)
    loanrepaymentterm_64 = models.DecimalField(max_digits=25, decimal_places=0,help_text='Please specify Loan repayment term',blank=True, null=True)
    interestrate_65 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify Interest rate',blank=True, null=True)
    keyreasonsformakinginvestment_66 = models.CharField(max_length=500, help_text='Please state key reasons for making investment',blank=True, null=True)
    nonfinancialbenefits_67 = models.ManyToManyField(Benefit, help_text='Please state any non-financial benefits realised by the project',blank=True)
    financialperformance_68 = models.CharField(max_length=500, help_text='Please rate actual financial performance compared with expectation',blank=True, null=True, choices = SATISFACTION)
    overallsatisfaction_69 = models.CharField(max_length=500, help_text='Please rate overall satisfaction with the investment',blank=True, null=True,choices = SATISFACTION)
    otherinformation_70 = models.TextField( help_text='Please describe/attach any other information you would like to share concerning your investment, e.g. technical specifications, before/after status, etc',blank=True, null=True)
    energysavingstotal_71 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, total',blank=True, null=True)
    energysavingsgridelectricity_72 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, grid electricity',blank=True, null=True)
    energysavingsgas_73 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, gas',blank=True, null=True)
    energysavingsoil_74 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, oil',blank=True, null=True)
    energysavingscoal_75 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, coal/coal-based products',blank=True, null=True)
    energysavingsdistrictheating_76 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, district heating',blank=True, null=True)
    energysavingsdistrictcooling_77 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, district cooling',blank=True, null=True)
    energysavingsCHP_78 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, CHP',blank=True, null=True)
    energysavingsbiomass_79 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, biomass',blank=True, null=True)
    energysavingsbiofuels_80 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, biofuels',blank=True, null=True)
    energysavingselectricity_81 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, renewable electricity',blank=True, null=True)
    energysavingsrenewableheat_82 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings, renewable heat',blank=True, null=True)
    adjustedenergysavingstotal_83 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, total',blank=True, null=True)
    adjustedenergysavingstotalgridelectricity_84 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, grid electricity',blank=True, null=True)
    adjustedenergysavingstotalgas_85 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, gas',blank=True, null=True)
    adjustedenergysavingstotaloil_86 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, oil',blank=True, null=True)
    adjustedenergysavingstotalcoal_87 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, coal/coal-based products',blank=True, null=True)
    adjustedenergysavingstotaldistrictheating_88 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, district heating',blank=True, null=True)
    adjustedenergysavingstotaldistrictcooling_89 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, district cooling',blank=True, null=True)
    adjustedenergysavingstotalCHP_90 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, CHP',blank=True, null=True)
    adjustedenergysavingstotalbiomass_91 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, biomass',blank=True, null=True)
    adjustedenergysavingstotalbiofuels_92 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, biofuels',blank=True, null=True)
    adjustedenergysavingstotalrenewableelectricity_93 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, renewable electricity',blank=True, null=True)
    adjustedenergysavingstotalrenewableheat_94 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy savings adjusted for weather/season/production, renewable heat',blank=True, null=True)
    hastheadjustedenergysavingsverified_95 = models.CharField(max_length=500,help_text='Please specify Have the adjusted project energy savings been independently verified?',blank=True, null=True, choices = VERIFIED)
    energypricebeforetotal_96 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, total',blank=True, null=True)
    energypricebeforegridelectricity_97 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, grid electricity',blank=True, null=True)
    energypricebeforegas_98 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, gas',blank=True, null=True)
    energypricebeforeoil_99 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, oil',blank=True, null=True)
    energypricebeforecoal_100 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, coal/coal-based products',blank=True, null=True)
    energypricebeforedistrictheating_101 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, district heating',blank=True, null=True)
    energypricebeforedistrictcooling_102 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, district cooling',blank=True, null=True)
    energypricebeforeCHP_103 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, CHP',blank=True, null=True)
    energypricebeforebiomass_104 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, biomass',blank=True, null=True)
    energypricebeforebiofuels_105 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, biofuels',blank=True, null=True)
    energypricebeforerenewableelectricity_106 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, renewable electricity',blank=True, null=True)
    energypricebeforerenewableheat_107 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price before intervention, EUR/kWh, renewable heat',blank=True, null=True)
    energypriceaftertotal_108 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, total',blank=True, null=True)
    energypriceaftergridelectricity_109 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, grid electricity',blank=True, null=True)
    energypriceaftergas_110 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, gas',blank=True, null=True)
    energypriceafteroil_111 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, oil',blank=True, null=True)
    energypriceaftercoal_112 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, coal/coal-based products',blank=True, null=True)
    energypriceafterdistrictheating_113 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, district heating',blank=True, null=True)
    energypriceafterdistrictcooling_114 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, district cooling',blank=True, null=True)
    energypriceafterCHP_115 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, CHP',blank=True, null=True)
    energypriceafterbiomass_116 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, biomass',blank=True, null=True)
    energypriceafterbiofuels_117 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, biofuels',blank=True, null=True)
    energypriceafterrenewableelectricity_118 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, renewable electricity',blank=True, null=True)
    energypriceafterrenewableheat_119 = models.DecimalField(max_digits=25, decimal_places=2,help_text='Please specify energy price after intervention, EUR/kWh, renewable heat',blank=True, null=True)
    energyconsbeforegridelectricity_120 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, grid electricity',blank=True, null=True)
    energyconsbeforegas_121 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, gas',blank=True, null=True)
    energyconsbeforeoil_122 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, oil',blank=True, null=True)
    energyconsbeforecoal_123 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, coal/coal-based products',blank=True, null=True)
    energyconsbeforedistrictheating_124 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, district heating',blank=True, null=True)
    energyconsbeforedistrictcooling_125 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, district cooling',blank=True, null=True)
    energyconsbeforeCHP_126 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, CHP',blank=True, null=True)
    energyconsbeforebiomass_127 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, biomass',blank=True, null=True)
    energyconsbeforebiofuels_128 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, biofuels',blank=True, null=True)
    energyconsbeforerenewableelectricity_129 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, renewable electricity',blank=True, null=True)
    energyconsbeforerenewableheat_130 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, renewable heat',blank=True, null=True)
    energyconsbeforespaceheating_131 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, space heating',blank=True, null=True)
    energyconsbeforespacecooling_132 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, space cooling',blank=True, null=True)
    energyconsbeforewaterheating_133 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, water heating',blank=True, null=True)
    energyconsbeforeventilation_134 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, ventilation',blank=True, null=True)
    energyconsbeforerefrigeration_135 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, refrigeration',blank=True, null=True)
    energyconsbeforepumps_136 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, pumps and fans',blank=True, null=True)
    energyconsbeforecatering_137 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, catering',blank=True, null=True)
    energyconsbeforeprocessenergy_138 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, process energy',blank=True, null=True)
    energyconsbeforelighting_139 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, lighting',blank=True, null=True)
    energyconsbeforeappliances_140 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, appliances',blank=True, null=True)
    energyconsaftergridelectricity_141 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, grid electricity',blank=True, null=True)
    energyconsaftergas_142 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, gas',blank=True, null=True)
    energyconsafteroil_143 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, oil',blank=True, null=True)
    energyconsaftercoal_144 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, coal/coal-based products',blank=True, null=True)
    energyconsafterdistrictheating_145 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, district heating',blank=True, null=True)
    energyconsafterdistrictcooling_146 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, district cooling',blank=True, null=True)
    energyconsafterCHP_147 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, CHP',blank=True, null=True)
    energyconsafterbiomass_148 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, biomass',blank=True, null=True)
    energyconsafterbiofuels_149 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, biofuels',blank=True, null=True)
    energyconsafterrenewableelectricity_150 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, renewable electricity',blank=True, null=True)
    energyconsafterrenewableheat_151 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, renewable heat',blank=True, null=True)
    energyconsafterspaceheating_152 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, space heating',blank=True, null=True)
    energyconsafterspacecooling_153 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, space cooling',blank=True, null=True)
    energyconsafterwaterheating_154 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, water heating',blank=True, null=True)
    energyconsafterventilation_155 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, ventilation',blank=True, null=True)
    energyconsafterrefrigeration_156 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, refrigeration',blank=True, null=True)
    energyconsafterpumps_157 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, pumps and fans',blank=True, null=True)
    energyconsaftercatering_158 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, catering',blank=True, null=True)
    energyconsafterprocessenergy_159 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, process energy',blank=True, null=True)
    energyconsafterlighting_160 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, lighting',blank=True, null=True)
    energyconsafterppliances_161 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, appliances',blank=True, null=True)
    adjustedenergyconsbeforetotal_162 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, total',blank=True, null=True)
    adjustedenergyconsbeforegridelectricity_163 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, grid electricity',blank=True, null=True)
    adjustedenergyconsbeforegas_164 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, gas',blank=True, null=True)
    adjustedenergyconsbeforeoil_165 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, oil',blank=True, null=True)
    adjustedenergyconsbeforecoal_166 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, coal/coal-based products',blank=True, null=True)
    adjustedenergyconsbeforedistrictheating_167 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, district heating',blank=True, null=True)
    adjustedenergyconsbeforedistrictcooling_168 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, district cooling',blank=True, null=True)
    adjustedenergyconsbeforeCHP_169 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, CHP',blank=True, null=True)
    adjustedenergyconsbeforebiomass_170 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, biomass',blank=True, null=True)
    adjustedenergyconsbeforebiofuels_171 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, biofuels',blank=True, null=True)
    adjustedenergyconsbeforerenewableelectricity_172 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, renewable electricity',blank=True, null=True)
    adjustedenergyconsbeforerenewableheat_173 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, renewable heat',blank=True, null=True)
    adjustedenergyconsbeforespaceheating_174 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, space heating',blank=True, null=True)
    adjustedenergyconsbeforespacecooling_175 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, space cooling',blank=True, null=True)
    adjustedenergyconsbeforewaterheating_176 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, water heating',blank=True, null=True)
    adjustedenergyconsbeforeventilation_177 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, ventilation',blank=True, null=True)
    adjustedenergyconsbeforerefrigeration_178 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, refrigeration',blank=True, null=True)
    adjustedenergyconsbeforepumps_179 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, pumps and fans',blank=True, null=True)
    adjustedenergyconsbeforecatering_180 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, catering',blank=True, null=True)
    adjustedenergyconsbeforeprocessenergy_181 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, process energy',blank=True, null=True)
    adjustedenergyconsbeforelighting_182 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, lighting',blank=True, null=True)
    adjustedenergyconsbeforeappliances_183 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption before intervention, adjusted for weather/season/production, appliances',blank=True, null=True)
    adjustedenergyconsaftertotal_184 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, total',blank=True, null=True)
    adjustedenergyconsaftergridelectricity_185 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, grid electricity',blank=True, null=True)
    adjustedenergyconsaftergas_186 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, gas',blank=True, null=True)
    adjustedenergyconsafteroil_187 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, oil',blank=True, null=True)
    adjustedenergyconsaftercoal_188 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, coal/coal-based products',blank=True, null=True)
    adjustedenergyconsafterdistrictheating_189 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, district heating',blank=True, null=True)
    adjustedenergyconsafterdistrictcooling_190 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, district cooling',blank=True, null=True)
    adjustedenergyconsafterCHP_191 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, CHP',blank=True, null=True)
    adjustedenergyconsafterbiomass_192 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, biomass',blank=True, null=True)
    adjustedenergyconsafterbiofuels_193 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, biofuels',blank=True, null=True)
    adjustedenergyconsafterrenewableelectricity_194 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, renewable electricity',blank=True, null=True)
    adjustedenergyconsafterrenewableheat_195 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, renewable heat',blank=True, null=True)
    adjustedenergyconsafterspaceheating_196 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, space heating',blank=True, null=True)
    adjustedenergyconsafterspacecooling_197 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, space cooling',blank=True, null=True)
    adjustedenergyconsafterwaterheating_198 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, water heating',blank=True, null=True)
    adjustedenergyconsafterventilation_199 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, ventilation',blank=True, null=True)
    adjustedenergyconsafterrefrigeration_200 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, refrigeration',blank=True, null=True)
    adjustedenergyconsafterpumps_201 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, pumps and fans',blank=True, null=True)
    adjustedenergyconsaftercatering_202 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, catering',blank=True, null=True)
    adjustedenergyconsafterprocessenergy_203 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, process energy',blank=True, null=True)
    adjustedenergyconsafterlighting_204 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, lighting',blank=True, null=True)
    adjustedenergyconsafterappliances_205 = models.DecimalField(max_digits=25, decimal_places=4,help_text='Please specify energy consumption after intervention, adjusted for weather/season/production, appliances',blank=True, null=True)
    indicator_energy_saved_AK = models.DecimalField(max_digits=25, decimal_places=4,help_text='Indicator for energy saved', blank=True, null=True)
    indicator_simple_payback_time_AA = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for simple payback time', blank=True, null=True)
    indicator_grouped_simple_payback_time_AB = models.CharField(max_length=5,help_text='Indicator for grouped simple payback time', blank=True, null=True)
    indicator_other_saving_time_W = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for other saving',blank=True, null=True)
    indicator_EURmwha_AT = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for other EUR/Mwh/a',blank=True, null=True)
    indicator_EURm2_AU = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for other EUR/m2',blank=True, null=True)
    indicator_unit_energy_before_AC = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for unit energy before', blank=True, null=True)
    indicator_unit_energy_forecast_AD = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for unit energy forecast', blank=True, null=True)
    indicator_unit_energy_after_AE = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for unit energy after', blank=True, null=True)
    indicator_unit_energy_saved_actual_AI = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for unit energy saved actual', blank=True, null=True)
    indicator_forecast_optimism_AN =models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for forecast optimism', blank=True, null=True)
    indicator_climate_G = models.CharField(max_length=200,  help_text='Indicator for climate', blank=True, null=True, choices = CLIMATEZONES)
    indicator_avoidance_cost_AT = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for avoidance cost', blank=True, null=True)
    indicator_area_CAPEX_AU = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for area capex', blank=True, null=True)
    indicator_saving_pct_forecast_AL = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for saving pct forecast', blank=True, null=True)
    indicator_saving_pct_actual_AM = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for saving pct actual', blank=True, null=True)
    indicator_saving_pct_other_AS = models.DecimalField(max_digits=25, decimal_places=2, help_text='Indicator for saving pct other', blank=True, null=True)
    indicator_simple_payback_time_aftergrant = models.DecimalField(max_digits=25, decimal_places=2,help_text='Indicator for simple payback time after grant', blank=True, null=True)
    measures_main = models.CharField(max_length=200,blank=True, null=True)
    verified_simple = models.CharField(max_length=15,help_text='Please select if and how the project energy savings have been independently verified',blank=True, null=True, choices=VERIFIED_SIMPLE)
    indicator_avoidance_cost_lifetime = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure', blank=True, null=True)
    indicator_avoidance_cost0 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 0', blank=True, null=True)
    indicator_avoidance_cost1 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 1', blank=True, null=True)
    indicator_avoidance_cost2 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 2', blank=True, null=True)
    indicator_avoidance_cost3 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 3', blank=True, null=True)
    indicator_avoidance_cost4 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 4', blank=True, null=True)
    indicator_avoidance_cost5 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 5', blank=True, null=True)
    indicator_avoidance_cost6 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 6', blank=True, null=True)
    indicator_avoidance_cost7 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 7', blank=True, null=True)
    indicator_avoidance_cost8 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 8', blank=True, null=True)
    indicator_avoidance_cost9 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 9', blank=True, null=True)
    indicator_avoidance_cost10 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 10', blank=True, null=True)
    indicator_avoidance_cost11 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 11', blank=True, null=True)
    indicator_avoidance_cost12 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 12', blank=True, null=True)
    indicator_avoidance_cost13 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 13', blank=True, null=True)
    indicator_avoidance_cost14 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 14', blank=True, null=True)
    indicator_avoidance_cost15 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 15', blank=True, null=True)
    indicator_avoidance_cost16 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 16', blank=True, null=True)
    indicator_avoidance_cost17 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 17', blank=True, null=True)
    indicator_avoidance_cost18 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 18', blank=True, null=True)
    indicator_avoidance_cost19 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 19', blank=True, null=True)
    indicator_avoidance_cost20 = models.DecimalField(max_digits=25, decimal_places=4, help_text='Average cost in Eurocent for each kWh energy saved over the lifetime of the measure with discount rate 20', blank=True, null=True)
    def save(self, force_insert=False, force_update=False, **kwargs):
        #Simplify verification column
        if self.havetheprojectenergysavingsbeenverified_42 is not None and self.havetheprojectenergysavingsbeenverified_42.strip() != '':
            if self.havetheprojectenergysavingsbeenverified_42 == 'not verified':
                self.verified_simple = 'Non-verified'
            else:
                self.verified_simple = 'Verified'
        else:
            self.verified_simple = 'Unknown'
        #indicator_energy_saved_AK
        if self.energyconsumptionbefore_31 is not None and self.energyconsumptionafter_38 is not None:
            self.indicator_energy_saved_AK = self.energyconsumptionbefore_31 - self.energyconsumptionafter_38
        else:
            self.indicator_energy_saved_AK = self.energysavingstotal_71
        #indicator_other_saving_time_W
        if self.additionalfinancialbenefits_53 is not None:
            self.additionalfbenefits = self.additionalfinancialbenefits_53
        else:
            self.additionalfbenefits = 0
        if self.additionalcosts_54 is not None:
            self.additionalcosts = self.additionalcosts_54
        else:
            self.additionalcosts = 0
        self.indicator_other_saving_time_W = self.additionalfbenefits - self.additionalcosts

        #indicator_simple_payback_time_AA
        if self.netannualsaving_55 is not None and self.valueofeeinvestment_51 is not None:
            if self.indicator_other_saving_time_W is not None:
                othersaving = self.indicator_other_saving_time_W
            else:
                othersaving = 0
            if self.netannualsaving_55 + othersaving > 0:
                self.indicator_simple_payback_time_AA = self.valueofeeinvestment_51 / (self.netannualsaving_55 + othersaving)
                curGrant = 0
                if self.valueofgrant_61 is not None:
                    curGrant = self.valueofgrant_61
                self.indicator_simple_payback_time_aftergrant = (self.valueofeeinvestment_51 - curGrant) / (self.netannualsaving_55 + othersaving)
            else:
                self.indicator_simple_payback_time_AA = 0
                self.indicator_simple_payback_time_aftergrant = 0
        else:
            self.indicator_simple_payback_time_AA = 0
            self.indicator_simple_payback_time_aftergrant = 0
        #indicator_grouped_simple_payback_time_AB
        self.indicator_grouped_simple_payback_time_AB = paybackgroup(self.indicator_simple_payback_time_AA)
        #indicator indicator_EURmwha_AT
        if self.indicator_energy_saved_AK  is not None and self.valueofeeinvestment_51 is not None:
            if self.indicator_energy_saved_AK  > 0:
               self.indicator_EURmwha_AT = self.valueofeeinvestment_51 / self.indicator_energy_saved_AK

        # indicator indicator_EURm2
        if self.floorarea_17 is not None:
            if self.netannualsaving_55 is not None:
                if self.floorarea_17 > 0:
                    self.indicator_EURm2_AU = self.netannualsaving_55 / self.floorarea_17
            elif self.energyconsumptionbefore_31 is not None and self.energyconsumptionafter_38 is not None:
                if self.floorarea_17 > 0:
                    self.indicator_EURm2_AU = (self.energyconsumptionafter_38 - self.energyconsumptionbefore_31) / self.floorarea_17

        # indicator unit energy before,forecast and after
        if self.floorarea_17 is not None and self.energyconsumptionbefore_31 is not None:
            if self.floorarea_17 > 0:
                self.indicator_unit_energy_before_AC = self.energyconsumptionbefore_31 / self.floorarea_17

        if self.floorarea_17 is not None and self.predictedenergyconsumptionafter_36 is not None:
            if self.floorarea_17 > 0:
                self.indicator_unit_energy_forecast_AD = self.predictedenergyconsumptionafter_36 / self.floorarea_17

        if self.floorarea_17 is not None and self.energyconsumptionafter_38 is not None:
            if self.floorarea_17 > 0:
                self.indicator_unit_energy_after_AE = self.energyconsumptionafter_38 / self.floorarea_17

        # indicator forecast optimism

        if self.indicator_unit_energy_before_AC is not None and self.indicator_unit_energy_forecast_AD is not None and \
           self.indicator_unit_energy_after_AE is not None :
            if self.indicator_unit_energy_before_AC >0 and self.indicator_unit_energy_forecast_AD >0 and \
                            self.indicator_unit_energy_after_AE >0:
                self.indicator_forecast_optimism_AN = self.indicator_unit_energy_after_AE / self.indicator_unit_energy_before_AC - self.indicator_unit_energy_forecast_AD / self.indicator_unit_energy_before_AC
        # indicator_unit_energy_saved_actual
        if self.indicator_unit_energy_before_AC is not None and  self.indicator_unit_energy_after_AE is not None:
            self.indicator_unit_energy_saved_actual_AI = self.indicator_unit_energy_before_AC - self.indicator_unit_energy_after_AE
        # indicator_climate_G
        # To decide the algorithm for calculating climate_g
        # indicator_avoidance_cost_AT
        if self.indicator_energy_saved_AK is not None and self.valueofeeinvestment_51 is not None:
            if self.indicator_energy_saved_AK > 0:
                self.indicator_avoidance_cost_AT = self.valueofeeinvestment_51 / self.indicator_energy_saved_AK
        # indicator_area__CAPEX_AU
        if self.floorarea_17 is not None and self.valueofeeinvestment_51 is not None:
            if self.floorarea_17 > 0:
               self.indicator_area_CAPEX_AU = self.valueofeeinvestment_51 / self.floorarea_17
        # indicator_saving_pct_other_AS
        if self.indicator_other_saving_time_W is not None and self.netannualsaving_55 is not None:
            if self.indicator_other_saving_time_W > 0:
                 self.indicator_saving_pct_other_AS = self.indicator_other_saving_time_W / (self.indicator_other_saving_time_W + self.netannualsaving_55)
        # indicator_saving_pct_forecast_AL
        if self.indicator_unit_energy_before_AC is not None and self.indicator_unit_energy_forecast_AD is not None:
            if self.indicator_unit_energy_before_AC > 0 and self.indicator_unit_energy_forecast_AD > 0 :
                self.indicator_saving_pct_forecast_AL = -1 * (self.indicator_unit_energy_forecast_AD / self.indicator_unit_energy_before_AC-1)
        # indicator_saving_pct_actual_AM
        if self.indicator_unit_energy_before_AC is not None and self.indicator_unit_energy_after_AE is not None:
            if self.indicator_unit_energy_before_AC > 0 and self.indicator_unit_energy_after_AE > 0 :
                self.indicator_saving_pct_actual_AM = -1 *(self.indicator_unit_energy_after_AE/self.indicator_unit_energy_before_AC-1)
        super(Project, self).save(force_insert, force_update)

    # When measures change, map multiple measures into a single description for all of them
    @staticmethod
    def measures_changed(sender,instance, **kwargs):

        def calculate_indicator_avoidance_cost(inst, lf, k):
            if k == 0:
                ac = 100 * inst.valueofeeinvestment_51 / (inst.indicator_energy_saved_AK * lf)
            else:
                ac = 100 * (inst.valueofeeinvestment_51 / inst.indicator_energy_saved_AK)
                ac /= ((1 - (1 + 0.01 * k)**(-1 * lf)) / (0.01 * k))

            return ac

        countMeasures = instance.measures_18.all().count()

        # initially clear
        instance.measures_main = ''

        if countMeasures > 0:
            # Rule 1-For industry - allow only one measure type.
            # If more than one,  take the first of the measures and ignore others
            if instance.istheinvestmentinabuilding_12 == 'Industry':
                instance.measures_main = instance.measures_18.first().root_title

                # avoidance cost estimation
                if instance.valueofeeinvestment_51 is not None and instance.indicator_energy_saved_AK is not None and instance.indicator_energy_saved_AK > 0 :
                    lifetime = instance.measures_18.first().lifetime
                    for i in range(0, 21):
                        setattr(instance, 'indicator_avoidance_cost%d' % i,
                                calculate_indicator_avoidance_cost(instance, lifetime, i))

            elif instance.istheinvestmentinabuilding_12 == 'Building':
                # Avoidance Cost
                if instance.valueofeeinvestment_51 is not None and instance.indicator_energy_saved_AK is not None and instance.indicator_energy_saved_AK > 0:
                    lifetime = instance.measures_18.aggregate(Max('lifetime'))['lifetime__max']
                    for i in range(0, 21):
                        setattr(instance, 'indicator_avoidance_cost%d' % i,
                                calculate_indicator_avoidance_cost(instance, lifetime, i))

                # Rule 2 - For buildings - Take the lowest common category if exists

                # first check 2nd level (first 6 characters of code)
                # then the 1st level (first 3 characters of code)
                for idx in [6, 3]:
                    cur_code = instance.measures_18.first().code[0:idx]
                    if instance.measures_18.filter(code__startswith=cur_code).count() == countMeasures:
                        # All measures of project have the same level code
                        instance.measures_main = Measure.objects.get(code=cur_code).root_title
                        break

                if not instance.measures_main:
                    instance.measures_main = 'Integrated Renovation'

        # save anyway
        instance.save()

m2m_changed.connect(Project.measures_changed, sender=Project.measures_18.through)


class Chart(models.Model):
    # generic information
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    title = models.TextField(blank=False, null=False)

    # chart type & format
    chart_type = models.CharField(max_length=255)
    chart_format = models.CharField(max_length=255)

    # fields & filtering information
    fields = models.TextField(editable=False)
    filters = models.TextField(editable=False)

    # is this a template?
    is_template = models.BooleanField(default=False)

    def __str__(self):
        return '%s (created by %s) - %s' % (self.title, self.created_by.username,
                                            '[Template]' if self.is_template else '[Chart]')


class InvalidUnitError(ValueError):
    pass


class Formula(models.Model):
    # generic information
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    name = models.TextField(blank=False, null=False)

    # the actual formula
    # e.g (`energydemandbefore_19` - `energydemandafter_20`)/`energydemandbefore_19`
    value = models.TextField(blank=False, null=False)

    # is this a public formula?
    is_valid = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    @property
    def dependencies(self):
        """
        :return: A list with all the variables used in the formula
        """
        return list(set([prop[1:-1] for prop in re.findall(r'`\w+`', self.value)]))

    @property
    def internal_value(self):
        return '$%d' % self.pk

    @staticmethod
    def math():
        return [fn['name'].split('(')[0] for fn in MATH_FUNCTIONS]

    @staticmethod
    def random():
        return [fn['name'].split('(')[0] for fn in RAND_FUNCTIONS]

    @staticmethod
    def trig():
        return [fn['name'].split('(')[0] for fn in TRIG_FUNCTIONS]

    @staticmethod
    def safe_function_info():
        result = []

        for item in MATH_FUNCTIONS:
            result.append((item['name'], item['description']))

        for item in RAND_FUNCTIONS:
            result.append((item['name'], item['description']))

        for item in TRIG_FUNCTIONS:
            result.append((item['name'], item['description']))

        return result

    @staticmethod
    def functions():
        return [fn[0].split('(')[0] for fn in Formula.safe_function_info()]

    @staticmethod
    def safe(value):
        """
        :param value: A potential formula
        :return: True if formula contains only numbers, operators and safe functions, False otherwise
        """
        for token in re.findall(r"[\w']+", value):
            try:
                float(token)
            except ValueError:
                # allowed functions here
                if token not in Formula.functions():
                    return False

            return True

    @staticmethod
    def find_unit(variable):
        for vu in VARIABLE_UNITS:
            if vu[0] == variable:
                return vu[1]

        raise ValueError('Variable "%s" not found' % variable)

    @staticmethod
    def _normalize_unit(unit):
        """
        :param unit: The continuous version of the unit, e.g "€/kWh"
        :return:
        """
        unit_str = unit
        unit_str = unit_str.replace('kWh', 'kW*h').replace('²', '**2')

        return unit_str, re.split(r'[\s,.|/*]+', unit_str)

    @property
    def unit(self):
        try:
            return self.suggest_unit(fail_on_invalid=False)
        except ValueError:
            return '-'

    def suggest_unit(self, fail_on_invalid=True):

        # ignore minus as it could incorrectly cause expressions to collapse
        # e.g € - € => €, not empty unit
        value = self.value.replace('-', '+').replace(' ', '')
        units = {}

        # this is the symbols variable, should not use any unit character inside
        q = []

        # make sure value is safe to proceed
        if self.errors(include_unit_errors=False):
            raise ValueError('Can\'t detect unit of invalid expression')

        # replace each dependency with its unit & define symbols
        unit_cnt = 0
        for dependency in self.dependencies:
            unit_str, du = Formula._normalize_unit(Formula.find_unit(dependency))
            if not du:
                value = value.replace('`' + dependency + '`', '1')

            for unit in du:
                try:
                    # do not replace numbers with tokens
                    float(unit)
                except ValueError:
                    if unit not in units:
                        units[unit] = 'q[%d]' % unit_cnt
                        q.append(sympy.Symbol(unit))
                        unit_cnt += 1

                    unit_str = unit_str.replace(unit, units[unit])

            # replace in value
            value = value.replace('`' + dependency + '`', '(' + unit_str + ')')

        # remove functions
        for fn in Formula.functions():
            value = value.replace(str(fn) + '(', '(')

        # simplify expression
        expr_result = str(eval(value))

        # replace original symbols
        for unit in units:
            expr_result = expr_result.replace(units[unit], unit)

        # replace ** with ^
        expr_result = expr_result.replace('**', '^')

        # remove digits
        result = ''
        to_remove_constant = True
        for x in expr_result:
            if x == ' ':
                continue

            try:
                int(x)

                if not to_remove_constant:
                    result += x
            except ValueError:
                result += x

            # should not remove the next constant if it exposes to power
            to_remove_constant = x not in ['^', ]

        # no unit remaining -- assume percentage:
        if not result:
            return '%'

        # remove trailing symbols
        while result and result[0] in ['+', '*', ]:
            result = result[1:]

        while result and result[len(result) - 1] in ['+', '*', '/']:
            result = result[:-1]

        # if addition is included, the formula most probably does not make sense
        if '+' in result and fail_on_invalid:
            # format error string
            adders = result.split('+')
            err_str = adders[0]
            for idx, term in enumerate(adders[1:]):
                if not term.strip():
                    continue

                if idx == 0:
                    err_str += ' with %s' % term
                elif idx + 2 < len(adders):
                    err_str += ', %s' % term
                else:
                    err_str += ' and %s' % term

            # raise error
            raise InvalidUnitError('Formula seems to be incorrect: adding %s' % err_str)

        if len(result):
            if result[0] == '*':
                result = result[1:]
            elif result[0] == '/':
                result = '1' + result[1:]

        return result

    def apply(self, context):
        """
        :param context: A dictionary of variables and their values
        :return: The result of the formula after applying the context
        """
        # modules for formula calculation
        ###

        # make sure all values are there
        for dependency in self.dependencies:
            if dependency not in context:
                raise ValueError('Missing value "%s"' % dependency)

        # apply context
        value = self.value
        for key in context:
            value = value.replace('`' + key + '`', str(context[key]))

        # make sure user input is safe
        if not Formula.safe(value):
            raise ValueError('Unsafe formula "%s"' % value)

        # remove functions
        for fn in Formula.functions():
            value = value.replace(str(fn) + '(', '(')

        # evaluate the expression
        try:
            result = eval(value)
        except ZeroDivisionError:
            result = None

        # respond
        return result

    def errors(self, include_unit_errors=True):
        """
        :return: A list of all the errors in the formula
        """
        dummy_context = {}
        errors = []
        for prop in self.dependencies:
            # make sure the variable is valid
            if prop not in VALUE_VARIABLE_NAMES_LIST:
                errors.append('Unknown variable %s' % prop)

            dummy_context[prop] = 0

        try:
            dummy_result = self.apply(dummy_context)
            if type(dummy_result) not in [int, float, type(None)]:
                errors.append('Incorrect return type %s: Must be either an int or a float' % type(dummy_result))
                return errors
        except SyntaxError as se:
            try:
                errors.append(str(se).split(' (')[0])
            except IndexError:
                errors.append(str(se))
        except ValueError:
            errors.append('Unknown expression')

        if include_unit_errors and not errors:
            try:
                self.suggest_unit()
            except InvalidUnitError as err:
                errors.append(str(err))

        return errors

    def save(self, *args, **kwargs):
        """
        Override the save method to store the `valid`
        """
        try:
            self.is_valid = len(self.errors(include_unit_errors=False)) == 0
        except ValueError:  # unsafe formula or incorrect context
            self.is_valid = False

        super(Formula, self).save(*args, **kwargs)

    def __str__(self):
        return '=%s' % self.value
