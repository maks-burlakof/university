package Lab6_2;

import java.util.Random;
import java.util.concurrent.*;

public class Hypermarket {
    private final int capacity;
    private final BlockingQueue<Integer> spaces;

    public Hypermarket(int capacity) {
        this.capacity = capacity;
        this.spaces = new ArrayBlockingQueue<>(capacity);
        for (int i = 1; i <= capacity; i++) {
            spaces.add(i);
        }
    }

    public boolean stay(int carId, long maxWaitTimeMs) throws InterruptedException {
        while (true) {
            Integer spaceId = spaces.poll(maxWaitTimeMs, TimeUnit.MILLISECONDS);
            if (spaceId != null) {
                System.out.printf("Customer %d stayed in space %d%n", carId, spaceId);
                return true;
            } else {
                System.out.printf("Customer %d couldn't find a space%n", carId);
                Thread.sleep(2000);
            }
        }
    }

    public void leave(int carId, int spaceId) {
        spaces.add(spaceId);
        System.out.printf("Customer %d left from space %d%n", carId, spaceId);
    }

    public static void main(String[] args) throws InterruptedException {
        Hypermarket market = new Hypermarket(3);
        Random random = new Random();
        for (int i = 1; i <= 5; i++) {
            int customerId = i;
            Thread thread = new Thread(() -> {
                try {
                    boolean parked = market.stay(customerId, 1000);
                    if (parked) {
                        Thread.sleep(random.nextInt(5000) + 1000);
                        market.leave(customerId, customerId % 3 + 1);
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
            thread.start();
        }
    }
}
