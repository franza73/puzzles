#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <cstdint>

int main() {
    const double d_x = 1e-8;
    const double X = 102.0;
    const double FD_L1 = 36.0 / 51.0;
    const double FD_L2 = 38.0 / 51.0;
    const double eps = d_x / 200.0;

    int64_t one_dx = static_cast<int64_t>(1.0 / d_x);         // size of 1 window
    int64_t total_steps = static_cast<int64_t>(X / d_x);      // total number of steps

    // circular buffer of size one_dx
    std::vector<double> buffer(one_dx, 0.0);

    double x = 0.0;
    int64_t k = 0;
    double SM = 0.0;

    std::cout << std::setprecision(10) << std::fixed;

    // First phase: x in [0, 1) → M = 0
    while (k < one_dx) {
        x += d_x;
        ++k;
    }

    // Second phase: x in [1, X)
    while (k < total_steps) {
        // Remove the oldest value and add the new one to maintain rolling sum
        int64_t idx = k % one_dx;

        SM -= buffer[idx];  // Remove outgoing value from window
        double new_value = 1.0 + (2.0 / (x - 1.0 + eps)) * SM;
        SM += new_value;    // Add new value to window

        buffer[idx] = new_value;

        double FD = new_value / x;

        if (x > 2.0) {
            if (std::abs(FD - FD_L1) < eps) {
                std::cout << "x = " << x
                          << ", FD = " << FD
                          << " (close to FD_L1)"
                          << ", abs diff = " << std::scientific << std::setprecision(2)
                          << std::abs(FD - FD_L1) << std::fixed << "\n";
            }
            if (std::abs(FD - FD_L2) < eps) {
                std::cout << "x = " << x
                          << ", FD = " << FD
                          << " (close to FD_L2)"
                          << ", abs diff = " << std::scientific << std::setprecision(2)
                          << std::abs(FD - FD_L2) << std::fixed << "\n";
            }
        }

        x += d_x;
        ++k;
    }

    return 0;
}
