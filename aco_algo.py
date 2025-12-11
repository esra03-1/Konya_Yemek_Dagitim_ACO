# aco_algo.py
import numpy as np
import random

class AntColonyOptimizer:
    def __init__(self, distance_matrix, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
        self.distance_matrix = distance_matrix
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # Feromon önemi
        self.beta = beta    # Mesafe önemi (Heuristic)
        self.evaporation_rate = evaporation_rate # Buharlaşma
        self.Q = Q          # Feromon sabiti
        self.n_cities = len(distance_matrix)
        
        # Feromon matrisini başlat (küçük pozitif değerlerle)
        self.pheromones = np.ones((self.n_cities, self.n_cities)) * 0.1

    def run(self):
        best_path = None
        best_distance = float('inf')
        fitness_history = []

        for iteration in range(self.n_iterations):
            paths = []
            path_distances = []

            # Her karınca için bir tur oluştur
            for _ in range(self.n_ants):
                path = self._construct_solution()
                dist = self._calculate_path_distance(path)
                paths.append(path)
                path_distances.append(dist)

                # En iyi çözümü güncelle (Elitizm)
                if dist < best_distance:
                    best_distance = dist
                    best_path = path

            # Feromonları güncelle
            self._update_pheromones(paths, path_distances)
            
            # Geçmişi kaydet
            fitness_history.append(best_distance)
            
        return best_path, best_distance, fitness_history

    def _construct_solution(self):
        path = [0] # Her zaman 0. noktadan (Merkez Mutfak) başla
        visited = {0}

        for _ in range(self.n_cities - 1):
            current_city = path[-1]
            probabilities = self._calculate_probabilities(current_city, visited)
            
            # Rulet Tekerleği Seçimi
            next_city = self._roulette_wheel_selection(probabilities)
            path.append(next_city)
            visited.add(next_city)

        path.append(0) # Tura geri dön
        return path

    def _calculate_probabilities(self, current_city, visited):
        probabilities = []
        unvisited_cities = [city for city in range(self.n_cities) if city not in visited]

        for city in unvisited_cities:
            pheromone = self.pheromones[current_city][city] ** self.alpha
            # Mesafe 0 ise (hata önleme) çok küçük sayı ekle
            dist = self.distance_matrix[current_city][city]
            heuristic = (1.0 / (dist + 1e-10)) ** self.beta
            probabilities.append(pheromone * heuristic)

        total = sum(probabilities)
        return [p / total for p in probabilities], unvisited_cities

    def _roulette_wheel_selection(self, probabilities_data):
        probs, cities = probabilities_data
        # Kümülatif toplam ile seçim (Hocanın notlarındaki gibi)
        r = random.random()
        cumulative = 0
        for i, p in enumerate(probs):
            cumulative += p
            if r <= cumulative:
                return cities[i]
        return cities[-1] # Garanti dönüş

    def _calculate_path_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distance_matrix[path[i]][path[i+1]]
        return distance

    def _update_pheromones(self, paths, distances):
        # 1. Buharlaşma
        self.pheromones *= (1 - self.evaporation_rate)

        # 2. Yeni Feromon Ekleme
        for path, dist in zip(paths, distances):
            deposit = self.Q / dist
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                self.pheromones[u][v] += deposit
                self.pheromones[v][u] += deposit # Simetrik yol