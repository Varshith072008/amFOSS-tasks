import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        Scanner BH = new Scanner(System.in);
        int d = BH.nextInt();
        for (int i = 0; i < d; i++) {
            int rajuroom = BH.nextInt();
            int raviroom = BH.nextInt();
            int rajuFloor = (rajuroom - 1) / 10;
            int raviFloor = (raviroom - 1) / 10;
            int floorstotravel = Math.abs(rajuFloor - raviFloor);
            System.out.println(floorstotravel);
        }
             
        
    }
}