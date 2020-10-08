#ifndef flag
#define flag
#include <vector>
#include <string>
#include <stack>
#include <iostream>
using namespace std;
class Fake_db{      //stand for fake dynamic bitset
    vector<wchar_t> bs;
    wstring bin;
    wstring calc(int s , int n);
public:
    Fake_db(int size , int number);
    void show();
    wchar_t at(int index){ return bs.at(index); }
    wstring get_string() { return bin ; }
};
void Fake_db::show(){
    wcout << L'[';
    for ( auto i : bs){
        wcout << i ;
    }
    wcout << L']' << endl;
}
wstring Fake_db::calc(int s , int  n){
    wstring result ;
    stack<wchar_t> st;
    while(n){
        st.push( static_cast<wchar_t>((n%2) + '0'));
        n /= 2;
    }
    while( st.size()  < s){
        st.push(L'0');
    }
    while(!st.empty()){
        result.push_back(st.top());
        st.pop();        
    }
    return result;
}
Fake_db::Fake_db(int size , int number){
    bin = calc(size , number);
    for(auto i : bin){
        bs.push_back(i);
    }
}

#endif