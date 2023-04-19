package Lab4_2;

import java.util.ArrayList;
import java.util.Comparator;

public class Taxpayer {
    private String name;
    private String ssn;
    private double taxValue;
    private ArrayList<Income> incomes;

    public Taxpayer(String name, String ssn, double taxValue) {
        this.name = name;
        this.ssn = ssn;
        this.taxValue = taxValue;
        this.incomes = new ArrayList<>();
    }

    public double getTaxValue() {
        return this.taxValue;
    }

    public void addIncome(Income income) {
        this.incomes.add(income);
    }

    public void sortAndPrintIncomes() {
        // Sort incomes by amount
        incomes.sort(Comparator.comparingDouble(Income::getAmount));

        // Print sorted incomes
        System.out.println("Отсортированный список налогов:");
        for (Income income : incomes) {
            System.out.println("Тип: " + income.getType() + ", Налог: " + String.format("%.3f", (income.getAmount()*this.taxValue/100)) + " р.");
        }
    }

    public double calculateTotalIncomes() {
        double amount = 0;
        for (Income income : incomes) {
            amount += income.getAmount();
        }
        return amount;
    }

    public String calculateTotalTax() {
        double amount = 0;
        for (Income income : incomes) {
            amount += (income.getAmount()*this.taxValue/100);
        }
        return String.format("%.3f",amount);
    }

    @Override
    public String toString() {
        return this.name + ", " + this.ssn + ", ставка " + this.taxValue + "%";
    }
}
