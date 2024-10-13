#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

using namespace std;

vector<int> galtonbox(int n, int N) {
	vector<int> v(n + 1, 0);
	for (int turn = 0; turn < N; ++turn) {
		int i = 0;
		for (int j = 0; j < n; ++j) {
			if (rand()%2) ++i;
		}
		++v[i];
	}
	return v;
}

double normal_pdf(double x, double m, double s) {
    static const double inv_sqrt_2pi = 0.3989422804014327;
    double a = (x - m) / s;
    return inv_sqrt_2pi / s * exp(-0.5 * a * a);
}

vector<double> normal_distr(int n) {
	vector<double> v(n + 1);
	for (int i = 0; i <= n; ++i) {
		v[i] = normal_pdf(i, double(n)/2, sqrt(double(n)/4));
	}
	return v;
}

// v1.size() = v2.size() = n
double mse(const vector<double>& v1, const vector<double>& v2) {
	int n = v1.size();
	double mse = 0;
	for (int i = 0; i <= n; ++i)
		mse += (v1[i] - v2[i])*(v1[i] - v2[i]);
	
	return mse/double(n);
}

int main() {
	
	srand(time(0));
	cout.setf(ios::fixed);
	cout.precision(5);
	
	int n, N;
	cin >> n >> N;
	
	vector<int> gb = galtonbox(n, N);
	vector<double> binomial(n + 1);
	for (int i = 0; i <= n; ++i) binomial[i] = gb[i]/double(N);
	vector<double> normal = normal_distr(n);

	cout << "Experiment result: binomial distribution" << endl;
	for (int i = 0; i <= n; ++i)
		cout << i << ' ' << binomial[i] << endl;

	cout << "Normal distribution" << endl;
	for (int i = 0; i <= n; ++i)
		cout << i << ' ' << normal[i] << endl;

	cout << "Mean quadratic error" << endl;
	cout << mse(normal, binomial) << endl;
}