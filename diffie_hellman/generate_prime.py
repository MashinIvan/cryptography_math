import random
import math
import matplotlib.pyplot as plt
import typing


def generate_first_primes(limit: int = 100) -> typing.Iterable[int]:
    found = 0
    number = 2

    while not found >= limit:
        isprime = True

        for x in range(2, int(math.sqrt(number) + 1)):
            if number % x == 0: 
                isprime = False
                break

        if isprime:
            found += 1
            yield number

        number += 1


def get_low_level_prime(n_bits: int = 1024, n_first_primes: int = 100) -> int:
    first_primes = list(generate_first_primes(n_first_primes))

    def generate_n_bit_random(n_bits: int) -> int:
        number_order = math.ceil(math.log(2**n_bits, 10))
        number = random.randint(10**(number_order - 1), 10**number_order)
        if number % 2 == 0:
            number +=1
        return number

    def is_low_level_prime(number: int) -> bool:
        for prime in first_primes:
            if number % prime == 0:
                return False
        return True

    candidate = generate_n_bit_random(n_bits)
    while not is_low_level_prime(candidate):
        candidate = generate_n_bit_random(n_bits)
    
    return candidate


def is_rabin_miller_prime(number: int, iterations: int = 10) -> bool:
    even_component = number - 1
    k = 1

    helper = even_component // 2
    while helper % 2 == 0:
        helper //= 2
        k += 1

    m = even_component // 2**k

    for i in range(iterations):
        a = random.randint(2, number - 1)
        b = pow(a, m, number)
        if b == 1 or b == number - 1:
            continue
        else:
            if k < 1:
                return False
            for r in range(1, k + 1):
                b = pow(b, 2, number)
                if b == number - 1:
                    break
                elif b == 1:
                    return False

    return True


def generate_prime(n_bits: int = 1024,
                   n_first_primes: int = 100,
                   n_rabin_miller_iterations: int = 20) -> int:
    candidate = get_low_level_prime(n_bits, n_first_primes)
    while not is_rabin_miller_prime(candidate, n_rabin_miller_iterations):
        candidate = get_low_level_prime(n_bits, n_first_primes)

    return candidate
