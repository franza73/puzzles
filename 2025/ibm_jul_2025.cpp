/*
d_x = 1e-8
x = 6.0507200116, FD = 0.7058823529 (close to FD_L1)
x = 100.9574657912, FD = 0.7450980392 (close to FD_L2), abs diff = 8.33e-15
./ibm_jul_2025  548.08s user 255.11s system 81% cpu 16:21.35 total

*/


#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <cstdint>

int main() {
    const double d_x = 5e-9;
    const double X = 102.0;
    const double FD_L1 = 36.0 / 51.0;
    const double FD_L2 = 38.0 / 51.0;
    const double eps = d_x / 200.0;
    const double eps2 = 1.0e-13;

    std::vector<double> M;
    double x = 0.0;

    int64_t one_dx = static_cast<int64_t>(1.0 / d_x);
    int64_t total_steps = static_cast<int64_t>(X / d_x);
    int64_t k = 0;
    double SM = 0.0;

    // Initialize M with zeros for x in [0, 1)
    while (k < one_dx) {
        M.push_back(0.0);
        x += d_x;
        ++k;
    }

    // Compute M for x ≥ 1
    while (k < total_steps) {
        SM += d_x * M[k - one_dx];

        double term = 1.0 + (2.0 / (x - 1.0)) * SM;
        M.push_back(term);

        double FD = term / x;

        if (x > 2.0) {
            if (std::abs(FD - FD_L1) < eps) {
                std::cout << std::fixed << std::setprecision(10)
                          << "x = " << x << ", FD = " << FD << " (close to FD_L1)\n";
            }
            if (std::abs(FD - FD_L2) < eps2) {
                std::cout << std::fixed << std::setprecision(10)
                          << "x = " << x
                          << ", FD = " << FD
                          << " (close to FD_L2)"
                          << ", abs diff = " << std::scientific << std::setprecision(2)
                          << std::abs(FD - FD_L2)
                          << "\n";
            }
        }

        x += d_x;
        ++k;
    }

    return 0;
}

