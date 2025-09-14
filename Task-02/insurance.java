import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner myins = new Scanner(System.in);
        int d = myins.nextInt();
        for (int i = 0; i < d; i++) {
            int x = myins.nextInt();
            int y = myins.nextInt();
            
            if (y <= x){
                System.out.println(y);
            } else {
                System.out.println(x);
                } 
     }                       
   }
}