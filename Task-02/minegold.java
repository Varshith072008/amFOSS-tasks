import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner MIG = new Scanner(System.in);
        int d = MIG.nextInt();
        for (int i = 0; i < d; i++){
        int n = MIG.nextInt();
        int a = MIG.nextInt();
        int b = MIG.nextInt(); 
            int totalcap = (n + 1) * b;
            if (totalcap >= a){
                System.out.println("YES");
            } else {
                System.out.println("NO");
            }
        }   
    }
}