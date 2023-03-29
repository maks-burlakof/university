package Lab4;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FileManager {
    private List<Partition> partitions;
    private Scanner scanner;

    public FileManager() {
        this.partitions = new ArrayList<>();
        this.scanner = new Scanner(System.in);
    }

    private int readIntInput() {
        int input = 0;
        boolean validInput = false;
        while (!validInput) {
            try {
                input = Integer.parseInt(scanner.nextLine());
                validInput = true;
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid integer.");
            }
        }
        return input;
    }

    public Partition findPartitionByDesignation() throws IllegalArgumentException {
        System.out.print("Enter partition designation: ");
        String designation = scanner.nextLine();
        for (Partition partition : partitions) {
            if (partition.getDesignation().equals(designation)) {
                return partition;
            }
        }
        throw new IllegalArgumentException("Partition with designation " + designation + " not found.");
    }

    public void run() {
        while (true) {
            System.out.println("\nSelect an option:\n1. View partitions contents\n2. Create\n3. Search for files by extension\n4. Calculate memory\n5. Exit");
            switch (readIntInput()) {
                case 1:
                    for (Partition partition : partitions) {
                        partition.view();
                    }
                    break;
                case 2:
                    createMenu();
                    break;
                case 3:
                    try {
                        Partition partition = findPartitionByDesignation();
                        Folder folder = partition.findFolderByName();
                        System.out.print("Enter file extension: ");
                        String extension = scanner.nextLine();
                        List<File> files = folder.findFilesByExtension(extension);
                        System.out.println("Files with extension " + extension + " in folder " + folder.getName() + ":");
                        for (File file : files) {
                            System.out.println(file);
                        }
                    } catch (IllegalArgumentException e) {
                        System.out.println("Invalid search data: " + e.getMessage());
                    }
                    break;
                case 4:
                    calculateMemory();
                    break;
                case 5:
                    scanner.close();
                    return;
                default:
                    System.out.println("Invalid option");
            }
        }
    }

    private void createMenu() {
        while (true) {
            System.out.println("\nSelect an option:\n1. Create partition\n2. Create folder\n3. Create file\n4. Back");
            switch (readIntInput()) {
                case 1:
                    try {
                        System.out.print("Enter partition name: ");
                        String name = scanner.nextLine();
                        System.out.print("Enter partition designation: ");
                        String designation = scanner.nextLine();
                        partitions.add(new Partition(name, designation));
                        System.out.println("Partition created successfully");
                    } catch (IllegalArgumentException e) {
                        System.out.println("Invalid partition data: " + e.getMessage());
                    }
                    break;
                case 2:
                    try {
                        Partition partition = findPartitionByDesignation();
                        System.out.print("Enter folder name: ");
                        String name = scanner.nextLine();
                        Folder folder = new Folder(name);
                        partition.addFolder(folder);
                        System.out.println("Folder created successfully");
                    } catch (IllegalArgumentException e) {
                        System.out.println("Invalid folder data: " + e.getMessage());
                    }
                    break;
                case 3:
                    try {
                        Partition partition = findPartitionByDesignation();
                        Folder folder = partition.findFolderByName();
                        System.out.print("Enter file name: ");
                        String name = scanner.nextLine();
                        System.out.print("Enter file size: ");
                        int size = readIntInput();
                        File file = new File(name, size);
                        folder.addFile(file);
                        System.out.println("File created successfully");
                    } catch (IllegalArgumentException e) {
                        System.out.println("Invalid file data: " + e.getMessage());
                    }
                    break;
                case 4:
                    return;
                default:
                    System.out.println("Invalid option");
            }
        }
    }

    private void calculateMemory() {
        System.out.println("\nSelect an option:\n1. Calculate by partition\n2. Calculate by folder\n3. Back");
        try {
            switch (readIntInput()) {
                case 1:
                    Partition partition = findPartitionByDesignation();
                    System.out.println("Total size of files in partition " + partition.getName() + ": " + partition.getMemorySize() + " bytes");
                    break;
                case 2:
                    Partition part = findPartitionByDesignation();
                    Folder folder = part.findFolderByName();
                    System.out.println("Total size of files in folder " + folder.getName() + ": " + folder.getMemorySize() + " bytes");
                    break;
                case 3:
                    return;
                default:
                    System.out.println("Invalid option");
            }
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid data: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        FileManager fileManager = new FileManager();
        fileManager.run();
    }
}
