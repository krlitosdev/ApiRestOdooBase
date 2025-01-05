
class ClienteResPartner():
    def __init__(self):
        self.id=None
        self.name=None
        self.company_id=None
        self.create_date=None
        self.display_name=None
        self.date=None
        self.title=None
        self.parent_id=None
        self.ref=None
        self.lang=None
        self.tz=None
        self.user_id=None
        self.vat=None
        self.website=None
        self.comment=None
        self.credit_limit=None
        self.active=None
        self.employee=None
        self.function=None
        self.type=None
        self.street=None
        self.street2=None
        self.zip=None
        self.city=None
        self.state_id=None
        self.country_id=None
        self.partner_latitude=None
        self.partner_longitude=None
        self.email=None
        self.phone=None
        self.mobile=None
        self.is_company=None
        self.industry_id=None
        self.color=None
        self.partner_share=None
        self.commercial_partner_id=None
        self.commercial_company_name=None
        self.company_name=None
        self.create_uid=None
        self.write_uid=None
        self.write_date=None
        self.message_main_attachment_id=None
        self.email_normalized=None
        self.message_bounce=None
        self.signup_type=None
        self.signup_expiration=None
        self.signup_token=None
        self.calendar_last_notif_ack=None
        self.team_id=None
        self.partner_gid=None
        self.additional_info=None
        self.phone_sanitized=None
        self.debit_limit=None
        self.last_time_entries_checked=None
        self.invoice_warn=None
        self.invoice_warn_msg=None
        self.supplier_rank=None
        self.customer_rank=None
        self.picking_warn=None
        self.picking_warn_msg=None
        self.sale_warn=None
        self.sale_warn_msg=None
        self.l10n_latam_identification_type_id=None
    
    # Método para cargar valores desde un diccionario
    def cargar_datos(self, datos):
        for key, value in datos.items():
            setattr(self, key, value)