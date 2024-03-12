#include <vector>
#include <iostream>
#include <cmath>
using namespace std;

int count_primes(long n) {
    const int S = 10000000;
    cout << S << endl;
    vector<long> primes;
    long nsqrt = sqrt(n);
    vector<char> is_prime(nsqrt + 2, true);
    for (long i = 2; i <= nsqrt; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (long j = i * i; j <= nsqrt; j += i)
                is_prime[j] = false;
        }
    }

    int result = 0;
    vector<char> block(S);
    for (long k = 0; k * S <= n; k++) {
        fill(block.begin(), block.end(), true);
        long start = k * S;
        for (long p : primes) {
            long start_idx = (start + p - 1) / p;
            long j = max(start_idx, p) * p - start;
            for (; j < S; j += p)
                block[j] = false;
        }
        if (k == 0)
            block[0] = block[1] = false;
        for (long i = 0; i < S && start + i <= n; i++) {
            if (block[i])
                result++;
        }
    }
    cout << "\a";
    return result;
}

int main(void) {
    count_primes(100000000000);
    return 0;
}
