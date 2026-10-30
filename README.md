
# ShadowNet

**Local Security Analysis & Reporting Tool**

ShadowNet is a Python-based cybersecurity project that analyzes selected TCP ports on the local machine and generates security assessment reports.

The project is designed for educational purposes and authorized security assessments.

## Features

- TCP connectivity checks for selected ports
- Potential service identification by port number
- Local process and PID detection using psutil
- Listening address analysis
- Rule-based risk assessment
- Security recommendations
- JSON report generation
- HTML security dashboard
- Port distribution and risk visualizations
- Automated unit tests

## Technology Stack

- Python 3
- psutil
- HTML and CSS
- unittest
- JSON

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ShadowNet.git
cd ShadowNet
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the security analyzer:

```bash
python main.py
```

ShadowNet currently analyzes the local host:

`127.0.0.1`

The application checks these TCP ports:

| Port | Potential Service |
|------|-------------------|
| 21 | FTP |
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 8080 | Alternative HTTP |

## Reports

Each scan generates two files inside the `reports/` directory:

- A JSON report containing structured scan results
- An HTML dashboard containing charts, service information, and security recommendations

Open the generated HTML file in a browser to view the dashboard.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```text
ShadowNet/
├── main.py
├── risk_engine.py
├── service_detector.py
├── exposure_analyzer.py
├── recommendation_engine.py
├── html_report.py
├── tests/
│   ├── test_scanner.py
│   └── test_security.py
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## Security Limitations

- ShadowNet currently scans only the local host.
- Port numbers indicate potential services, not verified service identities.
- An open port does not necessarily indicate a vulnerability.
- A service listening on all interfaces is not necessarily accessible from the internet.
- Risk findings require manual validation.
- Local process information may depend on operating system permissions.

## Responsible Use

Use ShadowNet only on systems you own or are explicitly authorized to assess.

## Roadmap

- [x] TCP port checks
- [x] Local process detection
- [x] Network exposure analysis
- [x] Rule-based security recommendations
- [x] JSON reporting
- [x] HTML security dashboard
- [x] Unit tests
- [ ] GitHub Actions CI
- [ ] Expanded automated testing
- [ ] Improved error handling
- [ ] Configurable scan profiles

## License

A license has not yet been selected.
