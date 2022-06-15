#include <iostream>

int main()
{
    int tests;
    std :: cin >> tests;
    for (int _=0;_<tests;_++)
    {
        int n;
        std::cin >>n;
        int sum=0;
        int temp=0;
        for (int i=0;i<n;i++)
        {
            std:: cin>>temp;
            sum+=temp;
        }
        if (sum%2==0)
        {
            std:: cout <<"YES";
        }
        else
        {
            std:: cout <<"NO";
        }
    }
}