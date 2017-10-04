from django.test import TestCase
from django.contrib.auth.models import User

from derisk_app.models import Formula


class FormulaTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(email='test@test.com')

        # formula with no functions
        Formula.objects.create(created_by=test_user, name='F1',
                               value='(`energydemandbefore_19` - `energydemandafter_20`)/`energydemandbefore_19`')
        # formula with safe function
        Formula.objects.create(created_by=test_user, name='F2',
                               value='round((`energydemandbefore_19` - `energydemandafter_20`)/`energydemandbefore_19`)')
        # formula with unsafe function
        Formula.objects.create(created_by=test_user, name='F3',
                               value='import os and round((`energydemandbefore_19` - `energydemandafter_20`)/`energydemandbefore_19`)')
        # mistyped formula
        Formula.objects.create(created_by=test_user, name='F4',
                               value='`energydemandbefore_19` - `energydemandafter_20`)/`energydemandbefore_19`')
        # formula with unknown variable
        Formula.objects.create(created_by=test_user, name='F5',
                               value='`test` - 1')

        # Unit Guessing #

        # Simple expression with same units
        Formula.objects.create(created_by=test_user, name='FEur',
                               value='`npvactual_57` - `npvprior_56`')
        # Simple expression with same units and constant
        Formula.objects.create(created_by=test_user, name='FEurConst',
                               value='`npvactual_57` - `npvprior_56` + 100')
        # Adding variables with different units
        Formula.objects.create(created_by=test_user, name='FIncorrectAdd',
                               value='`indicator_unit_energy_before_AC` - `indicator_unit_energy_after_AE`')
        # Simple unit in function
        Formula.objects.create(created_by=test_user, name='FWithFunction',
                               value='round(`netannualsaving_55`)')
        # Assuming percentages
        value = '(`energydemandbefore_19` - `energydemandafter_20`) / `energydemandbefore_19` * 100'
        Formula.objects.create(created_by=test_user, name='FPercentage',
                               value=value)
        # Dealing with powers
        Formula.objects.create(created_by=test_user, name='FPower',
                               value='`floorarea_17`*`floorarea_17`')

    def test_formula_applied(self):
        f = Formula.objects.get(name='F1')
        self.assertEqual(0.54, f.apply({'energydemandbefore_19': 5, 'energydemandafter_20': 2.3}))

    def test_missing_arguments(self):
        f = Formula.objects.get(name='F1')
        self.assertRaises(ValueError, f.apply, {'energydemandbefore_19': 5, })

    def test_safe_function(self):
        f = Formula.objects.get(name='F2')
        self.assertAlmostEqual(0.54, f.apply({'energydemandbefore_19': 5, 'energydemandafter_20': 2.3}))

    def test_unsafe_function(self):
        f = Formula.objects.get(name='F3')
        self.assertRaises(ValueError, f.apply, {'energydemandbefore_19': 5, 'energydemandafter_20': 2.3})

    def test_div_by_zero_is_none(self):
        f = Formula.objects.get(name='F1')
        self.assertIsNone(f.apply({'energydemandbefore_19': 0, 'energydemandafter_20': 2.3}))

    def test_is_valid(self):
        f = Formula.objects.get(name='F1')
        self.assertTrue(f.is_valid)

    def test_is_not_valid_syntax_error(self):
        f = Formula.objects.get(name='F4')
        self.assertFalse(f.is_valid)

    def test_is_not_valid_unknown_variable(self):
        f = Formula.objects.get(name='F5')
        self.assertFalse(f.is_valid)

    def test_unit_simple_add(self):
        f = Formula.objects.get(name='FEur')
        self.assertEqual(f.suggest_unit(), '€')

    def test_unit_simple_add_with_const(self):
        f = Formula.objects.get(name='FEurConst')
        self.assertEqual(f.suggest_unit(), '€')

    def test_unit_adding_different_variables(self):
        f = Formula.objects.get(name='FIncorrectAdd')
        self.assertRaises(ValueError, f.suggest_unit)

    def test_unit_with_function(self):
        f = Formula.objects.get(name='FWithFunction')
        self.assertEqual(f.suggest_unit(), '€')

    def test_unit_assumed_percentage(self):
        f = Formula.objects.get(name='FPercentage')
        self.assertEqual(f.suggest_unit(), '%')

    def test_unit_powers(self):
        f = Formula.objects.get(name='FPower')
        self.assertEqual(f.suggest_unit(), 'm^4')
