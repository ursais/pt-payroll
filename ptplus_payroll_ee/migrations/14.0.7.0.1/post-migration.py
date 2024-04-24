AFF_INCOME_TAX_RULES = [
    "BASIC",
    "SUBS_REF_NUM",
    "SUBS_REF_TIC",
    "SUBS_REF_ESP",
    "ABONO_FALHAS_CAIXA",
    "DES_VPROP",
    "GRAT_AO_BAL",
    "SUBS_NOTURNO",
    "AJUD_CUSTO_NAC",
    "AJUD_CUSTO_NAC_75",
    "AJUD_CUSTO_NAC_50",
    "AJUD_CUSTO_NAC_25",
    "AJUD_CUSTO_INT",
    "AJUD_CUSTO_INT_75",
    "AJUD_CUSTO_INT_50",
    "AJUD_CUSTO_INT_25",
    "DIUTURNIDADES",
    "ISENCAO_HOR_TRAB",
    "FER_NAO_GOZ",
    "PREM_MENSAL",
    "PREM_N_MENSAL",
    "COM",
    "TRAB_NOT",
    "PREM_PREV",
    "PREM_PROD",
    "REG_2_TUR",
    "REG_3_TUR",
    "REG_4_TUR",
    "REG_5_TUR",
    "IND_CESS_CONT",
    "UT_PES_VA",
    "SUB_TRANS_VAL_PAS_SOC",
    "REND_ESP_2CIRS",
    "SUB_TRANS_VAL_PAS_SOC",
    "OUT_REN_ESP",
    "SUB_TRANS_TRIB",
    "TICKET_EDUC",
    "TIC_ENS_CHE_EST",
    "TIC_INF_CHE_CRE",
    "SUBS_DESLO",
]

OTHER_AFF_INCOME_TAX_RULES = [
    "IND_CESS_CONT",
    "IND_CESS_CONT_NAO_SS_SUJ_IRS",
]

LEAVES_RULES = [
    "FALTA110",
    "SUBS_ALIM120",
    "FERIAS130",
    "FALTA140",
    "FALTA150",
    "FALTA160",
    "FALTA170",
    "FALTA180",
    "FALTA190",
    "FALTA200",
    "FALTA210",
    "FALTA220",
    "FALTA230",
    "FALTA240",
    "FALTA250",
    "FALTA260",
    "FALTA270",
    "FALTA280",
    "FALTA310",
]

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    structure_pt_monthly_pay = env.ref(
        "ptplus_payroll_ee.hr_payroll_structure_pt_monthly_pay", raise_if_not_found=False
    )

    if not structure_pt_monthly_pay:
        return

    for rule in structure_pt_monthly_pay.rule_ids:
        dmr_subject_amount = rule.l10n_pt_dmr_subject_amount
        is_relevant_rule = rule.code in (AFF_INCOME_TAX_RULES + LEAVES_RULES)
        is_dmr_subject_valid = dmr_subject_amount and dmr_subject_amount != "N/A"

        if (rule.code in OTHER_AFF_INCOME_TAX_RULES) or (is_dmr_subject_valid and is_relevant_rule):
            rule.write({"l10n_pt_affects_income_tax": True})
        if rule.code == "BASIC":
            rule.write({
                "l10n_pt_affects_overtime_hourly_wage": True
            })
