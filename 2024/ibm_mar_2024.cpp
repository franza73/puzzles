#include <vector>
#include <iostream>
#include <cmath>
using namespace std;

vector<bool> segmentedSieve(long long L, long long R) {
    // generate all primes up to sqrt(R)
    long long lim = sqrt(R);
    vector<char> mark(lim + 1, false);
    vector<long long> primes;
    for (long long i = 2; i <= lim; ++i) {
        if (!mark[i]) {
            primes.emplace_back(i);
            for (long long j = i * i; j <= lim; j += i)
                mark[j] = true;
        }
    }

    vector<bool> isPrime(R - L + 1, true);
    for (long long i : primes)
        for (long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}

int main() {
    long long MAX = 60000000000;
    vector<bool> isprime = segmentedSieve(0, MAX);
    long long N = 1;
    int i;
    long long a_i;
    long long a_0;
    for (a_0 = 50000000000; a_0 < MAX; a_0++) {
        if (isprime[a_0])
            continue;
        i = 1;
        a_i = a_0;
        while (a_i < MAX) {
            a_i = a_i + i;
            if (a_i < MAX && isprime[a_i])
                break;
            i += 1;
        }
        if (i >= N) {
            cout << a_0 << " " << i << endl;
            N = i;
        }
    }
    cout << "final a_0 = " << a_0 << endl;
    return 0;
}
