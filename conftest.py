from _pytest.config import hookimpl
from py.xml import html


def pytest_html_results_table_header(cells):
    del cells[1]
    cells.insert(0, html.th("Testcase"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    del cells[1]
    cells.insert(0, html.td(report.testcase))
    cells.pop()


@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    testcase = str(item.function.__doc__)
    c = str(item.function.__name__)[5:]

    report.testcase = f"{c} [{testcase}]"


def pytest_html_report_title(report):
    report.title = "E2E Tio Patinhas"


def pytest_configure(config):
    config._metadata = {}
