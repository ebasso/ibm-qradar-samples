More details here https://ibmresilient.github.io/resilient-community-apps/fn_outbound_email/README.html


Edit app.config

```
[fn_outbound_email:templates]

## specify templates for email processing. These templates are added to the mail_template_select activity field
#   choose a label which will identify the template to use
#labelA=/path/to/template.jinja
sample_email = /data/templates/sample_email.jinja
sample_email2 = /data/templates/sample_email2.jinja

```

On playbook, change **Outbound Email: Send Email 2**
