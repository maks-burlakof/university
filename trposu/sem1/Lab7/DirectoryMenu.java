package Lab7;

import java.sql.SQLException;
import java.util.InputMismatchException;
import java.util.Scanner;

public class DirectoryMenu {
    private DirectoryDatabase db;
    private Scanner scanner;

    public DirectoryMenu(String databasePath) throws SQLException {
        this.db = new DirectoryDatabase(databasePath);
        this.db.createTablesIfNotExist();
        System.out.println("Connected to database!");
        this.scanner = new Scanner(System.in);
    }

    public void start() {
        System.out.println("Welcome to the Directory Manager!");
        while (true) {
            try {
                printMainMenu();
                int choice = getIntegerInput(1, 3);
                switch (choice) {
                    case 1:
                        viewRecordsMenu();
                        break;
                    case 2:
                        addRecordsMenu();
                        break;
                    case 3:
                        deleteRecordsMenu();
                        break;
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                scanner.nextLine(); // clear scanner buffer
            } catch (SQLException e) {
                System.err.println("Error: " + e.getMessage());
            }
        }
    }

    private void printMainMenu() {
        System.out.println("\n----- Main Menu -----");
        System.out.println("1. View existing records");
        System.out.println("2. Add new records");
        System.out.println("3. Delete records");
    }

    private void viewRecordsMenu() throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\n~~~~~ View Records Menu ~~~~~");
        System.out.println("1. View partitions");
        System.out.println("2. View folders");
        System.out.println("3. View files");

        int choice = getIntegerInput(1, 3);
        switch (choice) {
            case 1:
                printList(db.getAllPartitions(), "Partitions:");
                break;
            case 2:
                System.out.println("Enter partition name:");
                String partitionName = scanner.nextLine();
                printList(db.getAllFoldersOfPartition(partitionName), "Folders under " + partitionName + ":");
                break;
            case 3:
                System.out.println("Enter folder name:");
                String folderName = scanner.nextLine();
                printList(db.getAllFilesInFolder(folderName), "Files in " + folderName + ":");
                break;
        }
    }

    private void addRecordsMenu() throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\n~~~~~ Add Records Menu ~~~~~");
        System.out.println("1. Add partition");
        System.out.println("2. Add folder");
        System.out.println("3. Add file");

        int choice = getIntegerInput(1, 3);
        switch (choice) {
            case 1:
                System.out.println("Enter partition name:");
                String partitionName = scanner.nextLine();
                db.createPartition(partitionName);
                System.out.println("Partition added: " + partitionName);
                break;
            case 2:
                System.out.println("Enter folder name:");
                String folderName = scanner.nextLine();
                System.out.println("Enter partition name:");
                String partition = scanner.nextLine();
                db.createFolder(folderName, partition);
                System.out.println("Folder added: " + folderName);
                break;
            case 3:
                System.out.println("Enter file name:");
                String fileName = scanner.nextLine();
                System.out.println("Enter folder name:");
                String folder = scanner.nextLine();
                db.createFile(fileName, folder);
                System.out.println("File added: " + fileName);
                break;
        }
    }

    private void deleteRecordsMenu() throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\n~~~~~ Delete Records Menu ~~~~~");
        System.out.println("1. Delete partition");
        System.out.println("2. Delete folder");
        System.out.println("3. Delete file");

        int choice = getIntegerInput(1, 3);
        switch (choice) {
            case 1:
                System.out.println("Enter partition name:");
                String partitionName = scanner.nextLine();
                db.deletePartition(partitionName);
                System.out.println("Partition deleted: " + partitionName);
                break;
            case 2:
                System.out.println("Enter folder name:");
                String folderName = scanner.nextLine();
                db.deleteFolder(folderName);
                System.out.println("Folder deleted: " + folderName);
                break;
            case 3:
                System.out.println("Enter file name:");
                String fileName = scanner.nextLine();
                db.deleteFile(fileName);
                System.out.println("File deleted: " + fileName);
                break;
        }
    }

    private int getIntegerInput(int min, int max) {
        while (true) {
            try {
                int input = scanner.nextInt();
                if (input >= min && input <= max) {
                    return input;
                } else {
                    System.out.println("Invalid input. Please enter a number between " + min + " and " + max + ".");
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                scanner.nextLine(); // clear scanner buffer
            }
        }
    }

    private void printList(Iterable<String> items, String title) {
        System.out.println(title);
        for (String item : items) {
            System.out.println("- " + item);
        }
    }

    public static void main(String[] args) throws SQLException {
        DirectoryMenu menu = new DirectoryMenu("directory.db");
        menu.start();
    }
}
