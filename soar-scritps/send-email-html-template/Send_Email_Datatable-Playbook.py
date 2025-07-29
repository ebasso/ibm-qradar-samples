import hashlib
import time

MESSAGE_ID_DOMAIN = "qradarsoar.ibm.com"

inputs.mail_to = row.email
inputs.mail_incident_id = incident.id
inputs.mail_from = playbook.inputs.mail_from
inputs.mail_subject = "[{0}] {1}".format(incident.id, incident.name) if not playbook.inputs.get('mail_subject') else playbook.inputs.mail_subject

if playbook.inputs.get('mail_message_id'):
  # generate a message-id
  seed_value = str(int(time.time()*1000))
  uuid_hash = hashlib.md5(seed_value.encode()).hexdigest()
  msg_id = "{}-{}-{}-{}-{}".format(uuid_hash[0:8], uuid_hash[8:12], uuid_hash[12:16], uuid_hash[16:20], uuid_hash[20:])
  inputs.mail_message_id = "{}@{}".format(msg_id, MESSAGE_ID_DOMAIN)
  
if playbook.inputs.get('mail_in_reply_to') and incident.properties.email_message_id:
  inputs.mail_in_reply_to = incident.properties.email_message_id
  
  
if playbook.inputs.get('mail_body') and playbook.inputs.get('mail_body').content:
  inputs.mail_body = playbook.inputs.mail_body.content

inputs.mail_template_label = 'sample_email'
