#!/bin/bash

echo "=================================="
echo "EJECUTANDO PRUEBAS SELENIUM"
echo "=================================="

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Entorno virtual no activado. Activándolo..."
    source venv/bin/activate
fi

echo "Limpiando reportes anteriores..."
rm -f reports/*.html
rm -f screenshots/FAILED_*

echo "🔍 Verificando aplicación Flask..."
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "La aplicación Flask no está corriendo en localhost:5000"
    echo "   Por favor ejecuta: python app/app.py"
    exit 1
fi

echo "Aplicación Flask detectada"

case "$1" in
    "smoke")
        echo "Ejecutando tests SMOKE..."
        pytest tests/ -m smoke -v --html=reports/smoke_results.html --self-contained-html
        ;;
    "login")
        echo "Ejecutando tests de LOGIN..."
        pytest tests/test_login.py -v --html=reports/login_results.html --self-contained-html
        ;;
    "crud")
        echo "Ejecutando tests CRUD..."
        pytest tests/test_crear_producto.py tests/test_listar_productos.py tests/test_actualizar.py tests/test_eliminar.py -v --html=reports/crud_results.html --self-contained-html
        ;;
    "parallel")
        echo "Ejecutando tests en PARALELO..."
        pytest tests/ -n 4 -v --html=reports/test_results.html --self-contained-html
        ;;
    "quick")
        echo "Ejecución rápida (sin reporte HTML)..."
        pytest tests/ -v
        ;;
    *)
        echo "Ejecutando TODOS los tests..."
        pytest tests/ -v --html=reports/test_results.html --self-contained-html
        ;;
esac

EXIT_CODE=$?

echo ""
echo "=================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ TODAS LAS PRUEBAS PASARON"
else
    echo "❌ ALGUNAS PRUEBAS FALLARON"
fi
echo "=================================="

echo ""
echo "Reporte HTML generado en: reports/test_results.html"
echo "Screenshots de fallos en: screenshots/"

exit $EXIT_CODE