
import java.util.*;

class Solution {
    public int solution(int[] numbers) {
        Arrays.sort(numbers);
        return numbers[numbers.length-1] * numbers[numbers.length-2];
    }
}

//
// import java.util.*;

// class Solution {
//     public int solution(int[] numbers) {
//         Integer[] newArray = Arrays.stream(numbers).boxed().toArray(Integer[]::new);
//         int answer = 0;
//         Arrays.sort(newArray, Collections.reverseOrder());
//         return newArray[0]*newArray[1];
//     }
// }
