# Ejecutar servidor
fastapi run main.py

##### Codigo Example XMLRPC #####
    from xmlrpc import client
    url = 'http://localhost:8069'
    common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    res = common.version()
    print(res)

    dbname = 'prueba'
    user = 'user@gmail.com'
    pwd = 'password'
    uid = common.authenticate(dbname, user, pwd, {})
    print('-> Get UID')
    print(uid)

    models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    user_ids = models.execute_kw(dbname, uid, pwd, 'res.partner', 'search',[[['name', '=', 'Krlitos Admin']]])
    if user_ids:
        print('Existe el usuario',user_ids,"---",type(user_ids))
    else:
        print('No existe el usuario')


    # Crear un registro
    #vals = {
    #    'name': 'Odoolandia',
    #    'code': 'OD',
    #}
    #return_id = models.execute_kw(dbname,uid, pwd, 'res.country', 'create', [vals])
    #print('Registro creado, asignado el ID ',return_id) 

    country_data = models.execute_kw(dbname,uid,pwd,'res.partner','read',[[user_ids[0]],['name','company_id','website']])
    print(country_data)
##### END #####



# res.partner fields
'id','name','company_id','create_date','display_name','date','title','parent_id','ref','lang','tz','user_id','vat','website','comment','credit_limit','active','employee','function','type','street','street2','zip','city','state_id','country_id','partner_latitude','partner_longitude','email','phone','mobile','is_company','industry_id','color','partner_share','commercial_partner_id','commercial_company_name','company_name','create_uid','write_uid','write_date','message_main_attachment_id','email_normalized','message_bounce','signup_type','signup_expiration','signup_token','calendar_last_notif_ack','team_id','partner_gid','additional_info','phone_sanitized','debit_limit','last_time_entries_checked','invoice_warn','invoice_warn_msg','supplier_rank','customer_rank','picking_warn','picking_warn_msg','sale_warn','sale_warn_msg','l10n_latam_identification_type_id'

# Buscar un cliente en la tabla [res.partner]
request_search_status,request_search_value=odoo_bridge.Search_Client('res.partner','id','3')
