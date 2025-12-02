import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os

@pytest.fixture(scope="function")
def driver(request):

    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-notifications')

    print("\nIniciando Chrome WebDriver...")
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    yield driver
    
    if request.node.rep_call.failed:
        take_screenshot_on_failure(driver, request.node.name)
    
    print("\nCerrando Chrome WebDriver...")
    driver.quit()


def take_screenshot_on_failure(driver, test_name):

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_dir = 'screenshots'
    
    os.makedirs(screenshot_dir, exist_ok=True)
    
    clean_test_name = test_name.replace(' ', '_').replace('[', '_').replace(']', '_')
    screenshot_path = f'{screenshot_dir}/FAILED_{clean_test_name}_{timestamp}.png'
    
    try:
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Screenshot guardado: {screenshot_path}")
    except Exception as e:
        print(f"\nError al guardar screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():

    print("\n" + "="*70)
    print("INICIANDO SUITE DE PRUEBAS AUTOMATIZADAS CON SELENIUM")
    print("="*70)
    
    os.makedirs('screenshots', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    yield
    
    print("\n" + "="*70)
    print("SUITE DE PRUEBAS COMPLETADA")
    print("="*70)


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):

    print(f"\n{'='*70}")
    print(f"Ejecutando: {request.node.name}")
    print(f"Módulo: {request.node.parent.name}")
    print(f"{'='*70}")
    
    yield
    
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            print(f"Test PASÓ: {request.node.name}")
        elif request.node.rep_call.failed:
            print(f"Test FALLÓ: {request.node.name}")
        elif request.node.rep_call.skipped:
            print(f"Test OMITIDO: {request.node.name}")


def pytest_configure(config):

    config.addinivalue_line(
        "markers", "smoke: marca tests de smoke testing (críticos)"
    )
    config.addinivalue_line(
        "markers", "regression: marca tests de regresión (suite completa)"
    )
    config.addinivalue_line(
        "markers", "positive: marca tests de camino feliz"
    )
    config.addinivalue_line(
        "markers", "negative: marca tests negativos"
    )
    config.addinivalue_line(
        "markers", "boundary: marca tests de límites"
    )