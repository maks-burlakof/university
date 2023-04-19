package Lab4_2;

public class Income {
    private double amount;
    private String type;

    public Income(double amount, String type) {
        this.amount = amount;
        this.type = type;
    }

    public double getAmount() {
        return this.amount;
    }

    public String getType() {
        return this.type;
    }
}
