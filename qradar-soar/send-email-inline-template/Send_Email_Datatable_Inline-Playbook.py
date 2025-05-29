import hashlib
import time
from datetime import datetime

# Domínio usado para compor o Message-ID do e-mail
MESSAGE_ID_DOMAIN = "qradarsoar.ibm.com"

# Define o assunto do e-mail, com fallback para valor padrão
def get_subject():
    html = "Incident {0} - {1}".format(incident.id, incident.name) 
    subject = playbook.inputs.get('mail_subject')
    
    if subject and subject != '':
        html = "Incident {0} - {1}".format(incident.id, subject) 
    return html


# Função para gerar um Message-ID único baseado em timestamp e hash MD5
def generate_messageid():
    seed_value = str(int(time.time() * 1000))  # Timestamp em milissegundos
    uuid_hash = hashlib.md5(seed_value.encode()).hexdigest()  # Gera hash MD5
    msg_id = "{}-{}-{}-{}-{}".format(uuid_hash[0:8], uuid_hash[8:12], uuid_hash[12:16], uuid_hash[16:20], uuid_hash[20:])
    return msg_id


# Função para obter o campo mail_body
def get_description():
    html = '.'
    desc = incident.description.get('content')
    
    if desc and desc != '':
        html = desc
    return html

# Função para obter o campo mail_body
def get_mail_body():
    html = '.'
    mb = playbook.inputs.get('mail_body')
    
    if mb and mb.get('content'):
        html = mb.get('content')
    return html


# Função para gerar uma linha HTML com rótulo e valor de um campo do incidente
def get_row(label, field_name):
    html = ''
    
    if field_name == 'create_date':
        timestamp_s = int(incident.create_date) / 1000
        value = str(datetime.fromtimestamp(timestamp_s).strftime("%d/%m/%Y %H:%M"))
    elif field_name == 'incident_type_ids':
        value = incident.incident_type_ids
    elif field_name == 'severity_code':
        value = incident.severity_code
    elif field_name == 'plan_status':
        value = incident.plan_status
    elif field_name == 'phase_id':
        value = incident.phase_id
    else:
        value = 'NOT FOUND'
    
    # Se houver valor, monta a linha da tabela
    if value and value != '':
        html = "<tr><td class='label'>{} :</td><td class='value'>{}</td></tr>".format(label, value)
    return html


# ============================= main ====================================

# Define os campos de entrada do e-mail
inputs.mail_to = row.email
inputs.mail_incident_id = incident.id
inputs.mail_from = playbook.inputs.mail_from
inputs.mail_subject = get_subject()
inputs.mail_message_id = generate_messageid()

# Define o template HTML do corpo do e-mail
inputs.mail_inline_template = """
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #f4f4f4;
      font-family: Arial, sans-serif;
    }}
    .container {{
      max-width: 700px;
      margin: 20px auto;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 8px;
      overflow: hidden;
    }}
    .header, .footer {{
      background: rgb(20, 8, 88);
      color: #fff;
      padding: 20px;
    }}
    .footer {{
      background: #e6e6e6;
      color: #333;
      font-size: 12px;
    }}
    .content {{
      padding: 20px;
      font-size: 14px;
      color: #333;
    }}
    .section-title {{
      font-size: 16px;
      font-weight: bold;
      color: rgb(20, 8, 88);
      border-bottom: 1px solid #ccc;
      margin: 20px 0 10px;
    }}
    .info-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .info-table td {{
      padding: 6px 8px;
      vertical-align: top;
    }}
    .label {{
      font-weight: bold;
      color: rgb(20, 8, 88);
      background: #e6e6e6;
      width: 160px;
    }}
    a {{
      color: rgb(20, 8, 88);
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>Incident Notifications</h2>
    </div>
    <div class="content">
      <p>Alert from IBM QRadar SOAR.</p>

      <div class="section-title">{{{{ incident.id }}}} - {1}</div>
      <table class="info-table">
        <tr><td class="label">Incident ID:</td><td>{{ incident.id }}</td></tr>
        {4}{5}{6}
      </table>

      <div class="section-title">Description</div>
      <p>{2}</p>

      <div class="section-title">Message</div>
      {3}

      <div class="section-title">More information</div>
      <p>For details access Soar:</p>
      <p><a href="{{{{ template_helper.generate_incident_url({0}) }}}}" target="_blank">Click here</a></p>
    </div>
    <div class="footer">
      <p>Any Doubt consulte SOC TEAM.</p>
      <p style="text-align: right;">
        Regards,<br>
        <strong>Security Operations Center</strong>
      </p>
    </div>
  </div>
</body>
</html>
""".format(
    incident.id,
    incident.name,
    get_description(),
    get_mail_body(), 
    get_row('Date/Hour', 'create_date'),
    get_row('Category', 'incident_type_ids'),
    get_row('Severity', 'severity_code')
)
