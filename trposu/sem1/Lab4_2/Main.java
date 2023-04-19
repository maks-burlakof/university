package Lab4_2;

public class Main {
    public static void main(String[] args) {
        Taxpayer person = new Taxpayer("Иван Гришаёнок", "34571-1234-09", 13);

        Income principal_work = new Income(1650.55, "Доход с основного места работы");
        Income additional_work = new Income(487.32, "Доход с дополнительного места работы");
        Income royalties = new Income(213.00, "Доход с авторских вознаграждений");
        Income property_sales = new Income(50.15, "Доход с продажи имущества");
        Income gifts = new Income(12.09, "Доход с получения в подарок денежных сумм и имущества");
        Income transfers = new Income(0.12, "Доход с переводов из-за границы");
        Income benefits_aids = new Income(0.12, "Доход с льгот на материальную помощь");

        person.addIncome(principal_work);
        person.addIncome(additional_work);
        person.addIncome(royalties);
        person.addIncome(property_sales);
        person.addIncome(gifts);
        person.addIncome(transfers);
        person.addIncome(benefits_aids);

        System.out.println("Налогоплательщик: " + person);
        System.out.println("Итоговый доход: " + person.calculateTotalIncomes() + " р.");
        System.out.println("Ставка подоходного налога: " + person.getTaxValue() + "%");

        person.sortAndPrintIncomes();

        System.out.println("Итоговый налоговый вычет: " + person.calculateTotalTax() + " р.");
    }
}
