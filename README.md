# Mobile Accessibility Benchmark Suite

An automated script and data-collection suite designed to run spatial accessibility audits across commercial mobile applications. This tool generates quantitative performance metrics (such as touch-target failure densities in retail and financial apps) intended for empirical research, technical articles, and conference whitepapers.

## Empirical Findings: Spatial Accessibility Audit

| Application | Tested Viewport | Total Elements | Violations (<24px) | Failure Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Wikipedia Android** | Explore Feed | 38 | 12 | 31.58% |
| **Swag Labs Mobile** | Inventory List | 18 | 2 | 11.11% |

### Execution Commands
```bash
pip install -r requirements.txt
python scripts/fetch_apps.py
python run_benchmark.py

Pushing the JSON configuration, the download automation script, the CSV dataset, and the rendered markdown table gives you a clean, professional open-source benchmark repository without cluttering Git with binary files.
