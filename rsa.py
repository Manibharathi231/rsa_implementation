import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def xgcd(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return a, old_x, old_y

def mod_pow(base, exponent, mod):
    result = 1
    base %= mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent //= 2
        base = (base * base) % mod
    return result

def choose_keys():
    with open('primes-to-100k.txt', 'r') as f:
        primes = list(map(int, f.read().splitlines()))
    filtered_primes = [p for p in primes if p >= 17]
    while True:
        p = random.choice(filtered_primes)
        q = random.choice(filtered_primes)
        if p != q:
            n = p * q
            if n >= 256:
                break
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break
    _, d, _ = xgcd(e, phi)
    if d < 0:
        d += phi
    return p, q, n, phi, e, d

def encrypt_char(char, e, n):
    return mod_pow(ord(char), e, n)

def decrypt_char(cipher, d, n):
    return chr(mod_pow(cipher, d, n))

def main():
    print("Generating RSA keys...")
    p, q, n, phi, e, d = choose_keys()
    print("\nRSA Key Details:")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"phi = {phi}")
    print(f"e = {e}")
    print(f"d = {d}\n")

    message = input("Enter the message to encrypt: ").strip()
    if not message:
        print("No message entered. Exiting.")
        return

    encrypted = [encrypt_char(c, e, n) for c in message]
    print("\nEncrypted message (list of integers):")
    print(encrypted)

    decrypt_now = input("\nDo you want to decrypt the message? (y/n): ").lower()
    if decrypt_now == 'y':
        decrypted = ''.join([decrypt_char(val, d, n) for val in encrypted])
        print("\nDecrypted message:")
        print(decrypted)
    else:
        print("Decryption skipped.")

if __name__ == "__main__":
    main()
