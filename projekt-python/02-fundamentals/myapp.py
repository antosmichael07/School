import physics

def main():
    test_mass = 70
    test_distance = 1000

    print(f"Váha {test_mass} kg člověka na Zemi: {physics.weight_on_earth(test_mass):.3f} N")
    print(f"Váha {test_mass} kg člověka na Měsíci: {physics.weight_on_moon(test_mass):.3f} N")
    print(f"Čas, za který světlo urazí {test_distance} m: {physics.time_for_light(test_distance):.10f} s")
    print(f"Čas, za který zvuk urazí {test_distance} m: {physics.time_for_sound(test_distance):.3f} s")

if __name__ == "__main__":
    main()
