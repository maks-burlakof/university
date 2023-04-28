package Lab5_2;

import java.util.*;
import java.io.*;

public class StringSorter {
    public static void main(String[] args) {
        ArrayList<String> strings = new ArrayList<String>();
        try {
            Scanner input = new Scanner(new File("input.txt"));
            while (input.hasNextLine()) {
                String line = input.nextLine();
                strings.add(line);
            }
        }
        catch (java.io.FileNotFoundException e) {
            System.out.println("Error: File not found!");
            return;
        }

        Collections.sort(strings);

        for (String s : strings) {
            System.out.println(s);
        }
    }
}
