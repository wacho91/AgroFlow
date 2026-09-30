🌱 AgroFlow: SaaS ERP AgroTech de Nivel Enterprise
Python
FastAPI
React
PostgreSQL

https://agro-flow-one.vercel.app/login

🌍 El Problema Real (El mercado que resolvemos)
En la agricultura tradicional, el 80% de los medianos y pequeños agricultores gestionan sus fincas con cuadernos y Excel. Esto genera tres problemas críticos:

Ignorancia del Costo Real: No saben cuánto les costó producir un kilo de café o tomate hasta que termina la cosecha. A menudo, venden por debajo de su costo de producción.
Caos en Bodega: Los insumos (fertilizantes, químicos) se pierden, se vencen o son robados por falta de control de inventario.
Ceguera Climática: Reaccionan a las lluvias o sequías cuando el cultivo ya está dañado.
💡 La Solución: AgroFlow
AgroFlow es un ERP (Enterprise Resource Planning) Agrícola 100% en la nube. Lleva la trazabilidad financiera y operativa de una multinacional a la finca de cualquier familia campesina, accesible desde cualquier celular o computador.

🚀 Funcionalidades Principales (Módulos)
🏡 Fincas y Lotes: División clara del predio en parcelas (lotes) con seguimiento del "Costo Acumulado" de cada metro cuadrado de tierra.
🧪 Inventario Inteligente (Kardex): Control exacto de insumos en kilos/litros con alertas visuales automáticas (⚠️ Reabastecer / ✅ Óptimo).
👷‍♂️ Nómina Rural: Gestión de jornaleros y trabajadores temporales.
🌩️ Eventos Agrícolas (El Corazón del Sistema): Mediante Event Sourcing, cada vez que se aplica un insumo o se paga un jornal, el sistema descuenta la bodega automáticamente y suma el costo al Lote en tiempo real.
📅 Ciclos Productivos (Siembras): Desde que se siembra hasta que se cosecha. Calcula la ganancia neta de la cosecha e inyecta el ingreso automáticamente a la tesorería.
💰 Tesorería y Dashboard: Gráficas interactivas de ingresos vs egresos y balance neto.
☁️ API Climática en Tiempo Real: Integración con OpenWeatherMap. Lee el clima de cada municipio donde hay una finca y lanza alertas críticas (Ej: "⚠️ Hay lluvia. Evita aplicar fertilizantes hoy").
🏛️ Arquitectura y Stack Tecnológico
Construimos AgroFlow para ser escalable a millones de fincas, usando las mejores prácticas de la industria:

Backend (El Motor)
Lenguaje: Python 3.11
Framework: FastAPI (Asíncrono y ultrarrápido).
Arquitectura: Hexagonal (Ports and Adapters) y Clean Code. Separación estricta de Dominio, Aplicación e Infraestructura. Ningún archivo supera las 150 líneas.
ORM: SQLAlchemy Asíncrono.
Patrones de Diseño: Event Sourcing para la trazabilidad inmutable de costos agrícolas.

Frontend (La Interfaz)
Librería: React 18 + Vite.
Estilos: Tailwind CSS (Diseño Premium, responsive para celulares en el campo).
Gráficas: Recharts (Dashboards financieros).
Alertas: SweetAlert2 (Experiencia de usuario de nivel Enterprise).
Base de Datos y Nube
Base de Datos: PostgreSQL (Servido en la nube por Neon.tech).
Despliegue Backend: Render (Servidor Python 3.11.9).
Despliegue Frontend: Vercel (CDN global para carga instantánea).

🛡️ Ciberseguridad (Security by Design)
AgroFlow no sacrifica seguridad por usabilidad. Implementamos defensas contra los ataques más comunes (OWASP Top 10):

Autenticación JWT: Tokens de acceso con expiración de 24 horas. Las contraseñas nunca se guardan en texto plano.
Encriptación Bcrypt: Las contraseñas se hashean usando el algoritmo bcrypt directamente en el backend, blindado contra vulnerabilidades de librerías de terceros.
Políticas CORS: El backend rechaza peticiones de dominios no autorizados.
Validación Estricta (Pydantic): Todo dato que entra a la API es validado en tiempo de ejecución, previniendo inyecciones SQL o datos malformados.
Multi-Tenant Ready: La arquitectura de base de datos está preparada para aislamiento de datos por Tenant (Row Level Security), garantizando que una finca nunca pueda ver los datos de otra.

🛠️ Instalación y Puesta en Marcha (Para Desarrolladores)
Si deseas clonar y correr este proyecto localmente:

Clonar el repositorio:
git clone https://github.com/wacho91/AgroFlow.git
cd AgroFlow

Configurar Backend:
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt

Crea un archivo .env con las variables: DATABASE_URL, JWT_SECRET, OPENWEATHER_API_KEY.
Ejecuta el script python crear_admin.py para crear tu usuario inicial.
Levanta el servidor: uvicorn src.main:app --reload --port 8000

Configurar Frontend:
cd ../frontend
npm install

Crea un archivo .env con: VITE_API_URL=http://localhost:8000
Levanta el servidor: npm run dev

🤝 El Equipo
Este software fue diseñado, arquitectado y programado con visión comercial y técnica de nivel Enterprise.

Socio Arquitecto: Cristian (Fundador, Visionario del Negocio AgroTech, Arquitecto de Software e Inteligencia Artificial)
