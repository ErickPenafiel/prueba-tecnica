# 📧 Configuración de Gmail SMTP en n8n - Guía Técnica

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Paso 1: Habilitar Verificación en Dos Pasos](#paso-1-habilitar-verificación-en-dos-pasos)
4. [Paso 2: Generar Contraseña de Aplicación](#paso-2-generar-contraseña-de-aplicación)
5. [Paso 3: Configurar Credenciales SMTP en n8n](#paso-3-configurar-credenciales-smtp-en-n8n)
6. [Paso 4: Configurar Nodos de Email](#paso-4-configurar-nodos-de-email)
7. [Parámetros Técnicos del Servidor](#parámetros-técnicos-del-servidor)
8. [Prueba y Validación](#prueba-y-validación)
9. [Solución de Problemas](#solución-de-problemas)
10. [Mejores Prácticas de Seguridad](#mejores-prácticas-de-seguridad)

---

## Descripción General

Esta guía describe el proceso de configuración de una cuenta de Gmail como servidor SMTP para enviar correos electrónicos desde workflows de n8n. Gmail requiere autenticación mediante **Contraseñas de Aplicación** (App Passwords) cuando se accede desde aplicaciones de terceros.

**Tiempo estimado:** 10-15 minutos  
**Nivel de dificultad:** Intermedio  
**Requisitos:** Cuenta de Gmail activa, n8n instalado y funcionando

---

## Requisitos Previos

Antes de comenzar la configuración, asegúrate de cumplir con los siguientes requisitos:

| Requisito                    | Descripción                                | Estado      |
| ---------------------------- | ------------------------------------------ | ----------- |
| **Cuenta de Gmail**          | Cuenta activa de Google/Gmail              | ☐ Verificar |
| **n8n en ejecución**         | Instancia de n8n accesible (local o cloud) | ☐ Verificar |
| **Verificación en 2 pasos**  | Habilitada en la cuenta de Google          | ☐ Pendiente |
| **Contraseña de aplicación** | Generada desde configuración de Google     | ☐ Pendiente |

> **⚠️ Nota Importante:** Las Contraseñas de Aplicación **solo están disponibles** si la Verificación en Dos Pasos está habilitada en tu cuenta de Google.

---

## Paso 1: Habilitar Verificación en Dos Pasos

La Verificación en Dos Pasos (2FA) es un **requisito obligatorio** para usar Contraseñas de Aplicación con Gmail.

### 1.1 Acceder a la Configuración de Seguridad

1. **Navega a tu Cuenta de Google:**

   - URL: [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - O ve a: Google Account → Security

2. **Localiza la sección "Cómo inicias sesión en Google"**

3. **Busca "Verificación en dos pasos"**

### 1.2 Configurar la Verificación

| Paso | Acción                                      | Detalles                                        |
| ---- | ------------------------------------------- | ----------------------------------------------- |
| 1    | Haz clic en **"Verificación en dos pasos"** | Si ya está activada, verás el estado "Activada" |
| 2    | Haz clic en **"Empezar"** o **"Comenzar"**  | Si aún no está configurada                      |
| 3    | Verifica tu identidad                       | Ingresa tu contraseña de Google                 |
| 4    | Configura tu teléfono                       | Ingresa tu número telefónico                    |
| 5    | Elige método de verificación                | SMS, llamada o Google Authenticator             |
| 6    | Ingresa el código recibido                  | Valida el código de 6 dígitos                   |
| 7    | Haz clic en **"Activar"**                   | Confirma la activación                          |

### 1.3 Verificación Exitosa

Una vez completado, deberías ver:

```
✅ Verificación en dos pasos: ACTIVADA
   Se agregó el [fecha] • Administrar
```

---

## Paso 2: Generar Contraseña de Aplicación

Las Contraseñas de Aplicación son códigos de 16 caracteres que permiten a aplicaciones de terceros acceder a tu cuenta de Google sin usar tu contraseña principal.

### 2.1 Acceder a Contraseñas de Aplicación

1. **Regresa a la página de Seguridad:**

   - URL directa: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - O ve a: Security → "Cómo inicias sesión en Google" → "Contraseñas de aplicaciones"

2. **Es posible que se te solicite verificar tu identidad de nuevo**

### 2.2 Generar Nueva Contraseña

| Paso | Acción                            | Valor Recomendado                      |
| ---- | --------------------------------- | -------------------------------------- |
| 1    | **Seleccionar app**               | "Correo"                               |
| 2    | **Seleccionar dispositivo**       | "Otro (nombre personalizado)"          |
| 3    | **Ingresar nombre personalizado** | "n8n-workflow-automation" o "n8n-smtp" |
| 4    | Haz clic en **"Generar"**         | -                                      |

### 2.3 Copiar Contraseña Generada

Google mostrará una contraseña de 16 caracteres en el siguiente formato:

```
xxxx xxxx xxxx xxxx
```

**⚠️ MUY IMPORTANTE:**

- ✅ **Copia esta contraseña inmediatamente** (solo se muestra una vez)
- ✅ Guárdala en un gestor de contraseñas seguro
- ✅ **NO la compartas** con nadie
- ✅ Elimina los espacios al usarla en n8n: `xxxxxxxxxxxxxxxx`

**Ejemplo visual:**

```
┌─────────────────────────────────────────────┐
│  Tu contraseña de aplicación para           │
│  "n8n-smtp" es:                             │
│                                             │
│       abcd efgh ijkl mnop                   │
│                                             │
│  Cópiala ahora, no la volverás a ver.      │
│                                             │
│  [ Copiar ]            [ Listo ]            │
└─────────────────────────────────────────────┘
```

---

## Paso 3: Configurar Credenciales SMTP en n8n

### 3.1 Acceder al Administrador de Credenciales

1. **Abre la interfaz web de n8n:**

   - URL local: http://localhost:5678
   - Inicia sesión si es necesario

2. **Navega a Credentials:**

   - Opción 1: Menú lateral izquierdo → **Credentials** (icono de llave 🔑)
   - Opción 2: Settings (⚙️) → **Credentials**

3. **Crear nueva credencial:**
   - Haz clic en el botón **"Add Credential"** (superior derecha)

### 3.2 Seleccionar Tipo de Credencial

1. En el buscador de credenciales, escribe: **"SMTP"**

2. Selecciona: **"SMTP"** (no "Gmail" - usaremos configuración SMTP directa)

### 3.3 Completar Formulario de Credenciales

Completa los siguientes campos con los valores especificados en la tabla:

| Campo               | Valor                     | Descripción                                            |
| ------------------- | ------------------------- | ------------------------------------------------------ |
| **Credential Name** | `Gmail SMTP - Producción` | Nombre descriptivo (personalizable)                    |
| **Host**            | `smtp.gmail.com`          | Servidor SMTP de Gmail                                 |
| **Port**            | `465`                     | Puerto SSL/TLS (recomendado)                           |
| **SSL/TLS**         | `✅ Activado`             | Habilitar cifrado (obligatorio)                        |
| **Username**        | `tu-email@gmail.com`      | Tu dirección de correo completa                        |
| **Password**        | `xxxxxxxxxxxxxxxx`        | Contraseña de aplicación (16 caracteres, sin espacios) |

**Captura visual del formulario:**

```
┌────────────────────────────────────────────────────────┐
│  SMTP Credential                                       │
├────────────────────────────────────────────────────────┤
│  Credential Name                                       │
│  [ Gmail SMTP - Producción                ]           │
│                                                        │
│  Host                                                  │
│  [ smtp.gmail.com                          ]           │
│                                                        │
│  Port                                                  │
│  [ 465                                     ]           │
│                                                        │
│  SSL/TLS                                               │
│  [✓] Enable                                            │
│                                                        │
│  Username                                              │
│  [ tu-email@gmail.com                      ]           │
│                                                        │
│  Password                                              │
│  [ ••••••••••••••••                        ]           │
│                                                        │
│                            [ Test ] [ Save ]           │
└────────────────────────────────────────────────────────┘
```

### 3.4 Probar Conexión (Opcional pero Recomendado)

Antes de guardar, haz clic en **"Test"** para validar la configuración:

**Resultado esperado:**

```
✅ Connection test successful
   Connected to smtp.gmail.com:465
```

**Si falla:**

```
❌ Connection failed: Invalid login
   → Verifica usuario y contraseña
```

### 3.5 Guardar Credencial

1. Haz clic en **"Save"** (botón verde)
2. La credencial aparecerá en la lista con estado **"Active"**
3. Ahora está lista para usarse en nodos de Email

---

## Paso 4: Configurar Nodos de Email

### 4.1 Agregar Nodo "Send Email" al Workflow

1. **En tu workflow activo:**

   - Haz clic en el botón **"+"** para agregar un nodo
   - Busca: **"Send Email"**
   - Selecciona: **"Send Email"** (icono de sobre)

2. **Conecta el nodo** a tu flujo de datos

### 4.2 Configurar el Nodo

| Sección          | Campo        | Valor de Ejemplo                  | Descripción                              |
| ---------------- | ------------ | --------------------------------- | ---------------------------------------- |
| **Credentials**  | SMTP Account | `Gmail SMTP - Producción`         | Selecciona la credencial creada          |
| **Email Data**   | From Email   | `tu-email@gmail.com`              | Remitente (debe coincidir con la cuenta) |
|                  | To Email     | `destinatario@example.com`        | Destinatario(s) separados por comas      |
|                  | CC Email     | `copia@example.com`               | (Opcional) Copia                         |
|                  | BCC Email    | `copia-oculta@example.com`        | (Opcional) Copia oculta                  |
|                  | Subject      | `📊 Reporte Diario - {{$today}}`  | Asunto del correo (soporta variables)    |
| **Email Format** | Text         | `Contenido en texto plano`        | Versión de texto                         |
|                  | HTML         | `<h1>Título</h1><p>Contenido</p>` | Versión HTML (recomendado)               |
| **Attachments**  | Attachments  | (Opcional)                        | Archivos adjuntos desde nodos previos    |

### 4.3 Uso de Variables Dinámicas

Puedes usar datos de nodos anteriores usando la sintaxis de expresiones:

```javascript
// Subject con datos dinámicos
Subject: `⚠️ Alerta de Riesgo: {{ $json.company_name }}`

// Body con múltiples variables
HTML Body:
<html>
  <body>
    <h2>Análisis de Riesgo Completado</h2>
    <p><strong>Empresa:</strong> {{ $json.company_name }}</p>
    <p><strong>Riesgo:</strong> {{ $json.risk_status }}</p>
    <p><strong>Score:</strong> {{ $json.risk_score }}</p>
    <p><strong>Fecha:</strong> {{ $now }}</p>
  </body>
</html>
```

### 4.4 Configuración del workflow-riesgos.json

Para los nodos de email existentes en el workflow:

**Nodo: "Send email" (Errores)**

```yaml
Credential: Gmail SMTP - Producción
From: tu-email@gmail.com
To: equipo-tecnico@example.com
Subject: ❌ ERROR: Análisis de Riesgo - {{ $json.empresa }}
```

**Nodo: "Send email1" (Reportes Exitosos)**

```yaml
Credential: Gmail SMTP - Producción
From: tu-email@gmail.com
To: gerencia@example.com, compliance@example.com
Subject: 📊 Reporte de Riesgo: {{ $json.company }} - [{{ $json.risk_status }}]
```

---

## Parámetros Técnicos del Servidor

### Tabla de Configuración SMTP de Gmail

| Parámetro                   | Valor                 | Tipo    | Descripción                                               |
| --------------------------- | --------------------- | ------- | --------------------------------------------------------- |
| **Hostname**                | `smtp.gmail.com`      | String  | Servidor SMTP oficial de Gmail                            |
| **Puerto SSL/TLS**          | `465`                 | Integer | Puerto para conexiones cifradas SSL                       |
| **Puerto STARTTLS**         | `587`                 | Integer | Puerto alternativo con STARTTLS (no recomendado para n8n) |
| **Protocolo de Cifrado**    | `SSL/TLS`             | Enum    | Cifrado obligatorio para Gmail                            |
| **Método de Autenticación** | `LOGIN`               | String  | Autenticación con usuario/contraseña                      |
| **TLS Version**             | `TLS 1.2+`            | String  | Versión mínima soportada                                  |
| **Timeout de Conexión**     | `30s`                 | Integer | Tiempo de espera predeterminado                           |
| **Límites de Envío**        | 500/día (gratuito)    | Integer | Cuota diaria de Gmail gratuito                            |
|                             | 2,000/día (Workspace) | Integer | Cuota para cuentas de Google Workspace                    |

### Comparación de Puertos

| Puerto  | Protocolo          | Seguridad                       | Uso en n8n         | Recomendado |
| ------- | ------------------ | ------------------------------- | ------------------ | ----------- |
| **465** | SMTP sobre SSL/TLS | 🔒 Cifrado completo             | ✅ Compatible      | ⭐ **Sí**   |
| **587** | SMTP con STARTTLS  | 🔒 Cifrado después de handshake | ⚠️ Puede funcionar | No          |
| **25**  | SMTP sin cifrar    | ❌ Sin cifrado                  | ❌ No compatible   | ❌ **No**   |

> **Recomendación:** Usa siempre el **puerto 465 con SSL/TLS** para máxima compatibilidad y seguridad.

### Límites de Gmail

| Tipo de Cuenta       | Límite Diario    | Límite por Mensaje   | Destinatarios por Mensaje |
| -------------------- | ---------------- | -------------------- | ------------------------- |
| **Gmail Gratuito**   | 500 emails/día   | 25 MB (con adjuntos) | 500 destinatarios         |
| **Google Workspace** | 2,000 emails/día | 25 MB (con adjuntos) | 2,000 destinatarios       |

**⚠️ Nota sobre límites:**

- Los límites se reinician a las 00:00 PST (hora del Pacífico)
- Si excedes el límite, recibirás error: `"550 5.4.5 Daily sending quota exceeded"`
- Considera usar servicios como SendGrid o AWS SES para volúmenes altos

---

## Prueba y Validación

### Prueba Manual del Nodo

1. **En tu workflow con el nodo "Send Email" configurado:**

   - Asegúrate de tener datos de prueba en nodos anteriores
   - Haz clic en **"Execute Node"** (ejecutar solo este nodo)
   - O haz clic en **"Execute Workflow"** (ejecutar todo el workflow)

2. **Monitorear la ejecución:**

   - El nodo debe mostrar un **check verde (✓)** si fue exitoso
   - El nodo mostrará un **X rojo** si falló

3. **Verificar en tu bandeja de entrada:**
   - Revisa el correo en la cuenta de destino
   - Verifica que el remitente sea correcto
   - Confirma que el formato HTML se muestre correctamente

### Resultado Esperado

**Ejecución exitosa en n8n:**

```
✅ Send Email
   Output: 1 item
   Execution Time: 1.2s

   {
     "accepted": ["destinatario@example.com"],
     "rejected": [],
     "response": "250 2.0.0 OK"
   }
```

**Email recibido:**

```
De: tu-email@gmail.com
Para: destinatario@example.com
Asunto: 📊 Reporte de Riesgo: Tesla - [WARNING]
Fecha: 30/12/2024 14:30

[Contenido del email renderizado en HTML]
```

### Validación de Logs

```powershell
# Ver logs de n8n (si usas Docker)
docker-compose logs -f n8n

# Buscar errores SMTP
docker-compose logs n8n | grep -i smtp
```

---

## Solución de Problemas

### ❌ Error: "Invalid login: 535-5.7.8 Username and Password not accepted"

**Causa:** Contraseña incorrecta o no es una Contraseña de Aplicación.

**Soluciones:**

1. ✅ Verifica que usas una **Contraseña de Aplicación**, no tu contraseña de Google
2. ✅ Asegúrate de haber **eliminado los espacios** de la contraseña (16 caracteres continuos)
3. ✅ Regenera la contraseña de aplicación si es necesaria
4. ✅ Verifica que el **username sea tu email completo** (`usuario@gmail.com`)

```javascript
// ❌ Incorrecto
Password: "abcd efgh ijkl mnop"; // Con espacios

// ✅ Correcto
Password: "abcdefghijklmnop"; // Sin espacios
```

---

### ❌ Error: "Connection timeout" o "ETIMEDOUT"

**Causa:** Problemas de red o firewall bloqueando conexión.

**Soluciones:**

1. ✅ Verifica conectividad al servidor SMTP:

```powershell
# Windows PowerShell
Test-NetConnection -ComputerName smtp.gmail.com -Port 465

# Salida esperada:
# TcpTestSucceeded : True
```

2. ✅ Revisa configuración de firewall corporativo
3. ✅ Si estás detrás de proxy, configura proxy en n8n
4. ✅ Prueba con puerto alternativo `587` (con STARTTLS)

---

### ❌ Error: "Verification in two steps is not enabled"

**Causa:** La Verificación en Dos Pasos no está activa.

**Solución:**

1. ✅ Sigue los pasos de [Paso 1](#paso-1-habilitar-verificación-en-dos-pasos)
2. ✅ Espera 5-10 minutos después de activar 2FA
3. ✅ Cierra sesión y vuelve a iniciar en tu cuenta de Google
4. ✅ Intenta generar la Contraseña de Aplicación nuevamente

---

### ❌ Error: "Daily sending quota exceeded"

**Causa:** Has alcanzado el límite diario de Gmail.

**Solución:**

1. ✅ Espera 24 horas para que se reinicie la cuota
2. ✅ Reduce la frecuencia de envío en tu workflow
3. ✅ Considera usar **Google Workspace** (límite mayor: 2,000/día)
4. ✅ Para volúmenes altos, usa servicios dedicados:
   - SendGrid (n8n tiene nodo nativo)
   - AWS SES
   - Mailgun

**Implementar throttling en n8n:**

```javascript
// En un nodo Function antes de Send Email
// Limitar a 450 emails/día (margen de seguridad)

const dailyLimit = 450;
const currentCount = $input.all().length;

if (currentCount > dailyLimit) {
	throw new Error(`Daily limit reached: ${currentCount}/${dailyLimit} emails`);
}

return $input.all();
```

---

### ❌ Error: "Message rejected: Email address is not verified"

**Causa:** Intentas enviar desde un email diferente al configurado.

**Solución:**

1. ✅ El campo **"From Email"** debe coincidir **exactamente** con tu cuenta de Gmail
2. ✅ No puedes enviar desde `otro-email@example.com` usando SMTP de Gmail
3. ✅ Si necesitas un remitente personalizado, usa Google Workspace con alias configurados

```yaml
# ❌ Incorrecto
Username: tu-email@gmail.com
From Email: otro-email@example.com  # No coincide

# ✅ Correcto
Username: tu-email@gmail.com
From Email: tu-email@gmail.com  # Coincide
```

---

### ❌ Error: SSL/TLS handshake failed

**Causa:** Configuración incorrecta de cifrado.

**Solución:**

1. ✅ Asegúrate de que **SSL/TLS esté activado** en la credencial
2. ✅ Usa puerto **465** (no 587 sin STARTTLS)
3. ✅ Actualiza n8n a la última versión:

```powershell
# Docker
docker-compose pull n8n
docker-compose up -d
```

---

### ❌ Los emails llegan a Spam

**Causa:** Autenticación o reputación del dominio.

**Soluciones:**

1. ✅ **No uses links acortados** (bit.ly, etc.) en emails automáticos
2. ✅ **Evita palabras spam** en subject: "GRATIS", "URGENTE", "CLICK AQUÍ"
3. ✅ **Incluye un texto alternativo** además del HTML
4. ✅ **Personaliza el contenido** (evita plantillas genéricas)
5. ✅ **Configura SPF/DKIM** si usas dominio personalizado
6. ✅ Pide a destinatarios que **marquen como "No es spam"**

**Ejemplo de email bien estructurado:**

```html
<!-- ✅ Buenas prácticas -->
<html>
	<body>
		<!-- Logo corporativo -->
		<img src="https://tuempresa.com/logo.png" alt="Logo" />

		<!-- Saludo personalizado -->
		<h2>Hola {{ $json.nombre }},</h2>

		<!-- Contenido relevante -->
		<p>Este es tu reporte diario de análisis de riesgo.</p>

		<!-- Call to action claro -->
		<a
			href="https://tuempresa.com/reportes/{{ $json.id }}"
			style="background: blue; color: white; padding: 10px;"
		>
			Ver Reporte Completo
		</a>

		<!-- Footer con información de contacto -->
		<footer style="margin-top: 20px; font-size: 12px; color: gray;">
			<p>Este email fue enviado automáticamente por SafeBank AI</p>
			<p>
				Contacto:
				<a href="mailto:soporte@tuempresa.com">soporte@tuempresa.com</a>
			</p>
		</footer>
	</body>
</html>
```

---

## Mejores Prácticas de Seguridad

### 1. Gestión de Contraseñas de Aplicación

| Práctica                           | Descripción                                            | Prioridad |
| ---------------------------------- | ------------------------------------------------------ | --------- |
| **Usar Gestor de Contraseñas**     | Almacena contraseñas en LastPass, 1Password, Bitwarden | 🔴 Alta   |
| **No compartir contraseñas**       | Cada servicio debe tener su propia contraseña          | 🔴 Alta   |
| **Rotación periódica**             | Renueva contraseñas cada 90 días                       | 🟡 Media  |
| **Revocar credenciales no usadas** | Elimina contraseñas de apps obsoletas                  | 🟡 Media  |
| **Monitorear actividad**           | Revisa logs de acceso en Google Security               | 🟢 Baja   |

### 2. Seguridad en n8n

```yaml
# Variables de entorno recomendadas (.env)
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=contraseña_segura_aqui

# Para producción, usar HTTPS
N8N_PROTOCOL=https
N8N_SSL_KEY=/path/to/ssl/key.pem
N8N_SSL_CERT=/path/to/ssl/cert.pem
```

### 3. Auditoría y Monitoreo

**Revisa periódicamente:**

1. **Contraseñas de aplicación activas:**

   - URL: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Revoca las que no uses

2. **Actividad de la cuenta:**

   - URL: [https://myaccount.google.com/notifications](https://myaccount.google.com/notifications)
   - Verifica inicios de sesión sospechosos

3. **Logs de n8n:**

```powershell
# Ver logs de ejecución
docker-compose logs -f n8n | grep "Send Email"

# Filtrar errores SMTP
docker-compose logs n8n | grep -i "smtp error"
```

### 4. Principio de Mínimo Privilegio

- ✅ Usa cuentas de servicio dedicadas para automatización
- ✅ No uses tu cuenta personal de Gmail para workflows de producción
- ✅ Considera Google Workspace para mejor control de permisos
- ✅ Limita destinatarios a dominios verificados cuando sea posible

### 5. Backup y Recuperación

```powershell
# Backup de credenciales de n8n (cifradas en la DB)
docker exec -it $(docker ps -qf "name=n8n") sh
cd /home/node/.n8n
tar -czf backup-credentials-$(date +%Y%m%d).tar.gz database.sqlite
exit

# Copiar backup al host
docker cp $(docker ps -qf "name=n8n"):/home/node/.n8n/backup-credentials-*.tar.gz ./backups/
```

---

## Checklist de Configuración Final

Usa esta lista para verificar que todo está correctamente configurado:

- [ ] ✅ Verificación en Dos Pasos habilitada en cuenta de Google
- [ ] ✅ Contraseña de Aplicación generada y guardada de forma segura
- [ ] ✅ Credencial SMTP creada en n8n con los parámetros correctos
- [ ] ✅ Credencial probada exitosamente (Test connection)
- [ ] ✅ Nodo "Send Email" configurado en workflow
- [ ] ✅ Email de prueba enviado y recibido correctamente
- [ ] ✅ Variables dinámicas funcionando en Subject y Body
- [ ] ✅ Formato HTML renderizado correctamente
- [ ] ✅ Emails NO llegando a carpeta de Spam
- [ ] ✅ Logs de n8n sin errores SMTP
- [ ] ✅ Contraseña de aplicación documentada en gestor seguro
- [ ] ✅ Workflow activado y ejecutándose según schedule

---

## Referencias Adicionales

### Documentación Oficial

- [Documentación de n8n - Send Email Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.emailsend/)
- [Google: Contraseñas de aplicaciones](https://support.google.com/accounts/answer/185833)
- [Google: Verificación en dos pasos](https://support.google.com/accounts/answer/185839)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)

### Alternativas a Gmail SMTP

Si necesitas mayor capacidad de envío, considera:

| Servicio               | Límite Gratuito        | Precio           | Integración n8n |
| ---------------------- | ---------------------- | ---------------- | --------------- |
| **SendGrid**           | 100/día gratuito       | $14.95/mes (40k) | ✅ Nodo nativo  |
| **AWS SES**            | 62,000/mes (desde EC2) | $0.10/1000       | ✅ HTTP Request |
| **Mailgun**            | 5,000/mes gratuito     | $35/mes (50k)    | ✅ HTTP Request |
| **Brevo (Sendinblue)** | 300/día gratuito       | $25/mes (20k)    | ✅ HTTP Request |

---

## Soporte y Contacto

**¿Necesitas ayuda adicional?**

- 📖 Consulta la documentación completa del proyecto: [README.md](README.md)
- 🔧 Revisa la guía de solución de problemas de Docker
- 🌐 Consulta el foro de n8n: [community.n8n.io](https://community.n8n.io)
- 📧 Soporte técnico: soporte@tuempresa.com
