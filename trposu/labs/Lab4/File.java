package Lab4;

public class File {
    private String name;
    private int size;

    public File(String name, int size) {
        this.name = name;
        if (!name.contains(".")) {
            throw new IllegalArgumentException("File name must have an extension");
        }
        this.name = name;
        this.size = size;
    }

    public String getName() {
        return name;
    }

    public long getSize() {
        return size;
    }

    @Override
    public String toString() {
        return name;
    }
}
