class Solution {
    public int solution(int n) {
        int j =0;
        int factorial = 1;

        for (int i = 1; i <= n; i++) {

            factorial *= i;
            if(factorial > n){
                break;
            }
            j++;
            }
         return j;
    }
}