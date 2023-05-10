package Lab7_2;

import java.sql.*;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Taxpayer {
    private String name;
    private String ssn;
    private double taxValue;
    private Connection conn;

    public Taxpayer(String name, String ssn, double taxValue, String filename) throws SQLException {
        this.name = name;
        this.ssn = ssn;
        this.taxValue = taxValue;
        conn = DriverManager.getConnection("jdbc:sqlite:" + filename);
    }

    public void createTablesIfNotExist() throws SQLException {
        String sql = "CREATE TABLE IF NOT EXISTS incomes ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "type TEXT NOT NULL,"
                + "amount REAL NOT NULL"
                + ")";
        try (Statement stmt = conn.createStatement()) {
            stmt.executeUpdate(sql);
        }
    }

    public double getTaxValue() {
        return this.taxValue;
    }

    public void addIncome(Income income) throws SQLException {
        String sql = "INSERT INTO incomes (type, amount) VALUES (?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, income.getType());
            stmt.setString(2, income.getAmount());
            stmt.executeUpdate();
        }
    }

    public List<String> viewIncomes() throws SQLException {
        List<String> incomes = new ArrayList<>();
        String sql = "SELECT type, amount FROM incomes";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                String type = rs.getString("type");
                double amount = rs.getDouble("amount");
                incomes.add(String.format("%s: %.2f", type, amount));
            }
        }
        return incomes;
    }

    public void deleteIncome(String id) throws SQLException {
        String sql = "DELETE FROM incomes WHERE id = ?;";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, id);
            stmt.executeUpdate();
        }
    }

    public String calculateTotalIncomes() throws SQLException {
        double amount = 0;
        String sql = "SELECT SUM(CAST(amount AS REAL)) AS total FROM incomes;";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            ResultSet rs = pstmt.executeQuery();
            amount = rs.getDouble(1);
        }
        return String.format("%.2f", amount);
    }

    public double calculateTotalTax(String income_amount) {
        income_amount = income_amount.replace(",", ".");
        double income_amo = Double.parseDouble(income_amount);
        return income_amo * this.taxValue / 100;
    }

    @Override
    public String toString() {
        return this.name + ", " + this.ssn + ", ставка " + this.taxValue + "%";
    }
}
