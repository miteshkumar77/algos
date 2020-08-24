#include "range_sum.cpp" 
#include <bits/stdc++.h>




int main() {


    std::vector<int> t1{1, 2, 3, 4, 5, 6, 7, 8, 9}; 
    range_sum rs1(t1); 

    assert(rs1.sumRange(0, 8) == 45); 
    assert(rs1.sumRange(0, 7) == (45 - 9)); 
    rs1.update(5, 5); 
    assert(rs1.sumRange(0, 8) == 44); 
    std::cout << "All test cases passed." << std::endl; 
    return 0; 
}