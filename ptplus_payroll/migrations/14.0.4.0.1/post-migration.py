from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cfg = env["ir.config_parameter"].sudo()
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )

    companies.write(
        {
            "l10n_pt_default_meal_allowance_amount_paid_in_ticket": cfg.get_param(
                "standard.meal.allowance.amount.paid.in.ticket"
            ),
            "l10n_pt_default_meal_allowance_amount_paid_in_cash": cfg.get_param(
                "standard.meal.allowance.amount.paid.in.cash"
            ),
            "l10n_pt_default_meal_allowance_amount_paid_in_kind": cfg.get_param(
                "standard.meal.allowance.amount.paid.in.kind"
            ),
            "l10n_pt_default_first_overtime_hourly_rate": cfg.get_param(
                "standard.first.overtime.hourly.rate"
            ),
            "l10n_pt_default_remaining_overtime_hourly_rate": cfg.get_param(
                "standard.remaining.overtime.hourly.rate"
            ),
            "l10n_pt_default_night_work_rate": cfg.get_param(
                "standard.night.work.rate"
            ),
            "l10n_pt_default_meal_allowance_payment_method": cfg.get_param(
                "standard.meal.allowance.payment.method"
            ),
            "l10n_pt_default_holiday_allowance_payment_method": cfg.get_param(
                "standard.holiday.allowance.payment.method"
            ),
            "l10n_pt_default_holiday_allowance_payment_month": cfg.get_param(
                "standard.holiday.allowance.payment.month"
            ),
            "l10n_pt_default_christmas_allowance_payment_method": cfg.get_param(
                "standard.christmas.allowance.payment.method"
            ),
            "l10n_pt_default_christmas_allowance_payment_month": cfg.get_param(
                "standard.christmas.allowance.payment.month"
            ),
            "l10n_pt_default_value_per_km_in_own_vehicle": cfg.get_param(
                "standard.value.per.km.in.own.vehicle"
            ),
            "l10n_pt_default_value_per_km_in_public_transport": cfg.get_param(
                "standard.value.per.km.in.public.transport"
            ),
            "l10n_pt_default_per_diem_national": cfg.get_param(
                "standard.per.diem.national"
            ),
            "l10n_pt_default_per_diem_international": cfg.get_param(
                "standard.per.diem.international"
            ),
        }
    )

    cfg.search(
        [
            (
                "key",
                "in",
                [
                    "standard.meal.allowance.amount.paid.in.ticket",
                    "standard.meal.allowance.amount.paid.in.cash",
                    "standard.meal.allowance.amount.paid.in.kind",
                    "standard.first.overtime.hourly.rate",
                    "standard.remaining.overtime.hourly.rate",
                    "standard.night.work.rate",
                    "standard.meal.allowance.payment.method",
                    "standard.holiday.allowance.payment.method",
                    "standard.holiday.allowance.payment.month",
                    "standard.christmas.allowance.payment.method",
                    "standard.christmas.allowance.payment.month",
                    "standard.value.per.km.in.own.vehicle",
                    "standard.value.per.km.in.public.transport",
                    "standard.per.diem.national",
                    "standard.per.diem.international",
                ],
            )
        ]
    ).unlink()
