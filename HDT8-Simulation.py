import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Parámetros iniciales
RANDOM_SEED = 10
TIEMPO_TOTAL = 1440  # 24 horas en minutos

# Número de pacientes y intervalos entre llegadas (valores hipotéticos basados en datos de flujo hospitalario)
# Se recomienda ajustar estos valores según datos históricos locales.
NUM_PACIENTES = {
    'regular': 50,      # Aproximadamente 50 pacientes en un día normal
    'fin_semana': 100,  # Mayor afluencia durante el fin de semana
    'festivo': 150      # Aumento considerable en días festivos
}
INTERVALOS = {
    'regular': 20,      # Tiempo promedio entre llegadas en días regulares (basado en estudios de flujo)
    'fin_semana': 10,   # Llegadas más frecuentes durante el fin de semana
    'festivo': 5        # Mayor intensidad en días festivos
}

# Costos 
SALARIO_ENFERMERA_ANUAL = 93405  
# Valor basado en el promedio reportado por el Bureau of Labor Statistics (BLS) para enfermeras registradas en EE. UU. (BLS, 2023).

SALARIO_DOCTOR_ANUAL = 375200  
# Valor obtenido de informes como MedSchoolInsiders, que indican salarios elevados para médicos de emergencias (MedSchoolInsiders, 2023).

COSTO_EQUIPO_XRAY = 150000  
# Estimación dentro del rango típico para equipos de rayos X digitales, cuyo costo puede variar entre $100,000 y $200,000 (Maven Imaging, 2023).

COSTO_EQUIPO_LAB = 30000  
# Valor representativo para equipamiento básico de laboratorio; (Costo Total Para Laboratorio de Análisis Clínicos, s. f.)
  
# Tiempos de procesamiento (minutos)
TIEMPO_TRIAGE = 10  
# Tiempo de triaje basado en departamentos de emergencias eficientes (algunos estudios reportan promedios mayores, pero se usa 10 min para la simulación).
  
TIEMPO_DOCTOR = 30  
# Tiempo de consulta inicial con el doctor, acorde a promedios observados en estudios de ED (por ejemplo, Annals of Emergency Medicine).
  
TIEMPO_XRAY = 20  
# Tiempo estimado para la realización y procesamiento de un estudio de rayos X; valores en la práctica pueden variar.
  
TIEMPO_LAB = 30
# Tiempo de laboratorio;  (Revista Emergencias, 2007)

class SalaEmergencia:
    def __init__(self, env, num_enfermeras, num_doctores, num_xray, num_lab):
        self.env = env
        self.enfermeras = simpy.PriorityResource(env, capacity=num_enfermeras)
        self.doctores = simpy.PriorityResource(env, capacity=num_doctores)
        self.xray = simpy.PriorityResource(env, capacity=num_xray)
        self.lab = simpy.PriorityResource(env, capacity=num_lab)

class Paciente:
    def __init__(self, env, nombre):
        self.env = env
        self.nombre = nombre
        self.severidad = random.randint(1, 5)  # Severidad aleatoria del 1 al 5 (escala simple)
        self.tiempo_llegada = env.now
        self.tiempos_espera = {}

    def procesar(self, sala):
        with sala.enfermeras.request(priority=self.severidad) as req:
            yield req
            self.tiempos_espera['triage'] = self.env.now - self.tiempo_llegada
            yield self.env.timeout(TIEMPO_TRIAGE)

        with sala.doctores.request(priority=self.severidad) as req:
            yield req
            self.tiempos_espera['doctor'] = self.env.now - (self.tiempo_llegada + TIEMPO_TRIAGE)
            yield self.env.timeout(TIEMPO_DOCTOR)

        if random.random() < 0.5:
            with sala.xray.request(priority=self.severidad) as req:
                yield req
                self.tiempos_espera['xray'] = self.env.now - (self.tiempo_llegada + TIEMPO_TRIAGE + TIEMPO_DOCTOR)
                yield self.env.timeout(TIEMPO_XRAY)

        if random.random() < 0.7:
            with sala.lab.request(priority=self.severidad) as req:
                yield req
                tiempo_base = self.tiempo_llegada + TIEMPO_TRIAGE + TIEMPO_DOCTOR + (TIEMPO_XRAY if 'xray' in self.tiempos_espera else 0)
                self.tiempos_espera['lab'] = self.env.now - tiempo_base
                yield self.env.timeout(TIEMPO_LAB)

        tiempo_total = self.env.now - self.tiempo_llegada
        tiempos_totales.append(tiempo_total)
        tiempos_espera_etapas['triage'].append(self.tiempos_espera.get('triage', 0))
        tiempos_espera_etapas['doctor'].append(self.tiempos_espera.get('doctor', 0))
        tiempos_espera_etapas['xray'].append(self.tiempos_espera.get('xray', 0))
        tiempos_espera_etapas['lab'].append(self.tiempos_espera.get('lab', 0))

def generar_pacientes(env, sala, num_pacientes, intervalo):
    for i in range(num_pacientes):
        paciente = Paciente(env, f'Paciente_{i}')
        env.process(paciente.procesar(sala))
        yield env.timeout(random.expovariate(1.0 / intervalo))

def simular(tipo_dia, num_enfermeras, num_doctores, num_xray, num_lab):
    global tiempos_totales, tiempos_espera_etapas
    tiempos_totales = []
    tiempos_espera_etapas = {'triage': [], 'doctor': [], 'xray': [], 'lab': []}
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    sala = SalaEmergencia(env, num_enfermeras, num_doctores, num_xray, num_lab)
    env.process(generar_pacientes(env, sala, NUM_PACIENTES[tipo_dia], INTERVALOS[tipo_dia]))
    env.run(until=TIEMPO_TOTAL)
    
    tiempo_medio_total = np.mean(tiempos_totales) if tiempos_totales else float('inf')
    tiempos_medios_etapas = {etapa: np.mean(tiempos) if tiempos else 0 for etapa, tiempos in tiempos_espera_etapas.items()}
    
    logger.info(f"\n=== Día {tipo_dia} | Config: {num_enfermeras}E, {num_doctores}D, {num_xray}X, {num_lab}L ===")
    logger.info(f"Tiempo medio total: {tiempo_medio_total:.2f} minutos")
    logger.info(f"Tiempo medio espera triage: {tiempos_medios_etapas['triage']:.2f} minutos")
    logger.info(f"Tiempo medio espera doctor: {tiempos_medios_etapas['doctor']:.2f} minutos")
    logger.info(f"Tiempo medio espera rayos X: {tiempos_medios_etapas['xray']:.2f} minutos")
    logger.info(f"Tiempo medio espera laboratorio: {tiempos_medios_etapas['lab']:.2f} minutos")
    
    return tiempo_medio_total

# Configuraciones de recursos con costos (basadas en los valores anteriores)
CONFIGURACIONES = [
    {'enfermeras': 1, 'doctores': 1, 'xray': 1, 'lab': 1, 'costo': 668605, 'label': '1E,1D,1X,1L ($0.67M)'},
    {'enfermeras': 2, 'doctores': 2, 'xray': 1, 'lab': 1, 'costo': 1387210, 'label': '2E,2D,1X,1L ($1.39M)'},
    {'enfermeras': 3, 'doctores': 3, 'xray': 2, 'lab': 2, 'costo': 2105815, 'label': '3E,3D,2X,2L ($2.11M)'},
    {'enfermeras': 4, 'doctores': 4, 'xray': 2, 'lab': 2, 'costo': 2524420, 'label': '4E,4D,2X,2L ($2.52M)'},
]

# Ejecutar simulaciones
resultados = {tipo: {} for tipo in NUM_PACIENTES.keys()}
for tipo_dia in NUM_PACIENTES.keys():
    logger.info(f"\n=== Simulación para día {tipo_dia} ===")
    for config in CONFIGURACIONES:
        tiempo_medio = simular(tipo_dia, config['enfermeras'], config['doctores'], config['xray'], config['lab'])
        resultados[tipo_dia][config['label']] = tiempo_medio

# Gráfico de barras agrupadas
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(NUM_PACIENTES))
width = 0.15

for i, config in enumerate(CONFIGURACIONES):
    tiempos = [resultados[tipo][config['label']] for tipo in NUM_PACIENTES.keys()]
    ax.bar(x + i * width, tiempos, width, label=config['label'])

ax.set_ylabel('Tiempo Promedio (minutos)')
ax.set_title('Tiempos Promedios en Sala de Emergencia por Tipo de Día')
ax.set_xticks(x + width * (len(CONFIGURACIONES) - 1) / 2)
ax.set_xticklabels(NUM_PACIENTES.keys())
ax.legend(title='Configuración (Costo Anual)')
ax.grid(True, alpha=0.3)
plt.show()

# Análisis de costos
for config in CONFIGURACIONES:
    print(f"Configuración {config['label']}: Costo anual estimado = ${config['costo']:,.2f}")
