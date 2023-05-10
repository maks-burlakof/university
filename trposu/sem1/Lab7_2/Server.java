package Lab7_2;

import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) throws IOException {
        int portNumber = 4444;
        ServerSocket serverSocket = new ServerSocket(portNumber);

        while (true) {
            Socket clientSocket = serverSocket.accept();
            new ClientHandler(clientSocket).start();
        }
    }
}

class ClientHandler extends Thread {
    private Socket clientSocket;
    private BufferedReader in;
    private PrintWriter out;

    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
    }

    public void run() {
        try {
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            out = new PrintWriter(clientSocket.getOutputStream(), true);

            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                System.out.println("Received message from client: " + inputLine);
                // Modify the message here
                String modifiedMessage = inputLine.toUpperCase();
                System.out.println("Modified message: " + modifiedMessage);
                out.println(modifiedMessage);
            }

            out.close();
            in.close();
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
