from IA.Evolutivo import optimizar_pesos


def mostrar_pesos(pesos):
    for nombre, valor in pesos.items():
        print(f"  {nombre}: {valor:.4f}")


def ejecutar_optimizacion():
    mejor, historial = optimizar_pesos()

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


if __name__ == "__main__":
    ejecutar_optimizacion()
