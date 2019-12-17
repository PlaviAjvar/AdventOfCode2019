#include <vector>
#include <chrono>
#include <string>
#include <iostream>
#include <fstream>
using namespace std::chrono;

/*

WARNING

Depending on PC, may take a while. Runs in around 3 minutes on mine.

Time complexity is O(iter * nlog(n))

*/

int sum_c(int low_idx, int high_idx, std::vector <int>& cum_sum) {
    if(low_idx >= cum_sum.size()) {
        low_idx = cum_sum.size() - 1;
    }
    if(high_idx >= cum_sum.size()) {
        high_idx = cum_sum.size() - 1;
    }
    return cum_sum[high_idx] - cum_sum[low_idx];
}

short apply_pattern(std::vector <int>& cum_sum, int i, int pattern_len, int array_size) {
    int new_value = 0;
    for(int j = 0; j < cum_sum.size(); j += pattern_len) {
        new_value += sum_c(j + i - 1, j + 2*i - 1, cum_sum);
        new_value -= sum_c(j + 3*i - 1, j + 4*i - 1, cum_sum);
    }

    if(new_value > 0) {
        return new_value % 10;
    }
    return (-new_value) % 10;
}


std::string solve(std::vector <short>& arr, int offset) {
    short num_iter = 100;

    for(short iter = 0; iter < num_iter; ++iter) {
        std::vector <int> cum_sum(arr.size());
        for(int i = 1; i < arr.size(); ++i) {
            cum_sum[i] = cum_sum[i-1] + arr[i];
        }
        for(int i = 1; i < arr.size(); ++i) {
            int pattern_len = 4*i;
            arr[i] = apply_pattern(cum_sum, i, pattern_len, arr.size());
        }
        std::cout << "Iteration " << iter << " clear." << std::endl;
    }

    std::string str_sol = "";
    for(int i = offset; i < offset + 8; ++i) {
        str_sol += (char)('0' + arr[i]);
    }
    return str_sol;
}



int main() {
    auto start = high_resolution_clock::now();

    std::ifstream in_stream("input.txt");
    std::string input;
    in_stream >> input;
    std::vector <short> arr;

    int offset = 1;
    /*

    IMPORTANT

    Set solve_first to false for first part of problem.
    Set solve_first to true for second part of problem.

    */
    bool solve_first = false;

    if(solve_first) {
        arr = std::vector <short>(input.size()+1);
        for(int i = 1; i < arr.size(); ++i) {
            arr[i] = input[i-1] - '0';
        }
    }
    else {
        arr = std::vector <short>(input.size() * 10000 + 1);
        for(int i = 1; i < arr.size(); ++i) {
            arr[i] = input[(i-1) % input.size()] - '0';
        }

        offset = 1;
        int pow = 1;
        for(int i = 7; i >= 1; --i) {
            offset += arr[i] * pow;
            pow *= 10;
        }
    }

    std::cout << std::endl << "The solution is " << solve(arr, offset) << std::endl;

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    std::cout << std::endl << "Time taken to execute program is " << duration.count() / 1e6 << " seconds." << std::endl;
    return 0;
}
