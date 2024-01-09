#include <iostream>
#include <unordered_set>

using namespace	std;

int 
main()
{
	for (int N = 4310500; N <= 4313800; N++) {
		unordered_set < int >H;
		int		y0 = N;
		int		N2 = N * N;
		int		N1_2 = (N + 1) * (N + 1);
		for (int x = 0; x < N + 1; x++) {
			for (int y = y0; y >= x; y--) {
				int		v = x * x + x * y + y * y;
				if (N2 < v && v < N1_2) {
					H.insert(v);
					y0 = y;
				} else if (v <= N2) {
					break;
				}
			}
		}
		if (H.size() == 1000000)
			cout << N << " " << H.size() << "\a" << endl;
	}
}
