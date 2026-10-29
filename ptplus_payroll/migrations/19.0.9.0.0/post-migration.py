import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)  # pylint: disable=C0103


@openupgrade.migrate()
def migrate(env, version):
    # The PT salary rules below were created long ago via a UI export and
    # carry "__export__" xmlids; the 19.0 upgrade archived them. They are
    # still referenced by the "PT: Pagamento Mensal" structure, so reactivate
    # them. ptplus_payroll.rule_pt_tax_base_irs_adds_to_base_total
    # (IRS_SOMA_BASE_TOTAL) is intentionally excluded: the module data ships
    # it with active=False and would re-archive it on every update anyway.
    _logger.info("Reactivating PT salary rules archived during upgrade")
    env.cr.execute(
        """
        UPDATE hr_salary_rule r
        SET active = true
        FROM ir_model_data md
        JOIN ir_model_data smd
          ON smd.model = 'hr.payroll.structure'
         AND smd.res_id = r.struct_id
         AND smd.module = 'ptplus_payroll'
         AND smd.name = 'hr_payroll_structure_pt_monthly_pay'
        WHERE md.model = 'hr.salary.rule'
          AND md.res_id = r.id
          AND md.module = '__export__'
          AND r.code IN (
              'BASIC', 'ATTACH_SALARY', 'ASSIG_SALARY', 'CHILD_SUPPORT',
              'DEDUCTION', 'REIMBURSEMENT', 'GROSS', 'NET'
          )
        """
    )
