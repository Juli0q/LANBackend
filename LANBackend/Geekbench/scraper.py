from bs4 import BeautifulSoup
import requests

from benchmark_model import *


__HTTP_TIMEOUT = 5


def __validate_url(url):
    if 'https://browser.geekbench.com/v6/' not in url:
        return False

    if '/cpu/' not in url and '/compute/' not in url:
        return False

    split = url.split('/')
    if not split[-1].isdigit():
        return False

    return True


def __get_html(url):
    try:
        req = requests.get(url, timeout=__HTTP_TIMEOUT)
    except requests.exceptions.BaseHTTPError:
        return Result.CONNECTION_ERROR

    if req.status_code == 404:
        return Result.BENCHMARK_NOT_FOUND

    return Result.SUCCESS, req.content


def __get_device(soup, benchmark):
    benchmark.device = soup.find('h1').text.strip()


def __get_testkind(url, benchmark):
    if '/compute/' in url:
        benchmark.test = TestKind.GPU
    else:
        benchmark.test = TestKind.CPU


def __get_information_dict_values(table):
    tbody = table.find('tbody')
    if tbody is None:
        rows = table.find('thead').find_all('tr')
        # Header
        del rows[0]
    else:
        rows = tbody.find_all('tr')

    values = {}
    for row in rows:
        name_td = row.find('td', class_='system-name')
        if name_td is None:
            name_td = row.find('td', class_='name')

        name = name_td.text.strip()
        value_td = row.find('td', class_='system-value')
        if value_td is None:
            value_td = row.find('td', class_='value')

        value = value_td.text.strip()
        values[name] = value

    return values


def __get_information(soup, benchmark):
    tables = soup.find_all('table', class_='system-table')
    for table in tables:
        header = table.find('thead')
        if header is None:
            # Result Information (Upload Date, Views)
            continue

        th = header.find('th', class_='system-name')
        if th is None:
            th = header.find('th', class_='name')

        name = th.text.strip()
        values = __get_information_dict_values(table)

        if 'System' in name:
            benchmark.system_information = values
        elif 'CPU' in name:
            benchmark.cpu_information = values
        elif 'Memory' in name:
            benchmark.memory_information = values
        elif 'OpenCL' in name:
            benchmark.opencl_information = values
        elif 'Vulkan' in name:
            benchmark.opencl_information = values


def __get_performance_dict_values(table):
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    values = {}
    for row in rows:
        name_td = row.find('td', class_='name')
        name = name_td.text.strip()

        value_td = row.find('td', class_='score')
        description = value_td.find('span', class_='description').text.strip()
        value = value_td.find(string=True, recursive=False).text.strip()
        values[name + " Score"] = value
        values[name] = description

    return values


def __get_performance(soup, benchmark):
    tables = soup.find_all('table', class_='benchmark-table')
    for table in tables:
        header = table.find('thead').find('tr')
        name = header.find('th', class_='name').text.strip()
        score = int(header.find('th', class_='score').text.strip())
        values = __get_performance_dict_values(table)

        if 'Single-Core' in name:
            benchmark.single_core_performance = values
        elif 'Multi-Core' in name:
            benchmark.multi_core_performance = values
        elif 'OpenCL' in name or 'Vulkan' in name:
            benchmark.gpu_performance = values


def scrape_result(url):

    if not __validate_url(url):
        return Result.INVALID_URL

    result, html = __get_html(url)

    if result != Result.SUCCESS:
        return result

    soup = BeautifulSoup(html, 'html.parser')
    benchmark = Benchmark()
    __get_testkind(url, benchmark)
    __get_device(soup, benchmark)
    __get_information(soup, benchmark)
    __get_performance(soup, benchmark)
    return Result.SUCCESS, benchmark


if __name__ == '__main__':
    scrape_result('<enter your url>')
