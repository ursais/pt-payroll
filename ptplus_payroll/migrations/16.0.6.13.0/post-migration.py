from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    income_taxes = [
        env.ref(
            "ptplus_payroll.income_tax_762_ii_m_01_07_2023", raise_if_not_found=False
        ),
        env.ref(
            "ptplus_payroll.income_tax_762_v_m_01_07_2023", raise_if_not_found=False
        ),
        env.ref(
            "ptplus_payroll.income_tax_886,57_v_m_01_07_2023", raise_if_not_found=False
        ),
        env.ref(
            "ptplus_payroll.income_tax_1519,41_vi_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1677,09_vii_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_2042,64_vii_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1574,66_viii_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1779,19_ix_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1881,23_x_m_01_07_2023", raise_if_not_found=False
        ),
        env.ref(
            "ptplus_payroll.income_tax_762,00_xii_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1573,29_xiii_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1744,18_xiv_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1608,54_xv_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_1779,71_xvi_m_01_07_2023",
            raise_if_not_found=False,
        ),
        env.ref(
            "ptplus_payroll.income_tax_2114,29_xvi_m_01_07_2023",
            raise_if_not_found=False,
        ),
    ]
    for income_tax in income_taxes:
        if income_tax:
            income_tax.unlink()
