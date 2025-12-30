"""
Script de ejemplo para probar el endpoint de compliance check.
"""
import requests
import json


def test_compliance_check(client_name: str):
    """
    Prueba el endpoint de compliance check.
    
    Args:
        client_name: Nombre del cliente a consultar
    """
    url = "http://localhost:8000/api/v1/compliance-check"
    params = {"client_name": client_name}
    
    print(f"\n{'='*60}")
    print(f"Verificando compliance para: {client_name}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Resumen
            print(f"\n{'='*60}")
            print(f"RESULTADO: {data['status'].upper()}")
            if data['status'] == 'alert':
                print(f"⚠️  ALERTA DE RIESGO DETECTADA")
                print(f"Tipo: {data['analysis']['top_risk']}")
                print(f"Confianza: {data['analysis']['confidence']:.2%}")
            else:
                print(f"✅ Sin riesgos detectados")
            print(f"{'='*60}\n")
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Verifica que la API esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")


if __name__ == "__main__":
    # Ejemplos de consultas
    clientes = [
        "Tesla",
        "Microsoft",
        "Banco Santander",
        "FTX"  # Ejemplo que podría generar alerta
    ]
    
    print("\n" + "="*60)
    print("PRUEBA DE COMPLIANCE CHECK - SafeBank AI")
    print("="*60)
    
    for cliente in clientes:
        test_compliance_check(cliente)
        input("Presiona Enter para continuar con el siguiente cliente...")
