#include <iostream> 
#include <io.h> 
#include <fcntl.h> 
#include <string>
#include <utility>
#include <vector>
#include <stack>
#include <set>
#include <cmath>
#include "Fake_db.hpp"
using namespace std;
wchar_t characters [8] = { L'¬' , L'∧' , L'∨',L'→',L'↔',L'(',L')',L'$'};
vector<wchar_t> se;
vector<wstring> conjunctive;
vector<wstring> disjunctive;
pair<wchar_t , int> cs [8] = {
make_pair(characters[0] , 0) ,
make_pair(characters[1] , 1) ,
make_pair(characters[2] , 2) , 
make_pair(characters[3] , 3) , 
make_pair(characters[4] , 4) , 
make_pair(characters[5] , 5) ,
make_pair(characters[6] , 6) ,
make_pair(characters[7] , 7) ,
};
char precedence [8][8] = {
{'<','>','>','>','>','<','>','>'},
{'<','<','>','>','>','<','>','>'},
{'<','<','<','>','>','<','>','>'},
{'<','<','<','<','>','<','>','>'},
{'<','<','<','<','<','<','>','>'},
{'<','<','<','<','<','<','=',' '},
{' ',' ',' ',' ',' ',' ',' ',' '},
{'<','<','<','<','<','<',' ','='}
};
bool isoperator(wchar_t ch){
    bool exist  = false;
 for (int j = 0 ; j < 8 ; ++j){
            if(ch == characters[j]){
                exist = true;
                break;
            }
        }
        return exist;
}
int get_var_number(const wstring & expr){
    for(auto i : expr){
        bool exist = isoperator(i);
        if ( !exist ){
        bool already  = false;
        for (auto k : se){
            if ( i == k){
                already = true ;
                break;
            }
        }
        if (!already)
        se.push_back(i);   
        }
    }
    return se.size();
}
#include <regex>
//maybe it's a bad idea to use c++ regex here , for its bad performence , but now let's move on and optimize it later
wstring replace ( wchar_t target , wchar_t rep , wstring expr ){
    wstring whole = expr;
    wstring key = wstring(1,target);
    wstring repl = wstring(1,rep);
    wstring res = std::regex_replace(whole, std::wregex(key),  repl);
    return res;
}
int get(wchar_t c){
    for ( int i = 0 ; i < 8 ; ++i){
        if (c == cs[i].first){
            return cs[i].second;
        }
    }
    wcout << "index not found" << endl;
    return 0;   
}
bool eval(bool obj1 , wchar_t op , bool obj2){
    switch(op){
        case L'∧':{
            return obj1 && obj2;
        }
        case L'∨':{
            return obj1 || obj2;
        } 
        case L'→':{
            if ( obj1 && !obj2){
                return false;
            }
            else{
                return true;
            }
        }
        case L'↔':{
            return !(obj1 ^ obj2);
        }
        default:{
            wcout << "oper error!" << endl;
            return false;
        }
    }
}

wchar_t process_mid(const wstring & midexpr){
    stack<wchar_t> oper ;
    stack<bool> oand ;
    wstring pr = midexpr + L"$";
    auto bg = pr.begin();
    auto ed = pr.end();
    oper.push(L'$');
    while(bg != ed && !oper.empty()){
        auto c = *bg;
        if (!isoperator(c)){
            bool sign = (c == L'1') ? true : false;
            oand.push(sign);
            bg++;
        }
        else{
        wchar_t priority = precedence[get(oper.top())][get(c)];
        switch(priority){
            case L'<':{
                oper.push(c);
                bg++;
                break;
            }
            case L'>':{
                wchar_t op = oper.top();
                oper.pop();
                if(op == L'¬'){
                    bool obj = oand.top();
                    oand.pop();
                    oand.push(!obj);
                }
                else {
                    bool op2 = oand.top();
                    oand.pop();
                    bool op1 = oand.top();
                    oand.pop();
                    oand.push(eval(op1 , op , op2));
                }
                break;    
            }
            case L'=':{
                oper.pop();
                bg++;
            }
        }
        }
    }
    if ( oper.empty() && oand.size() == 1 ){
        return oand.top();
   }
   else
   {
       wcout << "invalid expression" << endl;
       exit(999);
   }
}

//make unit clause
wstring make_con(const wstring & vs ){
    wstring result = L"(";
    for(int i = 0 ; i<vs.size() ; ++i){
        bool sign = (vs[i] == L'1') ? true : false;
        wstring cat = wstring(1 , se[i]);
        if(sign){
            result += cat ;
        }
        else
        {
            result += (L"¬" + cat );
        }
        if ( i != vs.size() - 1){
            result += L"∧";
        }
    }
    return result+=L")";
}
wstring make_dis(const wstring & vs){
wstring result = L"(";
    for(int i = 0 ; i<vs.size() ; ++i){
        bool sign = (vs[i] == L'1') ? true : false;
        wstring cat = wstring(1 , se[i]);
        if(!sign){
            result += cat ;
        }
        else
        {
            result += (L"¬" + cat);
        }
        if ( i != vs.size() - 1){
            result += L"∨";
        }
    }
    return result += L")";
}

int main() 
{
    _setmode(_fileno(stdout), _O_WTEXT);
    _setmode(_fileno(stdin), _O_WTEXT);

    wcout << "Enter a valid logical expression : "<< endl;
    wstring expr ;
    wcin >> expr;
    
    int varNumber = get_var_number(expr);
    int limit = pow(2 , varNumber);


    for (auto var : se){
        wcout << "\t" << var ;
    }
    wcout << "\t" << expr << endl;
    wcout << wstring( (se.size() + 1) * 12, L'-') << endl;


    for ( int k = 0 ; k < limit ; ++k){
        Fake_db db(varNumber , k);
        wstring mid_expr = expr;
        for ( int cot = 0 ; cot < se.size() ; ++cot){
        mid_expr = replace(se[cot] , db.at(cot) , mid_expr);
        }
        bool tvalue = process_mid(mid_expr);

        for ( auto c : db.get_string()){
            wcout << "\t" << c ;
        }
        wcout << "\t" << tvalue << endl;
        wcout << wstring( (se.size() + 1) * 12, L'-') << endl;

        wstring values = db.get_string();
        
        if (tvalue){
            conjunctive.push_back(make_con(values));
        }
        else
        {
           disjunctive.push_back(make_dis(values)); 
        }
    } 

    wstring prime_conjunctive ;
    wstring prime_disjunctive ;

    for ( int i = 0 ; i < conjunctive.size() ; ++i){
        prime_conjunctive += conjunctive[i];
        if ( i != conjunctive.size() -1 ){
            prime_conjunctive += L"∨";
        }
    }

    for (int i = 0 ; i < disjunctive.size() ; ++i){
        prime_disjunctive += disjunctive[i];
        if ( i != disjunctive.size() -1 ){
            prime_disjunctive += L"∧";
        }
    }

    wcout << "The Conjunctive normal form is : " << prime_conjunctive << endl;
    wcout << "The Disjunctive normal form is : " << prime_disjunctive << endl;

    return 0;

} 

