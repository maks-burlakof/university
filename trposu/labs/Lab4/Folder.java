package Lab4;

import java.util.ArrayList;
import java.util.List;

public class Folder {
    private List<File> files;
    private String name;

    public Folder(String name) {
        this.name = name;
        if (name.contains(".")) {
            throw new IllegalArgumentException("The folder name must not contain an extension");
        }
        this.files = new ArrayList<>();
    }

    public String getName() {
        return this.name;
    }

    public void view() {
        System.out.println("  |- " + this);
        for (File file : files) {
            System.out.println("     - " + file);
        }
    }

    public List<File> findFilesByExtension(String extension) {
        List<File> matchingFiles = new ArrayList<>();
        for (File file : files) {
            if (file.getName().endsWith("." + extension)) {
                matchingFiles.add(file);
            }
        }
        return matchingFiles;
    }

    public List<File> getFiles() {
        return files;
    }

    public void addFile(File file) {
        files.add(file);
    }

    public long getMemorySize() {
        int size = 0;
        for (File file : files) {
            size += file.getSize();
        }
        return size;
    }

    @Override
    public String toString() {
        return this.name;
    }
}
