# 🔐 Guía Completa de Configuración de Google Cloud APIs

Esta guía te llevará paso a paso por el proceso de configuración de las APIs de Google Cloud (Drive, Sheets, Gmail) necesarias para el funcionamiento completo del workflow de n8n.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Habilitar APIs en Google Cloud](#habilitar-apis-en-google-cloud)
3. [Crear Credenciales OAuth 2.0](#crear-credenciales-oauth-20)
4. [Configurar Pantalla de Consentimiento](#configurar-pantalla-de-consentimiento)
5. [Configurar Credenciales en n8n](#configurar-credenciales-en-n8n)
6. [Solución de Problemas](#solución-de-problemas)

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ Una cuenta de Google (Gmail)
- ✅ Acceso a [Google Cloud Console](https://console.cloud.google.com/)
- ✅ n8n ejecutándose en `http://localhost:5678`
- ✅ Permisos de administrador en tu proyecto de Google Cloud

---

## 🚀 Habilitar APIs en Google Cloud

### Paso 1: Acceder a la Biblioteca de API

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. En el menú lateral, selecciona **API y servicios** → **Biblioteca**

![Biblioteca de API](https://ibb.co/992G8yG2)

### Paso 2: Buscar y Habilitar Google Drive API

1. En el buscador, escribe **"Google Drive API"**
2. Haz clic en la tarjeta de **Google Drive API**

![Google Drive API](https://ibb.co/QFmR6qCb)

3. Haz clic en el botón **"Habilitar"**
4. Espera a que la API se active (puede tomar unos segundos)

**Estado esperado:** Deberías ver **"Habilitada"** en verde

![API Habilitada](https://ibb.co/NnWxjS2H)

### Paso 3: Habilitar Google Sheets API

Repite el proceso para **Google Sheets API**:

1. Buscar: **"Google Sheets API"**
2. Hacer clic en la tarjeta
3. Hacer clic en **"Habilitar"**

### Paso 4: Habilitar Gmail API (Opcional)

Si necesitas enviar emails desde el workflow:

1. Buscar: **"Gmail API"**
2. Hacer clic en la tarjeta
3. Hacer clic en **"Habilitar"**

**Lista de APIs habilitadas:**

![APIs de Google Workspace](https://ibb.co/sdh0wBhc)

✅ Google Drive API  
✅ Google Sheets API  
✅ Gmail API (opcional)

---

## 🔑 Crear Credenciales OAuth 2.0

### Paso 1: Ir a Credenciales

1. En Google Cloud Console, ve a **API y servicios** → **Credenciales**
2. Haz clic en **"+ Crear credenciales"**
3. Selecciona **"ID de cliente de OAuth"**

![Crear credenciales](https://ibb.co/gLKjdybc)

### Paso 2: Configurar Pantalla de Consentimiento (Primera vez)

Si es la primera vez que creas credenciales OAuth, te pedirá configurar la pantalla de consentimiento:

1. Selecciona **"Externo"** como tipo de usuario
2. Haz clic en **"Crear"**

![Pantalla de consentimiento público](https://ibb.co/JWZcPF9B)

**Completa la información:**

- **Nombre de la aplicación:** `n8n Risk Automation` (o el nombre que prefieras)
- **Correo electrónico de asistencia:** Tu email
- **Logotipo de la aplicación:** (Opcional)
- **Dominios autorizados:** (Déjalo vacío por ahora)
- **Correo electrónico del desarrollador:** Tu email

3. Haz clic en **"Guardar y continuar"**

### Paso 3: Agregar Scopes (Alcances)

En la sección de **Scopes**, agrega los permisos necesarios:

```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/gmail.send (si usas Gmail)
```

**Manera fácil:**

1. Haz clic en **"Agregar o quitar scopes"**
2. Busca **"Google Drive API"** y selecciona todos los scopes necesarios
3. Busca **"Google Sheets API"** y selecciona los scopes
4. Haz clic en **"Actualizar"**

### Paso 4: Agregar Usuarios de Prueba

**⚠️ IMPORTANTE:** Como la app está en estado "Prueba", solo los usuarios agregados podrán usarla.

![Usuarios de prueba](https://ibb.co/kg35dt3C)

1. En la sección **"Usuarios de prueba"**, haz clic en **"+ Add users"**
2. Agrega tu correo electrónico (el que usarás para autenticarte en n8n)
3. Haz clic en **"Guardar"**

> **Nota:** Puedes agregar hasta 100 usuarios de prueba. Agrega todos los emails que necesiten acceso.

### Paso 5: Seleccionar Tipo de Aplicación

1. Vuelve a **Credenciales** → **"+ Crear credenciales"** → **"ID de cliente de OAuth"**
2. Selecciona **"Aplicación web"** como tipo de aplicación

![Tipo de aplicación](https://ibb.co/Xr0H26Kv)

### Paso 6: Configurar URIs Autorizados

**Orígenes autorizados de JavaScript:**

```
http://localhost:5678
```

**URIs de redirección autorizados:**

```
http://localhost:5678/rest/oauth2-credential/callback
```

![URIs de redirección](https://ibb.co/kg35dt3C)

> **⚠️ IMPORTANTE:** La URI de redirección debe ser **exactamente** como se muestra arriba. n8n requiere esta ruta específica.

### Paso 7: Obtener Client ID y Client Secret

1. Haz clic en **"Crear"**
2. Aparecerá un modal con tus credenciales:

![Credenciales OAuth creadas](https://ibb.co/Xr0H26Kv)

```
ID de cliente: 288338628033-6nrp00su3kddsnlfcqvba0hp0uattu3o.apps.googleusercontent.com
Secreto del cliente: GOCSPX-1ZFV4eFsnkjeSvKYfKNh8WEEAal
```

3. **COPIA Y GUARDA** estas credenciales de forma segura
4. Haz clic en **"Descargar JSON"** para tener un backup

> **⚠️ ADVERTENCIA:** El secreto del cliente solo se muestra una vez. Si lo pierdes, tendrás que crear nuevas credenciales.

---

## 🔌 Configurar Credenciales en n8n

### Paso 1: Abrir n8n

1. Accede a n8n en tu navegador: `http://localhost:5678`
2. Inicia sesión con tus credenciales

### Paso 2: Ir a Credenciales

1. En el menú lateral, haz clic en **"Credentials"** (🔑)
2. Haz clic en **"+ Add Credential"**

### Paso 3: Configurar Google Drive OAuth2

1. Busca **"Google Drive OAuth2 API"**
2. Completa los campos:

   - **Credential Name:** `Google Drive account` (o cualquier nombre descriptivo)
   - **Client ID:** Pega el Client ID que copiaste
   - **Client Secret:** Pega el Client Secret que copiaste
   - **OAuth Redirect URL:** (Auto-completado) `http://localhost:5678/rest/oauth2-credential/callback`

3. Haz clic en **"Sign in with Google"**

### Paso 4: Autorizar el Acceso

Se abrirá una ventana de autorización de Google:

![Google no verificó esta app](https://ibb.co/84BVnQGR)

**⚠️ Aparecerá una advertencia: "Google no verificó esta app"**

**Esto es NORMAL.** Tu aplicación está en modo de prueba.

**Para continuar:**

1. Haz clic en **"Configuración avanzada"** (o "Advanced")
2. Haz clic en **"Ir a [nombre de tu app] (no seguro)"**
3. Revisa los permisos solicitados
4. Haz clic en **"Permitir"**

### Paso 5: Verificar Conexión

Después de autorizar, deberías ver:

![Cuenta conectada](https://ibb.co/84BVnQGR)

✅ **"Account connected"** en verde

### Paso 6: Repetir para Google Sheets

1. Crea una nueva credencial: **"Google Sheets OAuth2 API"**
2. Usa el **mismo Client ID y Client Secret**
3. Haz clic en **"Sign in with Google"**
4. Autoriza (probablemente ya no te pida autorización si usaste la misma cuenta)

### Paso 7: Repetir para Gmail (Opcional)

Si necesitas enviar emails:

1. Crea credencial: **"Gmail OAuth2 API"**
2. Usa las **mismas credenciales**
3. Autoriza el acceso

---

## 🛠️ Solución de Problemas

### ❌ Error: "Redirect URI mismatch"

**Causa:** La URI de redirección no coincide con la configurada en Google Cloud.

**Solución:**

1. Ve a Google Cloud Console → Credenciales
2. Haz clic en el nombre de tu cliente OAuth
3. Verifica que la URI sea **exactamente:**
   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```
4. No debe haber espacios ni caracteres extra
5. Guarda los cambios y espera 5 minutos para que se propague

### ❌ Error: "Access blocked: This app's request is invalid"

**Causa:** La pantalla de consentimiento no está configurada correctamente.

**Solución:**

1. Ve a Google Cloud Console → **OAuth consent screen**
2. Verifica que el estado sea **"En producción"** o **"Prueba"**
3. Si está en Prueba, verifica que tu email esté en **"Test users"**
4. Completa todos los campos obligatorios

### ❌ Error: "The user is not in the test user list"

**Causa:** Intentas autenticarte con un email que no está en la lista de usuarios de prueba.

**Solución:**

1. Ve a Google Cloud Console → **OAuth consent screen** → **Público**
2. En **"Test users"**, haz clic en **"+ Add users"**
3. Agrega el email con el que intentas autenticarte
4. Guarda e intenta de nuevo

### ❌ Error: "Invalid grant" o "Token expired"

**Causa:** El token de acceso expiró o fue revocado.

**Solución:**

1. En n8n, ve a la credencial afectada
2. Haz clic en **"Reconnect"**
3. Autoriza de nuevo en la ventana de Google
4. Guarda la credencial

### ⚠️ La advertencia "Google no verificó esta app" aparece siempre

**Esto es normal** mientras tu app esté en modo de prueba.

**Opciones:**

1. **Opción 1 (Recomendada para desarrollo):** Acepta la advertencia cada vez
2. **Opción 2 (Para producción):** Solicita verificación de Google:
   - Ve a **OAuth consent screen**
   - Cambia el estado de **"Testing"** a **"In production"**
   - Solicita verificación (puede tomar semanas y requiere revisión)

---

## 📊 Tabla Resumen de Configuración

| API                   | ¿Obligatoria? | Uso en el Workflow                           |
| --------------------- | ------------- | -------------------------------------------- |
| **Google Drive API**  | ✅ Sí         | Buscar y verificar archivos de Google Sheets |
| **Google Sheets API** | ✅ Sí         | Leer lista de empresas y escribir resultados |
| **Gmail API**         | ⚠️ Opcional   | Enviar emails de notificación                |

---

## 🔒 Mejores Prácticas de Seguridad

1. ✅ **No compartas tus credenciales:** El Client ID y Secret son como una contraseña
2. ✅ **Usa usuarios de prueba:** Solo agrega emails de confianza mientras está en modo prueba
3. ✅ **Revisa permisos:** Solo otorga los scopes mínimos necesarios
4. ✅ **Monitorea accesos:** Revisa periódicamente en Google → Security → Third-party apps
5. ✅ **Rota credenciales:** Si sospechas que fueron comprometidas, crea nuevas
6. ✅ **No commitees credenciales:** Nunca subas el Client Secret a GitHub

---

## 📚 Enlaces Útiles

- [Google Cloud Console](https://console.cloud.google.com/)
- [Documentación OAuth 2.0 de Google](https://developers.google.com/identity/protocols/oauth2)
- [n8n Google Drive Docs](https://docs.n8n.io/integrations/builtin/credentials/google/)
- [n8n Google Sheets Docs](https://docs.n8n.io/integrations/builtin/credentials/google/)

---

## ✅ Checklist de Verificación

Antes de continuar con el workflow, verifica que:

- [ ] Google Drive API está habilitada
- [ ] Google Sheets API está habilitada
- [ ] Credenciales OAuth 2.0 creadas
- [ ] Client ID y Secret guardados de forma segura
- [ ] URI de redirección configurada: `http://localhost:5678/rest/oauth2-credential/callback`
- [ ] Tu email está en la lista de usuarios de prueba
- [ ] Credenciales configuradas en n8n
- [ ] Estado "Account connected" en verde en n8n
- [ ] Test de conexión exitoso (prueba leer un Google Sheet)

---

**¡Listo!** Ahora puedes volver al [README principal](README.md) y continuar con la importación del workflow.

**Siguiente paso:** [Importar el Workflow](README.md#paso-6-importar-el-workflow)
