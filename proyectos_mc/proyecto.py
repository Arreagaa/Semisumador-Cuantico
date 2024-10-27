# Importar los módulos necesarios de Qiskit y matplotlib
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Crear el simulador cuántico
simulator = Aer.get_backend('qasm_simulator')

# Definir las combinaciones de entrada A y B
combinaciones = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Recorrer combinaciones de A y B
for (a, b) in combinaciones:
    # Crear carpeta para la combinación
    carpeta = f"Reporte_A_{a}_B_{b}"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Crear circuito cuántico con 3 qubits y 2 bits clásicos
    qc = QuantumCircuit(3, 2)

    # Inicializar qubits A y B
    if a == 1:
        qc.x(0)  # Cambiar estado de A a 1
    if b == 1:
        qc.x(1)  # Cambiar estado de B a 1

    # Guardar circuito inicial
    qc.draw(output='mpl')
    plt.title(f"Circuito inicial A={a}, B={b}")
    plt.savefig(f"{carpeta}/Grupo19_Circuito_inicial_A_{a}_B_{b}(1).png")
    plt.close()

    # Aplicar CNOT para sumar A y B
    qc.cx(0, 1)

    # Guardar circuito después de la suma
    qc.draw(output='mpl')
    plt.title(f"Circuito después de CNOT (Suma) A={a}, B={b}")
    plt.savefig(f"{carpeta}/Grupo19_Circuito_suma_A_{a}_B_{b}(2).png")
    plt.close()

    # Aplicar Toffoli para calcular el acarreo
    qc.ccx(0, 1, 2)

    # Guardar circuito después del acarreo
    qc.draw(output='mpl')
    plt.title(f"Circuito después de Toffoli (Acarreo) A={a}, B={b}")
    plt.savefig(f"{carpeta}/Grupo19_Circuito_acarreo_A_{a}_B_{b}(3).png")
    plt.close()

    # Medir resultados (Suma en el qubit 1, Acarreo en el qubit 2)
    qc.measure(1, 0)
    qc.measure(2, 1)

    # Guardar circuito final con mediciones
    qc.draw(output='mpl')
    plt.title(f"Circuito final A={a}, B={b}")
    plt.savefig(f"{carpeta}/Grupo19_Circuito_final_A_{a}_B_{b}(4).png")
    plt.close()

    # Ejecutar el circuito en el simulador
    result = simulator.run(qc).result()

    # Obtener distribución de probabilidad de las mediciones
    counts = result.get_counts(qc)

    # Guardar histograma de resultados
    plot_histogram(counts)
    plt.title(f"Distribución de resultados A={a}, B={b}")
    plt.savefig(f"{carpeta}/Grupo19_Histograma_A_{a}_B_{b}(5).png")
    plt.close()

    # Obtener resultado más probable
    resultado = max(counts, key=counts.get)
    suma = resultado[0]
    acarreo = resultado[1]

    # Guardar resultados en archivo de texto
    with open(f"{carpeta}/Resultados_A_{a}_B_{b}(6).txt", 'w') as f:
        f.write(f"A={a}, B={b} Resultado más probable: Suma = {
                suma}, Acarreo = {acarreo}\n")
        f.write(f"Distribución completa de resultados: {counts}\n")

    # Mostrar estados de los qubits de entrada
    estados = ['0', '1']
    x_labels = ['A', 'B']
    y_values = [a, b]

    plt.bar(x_labels, y_values, color=['blue', 'orange'])
    plt.ylim(-0.5, 1.5)
    plt.ylabel('Estado del Qubit')
    plt.title(f"Estado Qubits Entrada A={a}, B={b}")
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.axhline(y=1, color='black', linewidth=0.5, linestyle='--')

    for i, v in enumerate(y_values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # Guardar gráfico de estados de los qubits de entrada
    plt.savefig(f"{carpeta}/Grupo19_Estado_Qubits_A_{a}_B_{b}(7).png")
    plt.close()

    # Guardar resumen del circuito en archivo de texto
    with open(f"{carpeta}/Resumen_A_{a}_B_{b}(8).txt", 'w') as f:
        f.write(f"Resumen A={a}, B={b}:\n")
        f.write(f"- Qubits A y B inicializados en {a} y {b}.\n")
        f.write(f"- CNOT aplicada para sumar (A xor B).\n")
        f.write(f"- Toffoli aplicada para el acarreo (A . B).\n")
        f.write(f"- Se midieron qubit 1 (suma) y qubit 2 (acarreo).\n")
        f.write(
            f"- Resultado más probable: suma = {suma}, acarreo = {acarreo}.\n")
        f.write(f"- Histograma generado con la probabilidad de cada resultado.\n")
        f.write(f"- Gráfico muestra estados de entrada A y B.\n")
