# simulator.py

import random
import json


class BiometricSimulator:

    def __init__(self):
        self.states = {
            "relaxed": {
                "breathing_rate": (10, 16),
                "heart_rate": (60, 75),
                "movement": (5, 20),
                "stress_level": "low"
            },

            "stressed": {
                "breathing_rate": (20, 30),
                "heart_rate": (90, 130),
                "movement": (40, 90),
                "stress_level": "high"
            },

            "meditation": {
                "breathing_rate": (6, 10),
                "heart_rate": (50, 65),
                "movement": (0, 10),
                "stress_level": "very low"
            }
        }

    def generate_data(self, state=None):

        if state is None:
            state = random.choice(list(self.states.keys()))

        if state not in self.states:
            raise ValueError("Invalid state")

        config = self.states[state]

        data = {
            "state": state,
            "breathing_rate": random.randint(*config["breathing_rate"]),
            "heart_rate": random.randint(*config["heart_rate"]),
            "movement": random.randint(*config["movement"]),
            "stress_level": config["stress_level"]
        }

        return data

    def generate_json(self, state=None):
        return json.dumps(
            self.generate_data(state),
            indent=2
        )


if __name__ == "__main__":

    simulator = BiometricSimulator()

    # Generar estado aleatorio
    print(simulator.generate_json())

    # Generar estado específico
    print(simulator.generate_json("meditation"))