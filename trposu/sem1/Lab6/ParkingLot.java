package Lab6;

import java.util.Random;
import java.util.concurrent.*;

public class ParkingLot {
    private final int capacity;
    private final BlockingQueue<Integer> spaces;

    public ParkingLot(int capacity) {
        this.capacity = capacity;
        this.spaces = new ArrayBlockingQueue<>(capacity);
        for (int i = 1; i <= capacity; i++) {
            spaces.add(i);
        }
    }

    public boolean park(int carId, long maxWaitTimeMs) throws InterruptedException {
        Integer spaceId = spaces.poll(maxWaitTimeMs, TimeUnit.MILLISECONDS);
        if (spaceId != null) {
            System.out.printf("Car %d parked in space %d%n", carId, spaceId);
            return true;
        } else {
            System.out.printf("Car %d couldn't find a parking space%n", carId);
            return false;
        }
    }

    public void unpark(int carId, int spaceId) {
        spaces.add(spaceId);
        System.out.printf("Car %d unparked from space %d%n", carId, spaceId);
    }

    public static void main(String[] args) throws InterruptedException {
        int capacity = 3, num_cars = 5, min_time = 3000, max_time = 5000;  // capacity - num of parking places, time in ms
        ParkingLot parkingLot = new ParkingLot(capacity);
        Random random = new Random();
        for (int i = 1; i <= num_cars; i++) {
            int carId = i;
            Thread thread = new Thread(() -> {
                boolean parked = false;
                while (!parked) {
                    try {
                        parked = parkingLot.park(carId, 1000);
                        Thread.sleep(random.nextInt(max_time - min_time + 1) + min_time);
                        if (parked) {
                            parkingLot.unpark(carId, carId % 3 + 1);
                        }
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            });
            thread.start();
        }
    }
}
