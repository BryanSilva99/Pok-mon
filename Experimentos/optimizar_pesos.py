import csv
import json
from pathlib import Path

from IA.Evolutivo import optimizar_pesos


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "Resultados"


def mostrar_pesos(pesos):
    for nombre, valor in pesos.items():
        print(f"  {nombre}: {valor:.4f}")


def guardar_resultados_optimizacion(mejor, historial):
    SALIDA.mkdir(exist_ok=True)

    with open(SALIDA / "genetic_best_weights.json", "w", encoding="utf-8") as archivo:
        json.dump(mejor["pesos"], archivo, indent=2, ensure_ascii=False)

    campos = [
        "generacion",
        "fitness",
        "win_rate_manual",
        "win_rate_heuristico",
        "win_rate_random",
        "pesos",
    ]
    with open(SALIDA / "genetic_history.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in historial:
            escritor.writerow(
                {
                    "generacion": fila["generacion"],
                    "fitness": fila["fitness"],
                    "win_rate_manual": fila["win_rate_manual"],
                    "win_rate_heuristico": fila["win_rate_heuristico"],
                    "win_rate_random": fila["win_rate_random"],
                    "pesos": json.dumps(fila["pesos"], ensure_ascii=False),
                }
            )


def ejecutar_optimizacion():
    mejor, historial = optimizar_pesos()
    guardar_resultados_optimizacion(mejor, historial)

    print("=== EVOLUCION DE PESOS ===")
    for registro in historial:
        print(
            f"Generacion {registro['generacion']}: fitness={registro['fitness']:.4f} | "
            f"vs Manual={registro['win_rate_manual']:.1f}% | "
            f"vs Heuristico={registro['win_rate_heuristico']:.1f}% | "
            f"vs Random={registro['win_rate_random']:.1f}%"
        )

    print("\n=== MEJORES PESOS ===")
    mostrar_pesos(mejor["pesos"])
    print(f"\nFitness final: {mejor['fitness']:.4f}")
    print(
        f"Win rate final vs Avanzado manual: "
        f"{mejor['vs_manual']['win_rate_1']:.1f}%"
    )
    print(
        f"Win rate final vs Heuristico: "
        f"{mejor['vs_heuristico']['win_rate_1']:.1f}%"
    )
    print(
        f"Win rate final vs Random: "
        f"{mejor['vs_random']['win_rate_1']:.1f}%"
    )
    print(f"\nResultados guardados en {SALIDA}")


if __name__ == "__main__":
    ejecutar_optimizacion()
