package Lab7;

import java.sql.*;
import java.util.*;

public class DirectoryDatabase {
    private Connection conn;

    public DirectoryDatabase(String filename) throws SQLException {
        conn = DriverManager.getConnection("jdbc:sqlite:" + filename);
    }

    public void createTablesIfNotExist() throws SQLException {
        String sql = "CREATE TABLE IF NOT EXISTS partitions ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "name TEXT NOT NULL"
                + ")";
        try (Statement stmt = conn.createStatement()) {
            stmt.executeUpdate(sql);
        }

        sql = "CREATE TABLE IF NOT EXISTS folders ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "name TEXT NOT NULL,"
                + "partition_id INTEGER NOT NULL,"
                + "FOREIGN KEY (partition_id) REFERENCES partitions(id)"
                + ")";
        try (Statement stmt = conn.createStatement()) {
            stmt.executeUpdate(sql);
        }

        sql = "CREATE TABLE IF NOT EXISTS files ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "name TEXT NOT NULL,"
                + "folder_id INTEGER NOT NULL,"
                + "FOREIGN KEY (folder_id) REFERENCES folders(id)"
                + ")";
        try (Statement stmt = conn.createStatement()) {
            stmt.executeUpdate(sql);
        }
    }

    public void createPartition(String partitionName) throws SQLException {
        String sql = "INSERT INTO partitions (name) VALUES (?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, partitionName);
            stmt.executeUpdate();
        }
    }

    public void createFolder(String folderName, String partitionName) throws SQLException {
        // Check if the partition exists
        String sql = "SELECT COUNT(*) AS count FROM partitions WHERE name = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, partitionName);
            ResultSet rs = pstmt.executeQuery();
            if (rs.getInt("count") == 0) {
                throw new SQLException("Partition " + partitionName + " does not exist.");
            }
        }

        sql = "INSERT INTO folders (name, partition_id) VALUES (?, (SELECT id FROM partitions WHERE name = ?))";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, folderName);
            stmt.setString(2, partitionName);
            stmt.executeUpdate();
        }
    }

    public void createFile(String fileName, String folderName) throws SQLException {
        String sql = "INSERT INTO files (name, folder_id) VALUES (?, (SELECT id FROM folders WHERE name = ?))";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, fileName);
            pstmt.setString(2, folderName);
            pstmt.executeUpdate();
        }
    }

    public void deletePartition(String partitionName) throws SQLException {
        String sql = "DELETE FROM partitions WHERE name = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, partitionName);
            int rowsDeleted = pstmt.executeUpdate();
            if (rowsDeleted == 0) {
                throw new SQLException("No partition found with name " + partitionName);
            }
        }
    }

    public void deleteFolder(String folderName) throws SQLException {
        String sql = "DELETE FROM folders WHERE name = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, folderName);
            int rowsDeleted = pstmt.executeUpdate();
            if (rowsDeleted == 0) {
                throw new SQLException("No folder found with name " + folderName);
            }
        }
    }

    public void deleteFile(String fileName) throws SQLException {
        String sql = "DELETE FROM files WHERE name = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, fileName);
            int rowsDeleted = pstmt.executeUpdate();
            if (rowsDeleted == 0) {
                throw new SQLException("No file found with name " + fileName);
            }
        }
    }

    public List<String> getAllPartitions() throws SQLException {
        List<String> partitions = new ArrayList<>();
        String sql = "SELECT name FROM partitions";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                partitions.add(rs.getString("name"));
            }
        }
        return partitions;
    }

    public List<String> getAllFoldersOfPartition(String partitionName) throws SQLException {
        List<String> folders = new ArrayList<>();
        String sql = "SELECT folders.name FROM folders "
                + "JOIN partitions ON folders.partition_id = partitions.id "
                + "WHERE partitions.name = ?";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, partitionName);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    folders.add(rs.getString("name"));
                }
            }
        }
        return folders;
    }

    public List<String> getAllFilesInFolder(String folderName) throws SQLException {
        List<String> files = new ArrayList<>();
        String sql = "SELECT files.name FROM files "
                + "JOIN folders ON files.folder_id = folders.id "
                + "WHERE folders.name = ?";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, folderName);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    files.add(rs.getString("name"));
                }
            }
        }
        return files;
    }

    public static void main(String[] args) {
        try {
            DirectoryDatabase db = new DirectoryDatabase("directory.db");
            System.out.println("Connected to database!");
            db.createTablesIfNotExist();

            db.createPartition("C:");
            db.createFolder("Program Files", "C:");
            db.createFolder("Java", "C:");

            List<String> partitions = db.getAllPartitions();
            System.out.println("Partitions:");
            for (String partition : partitions) {
                System.out.println(partition);
            }

            List<String> folders = db.getAllFoldersOfPartition("C:");
            System.out.println("Folders under C:");
            for (String folder : folders) {
                System.out.println(folder);
            }

            List<String> files = db.getAllFilesInFolder("Java");
            System.out.println("Files in Java:");
            for (String file : files) {
                System.out.println(file);
            }
        } catch (SQLException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
