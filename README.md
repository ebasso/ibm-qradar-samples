# IBM QRadar Samples

This repository provides a collection of sample scripts, configuration files, and integration examples for IBM QRadar. It is intended to help QRadar users, administrators, and developers get started with common use-cases, integrations, and automation tasks.


## Contents

Below is the directory structure of this repository, with a brief description of each folder:

```
ibm-qradar-samples/
├── siem-pulse-dashboards/
│   ├── microsoft-office365/        # Custom dashboards for Microsoft Office 365
│   ├── microsoft-windows/          # Custom dashboards for Microsoft Windows
│   └── trendmicro/
│       └── vision-one/             # Custom dashboards for Trend Micro Vision One
├── siem-restapi-python/            # Python samples for QRadar SIEM REST API
├── siem-sample-scripts/            # Example scripts for QRadar SIEM integration
├── soar-restapi-python/            # Python samples for QRadar SOAR REST API
├── soar-scritps/                   # Example QRadar SOAR scripts and playbooks
│   ├── send-email-html-template/   # Email playbook with HTML template
│   └── send-email-inline-template/ # Email playbook with inline template
├── LICENSE
├── README.md
```


## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/ebasso/ibm-qradar-samples.git
   cd ibm-qradar-samples
   ```

2. **Browse the folders**
   - Each directory contains README files or documentation to help you understand its contents and usage.

3. **Prerequisites**
   - IBM QRadar (on-premises or cloud)
   - Administrative or API access to your QRadar instance

## Usage

- Review the documentation within each sample for setup and usage instructions.
- Customize scripts and templates as needed for your environment.
- Test all samples in a non-production environment before deploying.

## Contributing

Contributions are welcome! If you have a useful sample to share, please open a pull request with a description and relevant documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This repository is maintained as a community resource and is not officially supported by IBM. Use samples at your own risk.
