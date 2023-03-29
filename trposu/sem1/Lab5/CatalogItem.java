package Lab5;

import java.util.ArrayList;
import java.util.List;

public class CatalogItem {
    private String name;
    private List<CatalogItem> subDirectories;

    public CatalogItem(String name) {
        this.name = name;
        this.subDirectories = new ArrayList<>();
    }

    public void addSubDirectory(CatalogItem subDirectory) {
        this.subDirectories.add(subDirectory);
    }

    public List<CatalogItem> getSubDirectories() {
        return subDirectories;
    }

    public void printDirectoryHierarchy(int indent) {
        for (int i = 0; i < indent; i++) {
            System.out.print("│   ");
        }
        System.out.println("├── " + this.toString());
        for (CatalogItem subDir : subDirectories) {
            subDir.printDirectoryHierarchy(indent + 1);
        }
    }

    @Override
    public String toString() {
        return name;
    }

    public static void main(String[] args) {
        CatalogItem root = new CatalogItem("root");
        CatalogItem subDir1 = new CatalogItem("subDir1");
        CatalogItem subDir2 = new CatalogItem("subDir2");
        CatalogItem subDir3 = new CatalogItem("subDir3");

        root.addSubDirectory(subDir1);
        root.addSubDirectory(subDir2);
        subDir1.addSubDirectory(subDir3);
        
        root.printDirectoryHierarchy(0);
    }
}