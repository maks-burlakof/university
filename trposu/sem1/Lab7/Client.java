package Lab7;

import java.io.*;
import java.net.*;

public class Client {
    public static void main(String[] args) {
        try {
            // Connect to the server on port 5000
            Socket socket = new Socket("localhost", 5000);
            System.out.println("Successfully connected to server: " + socket);

            // Read the job from the server
            InputStream is = socket.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String job = br.readLine();
            System.out.println("Received job: " + job);

            // Close the connection
            br.close();
            is.close();
            socket.close();
            System.out.println("Disconnected from server");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
