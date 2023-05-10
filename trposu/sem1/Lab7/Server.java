package Lab7;

import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
    public static void main(String[] args) {
        try {
            // Create a server socket that listens on port 5000
            ServerSocket serverSocket = new ServerSocket(5000);
            System.out.println("Server started and listening on port 5000");

            // Read the list of jobs from a file
            List<String> jobs = new ArrayList<>();
            BufferedReader br = new BufferedReader(new FileReader("jobs.txt"));
            String line;
            while ((line = br.readLine()) != null) {
                jobs.add(line);
            }
            br.close();

            // Wait for clients to connect
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected: " + clientSocket);

                // Select a random job and send it to the client
                Random random = new Random();
                String job = jobs.get(random.nextInt(jobs.size()));
                OutputStream os = clientSocket.getOutputStream();
                PrintWriter pw = new PrintWriter(os, true);
                pw.println(job);

                // Close the client connection
                pw.close();
                os.close();
                clientSocket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
