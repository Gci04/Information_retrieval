#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

void show(vector<float> &w) {
	cout << "Weights for {1, a, b, b*a, b/a, a/b, b*b, a*a} = ";
	for (auto wi: w) cout << wi << ", ";
	cout << endl;
}

void show_eq(vector<float> &w) {
	vector<string> params = { " + ", "*a + ", "*b + ", "*a*b + ", "*b/a + ", "*a/b + ", "*b2 + ", "*a2" };
	for (int i = 0; i < params.size(); i++) {
		cout << w[i] << params[i];
	}
	cout << endl;
}

void show_array(vector<float> &w) {
	cout << "[";
	for (int i = 0; i < w.size() - 1; i++) {
		cout << w[i] << ",";
	}
	cout << w[w.size()-1] << "]," << endl;
}


float feature(vector<float> &x, int idx) {
	switch (idx) {
		case 0: return 1.0;
		case 1: return x[0];
		case 2: return x[1];
		case 3: return x[1] * x[0];
		case 4: return x[1] / x[0];
		case 5: return x[0] / x[1];
		case 6: return x[1] * x[1];
		case 7: return x[0] * x[0];
	}
	return 0;
}

float fwd(vector<float> w, vector<float> sample) {
	float res = 0;
	for (int i = 0; i < w.size(); i++) res += w[i] * feature(sample, i);
	return res;
}

inline float sign(float x) { return x > 0 ? 1.0 : (x < 0 ? -1.0 : 0 ); }

void train(vector<float> &w, vector<vector<float>> data) {
	float rate = 0.0003;
	
	for (vector<float> sample : data) {
		// compute error
		float result = fwd(w, sample);
		float err = (sample[2] - result);

		for (int i = 0; i < w.size(); i++) {
			float dw = rate * err * feature(sample, i);
			w[i] = w[i] + dw;
		}
	}	
}

int main() {
	vector<float> weights = { -0.1, 0.2, -0.05, -0.0003, 0.4, 0.1, 0.8, 0.5 };
	// show(weights);
	vector<vector<float>> data = {
		{2, 3, 1.5},
		{4, 8, 2},
		{3, 2, 0.666666667},
		{2, 1, 0.5},
		{1, 8, 8},
		{1, 9, 9},
		{2, 2, 1},
		{4, 1, 0.25},
	};
	
	for (int i = 0; i < 10000000; i++) {
		train(weights, data);
		if (i % 1000 == 0) show_array(weights);
		// show(weights);
	}
	/*
	show(weights);
	for (auto s : data) cout << s[0] <<  "*x = "<<  s[1] << "; x = " << fwd(weights, s) << endl;
	cout << -200 <<  "*x = "<<  300 << "; x = " << fwd(weights, {-200, 300}) << endl;
	*/
	return 0;
}
