
import java.util.ArrayList;

class Solution {
    public int solution(int n) {
        int answer = 0;

        for (int i = 0; i<=n; i++) {
            int div = 0;
            for(int j=1; j<=i; j++){
                if(i%j==0){
                    div ++;
                }
            }
            if(div>2) answer++;
        }
       
        return answer;
    }
}