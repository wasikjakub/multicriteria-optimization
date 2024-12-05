import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from copy import deepcopy


class RSM:
    def get_rank(A1, A2, D):
        n_alternatives, n_criteria = D.shape
        M1 = []
        M2 = []

        for i in range(n_alternatives):
            condition = False

            for k in range(A1.shape[0]):
                for j in range(n_criteria):
                    if D[i, j] >= A1[k, j]:
                        condition = True

                    else:
                        condition = False
                        break

            if condition:
                for k in range(A1.shape[0]):
                    if np.equal(A1[k, :], D[i, :]).all():
                        break

                else:
                    M1.append(D[i, :])

        M1 = np.array(M1)

        for i in range(M1.shape[0]):
            condition = False

            for k in range(A2.shape[0]):
                for j in range(n_criteria):
                    if M1[i, j] <= A2[k, j]:
                        condition = True

                    else:
                        condition = False
                        break

            if condition:
                for k in range(A2.shape[0]):
                    if np.equal(A2[k, :], M1[i, :]).all():
                        break

                else:
                    M2.append(M1[i, :])

        return np.array(M2) if M2 else A1


    def get_incomparable_for_preference(D, pref):
        n_alternatives, n_criteria = D.shape
        incomparable_points = np.array([])

        for i in range(n_alternatives):
            n_greater = sum([1 for j in range(n_criteria) if pref[j] < D[i, j]])
            n_unequal = sum([1 for j in range(n_criteria) if pref[j] != D[i, j]])

            if n_unequal == 0 or 0 < n_greater < n_unequal:
                if incomparable_points.shape[0] == 0:
                    incomparable_points = D[i, :].reshape((1, n_criteria))

                incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria))), axis=0)

        return incomparable_points


    def internal_contradiction(A):
        n_criteria = A.shape[1]
        incomparable_points_part = get_incomparable_points(A)
        non_dominated_point = incomparable_points_part[0, :]
        incomparable_points = non_dominated_point.reshape((1, n_criteria))

        while incomparable_points_part.shape[0] > 2:
            incomparable_points_part = get_incomparable_points(incomparable_points_part[1:, :])
            non_dominated_point = incomparable_points_part[0,:]
            incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points), axis=0)

        if incomparable_points_part.shape[0] == 2:
            incomparable_points = np.concatenate((incomparable_points_part[1, :].reshape((1, n_criteria)), incomparable_points), axis=0)

        return incomparable_points


    def external_contradiction(A, B):
        n_criteria = A.shape[1]
        new_A = []

        for i in range(A.shape[0]):
            condition = False

            for k in range(B.shape[0]):
                for j in range(1, n_criteria):
                    if A[i, j] >= B[k, j]:
                        condition = True

                    else:
                        condition = False
                        break

                if condition:
                    comparison = B[k, :]
                    break

            if condition:
                if not np.equal(A[i, :], comparison).all():
                    new_A.append(A[i, :])

        return np.array(new_A)


    def reverse_criteria(D, directions):
        for i, direction in enumerate(directions):
            if direction == "max":
                D[:, i] = -D[:, i]

        return D


    def get_incomparable_points(D):
        n_alternatives, n_criteria = D.shape
        incomparable_points = D[0,:].reshape((1, n_criteria))
        non_dominated_point = D[0,:]

        for i in range(1, n_alternatives):
            n_greater = sum([1 for j in range(n_criteria) if non_dominated_point[j] < D[i, j]])
            n_unequal = sum([1 for j in range(n_criteria) if non_dominated_point[j] != D[i, j]])

            if n_unequal == 0 or 0 < n_greater < n_unequal:
                incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria))),axis=0)

            elif n_greater == 0:
                incomparable_points_old = incomparable_points
                non_dominated_point = D[i, :]

                if incomparable_points_old.shape[0] == 1:
                    incomparable_points = non_dominated_point.reshape((1, n_criteria))

                else:
                    incomparable_points_old = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points_old), axis=0)
                    incomparable_points = get_incomparable_points(incomparable_points_old)

        return incomparable_points


    def get_best_points(D, direction, n_criteria):
        if direction == 'max':
            D = -D

        incomparable_points = get_incomparable_points(D)
        non_dominated_point = incomparable_points[0, :]
        incomparable_points_part = incomparable_points
        incomparable_points = non_dominated_point.reshape((1, n_criteria))

        while incomparable_points_part.shape[0] > 2:
            incomparable_points_part = get_incomparable_points(incomparable_points_part[1:, :])
            non_dominated_point = incomparable_points_part[0, :]
            incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points), axis=0)

        if incomparable_points_part.shape[0] == 2:
            incomparable_points = np.concatenate((incomparable_points_part[1,:].reshape((1, n_criteria)), incomparable_points), axis=0)

        return -incomparable_points if direction == "max" else incomparable_points


    def determine_sets(pref, pref_qwo, D, directions):
        D = reverse_criteria(D, directions)
        n_criteria = D.shape[1]

        A0 = get_best_points(D, 'min', n_criteria)
        A3 = get_best_points(D, 'max', n_criteria)

        A1 = get_incomparable_for_preference(D, pref)

        if A1.shape[0] == 0:
            A1 = deepcopy(A0)

        A1 = internal_contradiction(A1)
        A1 = external_contradiction(A1, A0)

        if A1.shape[0] == 0:
            A1 = deepcopy(A0)

        A2 = get_incomparable_for_preference(D, pref_qwo)

        if A2.shape[0] == 0:
            A2 = deepcopy(A3)

        A2 = internal_contradiction(A2)
        A2 = external_contradiction(A2, A1)

        if A2.shape[0] == 0:
            A2 = deepcopy(A3)

        M = get_rank(A1, A2, D)

        if M.shape[0] == 0:
            M = deepcopy(A1)

        if 'max' in directions:
            M = reverse_criteria(M, directions)

        return M
    
    
class Topsis:
    def __init__(self, daneA, daneK):
        self.daneA = daneA
        self.daneK = daneK
    
    # Funkcja TOPSIS
    def licz_topsis(self):
        # Określenie wielkości problemu
        liczba_alternatyw, ilosc_kolumn = self.daneA.shape
        ilosc_kryteriow = ilosc_kolumn - 2  # Omiń ID i placeholder

        liczba_klas, ilosc_kryteriow_k = self.daneK.shape

        # Sprawdzenie punktów alternatyw
        alternatywy_ok = np.zeros(liczba_alternatyw, dtype=int)
        for i in range(liczba_alternatyw):
            alternatywy_ok[i] = all(
                self.daneK[0, j] <= self.daneA[i, j + 2] <= self.daneK[1, j]
                for j in range(ilosc_kryteriow)
            )

        # Filtracja alternatyw
        alternatywy_filtrowane = self.daneA[alternatywy_ok == 1]
        liczba_alternatyw_temp = alternatywy_filtrowane.shape[0]

        # Uzupełnienie macierzy decyzyjnej
        macierz_decyzyjna = alternatywy_filtrowane[:, 2:]

        # Przykładowy wektor wag
        wektor_wag = np.array([0.6, 0.2, 0.2])

        # Proces skalowania
        macierz_skalowana = np.zeros_like(macierz_decyzyjna, dtype=float)
        for j in range(ilosc_kryteriow):
            macierz_skalowana[:, j] = (
                macierz_decyzyjna[:, j] * wektor_wag[j] /
                np.sqrt(np.sum(macierz_decyzyjna[:, j] ** 2))
            )

        # Wyznaczenie wektora idealnego i antyidealnego
        wektor_idealny = np.array([
            np.max(macierz_skalowana[:, 0]),
            np.min(macierz_skalowana[:, 1]),
            np.min(macierz_skalowana[:, 2])
        ])
        wektor_anty_idealny = np.array([
            np.min(macierz_skalowana[:, 0]),
            np.max(macierz_skalowana[:, 1]),
            np.max(macierz_skalowana[:, 2])
        ])

        # Wyznaczenie odległości w przestrzeni euklidesowej
        odleglosci = np.zeros((liczba_alternatyw_temp, 2))
        for i in range(liczba_alternatyw_temp):
            suma_idealny = np.sum((macierz_skalowana[i] - wektor_idealny) ** 2)
            suma_anty_idealny = np.sum((macierz_skalowana[i] - wektor_anty_idealny) ** 2)
            odleglosci[i, 0] = np.sqrt(suma_idealny)
            odleglosci[i, 1] = np.sqrt(suma_anty_idealny)

        # Uszeregowanie obiektów
        ranking = np.zeros((liczba_alternatyw_temp, 2))
        for i in range(liczba_alternatyw_temp):
            ranking[i, 0] = alternatywy_filtrowane[i, 0]  # ID alternatywy
            ranking[i, 1] = odleglosci[i, 1] / (odleglosci[i, 0] + odleglosci[i, 1])

        # Wyświetlenie wyników
        print("Macierz decyzyjna:\n", macierz_decyzyjna)
        print("Wektor wag:\n", wektor_wag)
        print("Macierz skalowana:\n", macierz_skalowana)
        print("Wektor idealny:\n", wektor_idealny)
        print("Wektor antyidealny:\n", wektor_anty_idealny)
        print("Odległości:\n", odleglosci)
        print("Ranking:\n", ranking)

        # Rysowanie wyników
        # self.rysuj_wykres(macierz_decyzyjna, self.daneK)
        return ranking

    # Funkcja do rysowania wyników
    def rysuj_wykres(self, macierz_decyzyjna):
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # Rysowanie alternatyw
        ax.scatter(macierz_decyzyjna[:, 0], macierz_decyzyjna[:, 1], macierz_decyzyjna[:, 2], 
                color='blue', label='Alternatywy', s=50)

        # Rysowanie granic kryteriów
        ax.scatter(self.daneK[0, :], self.daneK[1, :], self.daneK[1, :], 
                color='red', label='Granice kryteriów', s=100, marker='o')

        # Ustawienia wykresu
        ax.set_xlabel("Kryterium 1")
        ax.set_ylabel("Kryterium 2")
        ax.set_zlabel("Kryterium 3")
        ax.legend()
        plt.title("Wizualizacja alternatyw i kryteriów")
        plt.show()


class UtaStar:
    def cut_criterion_interval(g_min, g_max, minMax, intervals):
        g = []
        for j in range(intervals + 1):
            g_i = g_min + ((j) / intervals) * (g_max - g_min)
            if minMax == "min":
                g.insert(0, g_i)
            elif minMax == "max":
                g.append(g_i)
        return g

    def UTASTAR(Fu, Fu_ref, ranks, minMax, intervals, delta, acc):
        if Fu.shape[1] != Fu_ref.shape[1]:
            raise ValueError("The number of criteria in Fu and Fu_ref is different")

        # Dimensions
        il_pkt, il_kryt = Fu_ref.shape

        w = []
        for i in range(il_kryt):
            w_i = np.zeros((il_pkt, intervals[i]))
            g_i = cut_criterion_interval(min(Fu_ref[:, i]), max(Fu_ref[:, i]), minMax[i], intervals[i])
            
            for k in range(il_pkt):
                if Fu_ref[k, i] not in g_i:
                    lower_b, upper_b = 0, 0
                    for j in range(len(g_i)):
                        if Fu_ref[k, i] > g_i[j]:
                            if minMax[i] == "min":
                                lower_b, upper_b = j, j - 1
                            elif minMax[i] == "max":
                                lower_b, upper_b = j, j + 1
                    
                    for j in range(intervals[i] - 1):
                        w_i[k, j] = 1
                    w_i[k, intervals[i] - 1] = (Fu_ref[k, i] - g_i[upper_b]) / (g_i[lower_b] - g_i[upper_b])
                else:
                    index = g_i.index(Fu_ref[k, i])
                    if index != 0:
                        for j in range(index):
                            w_i[k, j] = 1

            w.append(w_i)
        
        w = np.hstack(w)

        A, b, Aeq, beq = [], [], [], []
        for i in range(il_pkt - 1):
            if ranks[i] != ranks[i + 1]:
                A_i = w[i] - w[i + 1]
                A.append(A_i)
                b.append(delta)
            else:
                Aeq_i = w[i] - w[i + 1]
                Aeq.append(Aeq_i)
                beq.append(0)

        Aeq.append(np.ones(w.shape[1]))
        beq.append(1)
        A, b = -np.array(A), -np.array(b)
        Aeq, beq = np.array(Aeq), np.array(beq)
        lb = np.zeros(w.shape[1])
        ub = np.full(w.shape[1], np.inf)

        x = []
        tmp_start = 0
        for i in range(il_kryt):
            z = np.zeros(w.shape[1])
            z[tmp_start:tmp_start + intervals[i]] = -1
            tmp_start += intervals[i]

            # Correct bounds
            bounds = [(lb[j], ub[j]) for j in range(len(lb))]

            result = linprog(z, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")
            
            if result.success:
                x.append(result.x)
            else:
                raise ValueError(f"Linear programming failed: {result.message}")


        x_avg = np.mean(x, axis=0)

        u_g = []
        tmp = 0
        for i in range(il_kryt):
            # plt.figure()
            
            g_i = cut_criterion_interval(min(Fu_ref[:, i]), max(Fu_ref[:, i]), minMax[i], intervals[i])
            u_g_i_j = [0]
            for j in range(1, len(g_i)):
                u_g_i_j.append(u_g_i_j[j - 1] + x_avg[tmp])
                tmp += 1

            x1 = np.linspace(g_i[0], g_i[-1], acc)
            y1 = np.interp(x1, g_i, u_g_i_j)
            # plt.plot(g_i, u_g_i_j, '*', label='Points')
            # plt.plot(x1, y1, label='Interpolated')
            # plt.xlim(min(g_i), max(g_i))
            # plt.ylim(0, 1)
            # plt.title(f"Partial utility function for criterion {i + 1}")
            # plt.legend()
            # plt.show()
            u_g.append((x1, y1))

        U = []
        for i in range(Fu.shape[0]):
            temp = 0
            for j in range(il_kryt):
                x_vals, y_vals = u_g[j]
                temp += np.interp(Fu[i, j], x_vals, y_vals)
            U.append(temp)

        ranking = np.argsort(-np.array(U)) + 1
        return U, u_g, ranking