# Monitor de citas – Embajada del Japón en Colombia

Revisa el calendario cada 15 min y te manda un correo apenas se abra un día con cupo.

## 1. Crear el repositorio en GitHub

1. Crea un repo nuevo (puede ser **público**: así los minutos de GitHub Actions son
   ilimitados y gratis; si lo haces privado tienes 2000 min/mes gratis, que también
   alcanzan sin problema con esta frecuencia).
2. Sube estos 3 archivos manteniendo la misma carpeta:
   - `check_citas.py`
   - `requirements.txt`
   - `.github/workflows/check_citas.yml`

## 2. Crear una contraseña de aplicación de Gmail

1. Activa la verificación en 2 pasos en tu cuenta: https://myaccount.google.com/security
2. Genera una "Contraseña de aplicación" en: https://myaccount.google.com/apppasswords
3. Copia el código de 16 caracteres que te da (sin espacios).

## 3. Configurar los secretos en GitHub

En el repo: **Settings → Secrets and variables → Actions → New repository secret**
y crea estos tres:

| Nombre               | Valor                                              |
|-----------------------|-----------------------------------------------------|
| `GMAIL_USER`          | tu correo completo, ej. `tucorreo@gmail.com`        |
| `GMAIL_APP_PASSWORD`  | la contraseña de 16 caracteres del paso 2           |
| `NOTIFY_EMAIL`        | a dónde quieres que llegue el aviso (puede ser el mismo `GMAIL_USER`) |

## 4. Listo

El workflow corre solo cada 15 minutos. También puedes forzar una corrida manual
desde la pestaña **Actions → Monitor cita embajada Japon → Run workflow**.

Cuando detecte un día nuevo con cupo, te llega un correo con el/los días y el link
directo al calendario.

## Notas importantes

- El script solo revisa el **mes que se muestra por defecto** al entrar a la página
  (el actual). Si necesitas monitorear varios meses adelante, el calendario cambia
  de mes por JavaScript/AJAX y tocaría investigar la URL exacta que usa esa llamada
  — dime si la encuentras (revisando la pestaña "Red/Network" del navegador al
  hacer clic en "próximo mes") y ajusto el script.
- La clasificación de "disponible" se basa en que el ícono de los días llenos
  incluye la palabra `disabled` en su nombre de archivo. Si después de la primera
  corrida notas que nunca detecta nada (o detecta todo como disponible), avísame
  y ajustamos la regla mirando el HTML real de un día que sepas que sí tiene cupo.
- Cada corrida guarda su resultado en `state.json` dentro del repo — eso además
  mantiene el repo "activo", así GitHub no desactiva el cron por inactividad
  (lo hace automáticamente si un repo pasa 60 días sin commits).
