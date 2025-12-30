"""
Script de prueba para el endpoint de Risk Analysis unificado.
Versión 2.0 - Optimizado para n8n
"""
import requests
import json
from datetime import datetime


def test_risk_analysis(company_name: str):
    """
    Prueba el endpoint de análisis de riesgos unificado.
    
    Args:
        company_name: Nombre de la empresa a consultar
    """
    url = "http://localhost:8000/api/v1/risk-analysis"
    params = {"company_name": company_name}
    
    print(f"\n{'='*80}")
    print(f"🏦 ANÁLISIS DE RIESGOS - FinUp Risk Intelligence Platform")
    print(f"{'='*80}")
    print(f"Empresa: {company_name}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Mostrar JSON completo (formato con status_code, message, data)
            print("📄 RESPUESTA JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Extraer los datos del análisis
            analysis_data = data.get('data', {})
            
            # Resumen ejecutivo
            print(f"\n{'='*80}")
            print(f"📊 RESUMEN EJECUTIVO")
            print(f"{'='*80}")
            
            # Estado general con emoji
            status_emoji = {
                'clear': '✅',
                'warning': '⚠️',
                'alert': '🚨'
            }
            emoji = status_emoji.get(analysis_data.get('overall_risk_status', 'unknown'), '❓')
            
            print(f"\n{emoji} ESTADO GENERAL: {analysis_data.get('overall_risk_status', 'N/A').upper()}")
            print(f"   Risk Score: {analysis_data.get('overall_risk_score', 0):.1%}")
            print(f"   Revisión Manual: {'SÍ ⚠️' if analysis_data.get('requires_manual_review', False) else 'NO ✅'}")
            
            print(f"\n🎭 SENTIMENT ANALYSIS:")
            print(f"   Sentimiento de Mercado: {analysis_data.get('market_sentiment', 'N/A').upper()}")
            print(f"   Confianza: {analysis_data.get('sentiment_confidence', 0):.1%}")
            
            print(f"\n🔍 COMPLIANCE CHECK:")
            print(f"   Estado: {analysis_data.get('compliance_status', 'N/A').upper()}")
            print(f"   Tipo de Riesgo: {analysis_data.get('compliance_risk_type', 'N/A')}")
            print(f"   Confianza: {analysis_data.get('compliance_confidence', 0):.1%}")
            
            print(f"\n📰 EVIDENCIA:")
            print(f"   Noticias Encontradas: {analysis_data.get('news_found', 0)}")
            print(f"   Fuente: {analysis_data.get('evidence_source', 'N/A')}")
            print(f"   Titular: {analysis_data.get('evidence_headline', 'N/A')[:80]}...")
            
            print(f"\n💬 MENSAJE:")
            print(f"   {data.get('message', 'N/A')}")
            
            print(f"\n📋 STATUS CODE: {data.get('status_code', 'N/A')}")
            
            print(f"\n{'='*80}")
            
            # Simulación de integración n8n
            print(f"\n🤖 INTEGRACIÓN n8n - CAMPOS ÚTILES:")
            print(f"   - Para filtrar alertas: data.overall_risk_status === 'alert'")
            print(f"   - Para ordenar por riesgo: data.overall_risk_score (numérico)")
            print(f"   - Para casos pendientes: data.requires_manual_review === true")
            print(f"   - Para timestamp: data.analysis_timestamp")
            print(f"{'='*80}\n")
            
        elif response.status_code == 404:
            print(f"❌ Error 404: {response.json()['detail']}")
            print(f"   Sugerencia: Verifica que el nombre de la empresa sea correcto")
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"   Detalle: {response.json().get('detail', 'Error desconocido')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR DE CONEXIÓN")
        print("   No se puede conectar al servidor.")
        print("   Verifica que la API esté ejecutándose:")
        print("   → uvicorn app.main:app --reload")
        
    except requests.exceptions.Timeout:
        print("⏱️  TIMEOUT")
        print("   La primera ejecución puede tardar mientras carga el modelo BART (~1GB)")
        print("   Espera unos minutos y vuelve a intentar.")
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")


def test_health():
    """Verifica el estado de la API."""
    url = "http://localhost:8000/health"
    
    print(f"\n{'='*80}")
    print(f"🏥 HEALTH CHECK")
    print(f"{'='*80}\n")
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sistema Operacional")
            print(f"\nServicio: {data['service']}")
            print(f"Estado: {data['status']}")
            print(f"\nModelos de IA cargados:")
            for key, value in data['models_loaded'].items():
                print(f"  - {key}: {value}")
            print(f"\nAPIs integradas: {', '.join(data['apis_integrated'])}")
        else:
            print(f"⚠️  Estado: {response.status_code}")
    except Exception as e:
        print(f"❌ Sistema no disponible: {str(e)}")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Health check primero
    test_health()
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Tesla",
            "description": "Empresa tecnológica - esperado: sentiment positivo"
        },
        {
            "name": "Microsoft",
            "description": "Tech giant - esperado: bajo riesgo"
        },
        {
            "name": "FTX",
            "description": "Exchange quebrado - esperado: ALTA ALERTA"
        },
        {
            "name": "Banco Santander",
            "description": "Institución bancaria establecida"
        }
    ]
    
    print("\n" + "="*80)
    print("🧪 INICIANDO SUITE DE PRUEBAS")
    print("="*80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}/{len(test_cases)}: {test_case['name']}")
        print(f"   Descripción: {test_case['description']}")
        
        test_risk_analysis(test_case['name'])
        
        if i < len(test_cases):
            input("\n⏸️  Presiona Enter para continuar con el siguiente test...")
    
    print("\n" + "="*80)
    print("✅ SUITE DE PRUEBAS COMPLETADA")
    print("="*80)
    print("\n📚 Para más información, visita: http://localhost:8000/docs")
    print("🔗 README completo: README_RISK_INTELLIGENCE.md\n")
