# Microsoft Active Directory - Autentication


## Summary of Various Events  
This report provides an overview of key security events, including successful and failed login attempts, object modifications, and password changes. By analyzing these events, it becomes possible to detect potential security threats, such as brute-force attacks and compromised credentials, ensuring a more proactive approach to system security.  

## Event Distribution by Device (1 Day)  
This section presents an overview of events occurring across Microsoft Active Directory servers over a 24-hour period. By mapping the distribution of events, administrators can identify unusual activity patterns or potential security incidents linked to specific devices or systems.  

## Top 10 Users with Successful Logins  
This list highlights the users who have logged in successfully the most times. While frequent access may be expected for some roles, excessive logins could indicate compromised accounts or unauthorized credential sharing, warranting further investigation.  

**Risk:** High login frequency may suggest that an account is being misused, either due to credential leakage or inappropriate access practices.  

## Top 10 Users with Failed Logins  
By identifying users with the highest number of failed login attempts, this section helps uncover potential security threats. A high number of failures may indicate credential stuffing attacks, brute-force attempts, or users repeatedly entering incorrect passwords.  

**Risk:** A surge in failed logins could signal an ongoing attack, such as unauthorized attempts to escalate privileges or systematic testing of login credentials.  

## Failed Login Attempts - Timeline  
Tracking failed login attempts over time helps detect attack patterns. Spikes in unsuccessful logins at unusual hours or within short timeframes may indicate automated attack scripts or persistent hacking attempts.  

**Risk:** A clear pattern of failed attempts might reveal the presence of an active brute-force attack, allowing security teams to respond promptly and mitigate risks.  

## Top 10 Administrator Users with Successful Logins  
Administrator accounts have elevated privileges, making them prime targets for attackers. This section highlights administrators who have logged in most frequently, helping to identify potential misuse or unauthorized access.  

**Risk:** An unusual number of successful logins from an administrator account might indicate that it has been compromised, leading to possible privilege abuse or lateral movement within the system.  

## Administrator Logins - Timeline  
By analyzing the login activity of administrator accounts over time, it is possible to identify anomalies. Suspicious logins occurring outside typical working hours or in unusual patterns may be signs of unauthorized access attempts or insider threats.  

**Risk:** Any deviation from normal login behavior could indicate a security breach, requiring further investigation and possible remediation measures.  

## Failed Password Change Attempts - Timeline  
Failed password change attempts over time may indicate either user mistakes or security threats. Monitoring these failures can help detect unauthorized access attempts, social engineering tactics, or issues related to password policies.  

**Risk:** Multiple failed password change attempts may suggest an attacker attempting to take control of an account, underscoring the importance of strong password policies and multi-factor authentication.  
