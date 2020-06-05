from kivy.app import App
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import timeit
import random
import math
import time

Config.set('kivy', 'keyboard_mode', 'systemanddock')


def is_square(x):
    return (int(x ** 0.5)) ** 2 == x


def prime_number(n):
    a = 2
    while n % a != 0:
        a += 1
    return a == n


def ferma_factorize(n):

    if prime_number(n):
        return 1, n, 'This is a prime number'

    if n <= 1:
        return None, None, 'Error: number must be bigger 0'

    if n % 2 == 0:
        return None, None, 'Error: number must be odd'

    if is_square(n):
        return int(n ** 0.5), int(n ** 0.5), 'Operation success!'

    x = int(n ** 0.5) + 1

    while not is_square(x * x - n):
        x += 1

    y = int((x * x - n) ** 0.5)
    a, b = x - y, x + y
    return a, b, 'Operation success!'


def predict(point, weights, P):
    s = 0
    for i in range(len(point)):
        s += weights[i] * point[i]
    return 1 if s > P else 0


def perceptron(speed_of_learning, deadline, iterations):
    P = 4
    data = [(0, 6), (1, 5), (3, 3), (2, 4)]
    n = len(data[0])
    weights = [0.001, -0.004]
    outputs = [0, 0, 0, 1]
    start_time = timeit.default_timer()
    counter = 0
    for _ in range(iterations):
        total_error = 0

        for i in range(len(outputs)):
            prediction = predict(data[i], weights, P)
            err = outputs[i] - prediction
            total_error += err

            for j in range(n):
                delta = speed_of_learning * data[i][j] * err
                weights[j] += delta
        counter += 1
        if total_error == 0 or timeit.default_timer() - start_time > deadline:
            break
    return weights[0], weights[1], counter


def roots_genetic_get(a, b, c, d, y, mutate_chance=0.1):
    num_pop = 4
    population = [[random.randint(0, int(y / 4)) for i in range(4)] for j in range(num_pop)]
    chance = mutate_chance
    counter = 0
    roots = [i[0] * a + i[1] * b + i[2] * c + i[3] * d for i in population]
    while y not in roots:
        deltas = [1 / abs(i - y) for i in roots]
        chances = [i / sum(deltas) for i in deltas]

        for i in range(int(num_pop / 2)):
            temp = random.uniform(0, 1)
            if temp < chances[0]:
                param1 = population[0]
            elif temp < chances[0] + chances[1]:
                param1 = population[1]
            elif temp < chances[0] + chances[1] + chances[2]:
                param1 = population[2]
            else:
                param1 = population[3]
            param2 = param1
            while param2 == param1:
                temp2 = random.uniform(0, 1)
                if temp2 < chances[0]:
                    param2 = population[0]
                elif temp2 < chances[0] + chances[1]:
                    param2 = population[1]
                elif temp2 < chances[0] + chances[1] + chances[2]:
                    param2 = population[2]
                else:
                    param2 = population[3]
            gene = random.randint(0, 3)
            param1[gene], param2[gene] = param2[gene], param1[gene]
            for j in range(4):
                temp = random.uniform(0, 1)
                if temp < chance:
                    param1[j] += random.choice([-1, 1])
                temp = random.uniform(0, 1)
                if temp < chance:
                    param2[j] += random.choice([-1, 1])
            population[2 * i] = param1
            population[2 * i + 1] = param2
        roots = [j[0] * a + j[1] * b + j[2] * c + j[3] * d for j in population]
        counter += 1
    return population[roots.index(y)], counter


class Container(TabbedPanel):

    def first_calculate(self):

        start_time = time.time()

        try:
            inp_number = int(self.text_input.text)
            a, b, c = ferma_factorize(inp_number)
            self.first_number.text, self.second_number.text, self.state_factorization.text = str(a), str(b), c
        except:
            self.state_factorization.text = 'Incorrect input'

        end_time = time.time()
        total_time = end_time - start_time
        popup = Popup(title='Execution time',
                      content=Label(text=str(total_time)),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def second_calculate(self):

        try:
            speed_of_learning, deadline, number_of_iterations = float(self.speed_of_learning.text), int(self.deadline.text), int(
                self.number_of_iterations.text)
        except:
            speed_of_learning, deadline, number_of_iterations = 0.001, 5, 10000

        first, second, iters_used = perceptron(speed_of_learning, deadline, number_of_iterations)
        self.w1.text, self.w2.text, self.used_ires_num.text = str(first), str(second), str(iters_used)

    def third_calculate(self):

        try:
            a_value, b_value, c_value, d_value, y_value = int(self.a_value.text), int(self.b_value.text), int(self.c_value.text),\
                                                int(self.d_value.text), int(self.y_value.text)
        except:
            a_value, b_value, c_value, d_value, y_value = 1, 2, 3, 4, 16

        roots = roots_genetic_get(a_value, b_value, c_value, d_value, y_value)[0]
        self.roots.text = str(roots)

        iterations = []
        experiments = 10
        mutate_chances = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        for i in mutate_chances:
            steps = 0
            for j in range(experiments):
                steps += roots_genetic_get(a_value, b_value, c_value, d_value, y_value, i)[1]
            iterations.append(math.ceil(steps / experiments))
        ind = iterations.index(min(iterations))
        best_chance = mutate_chances[ind]
        self.mutate_chance.text = str(best_chance)


class MyApp(App):

    def build(self):

        return Container()


if __name__ == '__main__':

    MyApp().run()
