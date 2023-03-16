package Lab4;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Partition {
    private String name;
    private String designation;
    private List<Folder> folders;

    public Partition(String name, String designation) {
        this.name = name;
        if (name.contains(".")) {
            throw new IllegalArgumentException("The partition name must not contain an extension");
        }
        this.designation = designation;
        this.folders = new ArrayList<>();
    }

    public void view() {
        System.out.println("|- " + this);
        for (Folder folder : folders) {
            folder.view();
        }
    }

    public void addFolder(Folder folder) {
        folders.add(folder);
    }

    public Folder findFolderByName() throws IllegalArgumentException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter folder name: ");
        String name = scanner.nextLine();
        for (Folder folder : folders) {
            if (folder.getName().equals(name)) {
                return folder;
            }
        }
        throw new IllegalArgumentException("Folder with name " + name + " not found.");
    }

    public long getMemorySize() {
        long totalSize = 0;
        for (Folder folder : folders) {
            totalSize += folder.getMemorySize();
        }
        return totalSize;
    }

    public String getName() {
        return name;
    }

    public String getDesignation() {
        return designation;
    }

    @Override
    public String toString() {
        return designation + ": " + name;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        Partition partition = (Partition) obj;
        return designation.equals(partition.designation);
    }

    @Override
    public int hashCode() {
        return designation.hashCode();
    }
}
