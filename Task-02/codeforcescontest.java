import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner CFC = new Scanner(System.in);
        int d = CFC.nextInt();
        for (int i =0; i < d; i++){
            int x = CFC.nextInt();
            if (x <= 10){
                System.out.println("YES");   
            } else {
                System.out.println("NO");
            }
        }
    }
}