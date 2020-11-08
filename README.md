# Prague_FeistelCipher

You can run the code online without an IDE with link:

https://colab.research.google.com/drive/1tK1uiKzG2tn_2-ElrUB-0qs-MTWHNF_w?usp=sharing


Output:
Task 1

Encryption:
x: [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1]
0xd80b1a63


Task 2

Decryption:
u: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
0x80000000


Task 3
x from Encryption function: 0xd80b1a63
x from the equation Ak+Bu: 0xd80b1a63
Linearity of the system is proven


Task 4
A(k_guess = 0x4cfe0bf0) + Bu = x ->True
A(k_guess = 0xa5faf47e) + Bu = x ->True
A(k_guess = 0x6882322e) + Bu = x ->True
A(k_guess = 0x97c53992) + Bu = x ->True
A(k_guess = 0x4be77048) + Bu = x ->True




Task 5

Encryption:
x: [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1]
0x2e823d53


Task 7

Encryption:
x: [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1]
0x6a9b

Decryption:
u: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
0x0


Task 8
For u = 0x7929
For x = 0xd475
k' = [1 1 0 1 1 1 0 1 1 0 0 1 0 0 0 0]
k'' = [1 1 1 0 0 1 0 1 0 1 0 0 0 0 1 1]
For u = 0x95d3
For x = 0x2609
k' = [1 1 0 0 0 1 0 1 1 0 0 0 1 1 0 0]
k'' = [1 1 0 1 0 0 0 1 1 0 1 1 1 1 0 0]
For u = 0x8cba
For x = 0xb63
k' = [1 1 0 0 1 0 1 1 1 1 0 1 0 1 0 1]
k'' = [1 0 1 1 1 1 1 1 0 1 1 1 1 0 0 0]
For u = 0x8cba
For x = 0xb63
k' = [1 0 0 0 1 0 0 0 1 1 1 0 0 0 0 0]
k'' = [1 1 1 1 0 0 0 1 0 1 0 0 0 1 0 1]
For u = 0x8cba
For x = 0xb63
k' = [1 1 1 0 1 0 0 1 0 1 1 1 0 1 1 0]
k'' = [1 1 0 1 1 0 0 0 0 0 1 0 1 1 0 1]
Elapsed time in seconds: 157.46281671524048
