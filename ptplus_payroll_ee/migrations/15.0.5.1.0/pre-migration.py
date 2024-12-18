from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "ptplus_payroll_ee.rule_pt_prize",
                "ptplus_payroll_ee.rule_pt_prem_bon_oth_sim_monthly_char",
            ),
            (
                "ptplus_payroll_ee.input_pt_prize",
                "ptplus_payroll_ee.input_pt_prem_bon_oth_sim_monthly_char",
            ),
            (
                "ptplus_payroll_ee.rule_pt_premiums_bonuses_and_other_non_regular_benefits",
                "ptplus_payroll_ee.rule_pt_balance_sheet_gratuities",
            ),
            (
                "ptplus_payroll_ee.input_pt_premiums_bonuses_and_other_non_regular_benefits",
                "ptplus_payroll_ee.input_pt_balance_sheet_gratuities",
            ),
            (
                "ptplus_payroll_ee.entry_type_pt_first_overtime_hour",
                "ptplus_payroll_ee.entry_type_pt_overtime_first_hour",
            ),
            (
                "ptplus_payroll_ee.entry_type_pt_overtime_following_days_rate",
                "ptplus_payroll_ee.entry_type_pt_overtime_rest_days",
            ),
            (
                "ptplus_payroll_ee.entry_type_pt_overtime_remaining_hours_rate",
                "ptplus_payroll_ee.entry_type_pt_overtime_remaining_hours",
            ),
        ],
    )
