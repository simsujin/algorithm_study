class Solution {
    public int solution(int[] box, int n) {
        box[0] /= n;
        box[1] /= n;
        box[2] /= n;
        int answer = box[0] * box[1] * box[2];
        return answer;
    }
}