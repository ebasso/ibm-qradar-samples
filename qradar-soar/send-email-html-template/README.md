# How to Send Emails in IBM QRadar SOAR Using the `fn_outbound_email` App

IBM QRadar SOAR allows automated email sending through the **fn_outbound_email** app. This guide explains how to configure and use this functionality within playbooks, utilizing custom templates for email content.

More details here https://ibmresilient.github.io/resilient-community-apps/fn_outbound_email/README.html

## Prerequisites

- IBM QRadar SOAR configured.
- **fn_outbound_email** app installed.
- Access to edit the `app.config` file.
- `.jinja` templates created for email content.

## Configuring `app.config`

The **fn_outbound_email** app allows you to associate custom templates for sending emails. These templates are used by the **Outbound Email: Send Email 2** components within playbooks.

### Steps:

1. Edit the `app.config` file in your QRadar SOAR environment.
2. Locate or add the `[fn_outbound_email:templates]` section.
3. Add the desired templates using the following syntax:

```ini
[fn_outbound_email:templates]

## specify templates for email processing. These templates are added to the mail_template_select activity field
#   choose a label which will identify the template to use
#labelA=/path/to/template.jinja
sample_email = /data/templates/sample_email.jinja
sample_email2 = /data/templates/sample_email2.jinja
```


## Configuring the Playbook

In your playbook, add or edit the Outbound Email: Send Email 2 component. Set the mail_template_label input to match the label defined in app.config.

Example:

```python
inputs.mail_template_label = 'sample_email'
```

With this configuration, the app will send an email using the sample_email template, which points to /data/templates/sample_email.jinja.
